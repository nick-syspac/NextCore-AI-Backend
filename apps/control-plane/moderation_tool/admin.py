from django.contrib import admin
from .models import ModerationSession, AssessorDecision, OutlierDetection, BiasScore, ModerationLog


@admin.register(ModerationSession)
class ModerationSessionAdmin(admin.ModelAdmin):
    list_display = ('session_number', 'name', 'assessment_type', 'status', 'decisions_compared', 
                   'outliers_detected', 'bias_flags_raised', 'created_at')
    list_filter = ('status', 'assessment_type', 'created_at')
    search_fields = ('session_number', 'name', 'assessment_title')
    readonly_fields = ('session_number', 'created_at', 'updated_at', 'outliers_detected', 
                      'bias_flags_raised', 'decisions_compared', 'average_agreement_rate')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('session_number', 'name', 'description', 'assessment_type', 'status')
        }),
        ('Assessment Details', {
            'fields': ('assessment_title', 'total_submissions', 'assessors_count')
        }),
        ('Moderation Settings', {
            'fields': ('outlier_threshold', 'bias_sensitivity'),
            'description': 'Configure detection thresholds and sensitivity levels'
        }),
        ('Statistics', {
            'fields': ('decisions_compared', 'outliers_detected', 'bias_flags_raised', 'average_agreement_rate'),
            'classes': ('collapse',)
        }),
        ('Audit Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AssessorDecision)
class AssessorDecisionAdmin(admin.ModelAdmin):
    list_display = ('decision_number', 'session', 'student_id', 'assessor_name', 
                   'score', 'grade', 'is_outlier', 'has_bias_flag', 'marked_at')
    list_filter = ('is_outlier', 'has_bias_flag', 'requires_review', 'grade', 'marked_at')
    search_fields = ('decision_number', 'student_id', 'student_name', 'assessor_id', 'assessor_name')
    readonly_fields = ('decision_number', 'created_at')
    
    fieldsets = (
        ('Decision Information', {
            'fields': ('decision_number', 'session')
        }),
        ('Student Details', {
            'fields': ('student_id', 'student_name', 'submission_id')
        }),
        ('Assessor Details', {
            'fields': ('assessor_id', 'assessor_name', 'marked_at', 'marking_time_minutes')
        }),
        ('Scoring', {
            'fields': ('score', 'max_score', 'grade', 'criterion_scores')
        }),
        ('Flags', {
            'fields': ('is_outlier', 'has_bias_flag', 'requires_review'),
            'classes': ('collapse',)
        }),
        ('Comments', {
            'fields': ('comments',),
            'classes': ('collapse',)
        }),
    )


@admin.register(OutlierDetection)
class OutlierDetectionAdmin(admin.ModelAdmin):
    list_display = ('outlier_number', 'session', 'outlier_type', 'severity', 
                   'z_score', 'confidence_score', 'is_resolved', 'detected_at')
    list_filter = ('severity', 'outlier_type', 'is_resolved', 'detected_at')
    search_fields = ('outlier_number', 'decision__student_id', 'decision__assessor_name')
    readonly_fields = ('outlier_number', 'detected_at')
    
    fieldsets = (
        ('Outlier Information', {
            'fields': ('outlier_number', 'session', 'decision', 'outlier_type', 'severity')
        }),
        ('Statistical Analysis', {
            'fields': ('z_score', 'deviation_percentage', 'expected_score', 'actual_score', 
                      'cohort_mean', 'cohort_std_dev', 'assessor_mean', 'confidence_score')
        }),
        ('Explanation', {
            'fields': ('explanation',)
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolution_notes', 'resolved_by', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BiasScore)
class BiasScoreAdmin(admin.ModelAdmin):
    list_display = ('bias_number', 'session', 'assessor_name', 'bias_type', 
                   'bias_score', 'severity_level', 'is_validated', 'calculated_at')
    list_filter = ('bias_type', 'is_validated', 'severity_level', 'calculated_at')
    search_fields = ('bias_number', 'assessor_id', 'assessor_name')
    readonly_fields = ('bias_number', 'calculated_at')
    
    fieldsets = (
        ('Bias Information', {
            'fields': ('bias_number', 'session', 'assessor_id', 'assessor_name', 
                      'bias_type', 'bias_score', 'severity_level')
        }),
        ('Statistical Evidence', {
            'fields': ('sample_size', 'mean_difference', 'std_dev_ratio', 'evidence', 'affected_students')
        }),
        ('Recommendation', {
            'fields': ('recommendation',)
        }),
        ('Validation', {
            'fields': ('is_validated', 'validation_notes', 'validated_by', 'validated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ('session', 'action', 'decisions_processed', 'outliers_found', 
                   'bias_flags', 'processing_time_ms', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('session__session_number', 'description')
    readonly_fields = ('timestamp',)
    
    fieldsets = (
        ('Log Information', {
            'fields': ('session', 'action', 'description', 'performed_by')
        }),
        ('Metrics', {
            'fields': ('decisions_processed', 'outliers_found', 'bias_flags', 'processing_time_ms')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )
