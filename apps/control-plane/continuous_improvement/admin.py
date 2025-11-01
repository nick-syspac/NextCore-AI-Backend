from django.contrib import admin
from .models import (
    ImprovementCategory,
    ImprovementAction,
    ActionTracking,
    ImprovementReview,
)


@admin.register(ImprovementCategory)
class ImprovementCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category_type", "tenant", "is_active", "created_at"]
    list_filter = ["category_type", "is_active", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at"]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": [
                    "tenant",
                    "name",
                    "category_type",
                    "description",
                    "color_code",
                ]
            },
        ),
        ("ASQA Alignment", {"fields": ["related_standards"]}),
        ("Status", {"fields": ["is_active", "created_by", "created_at"]}),
    ]


@admin.register(ImprovementAction)
class ImprovementActionAdmin(admin.ModelAdmin):
    list_display = [
        "action_number",
        "title",
        "priority",
        "status",
        "compliance_status",
        "responsible_person",
        "target_completion_date",
    ]
    list_filter = [
        "status",
        "priority",
        "compliance_status",
        "source",
        "is_critical_compliance",
        "created_at",
    ]
    search_fields = ["action_number", "title", "description", "ai_summary"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "ai_processed_at",
        "compliance_status",
        "progress_percentage",
        "is_overdue",
        "days_until_due",
    ]
    filter_horizontal = ["supporting_staff"]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": [
                    "tenant",
                    "action_number",
                    "title",
                    "description",
                    "category",
                    "priority",
                    "source",
                    "tags",
                ]
            },
        ),
        (
            "AI Classification",
            {
                "fields": [
                    "ai_classified_category",
                    "ai_classification_confidence",
                    "ai_summary",
                    "ai_keywords",
                    "ai_related_standards",
                    "ai_processed_at",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Status & Timeline",
            {
                "fields": [
                    "status",
                    "compliance_status",
                    "progress_percentage",
                    "identified_date",
                    "planned_start_date",
                    "target_completion_date",
                    "actual_completion_date",
                    "is_overdue",
                    "days_until_due",
                ]
            },
        ),
        ("Assignment", {"fields": ["responsible_person", "supporting_staff"]}),
        (
            "Implementation Details",
            {
                "fields": [
                    "root_cause",
                    "proposed_solution",
                    "resources_required",
                    "estimated_cost",
                    "actual_cost",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Effectiveness & Impact",
            {
                "fields": [
                    "success_criteria",
                    "expected_impact",
                    "actual_impact",
                    "effectiveness_rating",
                ],
                "classes": ["collapse"],
            },
        ),
        ("Compliance", {"fields": ["is_critical_compliance"]}),
        (
            "Approval",
            {
                "fields": ["requires_approval", "approved_by", "approved_at"],
                "classes": ["collapse"],
            },
        ),
        (
            "Metadata",
            {
                "fields": ["attachments", "created_at", "created_by", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return self.readonly_fields + ["created_by", "action_number"]
        return self.readonly_fields


@admin.register(ActionTracking)
class ActionTrackingAdmin(admin.ModelAdmin):
    list_display = [
        "improvement_action",
        "update_type",
        "is_blocker",
        "progress_percentage",
        "created_at",
        "created_by",
    ]
    list_filter = ["update_type", "is_blocker", "blocker_resolved", "created_at"]
    search_fields = ["improvement_action__action_number", "update_text"]
    readonly_fields = ["created_at"]

    fieldsets = [
        (
            "Update Information",
            {
                "fields": [
                    "improvement_action",
                    "update_type",
                    "update_text",
                    "progress_percentage",
                ]
            },
        ),
        ("Status Changes", {"fields": ["old_status", "new_status"]}),
        (
            "Blockers",
            {"fields": ["is_blocker", "blocker_resolved", "blocker_resolution"]},
        ),
        ("Evidence", {"fields": ["evidence_provided"]}),
        ("Metadata", {"fields": ["created_at", "created_by"]}),
    ]


@admin.register(ImprovementReview)
class ImprovementReviewAdmin(admin.ModelAdmin):
    list_display = [
        "review_number",
        "title",
        "review_type",
        "review_date",
        "total_actions_reviewed",
        "reviewed_by",
    ]
    list_filter = ["review_type", "review_date", "created_at"]
    search_fields = ["review_number", "title", "key_findings"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "total_actions_reviewed",
        "actions_completed",
        "actions_on_track",
        "actions_at_risk",
        "actions_overdue",
    ]
    filter_horizontal = ["actions_reviewed", "attendees"]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": [
                    "tenant",
                    "review_number",
                    "title",
                    "review_type",
                    "review_date",
                ]
            },
        ),
        (
            "Review Scope",
            {
                "fields": [
                    "actions_reviewed",
                    "review_period_start",
                    "review_period_end",
                ]
            },
        ),
        (
            "Statistics",
            {
                "fields": [
                    "total_actions_reviewed",
                    "actions_completed",
                    "actions_on_track",
                    "actions_at_risk",
                    "actions_overdue",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "AI Insights",
            {
                "fields": ["ai_summary", "ai_trends", "ai_recommendations"],
                "classes": ["collapse"],
            },
        ),
        (
            "Review Outcomes",
            {
                "fields": [
                    "key_findings",
                    "areas_of_concern",
                    "recommendations",
                    "action_items",
                ]
            },
        ),
        ("Review Team", {"fields": ["reviewed_by", "attendees"]}),
        ("Approval", {"fields": ["approved_by", "approved_at"]}),
        (
            "Metadata",
            {
                "fields": ["notes", "attachments", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]
