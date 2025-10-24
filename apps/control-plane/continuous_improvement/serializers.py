from rest_framework import serializers
from .models import ImprovementCategory, ImprovementAction, ActionTracking, ImprovementReview
from django.contrib.auth import get_user_model

User = get_user_model()


class ImprovementCategorySerializer(serializers.ModelSerializer):
    """Serializer for improvement categories"""
    category_type_display = serializers.CharField(source='get_category_type_display', read_only=True)
    actions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ImprovementCategory
        fields = [
            'id', 'name', 'category_type', 'category_type_display',
            'description', 'color_code', 'related_standards',
            'is_active', 'actions_count', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_actions_count(self, obj):
        return obj.actions.filter(status__in=['identified', 'planned', 'in_progress']).count()


class ActionTrackingSerializer(serializers.ModelSerializer):
    """Serializer for action tracking updates"""
    created_by_name = serializers.SerializerMethodField()
    update_type_display = serializers.CharField(source='get_update_type_display', read_only=True)
    
    class Meta:
        model = ActionTracking
        fields = [
            'id', 'update_type', 'update_type_display', 'update_text',
            'progress_percentage', 'old_status', 'new_status',
            'is_blocker', 'blocker_resolved', 'blocker_resolution',
            'evidence_provided', 'created_at', 'created_by', 'created_by_name'
        ]
        read_only_fields = ['created_at']
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class ImprovementActionSerializer(serializers.ModelSerializer):
    """Serializer for improvement actions"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    responsible_person_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    source_display = serializers.CharField(source='get_source_display', read_only=True)
    compliance_status_display = serializers.CharField(source='get_compliance_status_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_until_due = serializers.IntegerField(read_only=True)
    progress_percentage = serializers.IntegerField(read_only=True)
    tracking_updates_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ImprovementAction
        fields = [
            'id', 'action_number', 'title', 'description',
            'category', 'category_name', 'priority', 'priority_display',
            'source', 'source_display', 'status', 'status_display',
            'ai_classified_category', 'ai_classification_confidence',
            'ai_summary', 'ai_keywords', 'ai_related_standards', 'ai_processed_at',
            'identified_date', 'planned_start_date', 'target_completion_date',
            'actual_completion_date',
            'responsible_person', 'responsible_person_name',
            'root_cause', 'proposed_solution', 'resources_required',
            'estimated_cost', 'actual_cost',
            'success_criteria', 'expected_impact', 'actual_impact',
            'effectiveness_rating',
            'compliance_status', 'compliance_status_display',
            'is_critical_compliance', 'is_overdue', 'days_until_due',
            'progress_percentage',
            'requires_approval', 'approved_by', 'approved_by_name', 'approved_at',
            'tags', 'attachments',
            'created_at', 'created_by', 'created_by_name', 'updated_at',
            'tracking_updates_count'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'ai_processed_at',
            'compliance_status', 'is_overdue', 'days_until_due', 'progress_percentage'
        ]
    
    def get_responsible_person_name(self, obj):
        return obj.responsible_person.get_full_name() if obj.responsible_person else None
    
    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None
    
    def get_approved_by_name(self, obj):
        return obj.approved_by.get_full_name() if obj.approved_by else None
    
    def get_tracking_updates_count(self, obj):
        return obj.tracking_updates.count()


class ImprovementActionDetailSerializer(ImprovementActionSerializer):
    """Detailed serializer with tracking updates"""
    tracking_updates = ActionTrackingSerializer(many=True, read_only=True)
    supporting_staff_details = serializers.SerializerMethodField()
    
    class Meta(ImprovementActionSerializer.Meta):
        fields = ImprovementActionSerializer.Meta.fields + [
            'tracking_updates', 'supporting_staff_details'
        ]
    
    def get_supporting_staff_details(self, obj):
        return [
            {
                'id': user.id,
                'name': user.get_full_name(),
                'email': user.email
            }
            for user in obj.supporting_staff.all()
        ]


class ImprovementReviewSerializer(serializers.ModelSerializer):
    """Serializer for improvement reviews"""
    review_type_display = serializers.CharField(source='get_review_type_display', read_only=True)
    reviewed_by_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ImprovementReview
        fields = [
            'id', 'review_number', 'title', 'review_type', 'review_type_display',
            'review_date', 'review_period_start', 'review_period_end',
            'total_actions_reviewed', 'actions_completed', 'actions_on_track',
            'actions_at_risk', 'actions_overdue',
            'ai_summary', 'ai_trends', 'ai_recommendations',
            'key_findings', 'areas_of_concern', 'recommendations', 'action_items',
            'reviewed_by', 'reviewed_by_name',
            'approved_by', 'approved_by_name', 'approved_at',
            'notes', 'attachments', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'created_at', 'updated_at',
            'total_actions_reviewed', 'actions_completed', 'actions_on_track',
            'actions_at_risk', 'actions_overdue'
        ]
    
    def get_reviewed_by_name(self, obj):
        return obj.reviewed_by.get_full_name() if obj.reviewed_by else None
    
    def get_approved_by_name(self, obj):
        return obj.approved_by.get_full_name() if obj.approved_by else None


class AIClassificationRequestSerializer(serializers.Serializer):
    """Serializer for AI classification request"""
    description = serializers.CharField()
    title = serializers.CharField(required=False)
    root_cause = serializers.CharField(required=False, allow_blank=True)


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_actions = serializers.IntegerField()
    by_status = serializers.DictField()
    by_priority = serializers.DictField()
    by_compliance = serializers.DictField()
    overdue_count = serializers.IntegerField()
    at_risk_count = serializers.IntegerField()
    completion_rate = serializers.FloatField()
    avg_days_to_complete = serializers.FloatField()
    critical_compliance_count = serializers.IntegerField()
    recent_completions = serializers.IntegerField()
