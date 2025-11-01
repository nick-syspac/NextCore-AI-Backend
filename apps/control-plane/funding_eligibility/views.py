from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    JurisdictionRequirement,
    EligibilityRule,
    EligibilityCheck,
    EligibilityCheckLog,
)
from .serializers import (
    JurisdictionRequirementSerializer,
    EligibilityRuleSerializer,
    EligibilityCheckSerializer,
    EligibilityCheckDetailSerializer,
    EligibilityCheckRequestSerializer,
    DashboardStatsSerializer,
)


class JurisdictionRequirementViewSet(viewsets.ModelViewSet):
    serializer_class = JurisdictionRequirementSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        return JurisdictionRequirement.objects.filter(tenant=tenant)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant, created_by=self.request.user)

    @action(detail=False, methods=["get"])
    def active(self, request):
        """Get currently active jurisdiction requirements"""
        tenant = request.tenant
        today = timezone.now().date()

        active_requirements = JurisdictionRequirement.objects.filter(
            tenant=tenant, is_active=True, effective_from__lte=today
        ).filter(Q(effective_to__isnull=True) | Q(effective_to__gte=today))

        serializer = self.get_serializer(active_requirements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def requirements_summary(self, request, pk=None):
        """Get human-readable summary of requirements"""
        requirement = self.get_object()

        summary = {
            "jurisdiction": requirement.get_jurisdiction_display(),
            "program_name": requirement.name,
            "funding_coverage": f"{requirement.funding_percentage}%",
            "student_contribution": f"${requirement.student_contribution}",
            "requirements": [],
        }

        # Build requirements list
        if requirement.requires_australian_citizen:
            summary["requirements"].append("Must be Australian citizen")
        elif requirement.requires_permanent_resident:
            summary["requirements"].append("Must be permanent resident")

        if requirement.requires_jurisdiction_resident:
            summary["requirements"].append(
                f"Must reside in {requirement.get_jurisdiction_display()} for at least "
                f"{requirement.min_jurisdiction_residency_months} months"
            )

        if requirement.min_age or requirement.max_age:
            age_req = "Age: "
            if requirement.min_age and requirement.max_age:
                age_req += f"{requirement.min_age}-{requirement.max_age} years"
            elif requirement.min_age:
                age_req += f"{requirement.min_age}+ years"
            else:
                age_req += f"under {requirement.max_age} years"
            summary["requirements"].append(age_req)

        if requirement.requires_year_12:
            summary["requirements"].append("Year 12 completion required")

        if requirement.requires_unemployed:
            summary["requirements"].append("Must be unemployed")
        elif requirement.requires_apprentice_trainee:
            summary["requirements"].append("Must be apprentice or trainee")

        if requirement.restricts_higher_qualifications:
            summary["requirements"].append(
                f"Cannot have qualifications higher than AQF {requirement.max_aqf_level or 'course level'}"
            )

        if requirement.has_income_threshold:
            summary["requirements"].append(
                f"Annual income must be below ${requirement.max_annual_income}"
            )

        # Priority groups
        priority = []
        if requirement.priority_indigenous:
            priority.append("Indigenous Australians (priority)")
        if requirement.allows_concession_card:
            priority.append("Concession card holders")
        if requirement.allows_disability:
            priority.append("People with disability")

        if priority:
            summary["priority_groups"] = priority

        return Response(summary)


class EligibilityRuleViewSet(viewsets.ModelViewSet):
    serializer_class = EligibilityRuleSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        queryset = EligibilityRule.objects.filter(tenant=tenant)

        # Filter by jurisdiction requirement
        jurisdiction_req = self.request.query_params.get("jurisdiction_requirement")
        if jurisdiction_req:
            queryset = queryset.filter(jurisdiction_requirement_id=jurisdiction_req)

        return queryset

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant, created_by=self.request.user)


