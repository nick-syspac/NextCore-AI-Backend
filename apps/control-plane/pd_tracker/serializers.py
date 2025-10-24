from rest_framework import serializers
from django.utils import timezone
from .models import PDActivity, TrainerProfile, PDSuggestion, ComplianceRule, ComplianceCheck


class PDActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PDActivity
        fields = '__all__'
        read_only_fields = ['activity_number', 'created_at', 'updated_at']


class PDActivityDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with additional computed fields"""
    days_duration = serializers.SerializerMethodField()
    is_recent = serializers.SerializerMethodField()
    
    class Meta:
        model = PDActivity
        fields = '__all__'
        read_only_fields = ['activity_number', 'created_at', 'updated_at']
    
    def get_days_duration(self, obj):
        return (obj.end_date - obj.start_date).days + 1
    
    def get_is_recent(self, obj):
        from datetime import timedelta
        from django.utils import timezone
        return obj.end_date >= (timezone.now().date() - timedelta(days=90))


class TrainerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerProfile
        fields = '__all__'
        read_only_fields = ['profile_number', 'created_at', 'updated_at']


class TrainerProfileDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with currency status"""
    vocational_currency_days_remaining = serializers.SerializerMethodField()
    industry_currency_days_remaining = serializers.SerializerMethodField()
    annual_progress_percentage = serializers.SerializerMethodField()
    recent_activities_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TrainerProfile
        fields = '__all__'
        read_only_fields = ['profile_number', 'created_at', 'updated_at']
    
    def get_vocational_currency_days_remaining(self, obj):
        if not obj.last_vocational_pd:
            return None
        from datetime import timedelta
        from django.utils import timezone
        expiry = obj.last_vocational_pd + timedelta(days=365)
        days_remaining = (expiry - timezone.now().date()).days
        return max(0, days_remaining)
    
    def get_industry_currency_days_remaining(self, obj):
        if not obj.last_industry_pd:
            return None
        from datetime import timedelta
        from django.utils import timezone
        expiry = obj.last_industry_pd + timedelta(days=730)  # 2 years for industry
        days_remaining = (expiry - timezone.now().date()).days
        return max(0, days_remaining)
    
    def get_annual_progress_percentage(self, obj):
        if obj.annual_pd_goal_hours <= 0:
            return 0
        return min(100, (obj.current_year_hours / obj.annual_pd_goal_hours) * 100)
    
    def get_recent_activities_count(self, obj):
        from datetime import timedelta
        from django.utils import timezone
        recent_date = timezone.now().date() - timedelta(days=90)
        return PDActivity.objects.filter(
            tenant=obj.tenant,
            trainer_id=obj.trainer_id,
            start_date__gte=recent_date,
            status='completed'
        ).count()


class PDSuggestionSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source='trainer_profile.trainer_name', read_only=True)
    
    class Meta:
        model = PDSuggestion
        fields = '__all__'
        read_only_fields = ['suggestion_number', 'generation_date', 'created_at']


class PDSuggestionDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with trainer profile details"""
    trainer_name = serializers.CharField(source='trainer_profile.trainer_name', read_only=True)
    trainer_role = serializers.CharField(source='trainer_profile.role', read_only=True)
    is_urgent = serializers.SerializerMethodField()
    days_until_deadline = serializers.SerializerMethodField()
    
    class Meta:
        model = PDSuggestion
        fields = '__all__'
        read_only_fields = ['suggestion_number', 'generation_date', 'created_at']
    
    def get_is_urgent(self, obj):
        return obj.priority_level in ['critical', 'high']
    
    def get_days_until_deadline(self, obj):
        if not obj.deadline:
            return None
        from django.utils import timezone
        return (obj.deadline - timezone.now().date()).days


class ComplianceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceRule
        fields = '__all__'
        read_only_fields = ['rule_number', 'created_at', 'updated_at']


class ComplianceCheckSerializer(serializers.ModelSerializer):
    trainer_name = serializers.CharField(source='trainer_profile.trainer_name', read_only=True)
    
    class Meta:
        model = ComplianceCheck
        fields = '__all__'
        read_only_fields = ['check_number', 'created_at']


class ComplianceCheckDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with trainer profile"""
    trainer_name = serializers.CharField(source='trainer_profile.trainer_name', read_only=True)
    trainer_role = serializers.CharField(source='trainer_profile.role', read_only=True)
    compliance_percentage = serializers.SerializerMethodField()
    is_urgent = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplianceCheck
        fields = '__all__'
        read_only_fields = ['check_number', 'created_at']
    
    def get_compliance_percentage(self, obj):
        return obj.compliance_score
    
    def get_is_urgent(self, obj):
        return obj.overall_status == 'non_compliant' or (
            obj.requires_action and obj.action_deadline and
            (obj.action_deadline - timezone.now().date()).days <= 30
        )


