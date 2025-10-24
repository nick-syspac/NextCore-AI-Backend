from django.contrib import admin
from .models import FeedbackTemplate, GeneratedFeedback, FeedbackCriterion, FeedbackLog


@admin.register(FeedbackTemplate)
class FeedbackTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'template_number', 'name', 'tenant', 'feedback_type', 'sentiment',
        'tone', 'total_feedback_generated', 'status', 'created_at'
    ]
    list_filter = ['status', 'feedback_type', 'sentiment', 'tone', 'tenant', 'created_at']
    search_fields = ['template_number', 'name', 'description']
    readonly_fields = [
        'template_number', 'total_feedback_generated', 'average_generation_time',
        'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Identification', {
            'fields': ('template_number', 'name', 'description', 'tenant', 'created_by')
        }),
        ('Template Configuration', {
            'fields': ('feedback_type', 'sentiment', 'tone')
        }),
        ('Rubric Mapping', {
            'fields': ('rubric', 'maps_to_criteria')
        }),
        ('Personalization Settings', {
            'fields': (
                'include_student_name', 'include_strengths', 'include_improvements',
                'include_next_steps', 'include_encouragement'
            )
        }),
        ('Content Templates', {
            'fields': (
                'opening_template', 'strengths_template', 'improvements_template',
                'next_steps_template', 'closing_template'
            ),
            'classes': ('collapse',)
        }),
        ('Sentiment Controls', {
            'fields': ('positivity_level', 'directness_level', 'formality_level')
        }),
        ('Performance', {
            'fields': ('total_feedback_generated', 'average_generation_time')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )


@admin.register(GeneratedFeedback)
class GeneratedFeedbackAdmin(admin.ModelAdmin):
    list_display = [
        'feedback_number', 'student_name', 'student_id', 'template',
        'score', 'max_score', 'sentiment_score', 'personalization_score',
        'requires_review', 'status', 'generated_at'
    ]
    list_filter = [
        'status', 'requires_review', 'template', 'generated_at', 'delivered_at'
    ]
    search_fields = [
        'feedback_number', 'student_id', 'student_name', 'assessment_title'
    ]
    readonly_fields = [
        'feedback_number', 'word_count', 'sentiment_score', 'tone_consistency',
        'personalization_score', 'reading_level', 'generation_time',
        'generated_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Identification', {
            'fields': ('feedback_number', 'template', 'status')
        }),
        ('Student Information', {
            'fields': ('student_id', 'student_name')
        }),
        ('Assessment Context', {
            'fields': ('assessment_title', 'score', 'max_score', 'grade', 'rubric_scores')
        }),
        ('Generated Content', {
            'fields': ('feedback_text', 'word_count')
        }),
        ('Analysis', {
            'fields': (
                'strengths_identified', 'improvements_identified', 'next_steps_suggested'
            ),
            'classes': ('collapse',)
        }),
        ('Quality Metrics', {
            'fields': (
                'sentiment_score', 'tone_consistency', 'personalization_score', 'reading_level'
            )
        }),
        ('Review & Delivery', {
            'fields': (
                'requires_review', 'review_notes', 'reviewed_by', 'reviewed_at',
                'delivered_at', 'delivery_method'
            )
        }),
        ('Metadata', {
            'fields': ('generation_time', 'generated_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FeedbackCriterion)
class FeedbackCriterionAdmin(admin.ModelAdmin):
    list_display = [
        'criterion_name', 'template', 'rubric_criterion', 'weight', 'display_order'
    ]
    list_filter = ['template']
    search_fields = ['criterion_name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('template', 'criterion_name', 'description')
        }),
        ('Rubric Mapping', {
            'fields': ('rubric_criterion',)
        }),
        ('Feedback by Performance Level', {
            'fields': (
                'excellent_feedback', 'good_feedback', 'satisfactory_feedback',
                'needs_improvement_feedback'
            )
        }),
        ('Settings', {
            'fields': ('weight', 'display_order')
        }),
    )


@admin.register(FeedbackLog)
class FeedbackLogAdmin(admin.ModelAdmin):
    list_display = [
        'template', 'action', 'performed_by', 'feedbacks_generated',
        'average_time_per_feedback', 'timestamp'
    ]
    list_filter = ['action', 'template', 'timestamp']
    search_fields = ['template__template_number', 'feedback__feedback_number']
    readonly_fields = ['average_time_per_feedback', 'timestamp']
    
    fieldsets = (
        ('Action Details', {
            'fields': ('template', 'feedback', 'action', 'performed_by')
        }),
        ('Performance Metrics', {
            'fields': (
                'feedbacks_generated', 'total_time', 'average_time_per_feedback',
                'average_sentiment', 'average_personalization'
            )
        }),
        ('Changes', {
            'fields': ('changes_made', 'previous_version'),
            'classes': ('collapse',)
        }),
        ('Additional Details', {
            'fields': ('details', 'timestamp'),
            'classes': ('collapse',)
        }),
    )