class EligibilityCheckViewSet(viewsets.ModelViewSet):
    serializer_class = EligibilityCheckSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        queryset = EligibilityCheck.objects.filter(tenant=tenant)

        # Filters
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        jurisdiction = self.request.query_params.get("jurisdiction")
        if jurisdiction:
            queryset = queryset.filter(jurisdiction=jurisdiction)

        eligible = self.request.query_params.get("is_eligible")
        if eligible is not None:
            queryset = queryset.filter(is_eligible=eligible.lower() == "true")

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EligibilityCheckDetailSerializer
        return EligibilityCheckSerializer

    @action(detail=False, methods=["post"])
    def check_eligibility(self, request):
        """
        Perform eligibility check with rules engine validation
        """
        serializer = EligibilityCheckRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Find appropriate jurisdiction requirement
        jurisdiction_req = JurisdictionRequirement.objects.filter(
            tenant=request.tenant, jurisdiction=data["jurisdiction"], is_active=True
        ).first()

        if not jurisdiction_req or not jurisdiction_req.is_currently_effective():
            return Response(
                {
                    "error": f"No active funding program found for {data['jurisdiction']}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Prepare student data
        student_data = {
            "citizenship_status": data.get("citizenship_status"),
            "is_jurisdiction_resident": data.get("is_jurisdiction_resident"),
            "jurisdiction_residency_months": data.get(
                "jurisdiction_residency_months", 0
            ),
            "highest_education": data.get("highest_education"),
            "highest_aqf_level": data.get("highest_aqf_level", 0),
            "employment_status": data.get("employment_status"),
            "annual_income": float(data.get("annual_income", 0)),
            "has_concession_card": data.get("has_concession_card", False),
            "concession_card_type": data.get("concession_card_type", ""),
            "has_disability": data.get("has_disability", False),
            "is_indigenous": data.get("is_indigenous", False),
            "visa_type": data.get("visa_type", ""),
            "visa_expiry": data.get("visa_expiry"),
            "age": None,  # Will calculate
        }

        # Calculate age
        dob = data["student_dob"]
        today = timezone.now().date()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        student_data["age"] = age

        # Run rules engine
        check_results = self._run_rules_engine(
            jurisdiction_req, data["aqf_level"], student_data
        )

        # Create eligibility check record
        eligibility_check = EligibilityCheck.objects.create(
            tenant=request.tenant,
            student_first_name=data["student_first_name"],
            student_last_name=data["student_last_name"],
            student_dob=data["student_dob"],
            student_email=data["student_email"],
            student_phone=data.get("student_phone", ""),
            course_code=data["course_code"],
            course_name=data["course_name"],
            aqf_level=data["aqf_level"],
            intended_start_date=data["intended_start_date"],
            jurisdiction=data["jurisdiction"],
            jurisdiction_requirement=jurisdiction_req,
            funding_program_code=data.get(
                "funding_program_code", jurisdiction_req.code
            ),
            student_data=student_data,
            status=check_results["status"],
            is_eligible=check_results["is_eligible"],
            eligibility_percentage=check_results["eligibility_percentage"],
            rules_checked=check_results["rules_checked"],
            rules_passed=check_results["rules_passed"],
            rules_failed=check_results["rules_failed"],
            check_results=check_results["details"],
            failed_rules=check_results["failed_rules"],
            warnings=check_results["warnings"],
            override_required=check_results["override_required"],
            prevents_enrollment=not check_results["is_eligible"]
            and not check_results["override_required"],
            checked_by=request.user,
        )

        # Create log entry
        EligibilityCheckLog.objects.create(
            eligibility_check=eligibility_check,
            action="check_created",
            details={"rules_results": check_results},
            notes=f"Eligibility check performed for {data['course_code']}",
            performed_by=request.user,
        )

        # Call external API if configured
        if jurisdiction_req.api_endpoint:
            api_result = self._call_verification_api(
                jurisdiction_req, eligibility_check, student_data
            )
            if api_result:
                eligibility_check.api_verified = True
                eligibility_check.api_response = api_result
                eligibility_check.api_verified_at = timezone.now()
                eligibility_check.save()

                EligibilityCheckLog.objects.create(
                    eligibility_check=eligibility_check,
                    action="api_called",
                    details={"api_response": api_result},
                    performed_by=request.user,
                )

        serializer = EligibilityCheckDetailSerializer(eligibility_check)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _run_rules_engine(self, jurisdiction_req, aqf_level, student_data):
        """
        Execute rules engine to validate eligibility
        """
        results = {
            "is_eligible": True,
            "status": "pending",
            "eligibility_percentage": 0.0,
            "rules_checked": 0,
            "rules_passed": 0,
            "rules_failed": 0,
            "details": {},
            "failed_rules": [],
            "warnings": [],
            "override_required": False,
        }

        failed_mandatory = []
        failed_optional = []

        # Check jurisdiction requirement rules
        jr_checks = self._check_jurisdiction_requirements(
            jurisdiction_req, aqf_level, student_data
        )
        results["rules_checked"] += jr_checks["checked"]
        results["rules_passed"] += jr_checks["passed"]
        results["rules_failed"] += jr_checks["failed"]
        results["details"]["jurisdiction_checks"] = jr_checks["details"]
        failed_mandatory.extend(jr_checks["failed_mandatory"])
        results["warnings"].extend(jr_checks["warnings"])

        # Check custom rules
        custom_rules = EligibilityRule.objects.filter(
            tenant=jurisdiction_req.tenant,
            jurisdiction_requirement=jurisdiction_req,
            is_active=True,
        ).order_by("priority")

        custom_results = []
        for rule in custom_rules:
            passed, message = rule.evaluate(student_data)
            results["rules_checked"] += 1

            rule_result = {
                "rule_name": rule.name,
                "rule_type": rule.rule_type,
                "passed": passed,
                "message": message,
                "is_mandatory": rule.is_mandatory,
                "override_allowed": rule.override_allowed,
            }
            custom_results.append(rule_result)

            if passed:
                results["rules_passed"] += 1
            else:
                results["rules_failed"] += 1
                if rule.is_mandatory:
                    failed_mandatory.append(rule_result)
                else:
                    failed_optional.append(rule_result)

        results["details"]["custom_rules"] = custom_results

        # Determine eligibility
        if failed_mandatory:
            results["is_eligible"] = False
            results["status"] = "ineligible"
            results["failed_rules"] = failed_mandatory

            # Check if all failed rules allow override
            if all(r.get("override_allowed", False) for r in failed_mandatory):
                results["override_required"] = True
                results["status"] = "conditional"
        elif failed_optional:
            results["is_eligible"] = True
            results["status"] = "conditional"
            results["warnings"].extend([r["message"] for r in failed_optional])
        else:
            results["is_eligible"] = True
            results["status"] = "eligible"

        # Calculate eligibility percentage
        if results["rules_checked"] > 0:
            results["eligibility_percentage"] = round(
                (results["rules_passed"] / results["rules_checked"]) * 100, 2
            )

        return results

    def _check_jurisdiction_requirements(self, req, aqf_level, student_data):
        """
        Check jurisdiction-specific requirements
        """
        result = {
            "checked": 0,
            "passed": 0,
            "failed": 0,
            "details": [],
            "failed_mandatory": [],
            "warnings": [],
        }

        # Citizenship check
        result["checked"] += 1
        citizenship = student_data.get("citizenship_status")
        if req.requires_australian_citizen:
            if citizenship == "citizen":
                result["passed"] += 1
                result["details"].append(
                    {
                        "check": "citizenship",
                        "passed": True,
                        "message": "Australian citizen",
                    }
                )
            else:
                result["failed"] += 1
                result["failed_mandatory"].append(
                    {
                        "rule_name": "Australian Citizenship",
                        "message": "Must be Australian citizen",
                        "override_allowed": False,
                    }
                )
                result["details"].append(
                    {
                        "check": "citizenship",
                        "passed": False,
                        "message": "Not Australian citizen",
                    }
                )
        elif req.requires_permanent_resident:
            if citizenship in ["citizen", "permanent_resident"]:
                result["passed"] += 1
                result["details"].append(
                    {
                        "check": "citizenship",
                        "passed": True,
                        "message": f"{citizenship}",
                    }
                )
            else:
                result["failed"] += 1
                result["failed_mandatory"].append(
                    {
                        "rule_name": "Permanent Residency",
                        "message": "Must be Australian citizen or permanent resident",
                        "override_allowed": False,
                    }
                )
                result["details"].append(
                    {
                        "check": "citizenship",
                        "passed": False,
                        "message": f"{citizenship} not eligible",
                    }
                )
        else:
            result["passed"] += 1
            result["details"].append(
                {
                    "check": "citizenship",
                    "passed": True,
                    "message": "No citizenship restriction",
                }
            )

        # Residency check
        if req.requires_jurisdiction_resident:
            result["checked"] += 1
            if student_data.get("is_jurisdiction_resident"):
                residency_months = student_data.get("jurisdiction_residency_months", 0)
                if residency_months >= req.min_jurisdiction_residency_months:
                    result["passed"] += 1
                    result["details"].append(
                        {
                            "check": "residency",
                            "passed": True,
                            "message": f"Resident for {residency_months} months",
                        }
                    )
                else:
                    result["failed"] += 1
                    result["failed_mandatory"].append(
                        {
                            "rule_name": "Jurisdiction Residency",
                            "message": f"Must reside in jurisdiction for at least {req.min_jurisdiction_residency_months} months",
                            "override_allowed": True,
                        }
                    )
                    result["details"].append(
                        {
                            "check": "residency",
                            "passed": False,
                            "message": f"Only {residency_months} months residency",
                        }
                    )
            else:
                result["failed"] += 1
                result["failed_mandatory"].append(
                    {
                        "rule_name": "Jurisdiction Residency",
                        "message": "Must be resident of jurisdiction",
                        "override_allowed": True,
                    }
                )
                result["details"].append(
                    {
                        "check": "residency",
                        "passed": False,
                        "message": "Not jurisdiction resident",
                    }
                )

        # Age check
        if req.min_age or req.max_age:
            result["checked"] += 1
            age = student_data.get("age", 0)
            age_ok = True
            age_msg = f"Age {age}"

            if req.min_age and age < req.min_age:
                age_ok = False
                age_msg = f"Age {age} below minimum {req.min_age}"
            if req.max_age and age > req.max_age:
                age_ok = False
                age_msg = f"Age {age} above maximum {req.max_age}"

            if age_ok:
                result["passed"] += 1
                result["details"].append(
                    {"check": "age", "passed": True, "message": age_msg}
                )
            else:
                result["failed"] += 1
                result["failed_mandatory"].append(
                    {
                        "rule_name": "Age Requirement",
                        "message": age_msg,
                        "override_allowed": True,
                    }
                )
                result["details"].append(
                    {"check": "age", "passed": False, "message": age_msg}
                )

        # Prior qualification check
        if req.restricts_higher_qualifications and req.max_aqf_level:
            result["checked"] += 1
            existing_aqf = student_data.get("highest_aqf_level", 0)

            if existing_aqf <= aqf_level:
                result["passed"] += 1
                result["details"].append(
                    {
                        "check": "prior_qualification",
                        "passed": True,
                        "message": f"Existing AQF {existing_aqf} <= course AQF {aqf_level}",
                    }
                )
            else:
                result["failed"] += 1
                result["failed_mandatory"].append(
                    {
                        "rule_name": "Prior Qualification Restriction",
                        "message": f"Cannot have qualification higher than AQF {aqf_level} (you have AQF {existing_aqf})",
                        "override_allowed": True,
                    }
                )
                result["details"].append(
                    {
                        "check": "prior_qualification",
                        "passed": False,
                        "message": f"Existing AQF {existing_aqf} > course AQF {aqf_level}",
                    }
                )

        # Income check
        if req.has_income_threshold and req.max_annual_income:
            result["checked"] += 1
            income = student_data.get("annual_income", 0)

            if income <= float(req.max_annual_income):
                result["passed"] += 1
                result["details"].append(
                    {
                        "check": "income",
                        "passed": True,
                        "message": f"Income ${income} within threshold ${req.max_annual_income}",
                    }
                )
            else:
                result["failed"] += 1
                result["failed_mandatory"].append(
                    {
                        "rule_name": "Income Threshold",
                        "message": f"Annual income ${income} exceeds maximum ${req.max_annual_income}",
                        "override_allowed": True,
                    }
                )
                result["details"].append(
                    {
                        "check": "income",
                        "passed": False,
                        "message": f"Income ${income} exceeds ${req.max_annual_income}",
                    }
                )

        # Employment check
        if req.requires_unemployed:
            result["checked"] += 1
            emp_status = student_data.get("employment_status")
            if emp_status == "unemployed":
                result["passed"] += 1
                result["details"].append(
                    {"check": "employment", "passed": True, "message": "Unemployed"}
                )
            else:
                result["failed"] += 1
                result["failed_mandatory"].append(
                    {
                        "rule_name": "Unemployment Requirement",
                        "message": "Must be unemployed",
                        "override_allowed": True,
                    }
                )
                result["details"].append(
                    {
                        "check": "employment",
                        "passed": False,
                        "message": f"Status: {emp_status}",
                    }
                )
        elif req.requires_apprentice_trainee:
            result["checked"] += 1
            emp_status = student_data.get("employment_status")
            if emp_status in ["apprentice", "trainee"]:
                result["passed"] += 1
                result["details"].append(
                    {
                        "check": "employment",
                        "passed": True,
                        "message": emp_status.title(),
                    }
                )
            else:
                result["failed"] += 1
                result["failed_mandatory"].append(
                    {
                        "rule_name": "Apprentice/Trainee Requirement",
                        "message": "Must be apprentice or trainee",
                        "override_allowed": False,
                    }
                )
                result["details"].append(
                    {
                        "check": "employment",
                        "passed": False,
                        "message": f"Status: {emp_status}",
                    }
                )

        return result

    def _call_verification_api(self, jurisdiction_req, eligibility_check, student_data):
        """
        Call external API for verification (mock for now)
        """
        if not jurisdiction_req.api_endpoint:
            return None

        try:
            # Mock API call - replace with actual implementation
            # In production, this would call state/federal government APIs
            payload = {
                "student_email": eligibility_check.student_email,
                "dob": str(eligibility_check.student_dob),
                "jurisdiction": eligibility_check.jurisdiction,
                "course_code": eligibility_check.course_code,
            }

            # For demo purposes, return mock response
            return {
                "verified": True,
                "verification_id": f'API-{timezone.now().strftime("%Y%m%d-%H%M%S")}',
                "message": "Mock API verification successful",
                "timestamp": timezone.now().isoformat(),
            }

            # Actual API call would be:
            # headers = {}
            # if jurisdiction_req.api_key_required:
            #     headers['Authorization'] = f'Bearer {get_api_key()}'
            #
            # response = requests.post(
            #     jurisdiction_req.api_endpoint,
            #     json=payload,
            #     headers=headers,
            #     timeout=10
            # )
            # return response.json()

        except Exception as e:
            return {"error": str(e), "verified": False}

    @action(detail=True, methods=["post"])
    def approve_override(self, request, pk=None):
        """
        Approve eligibility override
        """
        check = self.get_object()

        if not check.override_required:
            return Response(
                {"error": "This check does not require override"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reason = request.data.get("reason", "")
        if not reason:
            return Response(
                {"error": "Override reason is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        check.override_approved = True
        check.override_reason = reason
        check.override_approved_by = request.user
        check.override_approved_at = timezone.now()
        check.status = "override"
        check.is_eligible = True
        check.prevents_enrollment = False
        check.save()

        EligibilityCheckLog.objects.create(
            eligibility_check=check,
            action="override_approved",
            details={"reason": reason},
            notes=f"Override approved by {request.user.get_full_name()}",
            performed_by=request.user,
        )

        serializer = self.get_serializer(check)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def dashboard_stats(self, request):
        """
        Get dashboard statistics
        """
        tenant = request.tenant

        # Date range
        thirty_days_ago = timezone.now() - timedelta(days=30)

        checks = EligibilityCheck.objects.filter(tenant=tenant)
        recent_checks = checks.filter(checked_at__gte=thirty_days_ago)

        stats = {
            "total_checks": checks.count(),
            "eligible_count": checks.filter(is_eligible=True).count(),
            "ineligible_count": checks.filter(is_eligible=False).count(),
            "pending_count": checks.filter(status="pending").count(),
            "override_count": checks.filter(status="override").count(),
            "eligibility_rate": 0.0,
            "by_jurisdiction": {},
            "by_status": {},
            "recent_checks": recent_checks.count(),
            "prevented_enrollments": checks.filter(prevents_enrollment=True).count(),
            "top_failure_reasons": [],
        }

        # Eligibility rate
        if stats["total_checks"] > 0:
            stats["eligibility_rate"] = round(
                (stats["eligible_count"] / stats["total_checks"]) * 100, 2
            )

        # By jurisdiction
        by_jurisdiction = checks.values("jurisdiction").annotate(count=Count("id"))
        stats["by_jurisdiction"] = {
            item["jurisdiction"]: item["count"] for item in by_jurisdiction
        }

        # By status
        by_status = checks.values("status").annotate(count=Count("id"))
        stats["by_status"] = {item["status"]: item["count"] for item in by_status}

        # Top failure reasons
        ineligible_checks = checks.filter(is_eligible=False)
        failure_reasons = {}
        for check in ineligible_checks:
            for failed_rule in check.failed_rules:
                rule_name = failed_rule.get("rule_name", "Unknown")
                failure_reasons[rule_name] = failure_reasons.get(rule_name, 0) + 1

        stats["top_failure_reasons"] = [
            {"reason": reason, "count": count}
            for reason, count in sorted(
                failure_reasons.items(), key=lambda x: x[1], reverse=True
            )[:5]
        ]

        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)
