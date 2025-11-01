from django.contrib import admin
from .models import (
    EngagementHeatmap,
    AttendanceRecord,
    LMSActivity,
    DiscussionSentiment,
    EngagementAlert,
)


@admin.register(EngagementHeatmap)
class EngagementHeatmapAdmin(admin.ModelAdmin):
    list_display = [
        "heatmap_number",
        "student_name",
        "time_period",
        "start_date",
        "end_date",
        "overall_engagement_score",
        "risk_level",
        "engagement_trend",
        "alerts_triggered",
    ]
    list_filter = [
        "risk_level",
        "engagement_trend",
        "time_period",
        "tenant",
        "start_date",
    ]
    search_fields = ["heatmap_number", "student_name", "student_id"]
    readonly_fields = [
        "heatmap_number",
        "overall_engagement_score",
        "risk_level",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Heatmap Information",
            {
                "fields": (
                    "heatmap_number",
                    "tenant",
                    "student_id",
                    "student_name",
                    "time_period",
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "Engagement Scores",
            {
                "fields": (
                    "overall_engagement_score",
                    "attendance_score",
                    "lms_activity_score",
                    "sentiment_score",
                )
            },
        ),
        (
            "Risk Assessment",
            {
                "fields": (
                    "risk_level",
                    "risk_flags",
                    "engagement_trend",
                    "change_percentage",
                )
            },
        ),
        ("Heatmap Data", {"fields": ("heatmap_data",), "classes": ("collapse",)}),
        (
            "Intervention Tracking",
            {"fields": ("alerts_triggered", "interventions_applied")},
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = [
        "record_number",
        "student_id",
        "date",
        "status",
        "session_name",
        "minutes_late",
        "minutes_attended",
        "participation_level",
    ]
    list_filter = ["status", "participation_level", "date", "tenant"]
    search_fields = ["record_number", "student_id", "session_name"]
    readonly_fields = ["record_number", "created_at"]
    date_hierarchy = "date"

    fieldsets = (
        (
            "Record Information",
            {"fields": ("record_number", "heatmap", "tenant", "student_id")},
        ),
        (
            "Attendance Details",
            {
                "fields": (
                    "date",
                    "status",
                    "session_name",
                    "scheduled_start",
                    "scheduled_end",
                    "actual_arrival",
                    "actual_departure",
                )
            },
        ),
        (
            "Metrics",
            {"fields": ("minutes_late", "minutes_attended", "participation_level")},
        ),
        ("Notes", {"fields": ("notes",)}),
    )


@admin.register(LMSActivity)
class LMSActivityAdmin(admin.ModelAdmin):
    list_display = [
        "activity_number",
        "student_id",
        "date",
        "activity_type",
        "activity_name",
        "duration_minutes",
        "completion_status",
        "quality_score",
    ]
    list_filter = ["activity_type", "completion_status", "date", "tenant"]
    search_fields = ["activity_number", "student_id", "activity_name", "course_name"]
    readonly_fields = ["activity_number", "created_at"]
    date_hierarchy = "date"

    fieldsets = (
        (
            "Activity Information",
            {"fields": ("activity_number", "heatmap", "tenant", "student_id")},
        ),
        (
            "Activity Details",
            {
                "fields": (
                    "date",
                    "timestamp",
                    "activity_type",
                    "activity_name",
                    "duration_minutes",
                )
            },
        ),
        (
            "Engagement Metrics",
            {"fields": ("completion_status", "interaction_count", "quality_score")},
        ),
        ("Content Metadata", {"fields": ("course_name", "module_name")}),
    )


@admin.register(DiscussionSentiment)
class DiscussionSentimentAdmin(admin.ModelAdmin):
    list_display = [
        "sentiment_number",
        "student_id",
        "date",
        "message_type",
        "sentiment_label",
        "sentiment_score",
        "confidence",
        "primary_emotion",
    ]
    list_filter = [
        "sentiment_label",
        "primary_emotion",
        "message_type",
        "date",
        "tenant",
    ]
    search_fields = [
        "sentiment_number",
        "student_id",
        "message_content",
        "discussion_topic",
    ]
    readonly_fields = ["sentiment_number", "sentiment_label", "created_at"]
    date_hierarchy = "date"

    fieldsets = (
        (
            "Sentiment Information",
            {"fields": ("sentiment_number", "heatmap", "tenant", "student_id")},
        ),
        (
            "Message Details",
            {
                "fields": (
                    "date",
                    "timestamp",
                    "message_type",
                    "message_content",
                    "discussion_topic",
                )
            },
        ),
        (
            "Sentiment Analysis",
            {
                "fields": (
                    "sentiment_score",
                    "sentiment_label",
                    "confidence",
                    "primary_emotion",
                    "emotion_scores",
                )
            },
        ),
        (
            "Engagement Indicators",
            {
                "fields": (
                    "word_count",
                    "question_count",
                    "exclamation_count",
                    "reply_count",
                )
            },
        ),
        ("Risk Keywords", {"fields": ("negative_keywords", "help_seeking_keywords")}),
    )


@admin.register(EngagementAlert)
class EngagementAlertAdmin(admin.ModelAdmin):
    list_display = [
        "alert_number",
        "student_name",
        "alert_type",
        "severity",
        "status",
        "created_at",
        "acknowledged_by",
    ]
    list_filter = ["alert_type", "severity", "status", "tenant", "created_at"]
    search_fields = [
        "alert_number",
        "student_name",
        "student_id",
        "title",
        "description",
    ]
    readonly_fields = ["alert_number", "created_at", "updated_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Alert Information",
            {
                "fields": (
                    "alert_number",
                    "heatmap",
                    "tenant",
                    "student_id",
                    "student_name",
                )
            },
        ),
        (
            "Alert Details",
            {"fields": ("alert_type", "severity", "title", "description")},
        ),
        ("Trigger Metrics", {"fields": ("trigger_metrics", "recommended_actions")}),
        (
            "Status Tracking",
            {
                "fields": (
                    "status",
                    "acknowledged_by",
                    "acknowledged_at",
                    "resolved_at",
                    "resolution_notes",
                )
            },
        ),
    )
