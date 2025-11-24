from django.contrib import admin
from .models import (
    TAS, 
    TASTemplate, 
    TASTemplateSection, 
    TASTemplateSectionAssignment,
    TASVersion, 
    TASGenerationLog
)


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


@admin.register(TASTemplateSection)
class TASTemplateSectionAdmin(admin.ModelAdmin):
    list_display = [
        "section_name",
        "section_code",
        "content_type",
        "is_editable",
        "is_active",
        "parent_section",
        "template_count",
    ]
    list_filter = ["content_type", "is_editable", "is_active"]
    search_fields = ["section_name", "section_code", "description"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["section_name"]

    fieldsets = (
        (
            "Section Identification",
            {"fields": ("section_name", "section_code")},
        ),
        (
            "Content Configuration",
            {
                "fields": (
                    "description",
                    "content_type",
                    "default_content",
                )
            },
        ),
        (
            "Behavior",
            {
                "fields": (
                    "is_editable",
                    "is_active",
                    "parent_section",
                )
            },
        ),
        (
            "AI Integration",
            {"fields": ("gpt_prompt",), "classes": ("collapse",)},
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("parent_section")
    
    def template_count(self, obj):
        """Show how many templates use this section"""
        return obj.template_assignments.count()
    template_count.short_description = "Templates"


class TASTemplateSectionAssignmentInline(admin.TabularInline):
    model = TASTemplateSectionAssignment
    extra = 1
    fields = ["section", "section_order", "is_required", "custom_label"]
    autocomplete_fields = ["section"]


@admin.register(TASTemplateSectionAssignment)
class TASTemplateSectionAssignmentAdmin(admin.ModelAdmin):
    list_display = [
        "template",
        "section",
        "section_order",
        "is_required",
        "effective_label",
    ]
    list_filter = ["template", "is_required"]
    search_fields = [
        "template__name",
        "section__section_name",
        "section__section_code",
        "custom_label",
    ]
    readonly_fields = ["effective_label", "effective_description", "created_at", "updated_at"]
    ordering = ["template", "section_order"]

    fieldsets = (
        (
            "Assignment",
            {"fields": ("template", "section", "section_order", "is_required")},
        ),
        (
            "Customization",
            {
                "fields": (
                    "custom_label",
                    "custom_description",
                    "effective_label",
                    "effective_description",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("template", "section")


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


@admin.register(TASConversionSession)
class TASConversionSessionAdmin(admin.ModelAdmin):
    list_display = [
        "session_name",
        "source_tas",
        "tenant",
        "status",
        "progress_percentage",
        "quality_score",
        "created_at",
        "completed_at",
    ]
    list_filter = ["status", "tenant", "ai_model", "requires_human_review", "created_at"]
    search_fields = ["session_name", "source_tas__code", "source_tas__title"]
    readonly_fields = [
        "created_by",
        "created_at",
        "started_at",
        "completed_at",
        "updated_at",
        "processing_time_seconds",
        "reviewed_by",
        "reviewed_at",
    ]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Session Information",
            {
                "fields": (
                    "tenant",
                    "session_name",
                    "source_tas",
                    "target_tas",
                    "status",
                    "current_step",
                    "progress_percentage",
                )
            },
        ),
        (
            "AI Configuration",
            {"fields": ("ai_model", "conversion_options")},
        ),
        (
            "Conversion Results",
            {
                "fields": (
                    "standards_mapping",
                    "source_analysis",
                    "conversion_changes",
                    "compliance_report",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Quality Metrics",
            {
                "fields": (
                    "sections_converted",
                    "standards_updated",
                    "quality_score",
                    "requires_human_review",
                )
            },
        ),
        (
            "Performance",
            {
                "fields": (
                    "processing_time_seconds",
                    "ai_tokens_used",
                    "ai_cost_estimate",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Error Handling",
            {
                "fields": ("error_message", "error_details"),
                "classes": ("collapse",),
            },
        ),
        (
            "Review",
            {
                "fields": ("review_notes", "reviewed_by", "reviewed_at"),
                "classes": ("collapse",),
            },
        ),
        (
            "Audit",
            {
                "fields": ("created_by", "created_at", "started_at", "completed_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
