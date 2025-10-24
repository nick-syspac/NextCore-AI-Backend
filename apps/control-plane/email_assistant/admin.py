from django.contrib import admin
from .models import (
    StudentMessage, DraftReply, MessageTemplate,
    ConversationThread, ToneProfile, ReplyHistory
)


@admin.register(StudentMessage)
class StudentMessageAdmin(admin.ModelAdmin):
    list_display = ['message_number', 'student_name', 'subject', 'message_type', 
                   'priority', 'status', 'received_date']
    list_filter = ['status', 'priority', 'message_type', 'detected_sentiment']
    search_fields = ['message_number', 'student_name', 'student_email', 'subject']
    readonly_fields = ['message_number', 'created_at', 'updated_at']
    fieldsets = (
        ('Message Information', {
            'fields': ('message_number', 'tenant', 'student_name', 'student_email', 
                      'student_id', 'message_type')
        }),
        ('Content', {
            'fields': ('subject', 'message_body', 'received_date')
        }),
        ('Classification', {
            'fields': ('priority', 'category', 'detected_sentiment', 'detected_topics')
        }),
        ('Status', {
            'fields': ('status', 'requires_human_review')
        }),
        ('Context', {
            'fields': ('conversation_thread', 'previous_message_count')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(DraftReply)
class DraftReplyAdmin(admin.ModelAdmin):
    list_display = ['draft_number', 'student_message', 'tone_used', 'confidence_score',
                   'was_sent', 'generated_at']
    list_filter = ['tone_used', 'was_sent', 'was_edited', 'generation_status']
    search_fields = ['draft_number', 'reply_body']
    readonly_fields = ['draft_number', 'generated_at', 'word_count', 
                      'estimated_reading_time_seconds']
    fieldsets = (
        ('Draft Information', {
            'fields': ('draft_number', 'student_message')
        }),
        ('Content', {
            'fields': ('reply_subject', 'reply_body')
        }),
        ('Generation Settings', {
            'fields': ('tone_used', 'formality_level', 'include_greeting', 
                      'include_signature', 'template_used')
        }),
        ('Quality Metrics', {
            'fields': ('confidence_score', 'readability_score', 'word_count', 
                      'estimated_reading_time_seconds')
        }),
        ('User Interaction', {
            'fields': ('was_edited', 'was_sent', 'was_rejected', 'rejection_reason')
        }),
        ('Generation Metadata', {
            'fields': ('generation_status', 'generation_time_ms', 'llm_model_used', 
                      'generation_prompt')
        }),
        ('Timestamps', {
            'fields': ('generated_at', 'sent_at')
        }),
    )


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'usage_count', 'is_active', 
                   'is_system_template']
    list_filter = ['template_type', 'is_active', 'is_system_template']
    search_fields = ['name', 'description', 'template_body']
    readonly_fields = ['template_number', 'usage_count', 'last_used_at', 
                      'created_at', 'updated_at']
    fieldsets = (
        ('Template Information', {
            'fields': ('template_number', 'tenant', 'name', 'description', 'template_type')
        }),
        ('Content', {
            'fields': ('template_body', 'placeholders')
        }),
        ('Tone Settings', {
            'fields': ('default_tone', 'formality_level')
        }),
        ('Usage Tracking', {
            'fields': ('usage_count', 'success_rate', 'last_used_at')
        }),
        ('Status', {
            'fields': ('is_active', 'is_system_template', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ConversationThread)
class ConversationThreadAdmin(admin.ModelAdmin):
    list_display = ['thread_number', 'student_name', 'subject', 'message_count', 
                   'is_active', 'last_message_date']
    list_filter = ['is_active', 'is_resolved']
    search_fields = ['thread_number', 'student_name', 'student_email', 'subject']
    readonly_fields = ['thread_number', 'created_at', 'updated_at']


@admin.register(ToneProfile)
class ToneProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'tone_descriptor', 'formality_level', 'is_default', 
                   'is_active', 'usage_count']
    list_filter = ['is_default', 'is_active', 'tone_descriptor']
    search_fields = ['name', 'description']
    readonly_fields = ['profile_number', 'usage_count', 'created_at', 'updated_at']


@admin.register(ReplyHistory)
class ReplyHistoryAdmin(admin.ModelAdmin):
    list_display = ['history_number', 'student_message', 'sent_by', 'sent_at',
                   'time_saved_seconds', 'time_saved_percentage']
    list_filter = ['student_responded', 'follow_up_required']
    search_fields = ['history_number', 'sent_by']
    readonly_fields = ['history_number', 'time_saved_seconds', 'time_saved_percentage',
                      'created_at']
    fieldsets = (
        ('History Information', {
            'fields': ('history_number', 'student_message', 'draft_reply')
        }),
        ('Final Content', {
            'fields': ('final_subject', 'final_reply_body')
        }),
        ('Timing Metrics', {
            'fields': ('time_to_first_draft_seconds', 'time_to_send_seconds', 'edit_count')
        }),
        ('Efficiency Metrics', {
            'fields': ('estimated_manual_time_seconds', 'time_saved_seconds', 
                      'time_saved_percentage')
        }),
        ('Sender Info', {
            'fields': ('sent_by', 'sent_at')
        }),
        ('Quality Feedback', {
            'fields': ('student_responded', 'student_satisfied', 'follow_up_required')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
