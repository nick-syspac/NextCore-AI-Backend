from django.contrib import admin
from .models import DiaryEntry, AudioRecording, DailySummary, EvidenceDocument, TranscriptionJob


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = [
        'entry_number', 'trainer_name', 'session_date', 'course_name',
        'student_count', 'session_duration_minutes', 'entry_status', 'created_at'
    ]
    list_filter = ['entry_status', 'delivery_mode', 'session_date', 'tenant']
    search_fields = [
        'entry_number', 'trainer_name', 'course_name', 'course_code',
        'unit_of_competency', 'session_summary'
    ]
    readonly_fields = ['entry_number', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('entry_number', 'tenant', 'trainer_id', 'trainer_name')
        }),
        ('Session Details', {
            'fields': (
                'session_date', 'session_time_start', 'session_time_end',
                'session_duration_minutes', 'delivery_mode'
            )
        }),
        ('Course Information', {
            'fields': (
                'course_name', 'course_code', 'unit_of_competency',
                'student_count'
            )
        }),
        ('Content', {
            'fields': (
                'raw_transcript', 'manual_notes', 'session_summary',
                'key_topics_covered', 'student_engagement_notes',
                'challenges_encountered', 'follow_up_actions'
            )
        }),
        ('Evidence & Compliance', {
            'fields': (
                'learning_outcomes_addressed', 'assessment_activities',
                'resources_used', 'evidence_attachments'
            )
        }),
        ('AI Metadata', {
            'fields': (
                'transcription_model', 'summarization_model',
                'transcription_duration_seconds', 'summarization_tokens'
            )
        }),
        ('Status', {
            'fields': ('entry_status', 'is_pinned', 'is_shared')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    date_hierarchy = 'session_date'


@admin.register(AudioRecording)
class AudioRecordingAdmin(admin.ModelAdmin):
    list_display = [
        'recording_number', 'diary_entry', 'recording_filename',
        'recording_duration_seconds', 'processing_status', 'uploaded_at'
    ]
    list_filter = ['processing_status', 'recording_format', 'uploaded_at']
    search_fields = ['recording_number', 'recording_filename', 'diary_entry__entry_number']
    readonly_fields = ['recording_number', 'uploaded_at', 'processed_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('recording_number', 'diary_entry')
        }),
        ('Recording Details', {
            'fields': (
                'recording_filename', 'recording_file_path',
                'recording_file_size_mb', 'recording_duration_seconds',
                'recording_format'
            )
        }),
        ('Transcription', {
            'fields': (
                'transcript_text', 'transcript_confidence', 'transcript_language'
            )
        }),
        ('Processing', {
            'fields': ('processing_status', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'processed_at')
        }),
    )


@admin.register(DailySummary)
class DailySummaryAdmin(admin.ModelAdmin):
    list_display = [
        'summary_number', 'trainer_name', 'summary_date',
        'total_sessions', 'total_teaching_hours', 'total_students'
    ]
    list_filter = ['summary_date', 'tenant', 'generation_date']
    search_fields = ['summary_number', 'trainer_name', 'trainer_id']
    readonly_fields = ['summary_number', 'generation_date']
    fieldsets = (
        ('Basic Information', {
            'fields': ('summary_number', 'tenant', 'trainer_id', 'trainer_name', 'summary_date')
        }),
        ('Statistics', {
            'fields': (
                'total_sessions', 'total_teaching_hours',
                'total_students', 'courses_taught'
            )
        }),
        ('Content', {
            'fields': (
                'daily_highlights', 'overall_student_engagement',
                'key_achievements', 'challenges_summary', 'action_items_pending'
            )
        }),
        ('Evidence', {
            'fields': ('diary_entries_included', 'evidence_documents_created')
        }),
        ('Metadata', {
            'fields': ('generated_by_model', 'generation_date')
        }),
    )
    date_hierarchy = 'summary_date'


@admin.register(EvidenceDocument)
class EvidenceDocumentAdmin(admin.ModelAdmin):
    list_display = [
        'document_number', 'document_title', 'document_type',
        'diary_entry', 'generation_method', 'meets_compliance_standards', 'created_at'
    ]
    list_filter = [
        'document_type', 'document_format', 'generation_method',
        'meets_compliance_standards', 'created_at'
    ]
    search_fields = [
        'document_number', 'document_title', 'document_content',
        'diary_entry__entry_number'
    ]
    readonly_fields = ['document_number', 'created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('document_number', 'diary_entry', 'document_type', 'document_title')
        }),
        ('Content', {
            'fields': ('document_content', 'document_format')
        }),
        ('File Storage', {
            'fields': ('file_path', 'file_size_kb')
        }),
        ('Metadata', {
            'fields': ('generated_by', 'generation_method')
        }),
        ('Compliance', {
            'fields': ('meets_compliance_standards', 'compliance_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(TranscriptionJob)
class TranscriptionJobAdmin(admin.ModelAdmin):
    list_display = [
        'job_number', 'audio_recording', 'job_status',
        'transcription_engine', 'confidence_score', 'created_at'
    ]
    list_filter = ['job_status', 'transcription_engine', 'created_at']
    search_fields = ['job_number', 'audio_recording__recording_number']
    readonly_fields = ['job_number', 'created_at', 'started_at', 'completed_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('job_number', 'audio_recording', 'job_status')
        }),
        ('Configuration', {
            'fields': (
                'transcription_engine', 'language',
                'enable_speaker_diarization', 'enable_punctuation'
            )
        }),
        ('Results', {
            'fields': (
                'transcript_result', 'confidence_score', 'processing_time_seconds'
            )
        }),
        ('Error Handling', {
            'fields': ('error_message', 'retry_count', 'max_retries')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'started_at', 'completed_at')
        }),
    )
