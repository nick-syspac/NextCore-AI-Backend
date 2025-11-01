from django.contrib import admin
from .models import (
    RiskAssessment,
    RiskFactor,
    StudentEngagementMetric,
    SentimentAnalysis,
    InterventionAction,
)


@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = [
        "assessment_number",
        "student_name",
        "risk_level",
        "dropout_probability",
        "risk_score",
        "confidence",
        "status",
        "alert_triggered",
        "assessment_date",
    ]
    list_filter = [
        "risk_level",
        "status",
        "alert_triggered",
        "alert_acknowledged",
        "assessment_date",
    ]
    search_fields = ["assessment_number", "student_id", "student_name"]
    readonly_fields = [
        "assessment_number",
        "risk_level",
        "assessment_date",
        "created_at",
        "last_updated",
    ]

    fieldsets = (
        (
            "Student Information",
            {"fields": ("assessment_number", "student_id", "student_name")},
        ),
        (
            "Risk Scores",
            {
                "fields": (
                    "dropout_probability",
                    "risk_level",
                    "risk_score",
                    "confidence",
                    "engagement_score",
                    "performance_score",
                    "attendance_score",
                    "sentiment_score",
                )
            },
        ),
        ("Model Information", {"fields": ("model_version",)}),
        (
            "Status & Alerts",
            {
                "fields": (
                    "status",
                    "alert_triggered",
                    "alert_acknowledged",
                    "alert_acknowledged_by",
                    "alert_acknowledged_at",
                )
            },
        ),
        ("Intervention", {"fields": ("intervention_assigned", "intervention_notes")}),
        (
            "Metadata",
            {
                "fields": (
                    "assessment_date",
                    "last_updated",
                    "created_by",
                    "created_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(RiskFactor)
class RiskFactorAdmin(admin.ModelAdmin):
    list_display = [
        "factor_number",
        "assessment",
        "factor_type",
        "factor_name",
        "severity",
        "contribution",
        "threshold_exceeded",
        "trend",
    ]
    list_filter = ["factor_type", "severity", "threshold_exceeded", "trend"]
    search_fields = ["factor_number", "factor_name", "assessment__student_name"]
    readonly_fields = ["factor_number", "threshold_exceeded", "created_at"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "factor_number",
                    "assessment",
                    "factor_type",
                    "factor_name",
                    "description",
                )
            },
        ),
        ("Metrics", {"fields": ("weight", "contribution", "severity", "trend")}),
        (
            "Data Points",
            {"fields": ("current_value", "threshold_value", "threshold_exceeded")},
        ),
        ("Metadata", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(StudentEngagementMetric)
class StudentEngagementMetricAdmin(admin.ModelAdmin):
    list_display = [
        "metric_number",
        "student_name",
        "overall_engagement_score",
        "login_frequency",
        "assignment_submission_rate",
        "days_inactive",
        "measurement_date",
    ]
    list_filter = ["measurement_date"]
    search_fields = ["metric_number", "student_id", "student_name"]
    readonly_fields = ["metric_number", "measurement_date", "created_at"]

    fieldsets = (
        (
            "Student Information",
            {"fields": ("metric_number", "student_id", "student_name")},
        ),
        (
            "Engagement Metrics",
            {
                "fields": (
                    "login_frequency",
                    "time_on_platform",
                    "assignment_submission_rate",
                    "forum_participation",
                    "peer_interaction_score",
                )
            },
        ),
        (
            "Activity Patterns",
            {"fields": ("last_login", "days_inactive", "activity_decline_rate")},
        ),
        ("Overall Score", {"fields": ("overall_engagement_score",)}),
        (
            "Metadata",
            {"fields": ("measurement_date", "created_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        "analysis_number",
        "assessment",
        "source_type",
        "sentiment_label",
        "sentiment_score",
        "confidence",
        "analysis_date",
    ]
    list_filter = ["source_type", "sentiment_label", "analysis_date"]
    search_fields = ["analysis_number", "assessment__student_name", "text_sample"]
    readonly_fields = ["analysis_number", "sentiment_label", "analysis_date"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("analysis_number", "assessment", "source_type", "text_sample")},
        ),
        (
            "Sentiment Scores",
            {"fields": ("sentiment_score", "sentiment_label", "confidence")},
        ),
        (
            "Emotion Detection",
            {
                "fields": (
                    "frustration_detected",
                    "stress_detected",
                    "confusion_detected",
                    "disengagement_detected",
                )
            },
        ),
        ("Keywords & Patterns", {"fields": ("negative_keywords", "risk_indicators")}),
        ("Metadata", {"fields": ("analysis_date",), "classes": ("collapse",)}),
    )


@admin.register(InterventionAction)
class InterventionActionAdmin(admin.ModelAdmin):
    list_display = [
        "action_number",
        "assessment",
        "action_type",
        "priority",
        "status",
        "scheduled_date",
        "assigned_to",
    ]
    list_filter = ["action_type", "priority", "status", "scheduled_date"]
    search_fields = ["action_number", "assessment__student_name", "description"]
    readonly_fields = ["action_number", "created_at", "updated_at"]

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "action_number",
                    "assessment",
                    "action_type",
                    "description",
                    "priority",
                )
            },
        ),
        (
            "Scheduling",
            {"fields": ("scheduled_date", "completed_date", "status", "assigned_to")},
        ),
        ("Outcomes", {"fields": ("outcome_notes", "effectiveness_rating")}),
        (
            "Metadata",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
