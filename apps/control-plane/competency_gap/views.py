from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Q, Avg
from datetime import timedelta
import json

from .models import (
    TrainerQualification,
    UnitOfCompetency,
    TrainerAssignment,
    CompetencyGap,
    QualificationMapping,
    ComplianceCheck,
)
from .serializers import (
    TrainerQualificationSerializer,
    TrainerQualificationListSerializer,
    UnitOfCompetencySerializer,
    TrainerAssignmentSerializer,
    CompetencyGapSerializer,
    QualificationMappingSerializer,
    ComplianceCheckSerializer,
    CheckGapsRequestSerializer,
    CheckGapsResponseSerializer,
    AssignTrainerRequestSerializer,
    AssignTrainerResponseSerializer,
    ValidateMatrixRequestSerializer,
    ValidateMatrixResponseSerializer,
    GraphAnalysisRequestSerializer,
    GraphAnalysisResponseSerializer,
    GenerateComplianceReportRequestSerializer,
    GenerateComplianceReportResponseSerializer,
    DashboardStatsSerializer,
    BulkAssignRequestSerializer,
    BulkAssignResponseSerializer,
)


class TrainerQualificationViewSet(viewsets.ModelViewSet):
    queryset = TrainerQualification.objects.all()
    serializer_class = TrainerQualificationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = self.request.query_params.get("tenant")
        if tenant:
            queryset = queryset.filter(tenant=tenant)

        trainer_id = self.request.query_params.get("trainer_id")
        if trainer_id:
            queryset = queryset.filter(trainer_id=trainer_id)

        verification_status = self.request.query_params.get("verification_status")
        if verification_status:
            queryset = queryset.filter(verification_status=verification_status)

        return queryset.order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TrainerQualificationListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def check_gaps(self, request):
        """Check for competency gaps for a trainer-unit pair"""
        req_serializer = CheckGapsRequestSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)

        data = req_serializer.validated_data
        trainer_id = data["trainer_id"]
        unit_id = data["unit_id"]

        # Get unit and trainer qualifications
        try:
            unit = UnitOfCompetency.objects.get(id=unit_id)
        except UnitOfCompetency.DoesNotExist:
            return Response(
                {"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND
            )

        qualifications = TrainerQualification.objects.filter(
            trainer_id=trainer_id, verification_status="verified"
        )

        if not qualifications.exists():
            trainer_name = request.data.get("trainer_name", trainer_id)
        else:
            trainer_name = qualifications.first().trainer_name

        # Initialize gap analysis
        gaps_found = []
        matching_qualifications = []
        compliance_score = 0.0

        # Check TAE requirement
        has_tae = qualifications.filter(
            Q(qualification_code__istartswith="TAE40116")
            | Q(qualification_code__istartswith="TAE40122")
        ).exists()

        if unit.requires_tae and not has_tae:
            gaps_found.append(
                {
                    "gap_type": "missing_tae",
                    "severity": "critical",
                    "description": "Missing TAE40116/TAE40122 qualification",
                    "required": "TAE40116 or TAE40122",
                    "recommendation": "Complete Certificate IV in Training and Assessment",
                }
            )
        else:
            compliance_score += 30  # TAE worth 30%

        # Check qualification requirements
        required_quals = unit.required_qualifications or []
        trainer_qual_codes = list(
            qualifications.values_list("qualification_code", flat=True)
        )

        has_required_qual = False
        for req_qual in required_quals:
            if req_qual in trainer_qual_codes:
                has_required_qual = True
                qual = qualifications.get(qualification_code=req_qual)
                matching_qualifications.append(
                    {
                        "qualification_id": qual.qualification_id,
                        "qualification_code": qual.qualification_code,
                        "qualification_name": qual.qualification_name,
                        "match_strength": 1.0,
                    }
                )
                compliance_score += 30  # Required qual worth 30%
                break

        if not has_required_qual and required_quals:
            gaps_found.append(
                {
                    "gap_type": "missing_qualification",
                    "severity": "critical",
                    "description": f'Missing required qualification: {", ".join(required_quals)}',
                    "required": required_quals[0] if required_quals else "Unknown",
                    "recommendation": f"Obtain {required_quals[0]} or equivalent qualification",
                }
            )

        # Check industry experience
        max_experience = (
            qualifications.aggregate(Avg("industry_experience_years"))[
                "industry_experience_years__avg"
            ]
            or 0
        )
        required_experience = unit.required_industry_experience

        if required_experience > max_experience:
            gaps_found.append(
                {
                    "gap_type": "insufficient_experience",
                    "severity": "high",
                    "description": f"Requires {required_experience} years experience, has {max_experience:.0f}",
                    "required": f"{required_experience} years",
                    "recommendation": f"Gain additional {required_experience - max_experience:.0f} years of industry experience",
                }
            )
        else:
            compliance_score += 20  # Experience worth 20%

        # Check industry currency
        has_recent_work = qualifications.filter(recent_industry_work=True).exists()
        if unit.requires_industry_currency and not has_recent_work:
            gaps_found.append(
                {
                    "gap_type": "missing_currency",
                    "severity": "high",
                    "description": "No recent industry work documented",
                    "required": "Recent industry experience",
                    "recommendation": "Complete industry placement or update LinkedIn/GitHub profiles",
                }
            )
        else:
            compliance_score += 20  # Currency worth 20%

        # Check competency areas
        required_competencies = set(unit.required_competency_areas or [])
        trainer_competencies = set()
        for qual in qualifications:
            trainer_competencies.update(qual.competency_areas or [])

        missing_competencies = required_competencies - trainer_competencies
        if missing_competencies:
            gaps_found.append(
                {
                    "gap_type": "competency_mismatch",
                    "severity": "medium",
                    "description": f'Missing competency areas: {", ".join(missing_competencies)}',
                    "required": list(missing_competencies),
                    "recommendation": f'Complete training in: {", ".join(list(missing_competencies)[:3])}',
                }
            )

        # Calculate final compliance
        meets_requirements = len(gaps_found) == 0 or all(
            g["severity"] not in ["critical"] for g in gaps_found
        )
        can_deliver = meets_requirements and compliance_score >= 60

        recommendations = [
            g["recommendation"]
            for g in gaps_found
            if data.get("include_recommendations", True)
        ]

        response_data = {
            "trainer_id": trainer_id,
            "trainer_name": trainer_name,
            "unit_code": unit.unit_code,
            "unit_name": unit.unit_name,
            "meets_requirements": meets_requirements,
            "compliance_score": compliance_score,
            "gaps_found": gaps_found,
            "matching_qualifications": matching_qualifications,
            "recommendations": recommendations,
            "can_deliver": can_deliver,
            "message": f"Found {len(gaps_found)} gaps. Compliance score: {compliance_score:.1f}%",
        }

        resp_serializer = CheckGapsResponseSerializer(data=response_data)
        resp_serializer.is_valid(raise_exception=True)
        return Response(resp_serializer.data)

    @action(detail=False, methods=["post"])
    def assign_trainer(self, request):
        """Assign a trainer to a unit with compliance checking"""
        req_serializer = AssignTrainerRequestSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)

        data = req_serializer.validated_data
        trainer_id = data["trainer_id"]
        unit_id = data["unit_id"]

        try:
            unit = UnitOfCompetency.objects.get(id=unit_id)
        except UnitOfCompetency.DoesNotExist:
            return Response(
                {"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Get trainer name
        qual = TrainerQualification.objects.filter(trainer_id=trainer_id).first()
        trainer_name = qual.trainer_name if qual else trainer_id

        # Check for existing assignment
        existing = TrainerAssignment.objects.filter(
            tenant=request.data.get("tenant", "default"),
            trainer_id=trainer_id,
            unit=unit,
        ).first()

        if existing:
            return Response(
                {
                    "error": "Assignment already exists",
                    "assignment_id": existing.assignment_id,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Run compliance check if requested
        compliance_score = 0.0
        gaps = []
        meets_requirements = False

        if data.get("check_compliance", True):
            check_response = self.check_gaps(request)
            if check_response.status_code == 200:
                check_data = check_response.data
                compliance_score = check_data["compliance_score"]
                gaps = check_data["gaps_found"]
                meets_requirements = check_data["meets_requirements"]

        # Create assignment
        assignment = TrainerAssignment.objects.create(
            tenant=request.data.get("tenant", "default"),
            trainer_id=trainer_id,
            trainer_name=trainer_name,
            unit=unit,
            meets_requirements=meets_requirements,
            compliance_score=compliance_score,
            gaps_identified=[g["description"] for g in gaps],
            matching_qualifications=[],
            assignment_status=(
                "approved"
                if (meets_requirements or data.get("override_gaps", False))
                else "under_review"
            ),
            assignment_notes=data.get("assignment_notes", ""),
        )

        # Create gap records
        for gap_data in gaps:
            CompetencyGap.objects.create(
                tenant=request.data.get("tenant", "default"),
                trainer_id=trainer_id,
                trainer_name=trainer_name,
                unit=unit,
                assignment=assignment,
                gap_type=gap_data["gap_type"],
                gap_severity=gap_data["severity"],
                gap_description=gap_data["description"],
                required_qualification=gap_data.get("required", ""),
                recommended_action=gap_data.get("recommendation", ""),
            )

        response_data = {
            "assignment_id": str(assignment.id),
            "assignment_number": assignment.assignment_id,
            "assignment_status": assignment.assignment_status,
            "meets_requirements": meets_requirements,
            "compliance_score": compliance_score,
            "gaps_count": len(gaps),
            "message": f"Trainer assigned to {unit.unit_code}. Status: {assignment.assignment_status}",
        }

        resp_serializer = AssignTrainerResponseSerializer(data=response_data)
        resp_serializer.is_valid(raise_exception=True)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def bulk_assign(self, request):
        """Bulk assign a trainer to multiple units"""
        req_serializer = BulkAssignRequestSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)

        data = req_serializer.validated_data
        trainer_id = data["trainer_id"]
        unit_ids = data["unit_ids"]

        assignments = []
        successful = 0
        failed = 0

        for unit_id in unit_ids:
            assign_data = {
                "trainer_id": trainer_id,
                "unit_id": unit_id,
                "check_compliance": data.get("check_compliance", True),
                "tenant": request.data.get("tenant", "default"),
            }

            response = self.assign_trainer(
                type(
                    "Request",
                    (),
                    {"data": assign_data, "query_params": request.query_params},
                )()
            )

            if response.status_code == 201:
                successful += 1
                assignments.append(
                    {
                        "unit_id": unit_id,
                        "status": "success",
                        "assignment_id": response.data["assignment_id"],
                    }
                )
            else:
                failed += 1
                assignments.append(
                    {
                        "unit_id": unit_id,
                        "status": "failed",
                        "error": response.data.get("error", "Unknown error"),
                    }
                )

        response_data = {
            "total_assignments": len(unit_ids),
            "successful_assignments": successful,
            "failed_assignments": failed,
            "assignments": assignments,
            "message": f"Completed {successful}/{len(unit_ids)} assignments",
        }

        resp_serializer = BulkAssignResponseSerializer(data=response_data)
        resp_serializer.is_valid(raise_exception=True)
        return Response(resp_serializer.data)

    @action(detail=False, methods=["post"])
    def validate_matrix(self, request):
        """Validate the entire trainer matrix for compliance"""
        req_serializer = ValidateMatrixRequestSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)

        data = req_serializer.validated_data
        tenant = request.query_params.get("tenant", "default")

        # Create compliance check record
        check = ComplianceCheck.objects.create(
            tenant=tenant,
            check_type=data.get("check_type", "full_matrix"),
            check_status="running",
            trainer_ids=data.get("trainer_ids", []),
            unit_codes=data.get("unit_codes", []),
            started_at=timezone.now(),
        )

        # Get assignments to check
        assignments = TrainerAssignment.objects.filter(tenant=tenant)

        if data.get("trainer_ids"):
            assignments = assignments.filter(trainer_id__in=data["trainer_ids"])

        if data.get("unit_codes"):
            assignments = assignments.filter(unit__unit_code__in=data["unit_codes"])

        # Count results
        total = assignments.count()
        compliant = assignments.filter(meets_requirements=True).count()
        non_compliant = total - compliant

        # Get gaps
        gaps = CompetencyGap.objects.filter(tenant=tenant, is_resolved=False)

        if data.get("trainer_ids"):
            gaps = gaps.filter(trainer_id__in=data["trainer_ids"])

        if data.get("unit_codes"):
            gaps = gaps.filter(unit__unit_code__in=data["unit_codes"])

        gaps_count = gaps.count()
        critical_gaps = gaps.filter(gap_severity="critical").count()
        high_gaps = gaps.filter(gap_severity="high").count()
        medium_gaps = gaps.filter(gap_severity="medium").count()
        low_gaps = gaps.filter(gap_severity="low").count()

        # Calculate compliance percentage
        compliance_pct = (compliant / total * 100) if total > 0 else 0

        # Count unique trainers and units
        trainers_checked = assignments.values("trainer_id").distinct().count()
        units_checked = assignments.values("unit").distinct().count()

        # Update check record
        check.check_status = "completed"
        check.total_assignments_checked = total
        check.compliant_assignments = compliant
        check.non_compliant_assignments = non_compliant
        check.gaps_found = gaps_count
        check.critical_gaps = critical_gaps
        check.high_gaps = high_gaps
        check.medium_gaps = medium_gaps
        check.low_gaps = low_gaps
        check.overall_compliance_score = compliance_pct
        check.completed_at = timezone.now()
        check.execution_time_seconds = (
            check.completed_at - check.started_at
        ).total_seconds()
        check.save()

        response_data = {
            "check_id": str(check.id),
            "check_number": check.check_id,
            "total_assignments": total,
            "compliant_assignments": compliant,
            "non_compliant_assignments": non_compliant,
            "compliance_percentage": compliance_pct,
            "gaps_found": gaps_count,
            "critical_gaps": critical_gaps,
            "trainers_checked": trainers_checked,
            "units_checked": units_checked,
            "message": f"Matrix validation complete. Compliance: {compliance_pct:.1f}%",
        }

        resp_serializer = ValidateMatrixResponseSerializer(data=response_data)
        resp_serializer.is_valid(raise_exception=True)
        return Response(resp_serializer.data)

    @action(detail=False, methods=["post"])
    def graph_analysis(self, request):
        """Perform graph-based analysis of qualifications and competencies"""
        req_serializer = GraphAnalysisRequestSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)

        data = req_serializer.validated_data
        tenant = request.query_params.get("tenant", "default")

        # Build graph nodes and edges
        nodes = []
        edges = []

        # Get trainer qualifications as nodes
        if data.get("trainer_id"):
            qualifications = TrainerQualification.objects.filter(
                tenant=tenant, trainer_id=data["trainer_id"]
            )
        else:
            qualifications = TrainerQualification.objects.filter(tenant=tenant)[:10]

        for qual in qualifications:
            nodes.append(
                {
                    "id": f"qual-{qual.id}",
                    "type": "qualification",
                    "label": qual.qualification_code,
                    "name": qual.qualification_name,
                    "trainer_id": qual.trainer_id,
                }
            )

        # Get units as nodes
        units = UnitOfCompetency.objects.filter(tenant=tenant)[:20]
        for unit in units:
            nodes.append(
                {
                    "id": f"unit-{unit.id}",
                    "type": "unit",
                    "label": unit.unit_code,
                    "name": unit.unit_name,
                }
            )

        # Get mappings as nodes
        mappings = QualificationMapping.objects.filter(tenant=tenant)[:10]
        for mapping in mappings:
            nodes.append(
                {
                    "id": f"map-{mapping.id}",
                    "type": "mapping",
                    "label": mapping.source_qualification_code,
                    "match_strength": mapping.match_strength,
                }
            )

        # Create edges from assignments
        assignments = TrainerAssignment.objects.filter(tenant=tenant)[:30]
        for assignment in assignments:
            # Find trainer's qualifications
            trainer_quals = qualifications.filter(trainer_id=assignment.trainer_id)
            for qual in trainer_quals:
                edges.append(
                    {
                        "source": f"qual-{qual.id}",
                        "target": f"unit-{assignment.unit.id}",
                        "type": "can_deliver",
                        "weight": assignment.compliance_score / 100,
                        "compliant": assignment.meets_requirements,
                    }
                )

        # Find paths (simulated for demo)
        paths = []
        if data.get("find_paths", True):
            for assignment in assignments[:5]:
                trainer_quals = qualifications.filter(trainer_id=assignment.trainer_id)
                if trainer_quals.exists():
                    qual = trainer_quals.first()
                    paths.append(
                        {
                            "source": qual.qualification_code,
                            "target": assignment.unit.unit_code,
                            "path": [
                                qual.qualification_code,
                                assignment.unit.unit_code,
                            ],
                            "length": 1,
                            "strength": assignment.compliance_score / 100,
                        }
                    )

        # Calculate coverage score
        total_units = units.count()
        covered_units = (
            assignments.filter(meets_requirements=True)
            .values("unit")
            .distinct()
            .count()
        )
        coverage_score = (covered_units / total_units * 100) if total_units > 0 else 0

        analysis = {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "total_paths": len(paths),
            "coverage_percentage": coverage_score,
            "avg_compliance": assignments.aggregate(Avg("compliance_score"))[
                "compliance_score__avg"
            ]
            or 0,
        }

        response_data = {
            "nodes": nodes,
            "edges": edges,
            "paths": paths,
            "coverage_score": coverage_score,
            "analysis": analysis,
            "message": f"Graph contains {len(nodes)} nodes and {len(edges)} edges",
        }

        resp_serializer = GraphAnalysisResponseSerializer(data=response_data)
        resp_serializer.is_valid(raise_exception=True)
        return Response(resp_serializer.data)

    @action(detail=False, methods=["post"])
    def generate_compliance_report(self, request):
        """Generate detailed compliance report"""
        req_serializer = GenerateComplianceReportRequestSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)

        data = req_serializer.validated_data
        tenant = request.query_params.get("tenant", "default")

        # Get compliance check if provided
        if data.get("check_id"):
            try:
                check = ComplianceCheck.objects.get(id=data["check_id"])
            except ComplianceCheck.DoesNotExist:
                check = None
        else:
            check = None

        # Build report
        report_date = timezone.now()
        report_title = (
            f'Trainer Matrix Compliance Report - {report_date.strftime("%Y-%m-%d")}'
        )

        # Get assignments
        assignments = TrainerAssignment.objects.filter(tenant=tenant)
        if data.get("trainer_ids"):
            assignments = assignments.filter(trainer_id__in=data["trainer_ids"])
        if data.get("unit_codes"):
            assignments = assignments.filter(unit__unit_code__in=data["unit_codes"])

        # Compliance summary
        total_assignments = assignments.count()
        compliant = assignments.filter(meets_requirements=True).count()
        compliance_pct = (
            (compliant / total_assignments * 100) if total_assignments > 0 else 0
        )

        compliance_summary = {
            "total_assignments": total_assignments,
            "compliant_assignments": compliant,
            "non_compliant_assignments": total_assignments - compliant,
            "compliance_percentage": compliance_pct,
        }

        # By trainer
        trainer_reports = []
        trainers = assignments.values("trainer_id", "trainer_name").distinct()
        for trainer in trainers:
            trainer_assignments = assignments.filter(trainer_id=trainer["trainer_id"])
            trainer_compliant = trainer_assignments.filter(
                meets_requirements=True
            ).count()
            trainer_reports.append(
                {
                    "trainer_id": trainer["trainer_id"],
                    "trainer_name": trainer["trainer_name"],
                    "total_units": trainer_assignments.count(),
                    "compliant_units": trainer_compliant,
                    "compliance_rate": (
                        (trainer_compliant / trainer_assignments.count() * 100)
                        if trainer_assignments.count() > 0
                        else 0
                    ),
                }
            )

        # By unit
        unit_reports = []
        units = assignments.values("unit__unit_code", "unit__unit_name").distinct()
        for unit in units:
            unit_assignments = assignments.filter(
                unit__unit_code=unit["unit__unit_code"]
            )
            unit_compliant = unit_assignments.filter(meets_requirements=True).count()
            unit_reports.append(
                {
                    "unit_code": unit["unit__unit_code"],
                    "unit_name": unit["unit__unit_name"],
                    "total_trainers": unit_assignments.count(),
                    "compliant_trainers": unit_compliant,
                }
            )

        # Gap summary
        gaps = CompetencyGap.objects.filter(tenant=tenant, is_resolved=False)
        if data.get("trainer_ids"):
            gaps = gaps.filter(trainer_id__in=data["trainer_ids"])

        gap_summary = {
            "total_gaps": gaps.count(),
            "critical_gaps": gaps.filter(gap_severity="critical").count(),
            "high_gaps": gaps.filter(gap_severity="high").count(),
            "medium_gaps": gaps.filter(gap_severity="medium").count(),
            "low_gaps": gaps.filter(gap_severity="low").count(),
        }

        # Recommendations
        recommendations = []
        if gap_summary["critical_gaps"] > 0:
            recommendations.append(
                "Address critical gaps immediately - trainers cannot deliver assigned units"
            )
        if compliance_pct < 70:
            recommendations.append(
                "Overall compliance is below 70% - urgent review of trainer qualifications needed"
            )
        if gap_summary["high_gaps"] > 5:
            recommendations.append(
                "Multiple high-severity gaps identified - implement upskilling program"
            )

        # Generate markdown content
        report_content = f"""# {report_title}

## Executive Summary
- **Overall Compliance:** {compliance_pct:.1f}%
- **Total Assignments:** {total_assignments}
- **Compliant:** {compliant} ({compliance_pct:.1f}%)
- **Non-Compliant:** {total_assignments - compliant}

## Gap Summary
- **Critical Gaps:** {gap_summary['critical_gaps']}
- **High Priority:** {gap_summary['high_gaps']}
- **Medium Priority:** {gap_summary['medium_gaps']}
- **Low Priority:** {gap_summary['low_gaps']}

## Top Priority Actions
"""
        for i, rec in enumerate(recommendations, 1):
            report_content += f"{i}. {rec}\n"

        response_data = {
            "report_title": report_title,
            "report_date": report_date,
            "compliance_summary": compliance_summary,
            "trainer_reports": trainer_reports[:10],
            "unit_reports": unit_reports[:10],
            "gap_summary": gap_summary,
            "recommendations": recommendations,
            "report_content": report_content,
            "message": f"Report generated with {total_assignments} assignments analyzed",
        }

        resp_serializer = GenerateComplianceReportResponseSerializer(data=response_data)
        resp_serializer.is_valid(raise_exception=True)
        return Response(resp_serializer.data)

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        """Get dashboard statistics"""
        tenant = request.query_params.get("tenant")
        if not tenant:
            return Response(
                {"error": "tenant parameter required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Qualifications stats
        qualifications = TrainerQualification.objects.filter(tenant=tenant)
        total_trainers = qualifications.values("trainer_id").distinct().count()
        total_qualifications = qualifications.count()
        verified_qualifications = qualifications.filter(
            verification_status="verified"
        ).count()
        expired_qualifications = qualifications.filter(
            verification_status="expired"
        ).count()

        # Units stats
        units = UnitOfCompetency.objects.filter(tenant=tenant)
        total_units = units.count()
        core_units = units.filter(unit_type="core").count()
        elective_units = units.filter(unit_type="elective").count()

        # Assignments stats
        assignments = TrainerAssignment.objects.filter(tenant=tenant)
        total_assignments = assignments.count()
        approved_assignments = assignments.filter(assignment_status="approved").count()
        pending_assignments = assignments.filter(assignment_status="pending").count()
        rejected_assignments = assignments.filter(assignment_status="rejected").count()

        # Gaps stats
        gaps = CompetencyGap.objects.filter(tenant=tenant)
        total_gaps = gaps.count()
        critical_gaps = gaps.filter(gap_severity="critical").count()
        high_gaps = gaps.filter(gap_severity="high").count()
        unresolved_gaps = gaps.filter(is_resolved=False).count()

        # Compliance stats
        compliant_assignments = assignments.filter(meets_requirements=True).count()
        overall_compliance = (
            (compliant_assignments / total_assignments * 100)
            if total_assignments > 0
            else 0
        )

        thirty_days_ago = timezone.now() - timedelta(days=30)
        compliance_checks_this_month = ComplianceCheck.objects.filter(
            tenant=tenant, created_at__gte=thirty_days_ago
        ).count()

        # Recent checks
        recent_checks_qs = ComplianceCheck.objects.filter(tenant=tenant).order_by(
            "-created_at"
        )[:5]
        recent_checks = [
            {
                "check_id": check.check_id,
                "check_status": check.check_status,
                "compliance_score": check.overall_compliance_score,
                "gaps_found": check.gaps_found,
                "created_at": check.created_at.isoformat(),
            }
            for check in recent_checks_qs
        ]

        # Top gap types
        gap_types = (
            gaps.values("gap_type").annotate(count=Count("id")).order_by("-count")[:5]
        )
        top_gap_types = [
            {"gap_type": gt["gap_type"], "count": gt["count"]} for gt in gap_types
        ]

        # Trainers needing attention
        trainers_with_gaps = (
            gaps.filter(is_resolved=False)
            .values("trainer_id", "trainer_name")
            .annotate(gap_count=Count("id"))
            .order_by("-gap_count")[:5]
        )
        trainers_needing_attention = [
            {
                "trainer_id": t["trainer_id"],
                "trainer_name": t["trainer_name"],
                "unresolved_gaps": t["gap_count"],
            }
            for t in trainers_with_gaps
        ]

        stats = {
            "total_trainers": total_trainers,
            "total_qualifications": total_qualifications,
            "verified_qualifications": verified_qualifications,
            "expired_qualifications": expired_qualifications,
            "total_units": total_units,
            "core_units": core_units,
            "elective_units": elective_units,
            "total_assignments": total_assignments,
            "approved_assignments": approved_assignments,
            "pending_assignments": pending_assignments,
            "rejected_assignments": rejected_assignments,
            "total_gaps": total_gaps,
            "critical_gaps": critical_gaps,
            "high_gaps": high_gaps,
            "unresolved_gaps": unresolved_gaps,
            "overall_compliance_score": overall_compliance,
            "compliance_checks_this_month": compliance_checks_this_month,
            "recent_checks": recent_checks,
            "top_gap_types": top_gap_types,
            "trainers_needing_attention": trainers_needing_attention,
        }

        serializer = DashboardStatsSerializer(data=stats)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UnitOfCompetencyViewSet(viewsets.ModelViewSet):
    queryset = UnitOfCompetency.objects.all()
    serializer_class = UnitOfCompetencySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = self.request.query_params.get("tenant")
        if tenant:
            queryset = queryset.filter(tenant=tenant)

        qualification_code = self.request.query_params.get("qualification_code")
        if qualification_code:
            queryset = queryset.filter(qualification_code=qualification_code)

        unit_type = self.request.query_params.get("unit_type")
        if unit_type:
            queryset = queryset.filter(unit_type=unit_type)

        return queryset.order_by("unit_code")


class TrainerAssignmentViewSet(viewsets.ModelViewSet):
    queryset = TrainerAssignment.objects.all()
    serializer_class = TrainerAssignmentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = self.request.query_params.get("tenant")
        if tenant:
            queryset = queryset.filter(tenant=tenant)

        trainer_id = self.request.query_params.get("trainer_id")
        if trainer_id:
            queryset = queryset.filter(trainer_id=trainer_id)

        assignment_status = self.request.query_params.get("assignment_status")
        if assignment_status:
            queryset = queryset.filter(assignment_status=assignment_status)

        return queryset.order_by("-created_at")


class CompetencyGapViewSet(viewsets.ModelViewSet):
    queryset = CompetencyGap.objects.all()
    serializer_class = CompetencyGapSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = self.request.query_params.get("tenant")
        if tenant:
            queryset = queryset.filter(tenant=tenant)

        trainer_id = self.request.query_params.get("trainer_id")
        if trainer_id:
            queryset = queryset.filter(trainer_id=trainer_id)

        is_resolved = self.request.query_params.get("is_resolved")
        if is_resolved is not None:
            queryset = queryset.filter(is_resolved=is_resolved.lower() == "true")

        gap_severity = self.request.query_params.get("gap_severity")
        if gap_severity:
            queryset = queryset.filter(gap_severity=gap_severity)

        return queryset.order_by("-created_at")


class QualificationMappingViewSet(viewsets.ModelViewSet):
    queryset = QualificationMapping.objects.all()
    serializer_class = QualificationMappingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = self.request.query_params.get("tenant")
        if tenant:
            queryset = queryset.filter(tenant=tenant)

        return queryset.order_by("-match_strength")


class ComplianceCheckViewSet(viewsets.ModelViewSet):
    queryset = ComplianceCheck.objects.all()
    serializer_class = ComplianceCheckSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = self.request.query_params.get("tenant")
        if tenant:
            queryset = queryset.filter(tenant=tenant)

        check_status = self.request.query_params.get("check_status")
        if check_status:
            queryset = queryset.filter(check_status=check_status)

        return queryset.order_by("-created_at")
