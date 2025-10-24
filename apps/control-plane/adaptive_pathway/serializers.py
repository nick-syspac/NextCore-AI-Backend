from rest_framework import serializers
from .models import (
    LearningPathway, LearningStep, StudentProgress,
    PathwayRecommendation, ContentEmbedding
)


class LearningStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningStep
        fields = [
            'id', 'step_number', 'title', 'description', 'content_type',
            'content_url', 'sequence_order', 'is_prerequisite', 'prerequisites',
            'estimated_minutes', 'difficulty_rating', 'learning_objectives',
            'tags', 'status', 'completion_score', 'created_at',
            'started_at', 'completed_at'
        ]
        read_only_fields = ['step_number', 'created_at']


class LearningPathwaySerializer(serializers.ModelSerializer):
    steps = LearningStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = LearningPathway
        fields = [
            'id', 'pathway_number', 'tenant', 'student_id', 'student_name',
            'pathway_name', 'description', 'difficulty_level',
            'estimated_duration_hours', 'recommendation_confidence',
            'similarity_score', 'status', 'total_steps', 'completed_steps',
            'completion_percentage', 'personalization_factors',
            'similar_students', 'created_at', 'started_at',
            'completed_at', 'last_activity', 'steps'
        ]
        read_only_fields = ['pathway_number', 'completion_percentage', 'created_at', 'last_activity']


class StudentProgressSerializer(serializers.ModelSerializer):
    step_title = serializers.CharField(source='step.title', read_only=True)
    pathway_name = serializers.CharField(source='pathway.pathway_name', read_only=True)
    
    class Meta:
        model = StudentProgress
        fields = [
            'id', 'progress_number', 'tenant', 'student_id', 'pathway',
            'pathway_name', 'step', 'step_title', 'time_spent_minutes',
            'attempts', 'completion_score', 'struggle_indicators',
            'engagement_level', 'recommended_next_steps',
            'difficulty_adjustment', 'is_completed', 'completed_at',
            'started_at', 'last_activity'
        ]
        read_only_fields = ['progress_number', 'started_at', 'last_activity']


class PathwayRecommendationSerializer(serializers.ModelSerializer):
    pathway_name = serializers.CharField(source='recommended_pathway.pathway_name', read_only=True)
    pathway_description = serializers.CharField(source='recommended_pathway.description', read_only=True)
    
    class Meta:
        model = PathwayRecommendation
        fields = [
            'id', 'recommendation_number', 'tenant', 'student_id',
            'student_name', 'recommended_pathway', 'pathway_name',
            'pathway_description', 'algorithm_used', 'recommendation_score',
            'collaborative_score', 'embedding_similarity',
            'similar_students_count', 'similar_students_list',
            'common_pathways', 'recommendation_reasons', 'is_accepted',
            'feedback_score', 'created_at', 'expires_at'
        ]
        read_only_fields = ['recommendation_number', 'created_at']


class ContentEmbeddingSerializer(serializers.ModelSerializer):
    step_title = serializers.CharField(source='step.title', read_only=True)
    
    class Meta:
        model = ContentEmbedding
        fields = [
            'id', 'embedding_number', 'step', 'step_title',
            'embedding_vector', 'embedding_dimension', 'model_name',
            'text_content', 'similar_content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['embedding_number', 'embedding_dimension', 'created_at', 'updated_at']


class RecommendationRequestSerializer(serializers.Serializer):
    """Serializer for pathway recommendation requests"""
    student_id = serializers.CharField(max_length=100)
    student_name = serializers.CharField(max_length=200)
    current_skill_level = serializers.ChoiceField(
        choices=['beginner', 'intermediate', 'advanced', 'expert']
    )
    interests = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        default=list
    )
    learning_style = serializers.ChoiceField(
        choices=['visual', 'auditory', 'kinesthetic', 'reading'],
        required=False,
        default='visual'
    )
    time_commitment_hours = serializers.DecimalField(
        max_digits=4,
        decimal_places=1,
        required=False,
        default=10.0
    )
