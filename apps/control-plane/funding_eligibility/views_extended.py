"""
Extended views for funding eligibility system.
Implements hard-block enforcement for non-compliant enrolments.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction

from .models_extended import (
    Jurisdiction,
    Ruleset,
    RulesetArtifact,
    ReferenceTable,
    EligibilityRequest,
    ExternalLookup,
    EligibilityDecision,
    DecisionOverride,
    EvidenceAttachment,
    WebhookEndpoint,
    WebhookDelivery,
)
from .serializers_extended import (
    JurisdictionSerializer,
    RulesetSerializer,
    RulesetArtifactSerializer,
    ReferenceTableSerializer,
    EligibilityRequestSerializer,
    EligibilityRequestListSerializer,
    EligibilityDecisionSerializer,
    DecisionOverrideSerializer,
    EvidenceAttachmentSerializer,
    WebhookEndpointSerializer,
    WebhookDeliverySerializer,
    CreateEligibilityRequestSerializer,
    EvaluateRequestSerializer,
    CreateOverrideSerializer,
    UploadEvidenceSerializer,
    ActivateRulesetSerializer,
)
from .services.rules_engine import RulesEngine, EvaluationContext
from .services.connectors import ConnectorFactory

import logging

logger = logging.getLogger(__name__)


class TenantScopedMixin:
    """Mixin to scope querysets to tenant"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request.user, 'tenant'):
            return queryset.filter(tenant=self.request.user.tenant)
        return queryset.none()


class JurisdictionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Jurisdiction viewset - read-only, public access for browsing available jurisdictions.
    """
    queryset = Jurisdiction.objects.filter(active=True)
    serializer_class = JurisdictionSerializer
    permission_classes = [AllowAny]  # Public read-only access


class RulesetViewSet(viewsets.ModelViewSet):
    """
    Ruleset management viewset.
    """
    queryset = Ruleset.objects.all()
    serializer_class = RulesetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by jurisdiction"""
        queryset = super().get_queryset()
        jurisdiction = self.request.query_params.get('jurisdiction')
        
        if jurisdiction:
            queryset = queryset.filter(jurisdiction_code=jurisdiction)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set created_by"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a ruleset.
        Retires currently active rulesets for same jurisdiction.
        """
        ruleset = self.get_object()
        
        try:
            ruleset.activate()
            return Response({
                'status': 'activated',
                'ruleset': RulesetSerializer(ruleset).data
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def add_artifact(self, request, pk=None):
        """Add an artifact to a ruleset"""
        ruleset = self.get_object()
        
        if ruleset.status != 'draft':
            return Response(
                {'error': 'Can only add artifacts to draft rulesets'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = RulesetArtifactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ruleset=ruleset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferenceTableViewSet(viewsets.ModelViewSet):
    """
    Reference table management viewset.
    """
    queryset = ReferenceTable.objects.all()
    serializer_class = ReferenceTableSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by namespace"""
        queryset = super().get_queryset()
        namespace = self.request.query_params.get('namespace')
        
        if namespace:
            queryset = queryset.filter(namespace=namespace)
        
        # Only return currently valid tables by default
        now = timezone.now().date()
        return queryset.filter(
            valid_from__lte=now
        ).filter(
            models.Q(valid_until__gte=now) | models.Q(valid_until__isnull=True)
        )


class EligibilityRequestViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """
    Eligibility request viewset with hard-block enforcement.
    
    CRITICAL: Non-eligible requests MUST be blocked from proceeding to enrolment.
    """
    queryset = EligibilityRequest.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EligibilityRequestListSerializer
        elif self.action == 'create':
            return CreateEligibilityRequestSerializer
        return EligibilityRequestSerializer
    
    def get_queryset(self):
        """Filter by status, person, etc."""
        queryset = super().get_queryset()
        
        status_filter = self.request.query_params.get('status')
        person_id = self.request.query_params.get('person_id')
        jurisdiction = self.request.query_params.get('jurisdiction')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if person_id:
            queryset = queryset.filter(person_id=person_id)
        if jurisdiction:
            queryset = queryset.filter(jurisdiction_code=jurisdiction)
        
        return queryset.order_by('-requested_at')
    
    @transaction.atomic
    def create(self, request):
        """
        Create eligibility request and enqueue evaluation.
        """
        serializer = CreateEligibilityRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create request
        eligibility_request = EligibilityRequest.objects.create(
            tenant=request.user.tenant,
            person_id=serializer.validated_data['person_id'],
            course_id=serializer.validated_data['course_id'],
            jurisdiction_code=serializer.validated_data['jurisdiction_code'],
            input=serializer.validated_data['input'],
            metadata=serializer.validated_data.get('metadata', {}),
            requested_by=request.user,
        )
        
        # Enqueue external lookups
        from .tasks import enqueue_external_lookups
        enqueue_external_lookups.delay(eligibility_request.id)
        
        return Response(
            EligibilityRequestSerializer(eligibility_request).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def evaluate(self, request, pk=None):
        """
        Trigger eligibility evaluation.
        Uses rules engine to produce deterministic decision.
        """
        eligibility_request = self.get_object()
        
        serializer = EvaluateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        force = serializer.validated_data.get('force', False)
        ruleset_id = serializer.validated_data.get('ruleset_id')
        
        # Check if already evaluated
        if hasattr(eligibility_request, 'decision') and not force:
            return Response(
                {'error': 'Request already evaluated. Use force=true to re-evaluate.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get ruleset
        if ruleset_id:
            ruleset = get_object_or_404(Ruleset, id=ruleset_id, status='active')
        else:
            # Get active ruleset for jurisdiction
            ruleset = Ruleset.objects.filter(
                jurisdiction_code=eligibility_request.jurisdiction_code,
                status='active'
            ).first()
            
            if not ruleset:
                return Response(
                    {'error': 'No active ruleset for jurisdiction'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Collect external lookup results
        lookups = {}
        for lookup in eligibility_request.external_lookups.filter(status='success'):
            if lookup.provider not in lookups:
                lookups[lookup.provider] = {}
            lookups[lookup.provider].update(lookup.response_data)
        
        # TODO: Collect reference data
        reference_data = {}
        
        # Build evaluation context
        context = EvaluationContext(
            input_data=eligibility_request.input,
            lookups=lookups,
            reference_data=reference_data,
            jurisdiction_code=eligibility_request.jurisdiction_code,
            evaluation_date=timezone.now()
        )
        
        # Get ruleset artifacts
        artifacts = []
        for artifact in ruleset.artifacts.all():
            artifacts.append({
                'type': artifact.type,
                'name': artifact.name,
                'blob': artifact.blob,
            })
        
        # Evaluate
        engine = RulesEngine()
        result = engine.evaluate(artifacts, context, ruleset.version)
        
        # Create or update decision
        if hasattr(eligibility_request, 'decision') and force:
            # Delete old decision
            eligibility_request.decision.delete()
        
        decision = EligibilityDecision.objects.create(
            request=eligibility_request,
            ruleset=ruleset,
            outcome=result.outcome,
            reasons=result.reasons,
            clause_refs=result.clause_refs,
            decision_data=result.details,
            explanation=result.explanation,
            decided_by='system',
        )
        
        # Update request status
        eligibility_request.status = 'evaluated'
        eligibility_request.evaluated_at = timezone.now()
        eligibility_request.save()
        
        # Trigger webhooks for decision
        from .tasks import deliver_webhook
        deliver_webhook.delay(eligibility_request.id, 'decision.finalized')
        
        return Response(
            EligibilityDecisionSerializer(decision).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def check_eligibility(self, request, pk=None):
        """
        Check if request allows enrolment.
        
        HARD-BLOCK ENFORCEMENT:
        Returns 403 if decision is 'ineligible' and no override approved.
        SMS/LMS should check this endpoint before allowing enrolment.
        """
        eligibility_request = self.get_object()
        
        # Check if evaluated
        if not hasattr(eligibility_request, 'decision'):
            return Response(
                {
                    'can_enrol': False,
                    'reason': 'Eligibility not yet evaluated',
                    'status': eligibility_request.status
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        decision = eligibility_request.decision
        
        # Check for approved override
        approved_override = decision.overrides.filter(
            final_outcome='eligible'
        ).first()
        
        if approved_override:
            return Response({
                'can_enrol': True,
                'reason': 'Override approved',
                'decision': {
                    'outcome': approved_override.final_outcome,
                    'override_id': approved_override.id,
                    'approved_by': approved_override.approver.email,
                }
            })
        
        # Check decision outcome
        if decision.outcome == 'eligible':
            return Response({
                'can_enrol': True,
                'reason': 'Eligible',
                'decision': {
                    'outcome': decision.outcome,
                    'explanation': decision.explanation,
                }
            })
        elif decision.outcome == 'ineligible':
            return Response(
                {
                    'can_enrol': False,
                    'reason': 'Not eligible',
                    'decision': {
                        'outcome': decision.outcome,
                        'explanation': decision.explanation,
                        'reasons': decision.reasons,
                    }
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:  # 'review'
            return Response(
                {
                    'can_enrol': False,
                    'reason': 'Manual review required',
                    'decision': {
                        'outcome': decision.outcome,
                        'explanation': decision.explanation,
                    }
                },
                status=status.HTTP_403_FORBIDDEN
            )


class DecisionOverrideViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """
    Decision override viewset.
    Allows authorized users to override automated decisions.
    """
    queryset = DecisionOverride.objects.all()
    serializer_class = DecisionOverrideSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by decision"""
        queryset = DecisionOverride.objects.select_related(
            'decision__request__tenant'
        ).filter(
            decision__request__tenant=self.request.user.tenant
        )
        
        decision_id = self.request.query_params.get('decision')
        if decision_id:
            queryset = queryset.filter(decision_id=decision_id)
        
        return queryset.order_by('-approved_at')
    
    @transaction.atomic
    def create(self, request):
        """Create decision override"""
        serializer = CreateOverrideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        decision = get_object_or_404(
            EligibilityDecision,
            id=serializer.validated_data['decision_id']
        )
        
        # Check permissions (simplified - should check roles)
        if not request.user.is_staff:
            return Response(
                {'error': 'Only authorized staff can override decisions'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create override
        override = DecisionOverride.objects.create(
            decision=decision,
            reason_code=serializer.validated_data['reason_code'],
            justification=serializer.validated_data['justification'],
            final_outcome=serializer.validated_data['final_outcome'],
            policy_version=serializer.validated_data['policy_version'],
            evidence_refs=serializer.validated_data.get('evidence_refs', []),
            approver=request.user,
        )
        
        # Trigger webhooks
        from .tasks import deliver_webhook
        deliver_webhook.delay(decision.request.id, 'override.approved')
        
        return Response(
            DecisionOverrideSerializer(override).data,
            status=status.HTTP_201_CREATED
        )


class EvidenceAttachmentViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """
    Evidence attachment viewset.
    """
    queryset = EvidenceAttachment.objects.all()
    serializer_class = EvidenceAttachmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by request"""
        queryset = EvidenceAttachment.objects.select_related(
            'request__tenant'
        ).filter(
            request__tenant=self.request.user.tenant
        )
        
        request_id = self.request.query_params.get('request')
        if request_id:
            queryset = queryset.filter(request_id=request_id)
        
        return queryset.order_by('-uploaded_at')
    
    @transaction.atomic
    def create(self, request):
        """Upload evidence file"""
        # TODO: Implement file upload to S3
        # For now, return placeholder
        
        return Response(
            {'error': 'File upload not yet implemented'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Mark evidence as verified"""
        attachment = self.get_object()
        
        notes = request.data.get('notes', '')
        
        attachment.verified = True
        attachment.verifier = request.user
        attachment.verified_at = timezone.now()
        attachment.verification_notes = notes
        attachment.save()
        
        return Response(
            EvidenceAttachmentSerializer(attachment).data
        )


class WebhookEndpointViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """
    Webhook endpoint management viewset.
    """
    queryset = WebhookEndpoint.objects.all()
    serializer_class = WebhookEndpointSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Set tenant"""
        serializer.save(tenant=self.request.user.tenant)
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """Test webhook endpoint"""
        endpoint = self.get_object()
        
        # Send test event
        from .tasks import deliver_webhook_to_endpoint
        
        test_payload = {
            'event_type': 'test',
            'timestamp': timezone.now().isoformat(),
            'data': {'message': 'Test webhook'}
        }
        
        deliver_webhook_to_endpoint.delay(endpoint.id, test_payload)
        
        return Response({'status': 'test event queued'})
