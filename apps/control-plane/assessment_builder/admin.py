from django.contrib import admin
from .models import (
    Assessment,
    AssessmentTask,
    AssessmentCriteria,
    AssessmentGenerationLog,
)


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = [
        "assessment_number",
        "unit_code",
        "unit_title",
        "assessment_type",
        "status",
        "ai_generated",
        "compliance_score",
        "created_at",
    ]
    list_filter = [
        "status",
        "assessment_type",
        "ai_generated",
        "is_compliant",
        "created_at",
    ]
    search_fields = [
        "assessment_number",
        "unit_code",
        "unit_title",
        "training_package",
    ]
    readonly_fields = [
        "assessment_number",
        "ai_generated",
        "ai_model",
        "ai_generation_time",
        "ai_generated_at",
        "dominant_blooms_level",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Assessment Details",
            {
                "fields": (
                    "assessment_number",
                    "tenant",
                    "title",
                    "assessment_type",
                    "status",
                )
            },
        ),
        (
            "Unit Information",
            {
                "fields": (
                    "unit_code",
                    "unit_title",
                    "training_package",
                    "unit_release",
                )
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "instructions",
                    "context",
                    "conditions",
                    "estimated_duration_hours",
                )
            },
        ),
        (
            "AI Generation",
            {
                "fields": (
                    "ai_generated",
                    "ai_model",
                    "ai_prompt",
                    "ai_generation_time",
                    "ai_generated_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Bloom's Taxonomy",
            {
                "fields": (
                    "blooms_analysis",
                    "blooms_distribution",
                    "dominant_blooms_level",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Compliance",
            {
                "fields": (
                    "is_compliant",
                    "compliance_score",
                    "compliance_notes",
                )
            },
        ),
        (
            "Unit Coverage",
            {
                "fields": (
                    "elements_covered",
                    "performance_criteria_covered",
                    "knowledge_evidence_covered",
                    "performance_evidence_covered",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Review & Approval",
            {
                "fields": (
                    "reviewed_by",
                    "reviewed_at",
                    "approved_by",
                    "approved_at",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_by",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(AssessmentTask)
class AssessmentTaskAdmin(admin.ModelAdmin):
    list_display = [
        "assessment",
        "task_number",
        "task_type",
        "blooms_level",
        "ai_generated",
        "estimated_time_minutes",
        "marks_available",
    ]
    list_filter = [
        "task_type",
        "blooms_level",
        "ai_generated",
    ]
    search_fields = [
        "assessment__assessment_number",
        "task_number",
        "question",
    ]
    readonly_fields = [
        "ai_generated",
        "blooms_verbs",
    ]

    fieldsets = (
        (
            "Task Details",
            {
                "fields": (
                    "assessment",
                    "task_number",
                    "task_type",
                    "display_order",
                )
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "question",
                    "context",
                )
            },
        ),
        (
            "Bloom's Taxonomy",
            {
                "fields": (
                    "blooms_level",
                    "blooms_verbs",
                )
            },
        ),
        (
            "Unit Mapping",
            {
                "fields": (
                    "maps_to_elements",
                    "maps_to_performance_criteria",
                    "maps_to_knowledge_evidence",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Assessment Metadata",
            {
                "fields": (
                    "question_count",
                    "estimated_time_minutes",
                    "marks_available",
                )
            },
        ),
        (
            "AI Generation",
            {
                "fields": (
                    "ai_generated",
                    "ai_rationale",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(AssessmentCriteria)
class AssessmentCriteriaAdmin(admin.ModelAdmin):
    list_display = [
        "assessment",
        "criterion_number",
        "task",
        "unit_element",
        "ai_generated",
    ]
    list_filter = [
        "ai_generated",
    ]
    search_fields = [
        "assessment__assessment_number",
        "criterion_text",
        "unit_element",
    ]

    fieldsets = (
        (
            "Criteria Details",
            {
                "fields": (
                    "assessment",
                    "task",
                    "criterion_number",
                    "criterion_text",
                    "display_order",
                )
            },
        ),
        (
            "Unit Mapping",
            {
                "fields": (
                    "unit_element",
                    "performance_criterion",
                    "knowledge_evidence",
                )
            },
        ),
        (
            "Evidence Guidance",
            {
                "fields": (
                    "satisfactory_evidence",
                    "not_satisfactory_evidence",
                )
            },
        ),
        (
            "AI Generation",
            {
                "fields": ("ai_generated",),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(AssessmentGenerationLog)
class AssessmentGenerationLogAdmin(admin.ModelAdmin):
    list_display = [
        "assessment",
        "action",
        "ai_model",
        "success",
        "generation_time",
        "tokens_used",
        "performed_at",
    ]
    list_filter = [
        "action",
        "success",
        "ai_model",
        "performed_at",
    ]
    search_fields = [
        "assessment__assessment_number",
        "error_message",
    ]
    readonly_fields = [
        "assessment",
        "action",
        "ai_model",
        "prompt_used",
        "response_text",
        "tokens_used",
        "generation_time",
        "success",
        "error_message",
        "performed_by",
        "performed_at",
    ]

    fieldsets = (
        (
            "Generation Details",
            {
                "fields": (
                    "assessment",
                    "action",
                    "ai_model",
                    "performed_by",
                    "performed_at",
                )
            },
        ),
        (
            "AI Prompt & Response",
            {
                "fields": (
                    "prompt_used",
                    "response_text",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Metrics",
            {
                "fields": (
                    "tokens_used",
                    "generation_time",
                )
            },
        ),
        (
            "Result",
            {
                "fields": (
                    "success",
                    "error_message",
                )
            },
        ),
    )

    def has_add_permission(self, request):
        # Logs are created automatically, no manual addition
        return False

    def has_change_permission(self, request, obj=None):
        # Logs are immutable
        return False
