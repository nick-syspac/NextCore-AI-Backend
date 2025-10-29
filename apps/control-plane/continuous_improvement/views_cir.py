"""
Extended viewsets for Continuous Improvement Register (CIR).
Provides REST API endpoints for all CIR entities with tenant scoping.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from django.db.models import Count, Avg, Q, F, Prefetch

from tenants.models import Tenant
from .models import ImprovementAction
from .models_cir import (
    ActionStep,
    Comment,
    Attachment,
    Verification,
    ClauseLink,
    SLAPolicy,
    KPISnapshot,
    TaxonomyLabel,
    AIRun,
)
from .serializers_cir import (
    ActionStepSerializer,
    CommentSerializer,
    CommentDetailSerializer,
    AttachmentSerializer,
    VerificationSerializer,
    ClauseLinkSerializer,
    SLAPolicySerializer,
    KPISnapshotSerializer,
    TaxonomyLabelSerializer,
    AIRunSerializer,
    ImprovementActionCIRDetailSerializer,
    ComplianceDashboardSerializer,
    AIClassifyRequestSerializer,
    AIClassifyResponseSerializer,
    AISummarizeRequestSerializer,
    AISummarizeResponseSerializer,
)
from .tasks_cir import (
    classify_improvement_action,
    summarize_improvement_action,
    compute_kpi_snapshots,
)


class TenantScopedMixin:
    """Mixin for tenant-scoped viewsets"""
    
    def get_tenant(self) -> Tenant:
        """Get tenant from URL kwargs"""
        tenant_id = self.kwargs.get('tenant_id')
        tenant_slug = self.kwargs.get('tenant_slug')
        
        if tenant_slug:
            return get_object_or_404(Tenant, slug=tenant_slug)
        elif tenant_id:
            return get_object_or_404(Tenant, id=tenant_id)
        else:
            raise NotFound("Tenant context required")


class ActionStepViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """ViewSet for action steps within improvement actions"""
    serializer_class = ActionStepSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        queryset = ActionStep.objects.filter(
            improvement_action__tenant=tenant
        ).select_related('improvement_action', 'owner')
        
        # Filter by improvement action
        action_id = self.request.query_params.get('action_id')
        if action_id:
            queryset = queryset.filter(improvement_action_id=action_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by owner
        owner_id = self.request.query_params.get('owner_id')
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        
        return queryset.order_by('improvement_action', 'sequence_order')
    
    @action(detail=True, methods=['post'])
    def complete(self, request, tenant_id=None, tenant_slug=None, pk=None):
        """Mark a step as completed"""
        step = self.get_object()
        
        step.status = 'completed'
        step.completed_at = timezone.now()
        step.progress_notes = request.data.get('notes', step.progress_notes)
        step.save()
        
        return Response(ActionStepSerializer(step, context={'request': request}).data)
    
    @action(detail=True, methods=['post'])
    def block(self, request, tenant_id=None, tenant_slug=None, pk=None):
        """Mark a step as blocked"""
        step = self.get_object()
        
        step.is_blocked = True
        step.status = 'blocked'
        step.blocker_description = request.data.get('blocker_description', '')
        step.save()
        
        return Response(ActionStepSerializer(step, context={'request': request}).data)


class CommentViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """ViewSet for comments on improvement actions"""
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CommentDetailSerializer
        return CommentSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        queryset = Comment.objects.filter(
            improvement_action__tenant=tenant
        ).select_related('improvement_action', 'author', 'parent').prefetch_related('mentioned_users')
        
        # Filter by action
        action_id = self.request.query_params.get('action_id')
        if action_id:
            queryset = queryset.filter(improvement_action_id=action_id)
        
        # Only top-level comments (no replies) unless specified
        if self.request.query_params.get('include_replies') != 'true':
            queryset = queryset.filter(parent__isnull=True)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
        # TODO: Send notifications to mentioned users


class AttachmentViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """ViewSet for file attachments"""
    serializer_class = AttachmentSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        queryset = Attachment.objects.filter(
            improvement_action__tenant=tenant
        ).select_related('improvement_action', 'uploaded_by')
        
        # Filter by action
        action_id = self.request.query_params.get('action_id')
        if action_id:
            queryset = queryset.filter(improvement_action_id=action_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class VerificationViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """ViewSet for verification records"""
    serializer_class = VerificationSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        return Verification.objects.filter(
            improvement_action__tenant=tenant
        ).select_related('improvement_action', 'verifier')
    
    def perform_create(self, serializer):
        verification = serializer.save(verifier=self.request.user)
        
        # Update action status based on verification outcome
        action = verification.improvement_action
        if verification.outcome == 'verified':
            action.status = 'completed'
            action.actual_completion_date = timezone.now().date()
            action.save()


class ClauseLinkViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """ViewSet for clause-action links"""
    serializer_class = ClauseLinkSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        queryset = ClauseLink.objects.filter(
            improvement_action__tenant=tenant
        ).select_related('improvement_action', 'clause', 'clause__standard', 'created_by')
        
        # Filter by action
        action_id = self.request.query_params.get('action_id')
        if action_id:
            queryset = queryset.filter(improvement_action_id=action_id)
        
        # Filter by source (ai vs human)
        source = self.request.query_params.get('source')
        if source:
            queryset = queryset.filter(source=source)
        
        # Filter by reviewed status
        reviewed = self.request.query_params.get('reviewed')
        if reviewed:
            queryset = queryset.filter(reviewed=(reviewed == 'true'))
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def review(self, request, tenant_id=None, tenant_slug=None, pk=None):
        """Review and approve a clause link"""
        link = self.get_object()
        
        link.reviewed = True
        link.reviewed_by = request.user
        link.reviewed_at = timezone.now()
        link.save()
        
        return Response(ClauseLinkSerializer(link, context={'request': request}).data)
    
    @action(detail=False, methods=['get'])
    def by_clause(self, request, tenant_id=None, tenant_slug=None):
        """Get all actions linked to a specific clause"""
        clause_id = request.query_params.get('clause_id')
        if not clause_id:
            return Response({'error': 'clause_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        links = self.get_queryset().filter(clause_id=clause_id)
        serializer = self.get_serializer(links, many=True)
        return Response(serializer.data)


class SLAPolicyViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """ViewSet for SLA policies"""
    serializer_class = SLAPolicySerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        return SLAPolicy.objects.filter(tenant=tenant).select_related('created_by')
    
    def perform_create(self, serializer):
        tenant = self.get_tenant()
        serializer.save(tenant=tenant, created_by=self.request.user)


class KPISnapshotViewSet(TenantScopedMixin, viewsets.ReadOnlyModelViewSet):
    """ViewSet for KPI snapshots (read-only, computed via tasks)"""
    serializer_class = KPISnapshotSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        queryset = KPISnapshot.objects.filter(tenant=tenant)
        
        # Filter by metric key
        metric_key = self.request.query_params.get('metric_key')
        if metric_key:
            queryset = queryset.filter(metric_key=metric_key)
        
        # Filter by period
        period = self.request.query_params.get('period')
        if period:
            queryset = queryset.filter(period=period)
        
        return queryset.order_by('-period_end', 'metric_key')
    
    @action(detail=False, methods=['post'])
    def compute(self, request, tenant_id=None, tenant_slug=None):
        """Trigger KPI snapshot computation"""
        tenant = self.get_tenant()
        
        period = request.data.get('period', 'monthly')
        period_start = request.data.get('period_start')
        period_end = request.data.get('period_end')
        
        # Trigger async task
        task = compute_kpi_snapshots.delay(
            tenant.id,
            period=period,
            period_start=period_start,
            period_end=period_end
        )
        
        return Response({
            'message': 'KPI computation started',
            'task_id': task.id
        }, status=status.HTTP_202_ACCEPTED)


class TaxonomyLabelViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """ViewSet for taxonomy labels"""
    serializer_class = TaxonomyLabelSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        queryset = TaxonomyLabel.objects.filter(tenant=tenant)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter active only
        if self.request.query_params.get('active_only') == 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset
    
    def perform_create(self, serializer):
        tenant = self.get_tenant()
        serializer.save(tenant=tenant)


class AIRunViewSet(TenantScopedMixin, viewsets.ReadOnlyModelViewSet):
    """ViewSet for AI run logs (read-only audit trail)"""
    serializer_class = AIRunSerializer
    
    def get_queryset(self):
        tenant = self.get_tenant()
        queryset = AIRun.objects.filter(tenant=tenant)
        
        # Filter by task type
        task_type = self.request.query_params.get('task_type')
        if task_type:
            queryset = queryset.filter(task_type=task_type)
        
        # Filter by target
        target_entity = self.request.query_params.get('target_entity')
        target_id = self.request.query_params.get('target_id')
        if target_entity:
            queryset = queryset.filter(target_entity=target_entity)
        if target_id:
            queryset = queryset.filter(target_id=target_id)
        
        return queryset.order_by('-created_at')


# Composite viewsets for rich functionality

class ImprovementActionCIRViewSet(TenantScopedMixin, viewsets.GenericViewSet):
    """
    Extended improvement action viewset with CIR-specific actions.
    Provides AI classification, summarization, and compliance tracking.
    """
    
    def get_queryset(self):
        tenant = self.get_tenant()
        return ImprovementAction.objects.filter(tenant=tenant).prefetch_related(
            'steps', 'comments', 'file_attachments', 'verifications', 'clause_links'
        )
    
    @action(detail=True, methods=['post'])
    def ai_classify(self, request, tenant_id=None, tenant_slug=None, pk=None):
        """Trigger AI classification for an action"""
        action = self.get_object()
        
        # Start async task
        task = classify_improvement_action.delay(
            action.id,
            auto_link_clauses=request.data.get('auto_link_clauses', True)
        )
        
        return Response({
            'message': 'AI classification started',
            'task_id': task.id,
            'action_id': action.id
        }, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=True, methods=['post'])
    def ai_summarize(self, request, tenant_id=None, tenant_slug=None, pk=None):
        """Generate AI summary for an action"""
        action = self.get_object()
        
        serializer = AISummarizeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Start async task
        task = summarize_improvement_action.delay(
            action.id,
            max_length=serializer.validated_data['max_length'],
            style=serializer.validated_data['style']
        )
        
        return Response({
            'message': 'AI summarization started',
            'task_id': task.id,
            'action_id': action.id
        }, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=['get'])
    def compliance_dashboard(self, request, tenant_id=None, tenant_slug=None):
        """Get comprehensive compliance dashboard data"""
        tenant = self.get_tenant()
        actions = self.get_queryset()
        
        # Overview stats
        total = actions.count()
        open_count = actions.filter(status__in=['identified', 'planned', 'in_progress']).count()
        overdue_count = actions.filter(compliance_status='overdue').count()
        closing_this_week = actions.filter(
            target_completion_date__gte=timezone.now().date(),
            target_completion_date__lte=timezone.now().date() + timezone.timedelta(days=7)
        ).count()
        
        overview = {
            'total_actions': total,
            'open': open_count,
            'overdue': overdue_count,
            'closing_this_week': closing_this_week
        }
        
        # Clause heatmap (actions per clause)
        clause_data = ClauseLink.objects.filter(
            improvement_action__tenant=tenant
        ).values(
            'clause__clause_number',
            'clause__title',
            'clause__standard__name'
        ).annotate(
            action_count=Count('improvement_action', distinct=True),
            overdue_count=Count(
                'improvement_action',
                filter=Q(improvement_action__compliance_status='overdue'),
                distinct=True
            )
        ).order_by('-action_count')[:20]
        
        clause_heatmap = list(clause_data)
        
        # SLA breaches
        sla_breaches = list(
            actions.filter(compliance_status='overdue').values(
                'id', 'action_number', 'title', 'priority', 'target_completion_date'
            ).order_by('target_completion_date')[:10]
        )
        
        # Recent activity
        recent_activity = []  # TODO: Implement activity stream
        
        # Trends
        trends = {
            'completion_rate_30d': 0,  # TODO: Calculate
            'avg_time_to_close': 0,
        }
        
        dashboard_data = {
            'overview': overview,
            'clause_heatmap': clause_heatmap,
            'sla_breaches': sla_breaches,
            'recent_activity': recent_activity,
            'trends': trends
        }
        
        serializer = ComplianceDashboardSerializer(dashboard_data)
        return Response(serializer.data)
