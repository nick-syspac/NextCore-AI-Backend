from django.contrib import admin
from .models import (
    PDActivity,
    TrainerProfile,
    PDSuggestion,
    ComplianceRule,
    ComplianceCheck,
)


@admin.register(PDActivity)
class PDActivityAdmin(admin.ModelAdmin):
    list_display = [
        "activity_number",
        "trainer_name",
        "activity_title",
        "activity_type",
        "start_date",
        "hours_completed",
        "status",
        "verification_status",
    ]
    list_filter = [
        "activity_type",
        "status",
        "verification_status",
        "maintains_vocational_currency",
        "maintains_industry_currency",
        "start_date",
    ]
    search_fields = [
        "activity_number",
        "trainer_name",
        "trainer_id",
        "activity_title",
        "description",
    ]
    readonly_fields = ["activity_number", "created_at", "updated_at"]

    fieldsets = (
        (
            "Activity Information",
            {
                "fields": (
                    "activity_number",
                    "tenant",
                    "trainer_id",
                    "trainer_name",
                    "trainer_role",
                    "department",
                )
            },
        ),
        (
            "Activity Details",
            {
                "fields": (
                    "activity_type",
                    "activity_title",
                    "description",
                    "provider",
                    "start_date",
                    "end_date",
                    "hours_completed",
                )
            },
        ),
        (
            "Compliance & Currency",
            {
                "fields": (
                    "compliance_areas",
                    "industry_sectors",
                    "qualification_levels",
                    "maintains_vocational_currency",
                    "maintains_industry_currency",
                    "maintains_teaching_currency",
                    "meets_asqa_requirements",
                    "compliance_notes",
                )
            },
        ),
        (
            "Evidence & Verification",
            {
                "fields": (
                    "evidence_type",
                    "evidence_files",
                    "verification_status",
                    "verified_by",
                    "verified_date",
                )
            },
        ),
        (
            "Outcomes & Reflection",
            {
                "fields": (
                    "learning_outcomes",
                    "application_to_practice",
                    "reflection_notes",
                )
            },
        ),
        ("Status", {"fields": ("status", "created_at", "updated_at")}),
    )


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = [
        "profile_number",
        "trainer_name",
        "role",
        "total_pd_hours",
        "vocational_currency_status",
        "industry_currency_status",
        "meets_asqa_requirements",
    ]
    list_filter = [
        "vocational_currency_status",
        "industry_currency_status",
        "meets_asqa_requirements",
        "vocational_currency_required",
    ]
    search_fields = ["profile_number", "trainer_name", "trainer_id", "email"]
    readonly_fields = ["profile_number", "created_at", "updated_at"]

    fieldsets = (
        (
            "Profile Information",
            {
                "fields": (
                    "profile_number",
                    "tenant",
                    "trainer_id",
                    "trainer_name",
                    "email",
                    "role",
                    "department",
                    "employment_start_date",
                )
            },
        ),
        (
            "Qualifications",
            {
                "fields": (
                    "highest_qualification",
                    "teaching_qualifications",
                    "industry_qualifications",
                )
            },
        ),
        (
            "Teaching Areas",
            {
                "fields": (
                    "teaching_subjects",
                    "teaching_qualification_levels",
                    "industry_sectors",
                )
            },
        ),
        (
            "Currency Requirements",
            {
                "fields": (
                    "vocational_currency_required",
                    "industry_currency_required",
                    "teaching_currency_required",
                )
            },
        ),
        (
            "Currency Tracking",
            {
                "fields": (
                    "total_pd_hours",
                    "vocational_pd_hours",
                    "industry_pd_hours",
                    "teaching_pd_hours",
                    "last_vocational_pd",
                    "last_industry_pd",
                    "last_teaching_pd",
                )
            },
        ),
        (
            "Currency Status",
            {"fields": ("vocational_currency_status", "industry_currency_status")},
        ),
        (
            "Compliance",
            {
                "fields": (
                    "meets_asqa_requirements",
                    "last_compliance_check",
                    "compliance_issues",
                )
            },
        ),
        (
            "Goals & Planning",
            {"fields": ("annual_pd_goal_hours", "current_year_hours", "pd_goals")},
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(PDSuggestion)
class PDSuggestionAdmin(admin.ModelAdmin):
    list_display = [
        "suggestion_number",
        "trainer_profile",
        "activity_title",
        "addresses_currency_gap",
        "priority_level",
        "status",
        "generation_date",
    ]
    list_filter = [
        "priority_level",
        "status",
        "addresses_currency_gap",
        "suggested_activity_type",
        "generation_date",
    ]
    search_fields = [
        "suggestion_number",
        "activity_title",
        "description",
        "trainer_profile__trainer_name",
    ]
    readonly_fields = ["suggestion_number", "generation_date", "created_at"]

    fieldsets = (
        (
            "Suggestion Information",
            {
                "fields": (
                    "suggestion_number",
                    "trainer_profile",
                    "suggested_activity_type",
                    "activity_title",
                    "description",
                    "rationale",
                )
            },
        ),
        (
            "Recommendation Context",
            {
                "fields": (
                    "addresses_currency_gap",
                    "priority_level",
                    "suggested_providers",
                    "estimated_hours",
                    "estimated_cost",
                )
            },
        ),
        ("Timeline", {"fields": ("suggested_timeframe", "deadline")}),
        (
            "LLM Metadata",
            {
                "fields": (
                    "generated_by_model",
                    "generation_date",
                    "prompt_used",
                    "confidence_score",
                )
            },
        ),
        (
            "Action Tracking",
            {"fields": ("status", "trainer_feedback", "linked_activity", "created_at")},
        ),
    )


@admin.register(ComplianceRule)
class ComplianceRuleAdmin(admin.ModelAdmin):
    list_display = [
        "rule_number",
        "rule_name",
        "regulatory_source",
        "reference_code",
        "requirement_type",
        "is_active",
        "effective_date",
    ]
    list_filter = [
        "regulatory_source",
        "requirement_type",
        "is_active",
        "effective_date",
    ]
    search_fields = ["rule_number", "rule_name", "reference_code", "description"]
    readonly_fields = ["rule_number", "created_at", "updated_at"]

    fieldsets = (
        (
            "Rule Metadata",
            {
                "fields": (
                    "rule_number",
                    "tenant",
                    "rule_name",
                    "description",
                    "regulatory_source",
                    "reference_code",
                )
            },
        ),
        (
            "Applicability",
            {
                "fields": (
                    "applies_to_roles",
                    "applies_to_sectors",
                    "applies_to_qualifications",
                )
            },
        ),
        ("Requirements", {"fields": ("requirement_type", "requirement_details")}),
        ("Validation", {"fields": ("is_active", "effective_date", "expiry_date")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(ComplianceCheck)
class ComplianceCheckAdmin(admin.ModelAdmin):
    list_display = [
        "check_number",
        "trainer_profile",
        "check_date",
        "overall_status",
        "compliance_score",
        "hours_completed",
        "hours_shortfall",
        "requires_action",
    ]
    list_filter = ["overall_status", "requires_action", "check_date"]
    search_fields = ["check_number", "trainer_profile__trainer_name", "checked_by"]
    readonly_fields = ["check_number", "created_at"]

    fieldsets = (
        (
            "Check Information",
            {
                "fields": (
                    "check_number",
                    "trainer_profile",
                    "check_date",
                    "check_period_start",
                    "check_period_end",
                    "checked_by",
                )
            },
        ),
        (
            "Results",
            {
                "fields": (
                    "overall_status",
                    "rules_checked",
                    "rules_met",
                    "rules_not_met",
                )
            },
        ),
        (
            "Findings",
            {
                "fields": (
                    "compliance_score",
                    "hours_required",
                    "hours_completed",
                    "hours_shortfall",
                    "findings",
                    "recommendations",
                )
            },
        ),
        (
            "Follow-up",
            {"fields": ("requires_action", "action_deadline", "actions_taken")},
        ),
        ("Timestamp", {"fields": ("created_at",)}),
    )
