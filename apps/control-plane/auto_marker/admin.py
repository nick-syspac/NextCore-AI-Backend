from django.contrib import admin
from .models import (
    AutoMarker,
    MarkedResponse,
    MarkingCriterion,
    CriterionScore,
    MarkingLog,
)


@admin.register(AutoMarker)
class AutoMarkerAdmin(admin.ModelAdmin):
    list_display = [
        "marker_number",
        "title",
        "tenant",
        "answer_type",
        "status",
        "total_responses_marked",
        "average_similarity_score",
        "created_at",
    ]
    list_filter = ["status", "answer_type", "similarity_model", "tenant", "created_at"]
    search_fields = ["marker_number", "title", "description", "question_text"]
    readonly_fields = [
        "marker_number",
        "total_responses_marked",
        "average_similarity_score",
        "average_marking_time",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Identification",
            {
                "fields": (
                    "marker_number",
                    "title",
                    "description",
                    "tenant",
                    "created_by",
                )
            },
        ),
        (
            "Question Configuration",
            {"fields": ("answer_type", "question_text", "model_answer", "max_marks")},
        ),
        (
            "Semantic Similarity Settings",
            {
                "fields": (
                    "similarity_model",
                    "similarity_threshold",
                    "partial_credit_enabled",
                    "min_similarity_for_credit",
                )
            },
        ),
        (
            "Keyword Matching",
            {"fields": ("use_keywords", "keywords", "keyword_weight")},
        ),
        (
            "Performance Metrics",
            {
                "fields": (
                    "total_responses_marked",
                    "average_similarity_score",
                    "average_marking_time",
                )
            },
        ),
        ("Status", {"fields": ("status", "created_at", "updated_at")}),
    )


@admin.register(MarkedResponse)
class MarkedResponseAdmin(admin.ModelAdmin):
    list_display = [
        "response_number",
        "student_name",
        "student_id",
        "auto_marker",
        "marks_awarded",
        "similarity_score",
        "confidence_score",
        "requires_review",
        "status",
        "marked_at",
    ]
    list_filter = [
        "status",
        "requires_review",
        "auto_marker",
        "marked_at",
        "created_at",
    ]
    search_fields = ["response_number", "student_id", "student_name", "response_text"]
    readonly_fields = [
        "response_number",
        "word_count",
        "similarity_score",
        "keyword_match_score",
        "combined_score",
        "marks_awarded",
        "confidence_score",
        "matched_keywords",
        "missing_keywords",
        "key_phrases_detected",
        "similarity_breakdown",
        "automated_feedback",
        "marking_time",
        "marked_at",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        ("Identification", {"fields": ("response_number", "auto_marker", "status")}),
        ("Student Information", {"fields": ("student_id", "student_name")}),
        ("Response Content", {"fields": ("response_text", "word_count")}),
        (
            "Scoring",
            {
                "fields": (
                    "similarity_score",
                    "keyword_match_score",
                    "combined_score",
                    "marks_awarded",
                    "confidence_score",
                )
            },
        ),
        (
            "Analysis",
            {
                "fields": (
                    "matched_keywords",
                    "missing_keywords",
                    "key_phrases_detected",
                    "similarity_breakdown",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Feedback & Review",
            {
                "fields": (
                    "automated_feedback",
                    "requires_review",
                    "review_reason",
                    "reviewer_notes",
                    "reviewed_by",
                    "reviewed_at",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": ("marking_time", "marked_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(MarkingCriterion)
class MarkingCriterionAdmin(admin.ModelAdmin):
    list_display = [
        "criterion_name",
        "auto_marker",
        "weight",
        "max_points",
        "required",
        "display_order",
    ]
    list_filter = ["required", "auto_marker"]
    search_fields = ["criterion_name", "description"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("auto_marker", "criterion_name", "description")},
        ),
        ("Expected Content", {"fields": ("expected_content", "criterion_keywords")}),
        ("Scoring", {"fields": ("weight", "max_points", "required")}),
        ("Display", {"fields": ("display_order",)}),
    )


@admin.register(CriterionScore)
class CriterionScoreAdmin(admin.ModelAdmin):
    list_display = ["response", "criterion", "similarity_score", "points_awarded"]
    list_filter = ["criterion", "response__auto_marker"]
    search_fields = ["response__response_number", "criterion__criterion_name"]
    readonly_fields = ["created_at"]


@admin.register(MarkingLog)
class MarkingLogAdmin(admin.ModelAdmin):
    list_display = [
        "auto_marker",
        "action",
        "performed_by",
        "responses_processed",
        "average_time_per_response",
        "timestamp",
    ]
    list_filter = ["action", "similarity_model", "auto_marker", "timestamp"]
    search_fields = ["auto_marker__marker_number", "response__response_number"]
    readonly_fields = ["average_time_per_response", "timestamp"]

    fieldsets = (
        (
            "Action Details",
            {"fields": ("auto_marker", "response", "action", "performed_by")},
        ),
        ("AI/Model Information", {"fields": ("similarity_model", "model_version")}),
        (
            "Performance Metrics",
            {
                "fields": (
                    "responses_processed",
                    "total_time",
                    "average_time_per_response",
                )
            },
        ),
        (
            "Score Changes",
            {
                "fields": ("original_score", "new_score", "adjustment_reason"),
                "classes": ("collapse",),
            },
        ),
        (
            "Additional Details",
            {"fields": ("details", "timestamp"), "classes": ("collapse",)},
        ),
    )
