from rest_framework import serializers
from .models import (
    TrainerQualification, UnitOfCompetency, TrainerAssignment,
    CompetencyGap, QualificationMapping, ComplianceCheck
)


# Model Serializers
class TrainerQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerQualification
        fields = '__all__'
        read_only_fields = ['qualification_id', 'created_at', 'updated_at']


class TrainerQualificationListSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()
    days_until_expiry = serializers.SerializerMethodField()
    
    class Meta:
        model = TrainerQualification
        fields = ['id', 'qualification_id', 'trainer_name', 'qualification_name', 
                  'qualification_code', 'verification_status', 'date_obtained', 
                  'expiry_date', 'is_expired', 'days_until_expiry']
    
    def get_is_expired(self, obj):
        from django.utils import timezone
        if obj.expiry_date:
            return obj.expiry_date < timezone.now().date()
        return False
    
    def get_days_until_expiry(self, obj):
        from django.utils import timezone
        if obj.expiry_date:
            delta = obj.expiry_date - timezone.now().date()
            return delta.days
        return None


class UnitOfCompetencySerializer(serializers.ModelSerializer):
    assignments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = UnitOfCompetency
        fields = '__all__'
        read_only_fields = ['unit_id', 'created_at', 'updated_at']
    
    def get_assignments_count(self, obj):
        return obj.assignments.count()


class TrainerAssignmentSerializer(serializers.ModelSerializer):
    unit_details = UnitOfCompetencySerializer(source='unit', read_only=True)
    gaps_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TrainerAssignment
        fields = '__all__'
        read_only_fields = ['assignment_id', 'created_at', 'updated_at']
    
    def get_gaps_count(self, obj):
        return obj.gaps.filter(is_resolved=False).count()


class CompetencyGapSerializer(serializers.ModelSerializer):
    unit_details = UnitOfCompetencySerializer(source='unit', read_only=True)
    
    class Meta:
        model = CompetencyGap
        fields = '__all__'
        read_only_fields = ['gap_id', 'created_at', 'updated_at']


class QualificationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualificationMapping
        fields = '__all__'
        read_only_fields = ['mapping_id', 'created_at', 'updated_at']


class ComplianceCheckSerializer(serializers.ModelSerializer):
    compliance_percentage = serializers.SerializerMethodField()
    duration_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplianceCheck
        fields = '__all__'
        read_only_fields = ['check_id', 'created_at', 'updated_at']
    
    def get_compliance_percentage(self, obj):
        if obj.total_assignments_checked > 0:
            return (obj.compliant_assignments / obj.total_assignments_checked) * 100
        return 0
    
    def get_duration_display(self, obj):
        if obj.execution_time_seconds:
            if obj.execution_time_seconds < 60:
                return f"{obj.execution_time_seconds:.1f}s"
            else:
                minutes = obj.execution_time_seconds / 60
                return f"{minutes:.1f}m"
        return "N/A"


# Request/Response Serializers
class CheckGapsRequestSerializer(serializers.Serializer):
    trainer_id = serializers.CharField()
    unit_id = serializers.IntegerField()
    check_all_requirements = serializers.BooleanField(default=True)
    include_recommendations = serializers.BooleanField(default=True)


class CheckGapsResponseSerializer(serializers.Serializer):
    trainer_id = serializers.CharField()
    trainer_name = serializers.CharField()
    unit_code = serializers.CharField()
    unit_name = serializers.CharField()
    meets_requirements = serializers.BooleanField()
    compliance_score = serializers.FloatField()
    gaps_found = serializers.ListField(child=serializers.DictField())
    matching_qualifications = serializers.ListField(child=serializers.DictField())
    recommendations = serializers.ListField(child=serializers.CharField())
    can_deliver = serializers.BooleanField()
    message = serializers.CharField()


class AssignTrainerRequestSerializer(serializers.Serializer):
    trainer_id = serializers.CharField()
    unit_id = serializers.IntegerField()
    check_compliance = serializers.BooleanField(default=True)
    override_gaps = serializers.BooleanField(default=False)
    assignment_notes = serializers.CharField(required=False, allow_blank=True)


