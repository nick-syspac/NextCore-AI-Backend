from django.contrib import admin
from .models import (
    EvidenceMapping,
    SubmissionEvidence,
    CriteriaTag,
    EvidenceAudit,
    EmbeddingSearch,
)


@admin.register(EvidenceMapping)
class EvidenceMappingAdmin(admin.ModelAdmin):
    list_display = (
        "mapping_number",
        "name",
        "assessment_type",
        "status",
        "total_evidence_tagged",
        "coverage_percentage",
        "created_at",
    )
    list_filter = ("status", "assessment_type", "created_at")
    search_fields = ("mapping_number", "name", "assessment_title", "unit_code")
    readonly_fields = (
        "mapping_number",
        "created_at",
        "updated_at",
        "total_evidence_tagged",
        "total_text_extracted",
        "embeddings_generated",
        "coverage_percentage",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "mapping_number",
                    "name",
                    "description",
                    "assessment_type",
                    "status",
                )
            },
        ),
        (
            "Assessment Details",
            {
                "fields": (
                    "assessment_title",
                    "unit_code",
                    "total_criteria",
                    "total_submissions",
                )
            },
        ),
        (
            "Configuration",
            {
                "fields": (
                    "auto_extract_text",
                    "generate_embeddings",
                    "require_evidence_per_criterion",
                    "min_evidence_length",
                ),
                "description": "Configure automatic processing and validation rules",
            },
        ),
        (
            "Statistics",
            {
                "fields": (
                    "total_evidence_tagged",
                    "total_text_extracted",
                    "embeddings_generated",
                    "coverage_percentage",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Audit Information",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(SubmissionEvidence)
class SubmissionEvidenceAdmin(admin.ModelAdmin):
    list_display = (
        "evidence_number",
        "mapping",
        "student_id",
        "submission_type",
        "extraction_status",
        "text_length",
        "total_tags",
        "submitted_at",
    )
    list_filter = ("extraction_status", "submission_type", "submitted_at")
    search_fields = ("evidence_number", "student_id", "student_name", "submission_id")
    readonly_fields = (
        "evidence_number",
        "created_at",
        "text_length",
        "total_tags",
        "extracted_at",
    )

    fieldsets = (
        ("Evidence Information", {"fields": ("evidence_number", "mapping")}),
        (
            "Student Details",
            {"fields": ("student_id", "student_name", "submission_id")},
        ),
        (
            "Submission Details",
            {
                "fields": (
                    "submission_title",
                    "submission_type",
                    "file_path",
                    "file_size_bytes",
                    "submitted_at",
                )
            },
        ),
        (
            "Extracted Content",
            {
                "fields": (
                    "extracted_text",
                    "text_length",
                    "extraction_status",
                    "extraction_method",
                    "extracted_at",
                )
            },
        ),
        (
            "Embeddings",
            {
                "fields": ("embedding_model", "embedding_dimension"),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata & Statistics",
            {
                "fields": ("metadata", "total_tags", "criteria_covered"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(CriteriaTag)
class CriteriaTagAdmin(admin.ModelAdmin):
    list_display = (
        "tag_number",
        "evidence",
        "criterion_id",
        "tag_type",
        "confidence_level",
        "is_validated",
        "tagged_at",
    )
    list_filter = ("tag_type", "confidence_level", "is_validated", "tagged_at")
    search_fields = ("tag_number", "criterion_id", "criterion_name", "tagged_text")
    readonly_fields = ("tag_number", "tagged_at")

    fieldsets = (
        (
            "Tag Information",
            {
                "fields": (
                    "tag_number",
                    "evidence",
                    "tag_type",
                    "confidence_level",
                    "confidence_score",
                )
            },
        ),
        (
            "Criteria Linkage",
            {"fields": ("criterion_id", "criterion_name", "criterion_description")},
        ),
        (
            "Tagged Text",
            {"fields": ("tagged_text", "text_start_position", "text_end_position")},
        ),
        (
            "Context",
            {"fields": ("context_before", "context_after"), "classes": ("collapse",)},
        ),
        ("Annotations", {"fields": ("notes", "keywords"), "classes": ("collapse",)}),
        (
            "Validation",
            {
                "fields": ("is_validated", "validated_by", "validated_at"),
                "classes": ("collapse",),
            },
        ),
        ("Audit", {"fields": ("tagged_by", "tagged_at"), "classes": ("collapse",)}),
    )


@admin.register(EvidenceAudit)
class EvidenceAuditAdmin(admin.ModelAdmin):
    list_display = (
        "mapping",
        "action",
        "submission_id",
        "criterion_id",
        "performed_by",
        "processing_time_ms",
        "timestamp",
    )
    list_filter = ("action", "timestamp")
    search_fields = (
        "mapping__mapping_number",
        "submission_id",
        "criterion_id",
        "performed_by",
    )
    readonly_fields = ("timestamp",)

    fieldsets = (
        (
            "Audit Information",
            {
                "fields": (
                    "mapping",
                    "action",
                    "description",
                    "performed_by",
                    "user_role",
                )
            },
        ),
        ("Related Objects", {"fields": ("submission_id", "criterion_id", "tag_id")}),
        (
            "Action Details",
            {"fields": ("action_data", "changes_made", "processing_time_ms")},
        ),
        ("Context", {"fields": ("ip_address", "user_agent"), "classes": ("collapse",)}),
        ("Timestamp", {"fields": ("timestamp",)}),
    )


@admin.register(EmbeddingSearch)
class EmbeddingSearchAdmin(admin.ModelAdmin):
    list_display = (
        "search_number",
        "mapping",
        "search_type",
        "results_count",
        "search_time_ms",
        "performed_by",
        "timestamp",
    )
    list_filter = ("search_type", "timestamp")
    search_fields = ("search_number", "query_text", "performed_by")
    readonly_fields = ("search_number", "timestamp")

    fieldsets = (
        (
            "Search Information",
            {"fields": ("search_number", "mapping", "search_type", "performed_by")},
        ),
        ("Query", {"fields": ("query_text",)}),
        ("Filters", {"fields": ("filter_criteria",), "classes": ("collapse",)}),
        ("Results", {"fields": ("results_count", "top_results", "search_time_ms")}),
    )
