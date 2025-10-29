"""
Extended serializers for Continuous Improvement Register (CIR).
Provides comprehensive API representations for all CIR entities.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

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
    Embedding,
)
from .models import ImprovementAction

User = get_user_model()


class ActionStepSerializer(serializers.ModelSerializer):
    """Serializer for action steps within improvement actions"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    owner_name = serializers.SerializerMethodField()
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ActionStep
        fields = [
            'id', 'improvement_action', 'title', 'description', 'sequence_order',
            'owner', 'owner_name', 'status', 'status_display',
            'due_date', 'started_at', 'completed_at',
            'progress_notes', 'evidence_refs',
            'is_blocked', 'blocker_description', 'blocker_resolved_at',
            'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_overdue']
    
    def get_owner_name(self, obj):
        return obj.owner.get_full_name() if obj.owner else None


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments on improvement actions"""
    author_name = serializers.SerializerMethodField()
    author_email = serializers.EmailField(source='author.email', read_only=True)
    visibility_display = serializers.CharField(source='get_visibility_display', read_only=True)
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'improvement_action', 'body', 'visibility', 'visibility_display',
            'parent', 'mentioned_users', 'author', 'author_name', 'author_email',
            'created_at', 'updated_at', 'edited', 'replies_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'author', 'edited']
    
    def get_author_name(self, obj):
        return obj.author.get_full_name() if obj.author else 'Unknown'
    
    def get_replies_count(self, obj):
        return obj.replies.count() if obj.pk else 0


class CommentDetailSerializer(CommentSerializer):
    """Detailed comment serializer with nested replies"""
    replies = serializers.SerializerMethodField()
    
    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + ['replies']
    
    def get_replies(self, obj):
        if obj.pk:
            replies = obj.replies.all()
            return CommentSerializer(replies, many=True, context=self.context).data
        return []


class AttachmentSerializer(serializers.ModelSerializer):
    """Serializer for file attachments"""
    uploaded_by_name = serializers.SerializerMethodField()
    kind_display = serializers.CharField(source='get_kind_display', read_only=True)
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = Attachment
        fields = [
            'id', 'improvement_action', 'file_uri', 'filename', 'file_size',
            'file_size_mb', 'mime_type', 'kind', 'kind_display',
            'sha256_hash', 'description',
            'uploaded_by', 'uploaded_by_name', 'uploaded_at'
        ]
        read_only_fields = ['uploaded_at', 'uploaded_by']
    
    def get_uploaded_by_name(self, obj):
        return obj.uploaded_by.get_full_name() if obj.uploaded_by else None
    
    def get_file_size_mb(self, obj):
        if obj.file_size:
            return round(obj.file_size / (1024 * 1024), 2)
        return None


class VerificationSerializer(serializers.ModelSerializer):
    """Serializer for verification records"""
    outcome_display = serializers.CharField(source='get_outcome_display', read_only=True)
    verifier_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Verification
        fields = [
            'id', 'improvement_action', 'outcome', 'outcome_display', 'notes',
            'evidence_reviewed', 'effectiveness_score',
            'requires_followup', 'followup_actions', 'followup_due_date',
            'verifier', 'verifier_name', 'verified_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'verifier', 'verified_at']
    
    def get_verifier_name(self, obj):
        return obj.verifier.get_full_name() if obj.verifier else None


class ClauseLinkSerializer(serializers.ModelSerializer):
    """Serializer for clause-action links"""
    source_display = serializers.CharField(source='get_source_display', read_only=True)
    clause_number = serializers.CharField(source='clause.clause_number', read_only=True)
    clause_title = serializers.CharField(source='clause.title', read_only=True)
    standard_name = serializers.CharField(source='clause.standard.name', read_only=True)
    reviewed_by_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ClauseLink
        fields = [
            'id', 'improvement_action', 'clause', 'clause_number', 'clause_title',
            'standard_name', 'source', 'source_display', 'confidence', 'rationale',
            'reviewed', 'reviewed_by', 'reviewed_by_name', 'reviewed_at',
            'created_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = ['created_at', 'created_by']
    
    def get_reviewed_by_name(self, obj):
        return obj.reviewed_by.get_full_name() if obj.reviewed_by else None
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class SLAPolicySerializer(serializers.ModelSerializer):
    """Serializer for SLA policies"""
    created_by_name = serializers.SerializerMethodField()
    applicable_actions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SLAPolicy
        fields = [
            'id', 'tenant', 'name', 'description', 'target_days',
            'applies_to_priorities', 'applies_to_sources', 'applies_to_categories',
            'warning_days_before', 'escalate_on_breach', 'escalation_recipients',
            'is_active', 'created_at', 'created_by', 'created_by_name',
            'updated_at', 'applicable_actions_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None
    
    def get_applicable_actions_count(self, obj):
        # This would require a more complex query in production
        return 0  # Placeholder


class KPISnapshotSerializer(serializers.ModelSerializer):
    """Serializer for KPI snapshots"""
    period_display = serializers.CharField(source='get_period_display', read_only=True)
    trend = serializers.SerializerMethodField()
    
    class Meta:
        model = KPISnapshot
        fields = [
            'id', 'tenant', 'period', 'period_display', 'period_start', 'period_end',
            'computed_at', 'metric_key', 'metric_value', 'metric_unit',
            'metadata', 'previous_value', 'variance_percentage', 'trend'
        ]
        read_only_fields = ['computed_at']
    
    def get_trend(self, obj):
        """Calculate trend direction"""
        if obj.variance_percentage is not None:
            if obj.variance_percentage > 0:
                return 'up'
            elif obj.variance_percentage < 0:
                return 'down'
        return 'flat'


class TaxonomyLabelSerializer(serializers.ModelSerializer):
    """Serializer for taxonomy labels"""
    
    class Meta:
        model = TaxonomyLabel
        fields = [
            'id', 'tenant', 'key', 'name', 'description',
            'color', 'icon', 'category', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at']


class AIRunSerializer(serializers.ModelSerializer):
    """Serializer for AI run logs"""
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    
    class Meta:
        model = AIRun
        fields = [
            'id', 'tenant', 'target_entity', 'target_id',
            'task_type', 'task_type_display', 'input_ref', 'output_json',
            'success', 'error_message', 'tokens_used', 'latency_ms',
            'model_name', 'model_version', 'created_at'
        ]
        read_only_fields = ['created_at']


class EmbeddingSerializer(serializers.ModelSerializer):
    """Serializer for embeddings"""
    
    class Meta:
        model = Embedding
        fields = [
            'id', 'tenant', 'entity', 'entity_id',
            'vector', 'model', 'dimension', 'created_at'
        ]
        read_only_fields = ['created_at']
        
    def to_representation(self, instance):
        """Exclude large vector field from list views"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        # Only include vector in detail views
        if request and request.parser_context.get('view') and hasattr(request.parser_context['view'], 'action'):
            if request.parser_context['view'].action == 'list':
                representation.pop('vector', None)
        
        return representation


