from django.contrib import admin
from .models import (
    AuthenticityCheck,
    SubmissionAnalysis,
    PlagiarismMatch,
    MetadataVerification,
    AnomalyDetection,
)


@admin.register(AuthenticityCheck)
class AuthenticityCheckAdmin(admin.ModelAdmin):
    list_display = [
        "check_number",
        "name",
        "assessment",
        "status",
        "total_submissions_checked",
        "plagiarism_cases_detected",
        "overall_integrity_score",
        "created_at",
    ]
    list_filter = ["status", "academic_integrity_mode", "created_at"]
    search_fields = ["check_number", "name", "assessment__title"]
    readonly_fields = [
        "check_number",
        "total_submissions_checked",
        "plagiarism_cases_detected",
        "metadata_issues_found",
        "anomalies_detected",
        "overall_integrity_score",
        "created_at",
        "updated_at",
    ]
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "check_number",
                    "assessment",
                    "name",
                    "description",
                    "created_by",
                )
            },
        ),
        (
            "Configuration",
            {
                "fields": (
                    "plagiarism_threshold",
                    "metadata_verification_enabled",
                    "anomaly_detection_enabled",
                    "academic_integrity_mode",
                )
            },
        ),
        (
            "Status & Statistics",
            {
                "fields": (
                    "status",
                    "total_submissions_checked",
                    "plagiarism_cases_detected",
                    "metadata_issues_found",
                    "anomalies_detected",
                    "overall_integrity_score",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(SubmissionAnalysis)
class SubmissionAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        "analysis_number",
        "submission_id",
        "student_name",
        "authenticity_check",
        "plagiarism_score",
        "combined_integrity_score",
        "integrity_status",
        "plagiarism_detected",
        "analyzed_at",
    ]
    list_filter = [
        "integrity_status",
        "plagiarism_detected",
        "metadata_issues",
        "anomalies_found",
        "analyzed_at",
    ]
    search_fields = [
        "analysis_number",
        "submission_id",
        "student_id",
        "student_name",
        "content_hash",
    ]
    readonly_fields = [
        "analysis_number",
        "content_hash",
        "word_count",
        "character_count",
        "analyzed_at",
    ]
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "analysis_number",
                    "authenticity_check",
                    "submission_id",
                    "student_id",
                    "student_name",
                )
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "submission_content",
                    "content_hash",
                    "word_count",
                    "character_count",
                    "content_embedding",
                )
            },
        ),
        (
            "Scores",
            {
                "fields": (
                    "plagiarism_score",
                    "metadata_verification_score",
                    "anomaly_score",
                    "combined_integrity_score",
                )
            },
        ),
        (
            "Results",
            {
                "fields": (
                    "integrity_status",
                    "plagiarism_detected",
                    "metadata_issues",
                    "anomalies_found",
                )
            },
        ),
        ("Metadata", {"fields": ("analysis_metadata", "analyzed_at")}),
    )


@admin.register(PlagiarismMatch)
class PlagiarismMatchAdmin(admin.ModelAdmin):
    list_display = [
        "match_number",
        "similarity_score",
        "match_type",
        "severity",
        "matched_percentage",
        "reviewed",
        "detected_at",
    ]
    list_filter = [
        "match_type",
        "severity",
        "reviewed",
        "false_positive",
        "detected_at",
    ]
    search_fields = [
        "match_number",
        "source_analysis__analysis_number",
        "matched_analysis__analysis_number",
    ]
    readonly_fields = ["match_number", "severity", "detected_at"]
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("match_number", "source_analysis", "matched_analysis")},
        ),
        (
            "Match Details",
            {
                "fields": (
                    "similarity_score",
                    "match_type",
                    "severity",
                    "matched_text_segments",
                    "matched_words_count",
                    "matched_percentage",
                )
            },
        ),
        (
            "Review",
            {
                "fields": (
                    "reviewed",
                    "false_positive",
                    "review_notes",
                    "reviewed_by",
                    "reviewed_at",
                )
            },
        ),
        ("Timestamps", {"fields": ("detected_at",)}),
    )


@admin.register(MetadataVerification)
class MetadataVerificationAdmin(admin.ModelAdmin):
    list_display = [
        "verification_number",
        "submission_analysis",
        "verification_status",
        "verification_score",
        "author_matches_student",
        "verified_at",
    ]
    list_filter = ["verification_status", "author_matches_student", "verified_at"]
    search_fields = ["verification_number", "submission_analysis__analysis_number"]
    readonly_fields = [
        "verification_number",
        "verification_status",
        "verification_score",
        "verified_at",
    ]
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("verification_number", "submission_analysis")},
        ),
        (
            "File Metadata",
            {
                "fields": (
                    "file_metadata",
                    "creation_timestamp",
                    "modification_timestamp",
                    "modification_history",
                )
            },
        ),
        ("Author Information", {"fields": ("author_info", "author_matches_student")}),
        (
            "Verification Results",
            {
                "fields": (
                    "verification_status",
                    "anomalies_detected",
                    "verification_score",
                )
            },
        ),
        ("Timestamps", {"fields": ("verified_at",)}),
    )


@admin.register(AnomalyDetection)
class AnomalyDetectionAdmin(admin.ModelAdmin):
    list_display = [
        "anomaly_number",
        "submission_analysis",
        "anomaly_type",
        "severity",
        "confidence_score",
        "impact_score",
        "acknowledged",
        "detected_at",
    ]
    list_filter = [
        "anomaly_type",
        "severity",
        "acknowledged",
        "false_positive",
        "detected_at",
    ]
    search_fields = [
        "anomaly_number",
        "submission_analysis__analysis_number",
        "description",
    ]
    readonly_fields = ["anomaly_number", "impact_score", "detected_at"]
    fieldsets = (
        ("Basic Information", {"fields": ("anomaly_number", "submission_analysis")}),
        (
            "Anomaly Details",
            {
                "fields": (
                    "anomaly_type",
                    "severity",
                    "anomaly_data",
                    "description",
                    "confidence_score",
                    "impact_score",
                )
            },
        ),
        ("Review", {"fields": ("acknowledged", "false_positive", "resolution_notes")}),
        ("Timestamps", {"fields": ("detected_at",)}),
    )
