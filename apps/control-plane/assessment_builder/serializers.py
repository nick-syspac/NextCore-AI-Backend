from rest_framework import serializers
from .models import Assessment, AssessmentTask, AssessmentCriteria, AssessmentGenerationLog


class AssessmentTaskSerializer(serializers.ModelSerializer):
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    blooms_level_display = serializers.SerializerMethodField()
    
    class Meta:
        model = AssessmentTask
        fields = [
            'id', 'task_number', 'task_type', 'task_type_display',
            'question', 'context',
            'ai_generated', 'ai_rationale',
            'blooms_level', 'blooms_level_display', 'blooms_verbs',
            'maps_to_elements', 'maps_to_performance_criteria', 'maps_to_knowledge_evidence',
            'question_count', 'estimated_time_minutes', 'marks_available',
            'display_order',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_blooms_level_display(self, obj):
        if obj.blooms_level:
            return obj.blooms_level.capitalize()
        return None


class AssessmentCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentCriteria
        fields = [
            'id', 'task', 'criterion_number', 'criterion_text',
            'unit_element', 'performance_criterion', 'knowledge_evidence',
            'satisfactory_evidence', 'not_satisfactory_evidence',
            'ai_generated', 'display_order',
            'created_at',
        ]
        read_only_fields = ['created_at']


class AssessmentSerializer(serializers.ModelSerializer):
    assessment_type_display = serializers.CharField(source='get_assessment_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    task_count = serializers.IntegerField(source='get_task_count', read_only=True)
    total_questions = serializers.IntegerField(source='get_total_questions', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'assessment_number',
            'unit_code', 'unit_title', 'training_package', 'unit_release',
            'assessment_type', 'assessment_type_display', 'title', 'version',
            'instructions', 'context', 'conditions',
            'ai_generated', 'ai_model', 'ai_generation_time', 'ai_generated_at',
            'blooms_analysis', 'blooms_distribution', 'dominant_blooms_level',
            'is_compliant', 'compliance_score', 'compliance_notes',
            'elements_covered', 'performance_criteria_covered',
            'knowledge_evidence_covered', 'performance_evidence_covered',
            'estimated_duration_hours',
            'status', 'status_display',
            'reviewed_by_name', 'reviewed_at', 'approved_by_name', 'approved_at',
            'task_count', 'total_questions',
            'created_at', 'updated_at', 'created_by_name',
        ]
        read_only_fields = ['assessment_number', 'created_at', 'updated_at']


class AssessmentDetailSerializer(AssessmentSerializer):
    tasks = AssessmentTaskSerializer(many=True, read_only=True)
    criteria = AssessmentCriteriaSerializer(many=True, read_only=True)
    
    class Meta(AssessmentSerializer.Meta):
        fields = AssessmentSerializer.Meta.fields + ['tasks', 'criteria']


class AssessmentGenerationRequestSerializer(serializers.Serializer):
    """
    Request serializer for generating assessments from unit codes
    """
    unit_code = serializers.CharField(max_length=50)
    unit_title = serializers.CharField(max_length=300)
    training_package = serializers.CharField(max_length=100, required=False, allow_blank=True)
    assessment_type = serializers.ChoiceField(choices=Assessment.ASSESSMENT_TYPE_CHOICES)
    
    # Optional unit details for better generation
    elements = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of unit elements"
    )
    performance_criteria = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of performance criteria"
    )
    knowledge_evidence = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of knowledge evidence items"
    )
    performance_evidence = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="List of performance evidence items"
    )
    
    # Generation options
    number_of_tasks = serializers.IntegerField(
        min_value=1,
        max_value=50,
        default=10,
        help_text="Number of tasks to generate"
    )
    include_context = serializers.BooleanField(
        default=True,
        help_text="Include realistic context/scenarios"
    )


class DashboardStatsSerializer(serializers.Serializer):
    """
    Dashboard statistics for assessments
    """
    total_assessments = serializers.IntegerField()
    by_status = serializers.DictField()
    by_type = serializers.DictField()
    
    ai_generated_count = serializers.IntegerField()
    ai_generation_rate = serializers.FloatField()
    
    avg_compliance_score = serializers.FloatField()
    avg_tasks_per_assessment = serializers.FloatField()
    
    blooms_distribution = serializers.DictField()
    
    recent_assessments = serializers.IntegerField()
