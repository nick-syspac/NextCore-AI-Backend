from django.contrib import admin
from .models import TAS, TASTemplate, TASVersion, TASGenerationLog


@admin.register(TASTemplate)
class TASTemplateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "template_type",
        "aqf_level",
        "is_active",
        "is_system_template",
        "created_at",
    ]
    list_filter = ["template_type", "aqf_level", "is_active", "is_system_template"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_by", "created_at", "updated_at"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "description", "template_type", "aqf_level")},
        ),
        (
            "Template Configuration",
            {"fields": ("structure", "default_sections", "gpt_prompts")},
        ),
        ("Status", {"fields": ("is_active", "is_system_template")}),
        (
            "Metadata",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TAS)
class TASAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "title",
        "tenant",
        "aqf_level",
        "status",
        "version",
        "is_current_version",
        "gpt_generated",
        "created_at",
    ]
    list_filter = [
        "status",
        "aqf_level",
        "gpt_generated",
        "is_current_version",
        "tenant",
    ]
    search_fields = ["code", "title", "qualification_name", "description"]
    readonly_fields = [
        "version",
        "gpt_generation_date",
        "created_by",
        "created_at",
        "updated_at",
        "submitted_by",
        "submitted_for_review_at",
        "reviewed_by",
        "reviewed_at",
        "approved_by",
        "approved_at",
        "published_at",
    ]
    date_hierarchy = "created_at"

    fieldsets = (
        ("Basic Information", {"fields": ("tenant", "title", "code", "description")}),
        (
            "Qualification Details",
            {
                "fields": (
                    "qualification_name",
                    "aqf_level",
                    "training_package",
                    "template",
                )
            },
        ),
        (
            "Document Content",
            {"fields": ("sections", "content", "metadata"), "classes": ("collapse",)},
        ),
        ("Status & Version", {"fields": ("status", "version", "is_current_version")}),
        (
            "GPT-4 Generation",
            {
                "fields": (
                    "gpt_generated",
                    "gpt_generation_date",
                    "gpt_model_used",
                    "gpt_tokens_used",
                    "generation_time_seconds",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Approval Workflow",
            {
                "fields": (
                    "submitted_for_review_at",
                    "submitted_by",
                    "reviewed_at",
                    "reviewed_by",
                    "approved_at",
                    "approved_by",
                    "published_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Audit",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TASVersion)
class TASVersionAdmin(admin.ModelAdmin):
    list_display = [
        "tas",
        "version_number",
        "created_by",
        "created_at",
        "was_regenerated",
    ]
    list_filter = ["was_regenerated", "created_at"]
    search_fields = ["tas__code", "tas__title", "change_summary"]
    readonly_fields = ["created_by", "created_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Version Information",
            {"fields": ("tas", "version_number", "change_summary", "changed_sections")},
        ),
        (
            "Content Changes",
            {
                "fields": ("content_diff", "previous_content", "new_content"),
                "classes": ("collapse",),
            },
        ),
        ("Regeneration", {"fields": ("was_regenerated", "regeneration_reason")}),
        (
            "Metadata",
            {"fields": ("created_by", "created_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(TASGenerationLog)
class TASGenerationLogAdmin(admin.ModelAdmin):
    list_display = [
        "tas",
        "status",
        "model_version",
        "tokens_total",
        "generation_time_seconds",
        "created_at",
        "completed_at",
    ]
    list_filter = ["status", "model_version", "created_at"]
    search_fields = ["tas__code", "tas__title", "error_message"]
    readonly_fields = ["created_by", "created_at", "completed_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Generation Request",
            {
                "fields": (
                    "tas",
                    "status",
                    "requested_sections",
                    "input_data",
                    "gpt_prompts",
                )
            },
        ),
        (
            "Generated Content",
            {"fields": ("generated_content",), "classes": ("collapse",)},
        ),
        (
            "Performance Metrics",
            {
                "fields": (
                    "model_version",
                    "tokens_prompt",
                    "tokens_completion",
                    "tokens_total",
                    "generation_time_seconds",
                )
            },
        ),
        (
            "Error Handling",
            {"fields": ("error_message", "retry_count"), "classes": ("collapse",)},
        ),
        (
            "Metadata",
            {
                "fields": ("created_by", "created_at", "completed_at"),
                "classes": ("collapse",),
            },
        ),
    )