class AssignTrainerResponseSerializer(serializers.Serializer):
    assignment_id = serializers.CharField()
    assignment_number = serializers.CharField()
    assignment_status = serializers.CharField()
    meets_requirements = serializers.BooleanField()
    compliance_score = serializers.FloatField()
    gaps_count = serializers.IntegerField()
    message = serializers.CharField()


class ValidateMatrixRequestSerializer(serializers.Serializer):
    trainer_ids = serializers.ListField(child=serializers.CharField(), required=False)
    unit_codes = serializers.ListField(child=serializers.CharField(), required=False)
    check_type = serializers.CharField(default='full_matrix')


class ValidateMatrixResponseSerializer(serializers.Serializer):
    check_id = serializers.CharField()
    check_number = serializers.CharField()
    total_assignments = serializers.IntegerField()
    compliant_assignments = serializers.IntegerField()
    non_compliant_assignments = serializers.IntegerField()
    compliance_percentage = serializers.FloatField()
    gaps_found = serializers.IntegerField()
    critical_gaps = serializers.IntegerField()
    trainers_checked = serializers.IntegerField()
    units_checked = serializers.IntegerField()
    message = serializers.CharField()


class GraphAnalysisRequestSerializer(serializers.Serializer):
    trainer_id = serializers.CharField(required=False)
    qualification_code = serializers.CharField(required=False)
    find_paths = serializers.BooleanField(default=True)
    max_depth = serializers.IntegerField(default=3)


class GraphAnalysisResponseSerializer(serializers.Serializer):
    nodes = serializers.ListField(child=serializers.DictField())
    edges = serializers.ListField(child=serializers.DictField())
    paths = serializers.ListField(child=serializers.DictField())
    coverage_score = serializers.FloatField()
    analysis = serializers.DictField()
    message = serializers.CharField()


class GenerateComplianceReportRequestSerializer(serializers.Serializer):
    check_id = serializers.IntegerField(required=False)
    trainer_ids = serializers.ListField(child=serializers.CharField(), required=False)
    unit_codes = serializers.ListField(child=serializers.CharField(), required=False)
    report_format = serializers.ChoiceField(choices=['summary', 'detailed', 'by_trainer', 'by_unit'], default='summary')
    include_recommendations = serializers.BooleanField(default=True)


class GenerateComplianceReportResponseSerializer(serializers.Serializer):
    report_title = serializers.CharField()
    report_date = serializers.DateTimeField()
    compliance_summary = serializers.DictField()
    trainer_reports = serializers.ListField(child=serializers.DictField())
    unit_reports = serializers.ListField(child=serializers.DictField())
    gap_summary = serializers.DictField()
    recommendations = serializers.ListField(child=serializers.CharField())
    report_content = serializers.CharField()
    message = serializers.CharField()


class DashboardStatsSerializer(serializers.Serializer):
    total_trainers = serializers.IntegerField()
    total_qualifications = serializers.IntegerField()
    verified_qualifications = serializers.IntegerField()
    expired_qualifications = serializers.IntegerField()
    
    total_units = serializers.IntegerField()
    core_units = serializers.IntegerField()
    elective_units = serializers.IntegerField()
    
    total_assignments = serializers.IntegerField()
    approved_assignments = serializers.IntegerField()
    pending_assignments = serializers.IntegerField()
    rejected_assignments = serializers.IntegerField()
    
    total_gaps = serializers.IntegerField()
    critical_gaps = serializers.IntegerField()
    high_gaps = serializers.IntegerField()
    unresolved_gaps = serializers.IntegerField()
    
    overall_compliance_score = serializers.FloatField()
    compliance_checks_this_month = serializers.IntegerField()
    
    recent_checks = serializers.ListField(child=serializers.DictField())
    top_gap_types = serializers.ListField(child=serializers.DictField())
    trainers_needing_attention = serializers.ListField(child=serializers.DictField())


class BulkAssignRequestSerializer(serializers.Serializer):
    trainer_id = serializers.CharField()
    unit_ids = serializers.ListField(child=serializers.IntegerField())
    check_compliance = serializers.BooleanField(default=True)


class BulkAssignResponseSerializer(serializers.Serializer):
    total_assignments = serializers.IntegerField()
    successful_assignments = serializers.IntegerField()
    failed_assignments = serializers.IntegerField()
    assignments = serializers.ListField(child=serializers.DictField())
    message = serializers.CharField()
