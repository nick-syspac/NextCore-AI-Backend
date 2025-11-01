from django.contrib import admin
from .models import (
    TrainerQualification,
    UnitOfCompetency,
    TrainerAssignment,
    CompetencyGap,
    QualificationMapping,
    ComplianceCheck,
)


@admin.register(TrainerQualification)
class TrainerQualificationAdmin(admin.ModelAdmin):
    list_display = [
        "qualification_id",
        "trainer_name",
        "qualification_code",
        "qualification_type",
        "verification_status",
        "date_obtained",
        "expiry_date",
    ]
    list_filter = ["verification_status", "qualification_type", "recent_industry_work"]
    search_fields = [
        "trainer_name",
        "trainer_id",
        "qualification_code",
        "qualification_name",
    ]
    readonly_fields = ["qualification_id", "created_at", "updated_at"]

    fieldsets = (
        (
            "Trainer Information",
            {"fields": ("qualification_id", "tenant", "trainer_id", "trainer_name")},
        ),
        (
            "Qualification Details",
            {
                "fields": (
                    "qualification_type",
                    "qualification_code",
                    "qualification_name",
                    "issuing_organization",
                )
            },
        ),
        (
            "Verification",
            {
                "fields": (
                    "date_obtained",
                    "expiry_date",
                    "verification_status",
                    "verification_document",
                )
            },
        ),
        ("Competencies", {"fields": ("competency_areas", "units_covered")}),
        (
            "Industry Currency",
            {"fields": ("industry_experience_years", "recent_industry_work")},
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(UnitOfCompetency)
class UnitOfCompetencyAdmin(admin.ModelAdmin):
    list_display = [
        "unit_id",
        "unit_code",
        "unit_name",
        "unit_type",
        "qualification_code",
        "requires_tae",
        "requires_industry_currency",
    ]
    list_filter = ["unit_type", "requires_tae", "requires_industry_currency"]
    search_fields = ["unit_code", "unit_name", "qualification_code"]
    readonly_fields = ["unit_id", "created_at", "updated_at"]

    fieldsets = (
        (
            "Unit Information",
            {
                "fields": (
                    "unit_id",
                    "tenant",
                    "unit_code",
                    "unit_name",
                    "unit_type",
                    "qualification_code",
                )
            },
        ),
        (
            "Requirements",
            {
                "fields": (
                    "required_qualifications",
                    "required_competency_areas",
                    "required_industry_experience",
                    "requires_tae",
                    "requires_industry_currency",
                )
            },
        ),
        (
            "Content",
            {"fields": ("learning_outcomes", "assessment_methods", "technical_skills")},
        ),
        ("Graph Relationships", {"fields": ("prerequisite_units", "related_units")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(TrainerAssignment)
class TrainerAssignmentAdmin(admin.ModelAdmin):
    list_display = [
        "assignment_id",
        "trainer_name",
        "unit",
        "assignment_status",
        "meets_requirements",
        "compliance_score",
        "assigned_date",
    ]
    list_filter = ["assignment_status", "meets_requirements"]
    search_fields = ["trainer_name", "trainer_id", "assignment_id"]
    readonly_fields = ["assignment_id", "created_at", "updated_at"]

    fieldsets = (
        (
            "Assignment Information",
            {
                "fields": (
                    "assignment_id",
                    "tenant",
                    "trainer_id",
                    "trainer_name",
                    "unit",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "assignment_status",
                    "assigned_date",
                    "approved_by",
                    "approved_date",
                )
            },
        ),
        (
            "Compliance",
            {
                "fields": (
                    "meets_requirements",
                    "compliance_score",
                    "gaps_identified",
                    "matching_qualifications",
                )
            },
        ),
        ("Notes", {"fields": ("assignment_notes", "rejection_reason")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(CompetencyGap)
class CompetencyGapAdmin(admin.ModelAdmin):
    list_display = [
        "gap_id",
        "trainer_name",
        "unit",
        "gap_type",
        "gap_severity",
        "is_resolved",
        "created_at",
    ]
    list_filter = ["gap_type", "gap_severity", "is_resolved"]
    search_fields = ["trainer_name", "trainer_id", "gap_description"]
    readonly_fields = ["gap_id", "created_at", "updated_at"]

    fieldsets = (
        (
            "Gap Information",
            {
                "fields": (
                    "gap_id",
                    "tenant",
                    "trainer_id",
                    "trainer_name",
                    "unit",
                    "assignment",
                )
            },
        ),
        ("Gap Details", {"fields": ("gap_type", "gap_severity", "gap_description")}),
        (
            "Requirements",
            {
                "fields": (
                    "required_qualification",
                    "required_competency",
                    "required_experience_years",
                    "current_qualifications",
                )
            },
        ),
        (
            "Resolution",
            {"fields": ("is_resolved", "resolution_date", "resolution_notes")},
        ),
        (
            "Recommendations",
            {"fields": ("recommended_action", "estimated_resolution_time")},
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(QualificationMapping)
class QualificationMappingAdmin(admin.ModelAdmin):
    list_display = [
        "mapping_id",
        "source_qualification_code",
        "match_strength",
        "match_confidence",
        "verified",
        "mapping_source",
    ]
    list_filter = ["verified", "mapping_source"]
    search_fields = ["source_qualification_code", "source_qualification_name"]
    readonly_fields = ["mapping_id", "created_at", "updated_at"]

    fieldsets = (
        (
            "Mapping Information",
            {
                "fields": (
                    "mapping_id",
                    "tenant",
                    "source_qualification_code",
                    "source_qualification_name",
                )
            },
        ),
        (
            "Target Competencies",
            {"fields": ("competency_areas", "match_strength", "match_confidence")},
        ),
        (
            "Equivalency",
            {"fields": ("equivalent_qualifications", "superseded_by", "supersedes")},
        ),
        ("Units Coverage", {"fields": ("units_covered", "units_partially_covered")}),
        (
            "Metadata",
            {"fields": ("mapping_source", "verified", "created_at", "updated_at")},
        ),
    )


@admin.register(ComplianceCheck)
class ComplianceCheckAdmin(admin.ModelAdmin):
    list_display = [
        "check_id",
        "check_type",
        "check_status",
        "total_assignments_checked",
        "overall_compliance_score",
        "gaps_found",
        "created_at",
    ]
    list_filter = ["check_status", "check_type"]
    search_fields = ["check_id"]
    readonly_fields = ["check_id", "created_at", "updated_at"]

    fieldsets = (
        (
            "Check Information",
            {"fields": ("check_id", "tenant", "check_type", "check_status")},
        ),
        ("Scope", {"fields": ("trainer_ids", "unit_codes")}),
        (
            "Results Summary",
            {
                "fields": (
                    "total_assignments_checked",
                    "compliant_assignments",
                    "non_compliant_assignments",
                    "gaps_found",
                )
            },
        ),
        (
            "Severity Breakdown",
            {"fields": ("critical_gaps", "high_gaps", "medium_gaps", "low_gaps")},
        ),
        ("Compliance", {"fields": ("overall_compliance_score",)}),
        (
            "Report",
            {"fields": ("report_summary", "detailed_results", "recommendations")},
        ),
        (
            "Execution",
            {
                "fields": (
                    "started_at",
                    "completed_at",
                    "execution_time_seconds",
                    "error_message",
                )
            },
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
