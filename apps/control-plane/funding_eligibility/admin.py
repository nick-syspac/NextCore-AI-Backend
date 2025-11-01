from django.contrib import admin
from .models import (
    JurisdictionRequirement,
    EligibilityRule,
    EligibilityCheck,
    EligibilityCheckLog,
)


@admin.register(JurisdictionRequirement)
class JurisdictionRequirementAdmin(admin.ModelAdmin):
    list_display = [
        "jurisdiction",
        "name",
        "code",
        "funding_percentage",
        "is_active",
        "effective_from",
        "effective_to",
    ]
    list_filter = ["jurisdiction", "is_active", "effective_from"]
    search_fields = ["name", "code"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Program Details",
            {"fields": ("tenant", "jurisdiction", "name", "code", "is_active")},
        ),
        (
            "Residency Requirements",
            {
                "fields": (
                    "requires_australian_citizen",
                    "requires_permanent_resident",
                    "requires_jurisdiction_resident",
                    "min_jurisdiction_residency_months",
                )
            },
        ),
        ("Age Requirements", {"fields": ("min_age", "max_age")}),
        (
            "Education Requirements",
            {"fields": ("requires_year_12", "allows_year_10_completion")},
        ),
        (
            "Employment Requirements",
            {
                "fields": (
                    "requires_unemployed",
                    "allows_employed",
                    "requires_apprentice_trainee",
                )
            },
        ),
        (
            "Prior Qualification Restrictions",
            {
                "fields": (
                    "restricts_higher_qualifications",
                    "max_aqf_level",
                )
            },
        ),
        (
            "Income Requirements",
            {"fields": ("has_income_threshold", "max_annual_income")},
        ),
        (
            "Special Categories",
            {
                "fields": (
                    "allows_concession_card",
                    "allows_disability",
                    "allows_indigenous",
                    "priority_indigenous",
                )
            },
        ),
        ("Funding Details", {"fields": ("funding_percentage", "student_contribution")}),
        ("API Integration", {"fields": ("api_endpoint", "api_key_required")}),
        (
            "Additional Rules",
            {"fields": ("additional_rules",), "classes": ("collapse",)},
        ),
        ("Validity Period", {"fields": ("effective_from", "effective_to")}),
        (
            "Audit Information",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(EligibilityRule)
class EligibilityRuleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "rule_type",
        "jurisdiction_requirement",
        "is_mandatory",
        "priority",
        "is_active",
    ]
    list_filter = ["rule_type", "is_mandatory", "is_active", "operator"]
    search_fields = ["name", "description"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Rule Details",
            {
                "fields": (
                    "tenant",
                    "jurisdiction_requirement",
                    "rule_type",
                    "name",
                    "description",
                    "is_active",
                )
            },
        ),
        (
            "Rule Logic",
            {
                "fields": (
                    "field_name",
                    "operator",
                    "expected_value",
                )
            },
        ),
        (
            "Rule Behavior",
            {
                "fields": (
                    "is_mandatory",
                    "priority",
                    "error_message",
                    "override_allowed",
                )
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


class EligibilityCheckLogInline(admin.TabularInline):
    model = EligibilityCheckLog
    extra = 0
    readonly_fields = ["action", "details", "notes", "performed_by", "performed_at"]
    can_delete = False


@admin.register(EligibilityCheck)
class EligibilityCheckAdmin(admin.ModelAdmin):
    list_display = [
        "check_number",
        "student_name",
        "course_code",
        "jurisdiction",
        "status",
        "is_eligible",
        "eligibility_percentage",
        "checked_at",
    ]
    list_filter = [
        "status",
        "jurisdiction",
        "is_eligible",
        "override_approved",
        "prevents_enrollment",
    ]
    search_fields = [
        "check_number",
        "student_first_name",
        "student_last_name",
        "student_email",
        "course_code",
        "course_name",
    ]
    readonly_fields = [
        "check_number",
        "checked_at",
        "updated_at",
        "api_verified_at",
        "override_approved_at",
    ]
    inlines = [EligibilityCheckLogInline]

    fieldsets = (
        ("Check Details", {"fields": ("tenant", "check_number", "status")}),
        (
            "Student Information",
            {
                "fields": (
                    "student_first_name",
                    "student_last_name",
                    "student_dob",
                    "student_email",
                    "student_phone",
                )
            },
        ),
        (
            "Enrollment Details",
            {
                "fields": (
                    "course_code",
                    "course_name",
                    "aqf_level",
                    "intended_start_date",
                )
            },
        ),
        (
            "Jurisdiction & Funding",
            {
                "fields": (
                    "jurisdiction",
                    "jurisdiction_requirement",
                    "funding_program_code",
                )
            },
        ),
        (
            "Student Eligibility Data",
            {"fields": ("student_data",), "classes": ("collapse",)},
        ),
        (
            "Check Results",
            {
                "fields": (
                    "is_eligible",
                    "eligibility_percentage",
                    "rules_checked",
                    "rules_passed",
                    "rules_failed",
                )
            },
        ),
        (
            "Detailed Results",
            {
                "fields": (
                    "check_results",
                    "failed_rules",
                    "warnings",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "API Verification",
            {
                "fields": (
                    "api_verified",
                    "api_response",
                    "api_verified_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Override Handling",
            {
                "fields": (
                    "override_required",
                    "override_approved",
                    "override_reason",
                    "override_approved_by",
                    "override_approved_at",
                )
            },
        ),
        (
            "Compliance",
            {
                "fields": (
                    "prevents_enrollment",
                    "compliance_notes",
                )
            },
        ),
        ("Validity Period", {"fields": ("valid_from", "valid_until")}),
        (
            "Audit Information",
            {
                "fields": ("checked_by", "checked_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def student_name(self, obj):
        return f"{obj.student_first_name} {obj.student_last_name}"

    student_name.short_description = "Student"


@admin.register(EligibilityCheckLog)
class EligibilityCheckLogAdmin(admin.ModelAdmin):
    list_display = ["eligibility_check", "action", "performed_by", "performed_at"]
    list_filter = ["action", "performed_at"]
    search_fields = ["eligibility_check__check_number", "notes"]
    readonly_fields = ["performed_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
