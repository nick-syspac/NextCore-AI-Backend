from django.contrib import admin
from .models import (
    TrainerProfile, VerificationScan, LinkedInActivity,
    GitHubActivity, CurrencyEvidence, EntityExtraction
)


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'profile_number', 'trainer_name', 'primary_industry',
        'currency_status', 'currency_score', 'last_verified_date'
    ]
    list_filter = ['currency_status', 'primary_industry', 'auto_verify_enabled']
    search_fields = ['profile_number', 'trainer_name', 'trainer_id', 'email']
    readonly_fields = ['profile_number', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('profile_number', 'tenant', 'trainer_id', 'trainer_name', 'email')
        }),
        ('Social Profiles', {
            'fields': ('linkedin_url', 'github_url', 'twitter_url', 'personal_website')
        }),
        ('Industry Details', {
            'fields': ('primary_industry', 'specializations', 'years_experience')
        }),
        ('Currency Status', {
            'fields': (
                'last_verified_date', 'currency_status', 'currency_score'
            )
        }),
        ('Verification Settings', {
            'fields': (
                'auto_verify_enabled', 'verification_frequency_days',
                'next_verification_date'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(VerificationScan)
class VerificationScanAdmin(admin.ModelAdmin):
    list_display = [
        'scan_number', 'trainer_profile', 'scan_type', 'scan_status',
        'currency_score', 'total_items_found', 'created_at'
    ]
    list_filter = ['scan_status', 'scan_type', 'created_at']
    search_fields = ['scan_number', 'trainer_profile__trainer_name']
    readonly_fields = ['scan_number', 'created_at', 'started_at', 'completed_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('scan_number', 'trainer_profile', 'scan_type')
        }),
        ('Configuration', {
            'fields': ('sources_to_scan', 'scan_status')
        }),
        ('Results', {
            'fields': (
                'total_items_found', 'relevant_items_count', 'currency_score'
            )
        }),
        ('Processing', {
            'fields': ('scan_duration_seconds', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'started_at', 'completed_at')
        }),
    )


@admin.register(LinkedInActivity)
class LinkedInActivityAdmin(admin.ModelAdmin):
    list_display = [
        'activity_number', 'activity_type', 'title', 'activity_date',
        'is_industry_relevant', 'relevance_score'
    ]
    list_filter = ['activity_type', 'is_industry_relevant', 'activity_date']
    search_fields = ['activity_number', 'title', 'description']
    readonly_fields = ['activity_number', 'extracted_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('activity_number', 'verification_scan', 'activity_type')
        }),
        ('Content', {
            'fields': ('title', 'description', 'url')
        }),
        ('Date Information', {
            'fields': ('activity_date', 'date_text')
        }),
        ('Extracted Entities', {
            'fields': ('skills_mentioned', 'technologies', 'companies', 'keywords')
        }),
        ('Relevance', {
            'fields': ('relevance_score', 'is_industry_relevant', 'relevance_reasoning')
        }),
        ('Metadata', {
            'fields': ('raw_data', 'extracted_at')
        }),
    )


@admin.register(GitHubActivity)
class GitHubActivityAdmin(admin.ModelAdmin):
    list_display = [
        'activity_number', 'activity_type', 'repository_name', 'language',
        'stars', 'is_industry_relevant', 'relevance_score'
    ]
    list_filter = ['activity_type', 'is_industry_relevant', 'language']
    search_fields = ['activity_number', 'repository_name', 'title', 'description']
    readonly_fields = ['activity_number', 'extracted_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('activity_number', 'verification_scan', 'activity_type')
        }),
        ('Content', {
            'fields': ('repository_name', 'title', 'description', 'url')
        }),
        ('Date Information', {
            'fields': ('activity_date', 'last_updated')
        }),
        ('Repository Metadata', {
            'fields': (
                'language', 'languages_used', 'topics',
                'stars', 'forks'
            )
        }),
        ('Extracted Entities', {
            'fields': ('technologies', 'frameworks', 'keywords')
        }),
        ('Relevance', {
            'fields': ('relevance_score', 'is_industry_relevant', 'relevance_reasoning')
        }),
        ('Activity Metrics', {
            'fields': ('commits_count', 'contributions_count')
        }),
        ('Metadata', {
            'fields': ('raw_data', 'extracted_at')
        }),
    )


@admin.register(CurrencyEvidence)
class CurrencyEvidenceAdmin(admin.ModelAdmin):
    list_display = [
        'evidence_number', 'evidence_type', 'trainer_profile',
        'currency_score', 'is_approved', 'created_at'
    ]
    list_filter = ['evidence_type', 'file_format', 'meets_rto_standards', 'is_approved']
    search_fields = ['evidence_number', 'title', 'trainer_profile__trainer_name']
    readonly_fields = ['evidence_number', 'created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('evidence_number', 'trainer_profile', 'verification_scan', 'evidence_type')
        }),
        ('Content', {
            'fields': ('title', 'content')
        }),
        ('Date Range', {
            'fields': ('evidence_start_date', 'evidence_end_date')
        }),
        ('Metrics', {
            'fields': (
                'total_activities', 'relevant_activities', 'currency_score'
            )
        }),
        ('Evidence Metadata', {
            'fields': ('linkedin_activities_included', 'github_activities_included')
        }),
        ('File Storage', {
            'fields': ('file_format', 'file_path', 'file_size_kb')
        }),
        ('Compliance', {
            'fields': ('meets_rto_standards', 'compliance_notes')
        }),
        ('Approval', {
            'fields': ('is_approved', 'approved_by', 'approved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(EntityExtraction)
class EntityExtractionAdmin(admin.ModelAdmin):
    list_display = [
        'extraction_number', 'source_type', 'entity_count',
        'extraction_confidence', 'extracted_at'
    ]
    list_filter = ['source_type', 'nlp_model_used', 'extracted_at']
    search_fields = ['extraction_number', 'source_url', 'source_text']
    readonly_fields = ['extraction_number', 'extracted_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('extraction_number', 'verification_scan', 'source_type')
        }),
        ('Source', {
            'fields': ('source_url', 'source_text')
        }),
        ('Extracted Entities', {
            'fields': ('entities', 'entity_count')
        }),
        ('Confidence', {
            'fields': ('extraction_confidence',)
        }),
        ('Processing', {
            'fields': ('nlp_model_used', 'processing_time_ms')
        }),
        ('Timestamps', {
            'fields': ('extracted_at',)
        }),
    )