# Request/Response Serializers

class LogActivityRequestSerializer(serializers.Serializer):
    """Request serializer for logging PD activities"""
    tenant = serializers.CharField(max_length=100)
    trainer_id = serializers.CharField(max_length=100)
    trainer_name = serializers.CharField(max_length=200)
    activity_type = serializers.ChoiceField(choices=[
        'formal_course', 'workshop', 'conference', 'webinar',
        'industry_placement', 'networking', 'research', 'mentoring',
        'self_study', 'certification', 'teaching_observation', 'curriculum_development'
    ])
    activity_title = serializers.CharField(max_length=300)
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    hours_completed = serializers.FloatField()
    compliance_areas = serializers.ListField(child=serializers.CharField(), required=False)
    maintains_vocational_currency = serializers.BooleanField(default=False)
    maintains_industry_currency = serializers.BooleanField(default=False)
    maintains_teaching_currency = serializers.BooleanField(default=False)


class GenerateSuggestionsRequestSerializer(serializers.Serializer):
    """Request serializer for generating LLM-powered PD suggestions"""
    trainer_id = serializers.CharField(max_length=100)
    focus_areas = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Optional specific areas to focus suggestions on"
    )
    include_critical_only = serializers.BooleanField(
        default=False,
        help_text="Only return critical priority suggestions"
    )
    max_suggestions = serializers.IntegerField(
        default=5,
        min_value=1,
        max_value=20
    )


class GenerateSuggestionsResponseSerializer(serializers.Serializer):
    """Response serializer for PD suggestions"""
    suggestions = PDSuggestionDetailSerializer(many=True)
    total_generated = serializers.IntegerField()
    currency_gaps = serializers.DictField()
    compliance_risks = serializers.ListField(child=serializers.CharField())


class CheckCurrencyRequestSerializer(serializers.Serializer):
    """Request serializer for checking trainer currency status"""
    trainer_id = serializers.CharField(max_length=100)
    check_period_months = serializers.IntegerField(
        default=12,
        min_value=1,
        max_value=36,
        help_text="Number of months to check back"
    )


class CheckCurrencyResponseSerializer(serializers.Serializer):
    """Response serializer for currency check"""
    trainer_profile = TrainerProfileDetailSerializer()
    vocational_status = serializers.ChoiceField(choices=['current', 'expiring_soon', 'expired', 'not_applicable'])
    industry_status = serializers.ChoiceField(choices=['current', 'expiring_soon', 'expired', 'not_applicable'])
    teaching_status = serializers.ChoiceField(choices=['current', 'expiring_soon', 'expired', 'not_applicable'])
    total_hours_period = serializers.FloatField()
    compliance_issues = serializers.ListField(child=serializers.CharField())
    recommendations = serializers.ListField(child=serializers.CharField())


class DashboardStatsSerializer(serializers.Serializer):
    """Response serializer for dashboard statistics"""
    total_activities = serializers.IntegerField()
    total_hours = serializers.FloatField()
    activities_last_30_days = serializers.IntegerField()
    hours_last_30_days = serializers.FloatField()
    
    # Currency status
    trainers_current = serializers.IntegerField()
    trainers_expiring_soon = serializers.IntegerField()
    trainers_expired = serializers.IntegerField()
    
    # By activity type
    activities_by_type = serializers.DictField()
    
    # Compliance
    compliance_checks_needed = serializers.IntegerField()
    pending_suggestions = serializers.IntegerField()
    pending_verifications = serializers.IntegerField()
    
    # Top performers
    top_trainers = serializers.ListField()
    
    # Trends
    monthly_hours = serializers.ListField()


class ComplianceReportRequestSerializer(serializers.Serializer):
    """Request serializer for compliance reports"""
    tenant = serializers.CharField(max_length=100)
    period_start = serializers.DateField()
    period_end = serializers.DateField()
    include_trainers = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Optional list of trainer IDs to include"
    )
    report_format = serializers.ChoiceField(
        choices=['summary', 'detailed', 'audit'],
        default='summary'
    )


class ComplianceReportResponseSerializer(serializers.Serializer):
    """Response serializer for compliance reports"""
    report_date = serializers.DateField()
    period_start = serializers.DateField()
    period_end = serializers.DateField()
    total_trainers = serializers.IntegerField()
    compliant_trainers = serializers.IntegerField()
    at_risk_trainers = serializers.IntegerField()
    non_compliant_trainers = serializers.IntegerField()
    compliance_checks = ComplianceCheckDetailSerializer(many=True)
    summary = serializers.DictField()
