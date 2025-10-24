from django.contrib import admin
from .models import Rubric, RubricCriterion, RubricLevel, RubricGenerationLog


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = [
        'rubric_number',
        'title',
        'rubric_type',
        'status',
        'assessment',
        'ai_generated',
        'created_at',
    ]
    list_filter = [
        'status',
        'rubric_type',
        'ai_generated',
        'created_at',
    ]
    search_fields = [
        'rubric_number',
        'title',
        'assessment__unit_code',
        'assessment__title',
    ]
    readonly_fields = [
        'rubric_number',
        'ai_generated',
        'ai_model',
        'ai_generation_time',
        'ai_generated_at',
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Rubric Details', {
            'fields': (
                'rubric_number',
                'tenant',
                'title',
                'description',
                'rubric_type',
                'status',
            )
        }),
        ('Links', {
            'fields': (
                'assessment',
                'task',
            )
        }),
        ('Scoring', {
            'fields': (
                'total_points',
                'passing_score',
            )
        }),
        ('AI Generation', {
            'fields': (
                'ai_generated',
                'ai_model',
                'ai_prompt',
                'ai_generation_time',
                'ai_generated_at',
            ),
            'classes': ('collapse',),
        }),
        ('NLP Summary', {
            'fields': (
                'nlp_summary',
                'nlp_key_points',
            ),
            'classes': ('collapse',),
        }),
        ('Taxonomy', {
            'fields': (
                'taxonomy_tags',
                'blooms_levels',
            ),
            'classes': ('collapse',),
        }),
        ('Review & Approval', {
            'fields': (
                'reviewed_by',
                'reviewed_at',
                'approved_by',
                'approved_at',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_by',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )


@admin.register(RubricCriterion)
class RubricCriterionAdmin(admin.ModelAdmin):
    list_display = [
        'rubric',
        'criterion_number',
        'title',
        'max_points',
        'blooms_level',
        'ai_generated',
    ]
    list_filter = [
        'blooms_level',
        'ai_generated',
    ]
    search_fields = [
        'rubric__rubric_number',
        'title',
        'description',
    ]
    
    fieldsets = (
        ('Criterion Details', {
            'fields': (
                'rubric',
                'criterion_number',
                'title',
                'description',
                'display_order',
            )
        }),
        ('Scoring', {
            'fields': (
                'weight',
                'max_points',
            )
        }),
        ('Unit Mapping', {
            'fields': (
                'maps_to_elements',
                'maps_to_performance_criteria',
                'maps_to_knowledge_evidence',
            ),
            'classes': ('collapse',),
        }),
        ('Taxonomy', {
            'fields': (
                'taxonomy_tags',
                'blooms_level',
            )
        }),
        ('AI & NLP', {
            'fields': (
                'ai_generated',
                'ai_rationale',
                'nlp_keywords',
            ),
            'classes': ('collapse',),
        }),
    )


@admin.register(RubricLevel)
class RubricLevelAdmin(admin.ModelAdmin):
    list_display = [
        'criterion',
        'level_name',
        'level_type',
        'points',
        'ai_generated',
    ]
    list_filter = [
        'level_type',
        'ai_generated',
    ]
    search_fields = [
        'criterion__title',
        'level_name',
        'description',
    ]
    
    fieldsets = (
        ('Level Details', {
            'fields': (
                'criterion',
                'level_name',
                'level_type',
                'points',
                'description',
                'display_order',
            )
        }),
        ('Guidance', {
            'fields': (
                'indicators',
                'examples',
            )
        }),
        ('AI & NLP', {
            'fields': (
                'ai_generated',
                'nlp_summary',
            ),
            'classes': ('collapse',),
        }),
    )


@admin.register(RubricGenerationLog)
class RubricGenerationLogAdmin(admin.ModelAdmin):
    list_display = [
        'rubric',
        'action',
        'ai_model',
        'nlp_model',
        'success',
        'generation_time',
        'performed_at',
    ]
    list_filter = [
        'action',
        'success',
        'ai_model',
        'nlp_model',
        'performed_at',
    ]
    search_fields = [
        'rubric__rubric_number',
        'error_message',
    ]
    readonly_fields = [
        'rubric',
        'action',
        'ai_model',
        'nlp_model',
        'prompt_used',
        'response_text',
        'tokens_used',
        'generation_time',
        'success',
        'error_message',
        'performed_by',
        'performed_at',
    ]
    
    fieldsets = (
        ('Generation Details', {
            'fields': (
                'rubric',
                'action',
                'ai_model',
                'nlp_model',
                'performed_by',
                'performed_at',
            )
        }),
        ('Prompt & Response', {
            'fields': (
                'prompt_used',
                'response_text',
            ),
            'classes': ('collapse',),
        }),
        ('Metrics', {
            'fields': (
                'tokens_used',
                'generation_time',
            )
        }),
        ('Result', {
            'fields': (
                'success',
                'error_message',
            )
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
