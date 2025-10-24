from rest_framework import serializers
from .models import FeedbackTemplate, GeneratedFeedback, FeedbackCriterion, FeedbackLog


class FeedbackCriterionSerializer(serializers.ModelSerializer):
    rubric_criterion_name = serializers.CharField(source='rubric_criterion.title', read_only=True)
    
    class Meta:
        model = FeedbackCriterion
        fields = [
            'id', 'criterion_name', 'description', 'rubric_criterion',
            'rubric_criterion_name', 'excellent_feedback', 'good_feedback',
            'satisfactory_feedback', 'needs_improvement_feedback',
            'weight', 'display_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FeedbackTemplateListSerializer(serializers.ModelSerializer):
    """Serializer for listing feedback templates"""
    total_generated = serializers.SerializerMethodField()
    rubric_name = serializers.CharField(source='rubric.title', read_only=True)
    
    class Meta:
        model = FeedbackTemplate
        fields = [
            'id', 'template_number', 'name', 'description', 'tenant',
            'feedback_type', 'sentiment', 'tone', 'rubric', 'rubric_name',
            'positivity_level', 'directness_level', 'formality_level',
            'total_feedback_generated', 'total_generated', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'template_number', 'created_at', 'updated_at']
    
    def get_total_generated(self, obj):
        return obj.generated_feedbacks.count()


class FeedbackTemplateDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with nested criteria"""
    criteria = FeedbackCriterionSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    rubric_name = serializers.CharField(source='rubric.title', read_only=True)
    sentiment_description = serializers.SerializerMethodField()
    
    class Meta:
        model = FeedbackTemplate
        fields = [
            'id', 'template_number', 'name', 'description', 'tenant',
            'created_by', 'created_by_name', 'feedback_type', 'sentiment',
            'tone', 'rubric', 'rubric_name', 'maps_to_criteria',
            'include_student_name', 'include_strengths', 'include_improvements',
            'include_next_steps', 'include_encouragement', 'opening_template',
            'strengths_template', 'improvements_template', 'next_steps_template',
            'closing_template', 'positivity_level', 'directness_level',
            'formality_level', 'sentiment_description', 'total_feedback_generated',
            'average_generation_time', 'status', 'criteria', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'template_number', 'total_feedback_generated',
            'average_generation_time', 'created_at', 'updated_at'
        ]
    
    def get_sentiment_description(self, obj):
        return obj.get_sentiment_description()


class GeneratedFeedbackListSerializer(serializers.ModelSerializer):
    """Serializer for listing generated feedback"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    percentage_score = serializers.SerializerMethodField()
    
    class Meta:
        model = GeneratedFeedback
        fields = [
            'id', 'feedback_number', 'template', 'template_name',
            'student_id', 'student_name', 'assessment_title',
            'score', 'max_score', 'percentage_score', 'grade',
            'word_count', 'sentiment_score', 'personalization_score',
            'requires_review', 'status', 'generated_at'
        ]
        read_only_fields = ['id', 'feedback_number', 'generated_at']
    
    def get_percentage_score(self, obj):
        return obj.get_percentage_score()


class GeneratedFeedbackDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for generated feedback"""
    template = FeedbackTemplateListSerializer(read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True)
    percentage_score = serializers.SerializerMethodField()
    
    class Meta:
        model = GeneratedFeedback
        fields = [
            'id', 'feedback_number', 'template', 'student_id', 'student_name',
            'assessment_title', 'score', 'max_score', 'percentage_score',
            'grade', 'rubric_scores', 'feedback_text', 'strengths_identified',
            'improvements_identified', 'next_steps_suggested', 'sentiment_score',
            'tone_consistency', 'word_count', 'reading_level',
            'personalization_score', 'requires_review', 'review_notes',
            'reviewed_by', 'reviewed_by_name', 'reviewed_at', 'delivered_at',
            'delivery_method', 'status', 'generation_time', 'generated_at',
            'updated_at'
        ]
        read_only_fields = [
            'id', 'feedback_number', 'word_count', 'sentiment_score',
            'tone_consistency', 'personalization_score', 'generation_time',
            'generated_at', 'updated_at'
        ]
    
    def get_percentage_score(self, obj):
        return obj.get_percentage_score()


class FeedbackLogSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = FeedbackLog
        fields = [
            'id', 'template', 'template_name', 'feedback', 'action',
            'performed_by', 'performed_by_name', 'feedbacks_generated',
            'total_time', 'average_time_per_feedback', 'average_sentiment',
            'average_personalization', 'changes_made', 'previous_version',
            'details', 'timestamp'
        ]
        read_only_fields = ['id', 'average_time_per_feedback', 'timestamp']


class GenerateFeedbackRequestSerializer(serializers.Serializer):
    """Serializer for feedback generation request"""
    student_id = serializers.CharField(max_length=100)
    student_name = serializers.CharField(max_length=255)
    assessment_title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    score = serializers.FloatField(required=False, allow_null=True)
    max_score = serializers.FloatField(required=False, allow_null=True)
    grade = serializers.CharField(max_length=10, required=False, allow_blank=True)
    rubric_scores = serializers.DictField(required=False, allow_null=True)
    custom_notes = serializers.CharField(required=False, allow_blank=True)


class BatchGenerateFeedbackRequestSerializer(serializers.Serializer):
    """Serializer for batch feedback generation"""
    feedbacks = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of feedback generation requests"
    )
    
    def validate_feedbacks(self, value):
        """Validate feedback format"""
        if not value:
            raise serializers.ValidationError("At least one feedback request is required")
        
        for idx, feedback in enumerate(value):
            if 'student_id' not in feedback:
                raise serializers.ValidationError(f"Feedback {idx}: student_id is required")
            if 'student_name' not in feedback:
                raise serializers.ValidationError(f"Feedback {idx}: student_name is required")
        
        return value
