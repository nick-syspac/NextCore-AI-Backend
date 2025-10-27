from django.contrib import admin
from .models import MicroCredential, MicroCredentialVersion, MicroCredentialEnrollment


@admin.register(MicroCredential)
class MicroCredentialAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'tenant', 'duration_hours', 'status', 'created_at']
    list_filter = ['status', 'delivery_mode', 'gpt_generated', 'tenant']
    search_fields = ['code', 'title', 'description', 'tags', 'skills_covered']
    readonly_fields = ['created_at', 'updated_at', 'gpt_generated', 'gpt_model_used', 'generation_time_seconds']
    fieldsets = (
        ('Basic Information', {
            'fields': ('tenant', 'title', 'code', 'description', 'status')
        }),
        ('Course Details', {
            'fields': ('duration_hours', 'delivery_mode', 'target_audience', 'learning_outcomes')
        }),
        ('Units and Content', {
            'fields': ('source_units', 'compressed_content')
        }),
        ('Metadata', {
            'fields': ('tags', 'skills_covered', 'industry_sectors', 'aqf_level')
        }),
        ('Assessment', {
            'fields': ('assessment_strategy', 'assessment_tasks')
        }),
        ('Enrollment', {
            'fields': ('price', 'max_participants', 'prerequisites')
        }),
        ('AI Generation', {
            'fields': ('gpt_generated', 'gpt_model_used', 'generation_time_seconds'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MicroCredentialVersion)
class MicroCredentialVersionAdmin(admin.ModelAdmin):
    list_display = ['micro_credential', 'version_number', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['micro_credential__code', 'change_summary']
    readonly_fields = ['created_at']


@admin.register(MicroCredentialEnrollment)
class MicroCredentialEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'micro_credential', 'status', 'enrolled_at']
    list_filter = ['status', 'enrolled_at']
    search_fields = ['student_name', 'student_email', 'micro_credential__title']
    readonly_fields = ['enrolled_at']
