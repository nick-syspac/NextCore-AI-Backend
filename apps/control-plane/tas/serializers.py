from rest_framework import serializers
from .models import TAS, TASTemplate, TASVersion, TASGenerationLog
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TASTemplateSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    aqf_level_display = serializers.CharField(source='get_aqf_level_display', read_only=True)
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)

    class Meta:
        model = TASTemplate
        fields = [
            'id', 'name', 'description', 'template_type', 'template_type_display',
            'aqf_level', 'aqf_level_display', 'structure', 'default_sections',
            'gpt_prompts', 'is_active', 'is_system_template', 'created_by',
            'created_by_details', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']


class TASVersionSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)

    class Meta:
        model = TASVersion
        fields = [
            'id', 'tas', 'version_number', 'change_summary', 'changed_sections',
            'content_diff', 'previous_content', 'new_content', 'created_by',
            'created_by_details', 'created_at', 'was_regenerated', 'regeneration_reason'
        ]
        read_only_fields = ['created_at']


class TASGenerationLogSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = TASGenerationLog
        fields = [
            'id', 'tas', 'requested_sections', 'input_data', 'gpt_prompts',
            'status', 'status_display', 'generated_content', 'model_version',
            'tokens_prompt', 'tokens_completion', 'tokens_total',
            'generation_time_seconds', 'error_message', 'retry_count',
            'created_by', 'created_by_details', 'created_at', 'completed_at'
        ]
        read_only_fields = ['created_at', 'completed_at']


class TASSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source='created_by', read_only=True)
    submitted_by_details = UserSerializer(source='submitted_by', read_only=True)
    reviewed_by_details = UserSerializer(source='reviewed_by', read_only=True)
    approved_by_details = UserSerializer(source='approved_by', read_only=True)
    template_details = TASTemplateSerializer(source='template', read_only=True)
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    aqf_level_display = serializers.CharField(source='get_aqf_level_display', read_only=True)
    
    # Computed fields
    time_saved = serializers.SerializerMethodField()
    version_count = serializers.SerializerMethodField()

    class Meta:
        model = TAS
        fields = [
            'id', 'tenant', 'title', 'code', 'description', 'qualification_name',
            'aqf_level', 'aqf_level_display', 'training_package', 'template',
            'template_details', 'sections', 'status', 'status_display', 'version',
            'is_current_version', 'gpt_generated', 'gpt_generation_date',
            'gpt_model_used', 'gpt_tokens_used', 'generation_time_seconds',
            'content', 'metadata', 'submitted_for_review_at', 'submitted_by',
            'submitted_by_details', 'reviewed_at', 'reviewed_by', 'reviewed_by_details',
            'approved_at', 'approved_by', 'approved_by_details', 'published_at',
            'created_by', 'created_by_details', 'created_at', 'updated_at',
            'time_saved', 'version_count'
        ]
        read_only_fields = [
            'version', 'created_at', 'updated_at', 'gpt_generation_date',
            'submitted_for_review_at', 'reviewed_at', 'approved_at', 'published_at'
        ]

    def get_time_saved(self, obj):
        return obj.get_time_saved()

    def get_version_count(self, obj):
        return TAS.objects.filter(tenant=obj.tenant, code=obj.code).count()


class TASGenerateRequestSerializer(serializers.Serializer):
    """Serializer for GPT-4 generation requests"""
    template_id = serializers.IntegerField(required=False, allow_null=True)
    code = serializers.CharField(max_length=50)
    qualification_name = serializers.CharField(max_length=300)
    aqf_level = serializers.ChoiceField(choices=TASTemplate.AQF_LEVELS)
    training_package = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    # Input data for GPT-4
    units_of_competency = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
        help_text="List of units with codes and titles"
    )
    delivery_mode = serializers.CharField(max_length=100, required=False, default='Face-to-face')
    duration_weeks = serializers.IntegerField(required=False, default=52)
    assessment_methods = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
        help_text="Preferred assessment methods"
    )
    additional_context = serializers.CharField(required=False, allow_blank=True)
    
    # Generation options
    sections_to_generate = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
        help_text="Specific sections to generate, or all if empty"
    )
    use_gpt4 = serializers.BooleanField(default=True)
    ai_model = serializers.CharField(
        max_length=50,
        required=False,
        default='gpt-4o',
        help_text="AI model to use for generation (e.g., gpt-4o, gpt-4-turbo, gpt-3.5-turbo)"
    )


class TASVersionCreateSerializer(serializers.Serializer):
    """Serializer for creating new TAS versions"""
    change_summary = serializers.CharField()
    changed_sections = serializers.ListField(child=serializers.CharField())
    regenerate_sections = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
        help_text="Sections to regenerate with GPT-4"
    )


class TASUpdateSerializer(serializers.Serializer):
    """Serializer for updating TAS document content"""
    title = serializers.CharField(max_length=300, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    qualification_name = serializers.CharField(max_length=300, required=False)
    training_package = serializers.CharField(max_length=100, required=False, allow_blank=True)
    sections = serializers.ListField(required=False)
    content = serializers.JSONField(required=False)
    metadata = serializers.JSONField(required=False)
    status = serializers.ChoiceField(
        choices=['draft', 'in_review', 'approved', 'published', 'archived'],
        required=False
    )
    
    # Version control
    create_version = serializers.BooleanField(
        default=False,
        help_text="Create a new version instead of updating current one"
    )
    change_summary = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Summary of changes (required if create_version is True)"
    )
    
    def validate(self, data):
        """Validate that change_summary is provided if create_version is True"""
        if data.get('create_version') and not data.get('change_summary'):
            raise serializers.ValidationError({
                'change_summary': 'Change summary is required when creating a new version'
            })
        return data
