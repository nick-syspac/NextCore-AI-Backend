from typing import Optional

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q, Prefetch

from .models import Evidence, ClauseEvidence, AuditReport, AuditReportClause
from .serializers import (
    EvidenceSerializer, ClauseEvidenceSerializer,
    AuditReportSerializer, AuditReportDetailSerializer, AuditReportClauseSerializer,
    EvidenceUploadSerializer, ClauseEvidenceGapSerializer
)
from policy_comparator.models import ASQAClause, ASQAStandard
from tenants.models import Tenant

from .services import auto_tag_clauses, detect_ner_entities, extract_text_from_file
from .tasks import process_evidence_document


class TenantScopedViewSetMixin:
    """Common helpers for retrieving the tenant from request context."""

    _tenant: Optional[Tenant] = None

    def get_tenant(self) -> Tenant:
        if self._tenant:
            return self._tenant

        tenant_slug = self.kwargs.get("tenant_slug")
        tenant_id = self.kwargs.get("tenant_id") or getattr(self.request, "tenant_id", None)

        if tenant_slug:
            tenant = get_object_or_404(Tenant, slug=tenant_slug)
        elif tenant_id:
            tenant = get_object_or_404(Tenant, id=tenant_id)
        else:
            raise NotFound("Tenant context is required for this endpoint.")

        self._tenant = tenant
        return tenant


