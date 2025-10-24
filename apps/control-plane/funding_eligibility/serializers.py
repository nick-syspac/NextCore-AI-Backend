from rest_framework import serializers
from .models import JurisdictionRequirement, EligibilityRule, EligibilityCheck, EligibilityCheckLog
from django.utils import timezone


class JurisdictionRequirementSerializer(serializers.ModelSerializer):
    jurisdiction_display = serializers.CharField(source='get_jurisdiction_display', read_only=True)
    is_currently_effective = serializers.BooleanField(read_only=True)
    custom_rules_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JurisdictionRequirement
        fields = [
            'id', 'jurisdiction', 'jurisdiction_display', 'name', 'code',
            'requires_australian_citizen', 'requires_permanent_resident', 
            'requires_jurisdiction_resident', 'min_jurisdiction_residency_months',
            'min_age', 'max_age',
            'requires_year_12', 'allows_year_10_completion',
            'requires_unemployed', 'allows_employed', 'requires_apprentice_trainee',
            'restricts_higher_qualifications', 'max_aqf_level',
            'has_income_threshold', 'max_annual_income',
            'allows_concession_card', 'allows_disability', 'allows_indigenous', 'priority_indigenous',
            'funding_percentage', 'student_contribution',
            'api_endpoint', 'api_key_required',
            'additional_rules',
            'is_active', 'effective_from', 'effective_to',
            'is_currently_effective', 'custom_rules_count',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_custom_rules_count(self, obj):
        return obj.custom_rules.filter(is_active=True).count()


class EligibilityRuleSerializer(serializers.ModelSerializer):
    rule_type_display = serializers.CharField(source='get_rule_type_display', read_only=True)
    operator_display = serializers.CharField(source='get_operator_display', read_only=True)
    jurisdiction_name = serializers.CharField(source='jurisdiction_requirement.name', read_only=True)
    
    class Meta:
        model = EligibilityRule
        fields = [
            'id', 'jurisdiction_requirement', 'jurisdiction_name',
            'rule_type', 'rule_type_display', 'name', 'description',
            'field_name', 'operator', 'operator_display', 'expected_value',
            'is_mandatory', 'priority',
            'error_message', 'override_allowed',
            'is_active',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class EligibilityCheckLogSerializer(serializers.ModelSerializer):
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.get_full_name', read_only=True)
    
    class Meta:
        model = EligibilityCheckLog
        fields = [
            'id', 'action', 'action_display', 'details', 'notes',
            'performed_by_name', 'performed_at',
        ]


class EligibilityCheckSerializer(serializers.ModelSerializer):
    jurisdiction_display = serializers.CharField(source='get_jurisdiction_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    jurisdiction_requirement_name = serializers.CharField(source='jurisdiction_requirement.name', read_only=True)
    student_age = serializers.SerializerMethodField()
    is_currently_valid = serializers.BooleanField(read_only=True)
    eligibility_summary = serializers.CharField(source='get_eligibility_summary', read_only=True)
    checked_by_name = serializers.CharField(source='checked_by.get_full_name', read_only=True)
    override_approved_by_name = serializers.CharField(source='override_approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = EligibilityCheck
        fields = [
            'id', 'check_number',
            'student_first_name', 'student_last_name', 'student_dob', 'student_email', 'student_phone',
            'course_code', 'course_name', 'aqf_level', 'intended_start_date',
            'jurisdiction', 'jurisdiction_display', 'jurisdiction_requirement', 'jurisdiction_requirement_name',
            'funding_program_code',
            'student_data',
            'status', 'status_display', 'is_eligible', 'eligibility_percentage',
            'rules_checked', 'rules_passed', 'rules_failed',
            'check_results', 'failed_rules', 'warnings',
            'api_verified', 'api_response', 'api_verified_at',
            'override_required', 'override_approved', 'override_reason',
            'override_approved_by_name', 'override_approved_at',
            'prevents_enrollment', 'compliance_notes',
            'valid_from', 'valid_until',
            'student_age', 'is_currently_valid', 'eligibility_summary',
            'checked_at', 'checked_by_name', 'updated_at',
        ]
        read_only_fields = ['check_number', 'checked_at', 'updated_at']
    
    def get_student_age(self, obj):
        return obj.calculate_age()


class EligibilityCheckDetailSerializer(EligibilityCheckSerializer):
    logs = EligibilityCheckLogSerializer(many=True, read_only=True)
    
    class Meta(EligibilityCheckSerializer.Meta):
        fields = EligibilityCheckSerializer.Meta.fields + ['logs']


class EligibilityCheckRequestSerializer(serializers.Serializer):
    """
    Serializer for initiating an eligibility check
    """
    # Student information
    student_first_name = serializers.CharField(max_length=100)
    student_last_name = serializers.CharField(max_length=100)
    student_dob = serializers.DateField()
    student_email = serializers.EmailField()
    student_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Enrollment details
    course_code = serializers.CharField(max_length=50)
    course_name = serializers.CharField(max_length=200)
    aqf_level = serializers.IntegerField(min_value=1, max_value=10)
    intended_start_date = serializers.DateField()
    
    # Jurisdiction
    jurisdiction = serializers.ChoiceField(choices=JurisdictionRequirement.JURISDICTION_CHOICES)
    funding_program_code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    # Student eligibility data
    citizenship_status = serializers.ChoiceField(
        choices=[
            ('citizen', 'Australian Citizen'),
            ('permanent_resident', 'Permanent Resident'),
            ('temporary_visa', 'Temporary Visa'),
            ('other', 'Other'),
        ]
    )
    is_jurisdiction_resident = serializers.BooleanField()
    jurisdiction_residency_months = serializers.IntegerField(min_value=0, required=False)
    
    # Education
    highest_education = serializers.ChoiceField(
        choices=[
            ('year_10', 'Year 10'),
            ('year_12', 'Year 12'),
            ('cert_i', 'Certificate I'),
            ('cert_ii', 'Certificate II'),
            ('cert_iii', 'Certificate III'),
            ('cert_iv', 'Certificate IV'),
            ('diploma', 'Diploma'),
            ('adv_diploma', 'Advanced Diploma'),
            ('bachelor', 'Bachelor Degree'),
            ('postgrad', 'Postgraduate'),
        ],
        required=False
    )
    highest_aqf_level = serializers.IntegerField(min_value=0, max_value=10, required=False)
    
    # Employment
    employment_status = serializers.ChoiceField(
        choices=[
            ('employed', 'Employed'),
            ('unemployed', 'Unemployed'),
            ('apprentice', 'Apprentice'),
            ('trainee', 'Trainee'),
            ('self_employed', 'Self Employed'),
            ('student', 'Student'),
        ],
        required=False
    )
    annual_income = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    
    # Special categories
    has_concession_card = serializers.BooleanField(required=False)
    concession_card_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    has_disability = serializers.BooleanField(required=False)
    is_indigenous = serializers.BooleanField(required=False)
    
    # Visa details (if applicable)
    visa_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    visa_expiry = serializers.DateField(required=False, allow_null=True)
    
    # Additional data
    additional_info = serializers.JSONField(required=False)


class DashboardStatsSerializer(serializers.Serializer):
    """
    Dashboard statistics for eligibility checks
    """
    total_checks = serializers.IntegerField()
    eligible_count = serializers.IntegerField()
    ineligible_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()
    override_count = serializers.IntegerField()
    eligibility_rate = serializers.FloatField()
    
    by_jurisdiction = serializers.DictField()
    by_status = serializers.DictField()
    
    recent_checks = serializers.IntegerField()
    prevented_enrollments = serializers.IntegerField()
    
    top_failure_reasons = serializers.ListField()
