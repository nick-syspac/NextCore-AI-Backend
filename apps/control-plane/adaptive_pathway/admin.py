from django.contrib import admin
from .models import (
    LearningPathway, LearningStep, StudentProgress,
    PathwayRecommendation, ContentEmbedding
)


@admin.register(LearningPathway)
class LearningPathwayAdmin(admin.ModelAdmin):
    list_display = [
        'pathway_number', 'student_name', 'pathway_name', 'difficulty_level',
        'status', 'completion_percentage', 'recommendation_confidence', 'created_at'
    ]
    list_filter = ['status', 'difficulty_level', 'tenant', 'created_at']
    search_fields = ['pathway_number', 'student_name', 'pathway_name', 'student_id']
    readonly_fields = ['pathway_number', 'completion_percentage', 'created_at', 'last_activity']
    
    fieldsets = (
        ('Pathway Information', {
            'fields': ('pathway_number', 'tenant', 'student_id', 'student_name', 
                      'pathway_name', 'description', 'difficulty_level', 
                      'estimated_duration_hours')
        }),
        ('Recommendation Metrics', {
            'fields': ('recommendation_confidence', 'similarity_score', 
                      'personalization_factors', 'similar_students')
        }),
        ('Progress Tracking', {
            'fields': ('status', 'total_steps', 'completed_steps', 
                      'completion_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'started_at', 'completed_at', 'last_activity')
        }),
    )


@admin.register(LearningStep)
class LearningStepAdmin(admin.ModelAdmin):
    list_display = [
        'step_number', 'title', 'pathway', 'content_type', 'sequence_order',
        'difficulty_rating', 'status', 'estimated_minutes'
    ]
    list_filter = ['content_type', 'status', 'is_prerequisite', 'created_at']
    search_fields = ['step_number', 'title', 'pathway__pathway_name']
    readonly_fields = ['step_number', 'created_at']
    
    fieldsets = (
        ('Step Information', {
            'fields': ('step_number', 'pathway', 'title', 'description', 
                      'content_type', 'content_url')
        }),
        ('Sequencing', {
            'fields': ('sequence_order', 'is_prerequisite', 'prerequisites')
        }),
        ('Learning Metadata', {
            'fields': ('estimated_minutes', 'difficulty_rating', 
                      'learning_objectives', 'tags')
        }),
        ('Progress', {
            'fields': ('status', 'completion_score', 'started_at', 'completed_at')
        }),
    )


@admin.register(StudentProgress)
class StudentProgressAdmin(admin.ModelAdmin):
    list_display = [
        'progress_number', 'student_id', 'pathway', 'step', 'engagement_level',
        'time_spent_minutes', 'completion_score', 'is_completed'
    ]
    list_filter = ['engagement_level', 'difficulty_adjustment', 'is_completed', 'tenant']
    search_fields = ['progress_number', 'student_id', 'pathway__pathway_name', 'step__title']
    readonly_fields = ['progress_number', 'started_at', 'last_activity']
    
    fieldsets = (
        ('Progress Information', {
            'fields': ('progress_number', 'tenant', 'student_id', 'pathway', 'step')
        }),
        ('Engagement Metrics', {
            'fields': ('time_spent_minutes', 'attempts', 'completion_score', 
                      'engagement_level')
        }),
        ('Learning Analytics', {
            'fields': ('struggle_indicators', 'difficulty_adjustment', 
                      'recommended_next_steps')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_at', 'started_at', 'last_activity')
        }),
    )


@admin.register(PathwayRecommendation)
class PathwayRecommendationAdmin(admin.ModelAdmin):
    list_display = [
        'recommendation_number', 'student_name', 'recommended_pathway',
        'algorithm_used', 'recommendation_score', 'is_accepted', 'created_at'
    ]
    list_filter = ['algorithm_used', 'is_accepted', 'tenant', 'created_at']
    search_fields = ['recommendation_number', 'student_name', 'student_id', 
                    'recommended_pathway__pathway_name']
    readonly_fields = ['recommendation_number', 'created_at']
    
    fieldsets = (
        ('Recommendation Information', {
            'fields': ('recommendation_number', 'tenant', 'student_id', 
                      'student_name', 'recommended_pathway', 'algorithm_used')
        }),
        ('Scoring Metrics', {
            'fields': ('recommendation_score', 'collaborative_score', 
                      'embedding_similarity')
        }),
        ('Collaborative Filtering Data', {
            'fields': ('similar_students_count', 'similar_students_list', 
                      'common_pathways', 'recommendation_reasons')
        }),
        ('User Feedback', {
            'fields': ('is_accepted', 'feedback_score')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at')
        }),
    )


@admin.register(ContentEmbedding)
class ContentEmbeddingAdmin(admin.ModelAdmin):
    list_display = [
        'embedding_number', 'step', 'model_name', 'embedding_dimension',
        'created_at', 'updated_at'
    ]
    list_filter = ['model_name', 'created_at', 'updated_at']
    search_fields = ['embedding_number', 'step__title', 'text_content']
    readonly_fields = ['embedding_number', 'embedding_dimension', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Embedding Information', {
            'fields': ('embedding_number', 'step', 'model_name', 
                      'embedding_dimension')
        }),
        ('Content', {
            'fields': ('text_content', 'embedding_vector')
        }),
        ('Similarity Cache', {
            'fields': ('similar_content',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