class EvidenceViewSet(TenantScopedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for evidence document management with NER auto-tagging
    """
    serializer_class = EvidenceSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filterset_fields = ["status", "evidence_type"]
    search_fields = ["evidence_number", "title", "description"]
    ordering_fields = ["uploaded_at", "evidence_date", "file_size"]
    ordering = ["-uploaded_at"]
    
    def get_queryset(self):
        tenant = self.get_tenant()
        return Evidence.objects.filter(tenant=tenant).select_related(
            'uploaded_by', 'reviewed_by'
        ).prefetch_related('auto_tagged_clauses')
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload(self, request, _tenant_id=None):
        """Upload evidence file and queue background processing."""
        tenant = self.get_tenant()
        serializer = EvidenceUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auto_tag = serializer.validated_data.get('auto_tag', True)
        uploaded_file = serializer.validated_data['file']
        file_size = getattr(uploaded_file, 'size', None)

        evidence = Evidence.objects.create(
            tenant=tenant,
            evidence_number=serializer.validated_data['evidence_number'],
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', ''),
            evidence_type=serializer.validated_data['evidence_type'],
            file=uploaded_file,
            file_size=file_size,
            evidence_date=serializer.validated_data['evidence_date'],
            tags=serializer.validated_data.get('tags', []),
            uploaded_by=request.user,
            status='processing' if auto_tag else 'uploaded'
        )

        # Kick off asynchronous processing (runs synchronously in eager mode during tests)
        process_evidence_document.delay(evidence.id, auto_tag=auto_tag)

        serializer_context = {'request': request}
        response_payload = EvidenceSerializer(evidence, context=serializer_context).data
        response_payload['processing'] = auto_tag

        return Response(response_payload, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def process_ner(self, request, _tenant_id=None, pk=None):
        """Manually trigger NER processing and auto-tagging for an evidence document."""
        evidence = self.get_object()

        extracted_text = evidence.extracted_text or extract_text_from_file(evidence)
        if not extracted_text:
            return Response(
                {"error": "No text available for NER processing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        evidence.extracted_text = extracted_text
        evidence.status = "processing"
        evidence.save(update_fields=["extracted_text", "status"])

        ner_entities = detect_ner_entities(extracted_text)
        evidence.ner_entities = ner_entities
        evidence.ner_processed_at = timezone.now()

        auto_tagged_count = auto_tag_clauses(evidence, extracted_text, ner_entities)

        evidence.status = "tagged" if auto_tagged_count > 0 else "uploaded"
        evidence.save(update_fields=["ner_entities", "ner_processed_at", "status"])

        payload = EvidenceSerializer(evidence, context={'request': request}).data

        return Response({
            "message": (
                f"NER processing complete. {len(ner_entities)} entities found. "
                f"{auto_tagged_count} clauses auto-tagged."
            ),
            "ner_entities": ner_entities,
            "auto_tagged_count": auto_tagged_count,
            "evidence": payload,
        })
    
    @action(detail=True, methods=['get'])
    def tagged_clauses(self, request, _tenant_id=None, pk=None):
        """
        Get all clauses tagged to this evidence with mapping details
        """
        evidence = self.get_object()
        mappings = ClauseEvidence.objects.filter(evidence=evidence).select_related(
            'asqa_clause', 'asqa_clause__standard', 'verified_by'
        ).order_by('-confidence_score')
        
        serializer = ClauseEvidenceSerializer(mappings, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def verify_tagging(self, request, _tenant_id=None, pk=None):
        """
        Verify/approve auto-tagged clauses for evidence
        """
        evidence = self.get_object()
        clause_evidence_ids = request.data.get('clause_evidence_ids', [])
        
        updated_count = ClauseEvidence.objects.filter(
            id__in=clause_evidence_ids,
            evidence=evidence
        ).update(
            is_verified=True,
            verified_by=request.user,
            verified_at=timezone.now()
        )
        
        if updated_count > 0:
            evidence.status = 'reviewed'
            evidence.reviewed_by = request.user
            evidence.reviewed_at = timezone.now()
            evidence.save()
        
        return Response({
            'message': f'{updated_count} clause mappings verified.',
            'evidence': EvidenceSerializer(evidence, context={'request': request}).data
        })
    

class ClauseEvidenceViewSet(TenantScopedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing clause-evidence mappings
    """
    serializer_class = ClauseEvidenceSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        return ClauseEvidence.objects.filter(
            evidence__tenant=tenant
        ).select_related(
            'asqa_clause', 'asqa_clause__standard',
            'evidence', 'verified_by'
        )
    
    @action(detail=False, methods=['get'])
    def gaps(self, request, _tenant_id=None):
        """
        Identify clauses with insufficient evidence (gap analysis)
        """
        tenant = self.get_tenant()
        standard_ids = request.query_params.getlist('standard_ids')
        
        # Get clauses for specified standards
        clauses_query = ASQAClause.objects.all()
        if standard_ids:
            clauses_query = clauses_query.filter(standard_id__in=standard_ids)
        
        gaps = []
        for clause in clauses_query.select_related('standard'):
            # Count evidence for this clause
            evidence_count = ClauseEvidence.objects.filter(
                asqa_clause=clause,
                evidence__tenant=tenant,
                evidence__status__in=['tagged', 'reviewed', 'approved']
            ).count()
            
            verified_count = ClauseEvidence.objects.filter(
                asqa_clause=clause,
                evidence__tenant=tenant,
                evidence__status__in=['tagged', 'reviewed', 'approved'],
                is_verified=True
            ).count()
            
            # Determine if sufficient evidence
            has_sufficient = verified_count >= 2  # At least 2 verified evidence items
            
            # Calculate gap severity
            if clause.compliance_level == 'critical':
                gap_severity = 'critical' if evidence_count == 0 else ('major' if verified_count < 2 else 'none')
            elif clause.compliance_level == 'essential':
                gap_severity = 'major' if evidence_count == 0 else ('minor' if verified_count < 1 else 'none')
            else:
                gap_severity = 'minor' if evidence_count == 0 else 'none'
            
            # Generate recommendations
            recommendations = []
            if evidence_count == 0:
                recommendations.append(f"Upload evidence for {clause.clause_number}")
                recommendations.append(f"Review policies related to: {', '.join(clause.keywords[:3]) if clause.keywords else 'this clause'}")
            elif verified_count < 2:
                recommendations.append(f"Verify existing evidence for {clause.clause_number}")
                recommendations.append("Upload additional supporting evidence")
            
            if gap_severity != 'none':
                gaps.append({
                    'asqa_clause': clause.id,
                    'clause_number': clause.clause_number,
                    'clause_title': clause.title,
                    'compliance_level': clause.compliance_level,
                    'evidence_count': evidence_count,
                    'verified_evidence_count': verified_count,
                    'has_sufficient_evidence': has_sufficient,
                    'gap_severity': gap_severity,
                    'recommendations': recommendations
                })
        
        return Response({
            'total_clauses': clauses_query.count(),
            'clauses_with_gaps': len(gaps),
            'critical_gaps': len([g for g in gaps if g['gap_severity'] == 'critical']),
            'major_gaps': len([g for g in gaps if g['gap_severity'] == 'major']),
            'minor_gaps': len([g for g in gaps if g['gap_severity'] == 'minor']),
            'gaps': gaps
        })


class AuditReportViewSet(TenantScopedViewSetMixin, viewsets.ModelViewSet):
    """
    ViewSet for audit report management
    """
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuditReportDetailSerializer
        return AuditReportSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        return AuditReport.objects.filter(tenant=tenant).prefetch_related(
            'asqa_standards',
            Prefetch('clause_entries', queryset=AuditReportClause.objects.select_related('asqa_clause'))
        )
    
    def perform_create(self, serializer):
        audit_report = serializer.save(
            tenant=self.get_tenant(),
            created_by=self.request.user
        )
        
        # Auto-generate clause entries
        self._generate_clause_entries(audit_report)
        
        # Calculate metrics
        audit_report.calculate_metrics()
    
    @action(detail=True, methods=['post'])
    def generate_report(self, request, _tenant_id=None, pk=None):
        """
        Generate clause-by-clause audit report with evidence mapping
        """
        audit_report = self.get_object()
        
        # Regenerate clause entries
        audit_report.clause_entries.all().delete()
        self._generate_clause_entries(audit_report)
        
        # Recalculate metrics
        audit_report.calculate_metrics()
        
        return Response(
            AuditReportDetailSerializer(audit_report, context={'request': request}).data
        )
    
    @action(detail=True, methods=['post'])
    def submit(self, request, _tenant_id=None, pk=None):
        """
        Submit audit report (mark as submitted to ASQA)
        """
        audit_report = self.get_object()
        
        if audit_report.status == 'submitted':
            return Response(
                {'error': 'Report already submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        audit_report.status = 'submitted'
        audit_report.submitted_at = timezone.now()
        audit_report.submitted_by = request.user
        audit_report.save()
        
        return Response(
            AuditReportSerializer(audit_report, context={'request': request}).data
        )
    
    def _generate_clause_entries(self, audit_report):
        """
        Generate clause entries for all clauses in selected standards
        """
        all_clauses = ASQAClause.objects.filter(
            standard__in=audit_report.asqa_standards.all()
        ).select_related('standard')
        
        for clause in all_clauses:
            entry = AuditReportClause.objects.create(
                audit_report=audit_report,
                asqa_clause=clause
            )
            
            # Update evidence counts and determine compliance
            entry.update_evidence_counts()
            
            # Link evidence
            evidence_mappings = ClauseEvidence.objects.filter(
                asqa_clause=clause,
                evidence__tenant=audit_report.tenant,
                evidence__status__in=['tagged', 'reviewed', 'approved']
            ).select_related('evidence')
            
            for mapping in evidence_mappings:
                entry.linked_evidence.add(mapping.evidence)