# Composite serializers for rich API responses

class ImprovementActionCIRDetailSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for improvement actions with all related CIR entities.
    Used for detail views and full data export.
    """
    from .serializers import ImprovementActionSerializer
    
    # Related entities
    steps = ActionStepSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    file_attachments = AttachmentSerializer(many=True, read_only=True)
    verifications = VerificationSerializer(many=True, read_only=True)
    clause_links = ClauseLinkSerializer(many=True, read_only=True)
    
    # Computed fields
    steps_completed = serializers.SerializerMethodField()
    steps_total = serializers.SerializerMethodField()
    has_pending_verification = serializers.SerializerMethodField()
    clause_coverage = serializers.SerializerMethodField()
    
    class Meta:
        model = ImprovementAction
        fields = '__all__'
    
    def get_steps_completed(self, obj):
        return obj.steps.filter(status='completed').count()
    
    def get_steps_total(self, obj):
        return obj.steps.count()
    
    def get_has_pending_verification(self, obj):
        return obj.verifications.filter(
            outcome__in=['not_verified', 'requires_rework']
        ).exists()
    
    def get_clause_coverage(self, obj):
        """Calculate clause coverage metrics"""
        links = obj.clause_links.all()
        return {
            'total': links.count(),
            'ai_suggested': links.filter(source='ai').count(),
            'manually_assigned': links.filter(source='human').count(),
            'reviewed': links.filter(reviewed=True).count(),
            'avg_confidence': float(
                links.filter(source='ai').aggregate(
                    avg=serializers.models.Avg('confidence')
                )['avg'] or 0
            )
        }


class ComplianceDashboardSerializer(serializers.Serializer):
    """Serializer for compliance dashboard data"""
    overview = serializers.DictField()
    clause_heatmap = serializers.ListField()
    sla_breaches = serializers.ListField()
    recent_activity = serializers.ListField()
    trends = serializers.DictField()


class AIClassifyRequestSerializer(serializers.Serializer):
    """Request serializer for AI classification"""
    description = serializers.CharField()
    title = serializers.CharField(required=False, allow_blank=True)
    source = serializers.CharField(required=False, allow_blank=True)


class AISummarizeRequestSerializer(serializers.Serializer):
    """Request serializer for AI summarization"""
    max_length = serializers.IntegerField(default=80, min_value=20, max_value=200)
    style = serializers.ChoiceField(
        choices=['concise', 'detailed', 'action-oriented'],
        default='action-oriented'
    )


class AIClassifyResponseSerializer(serializers.Serializer):
    """Response serializer for AI classification"""
    ai_labels = serializers.ListField(child=serializers.DictField())
    risk_rating = serializers.CharField()
    clause_suggestions = serializers.ListField(child=serializers.DictField())
    confidence = serializers.FloatField()
    processing_time_ms = serializers.IntegerField()


class AISummarizeResponseSerializer(serializers.Serializer):
    """Response serializer for AI summarization"""
    summary = serializers.CharField()
    key_points = serializers.ListField(child=serializers.CharField())
    processing_time_ms = serializers.IntegerField()
