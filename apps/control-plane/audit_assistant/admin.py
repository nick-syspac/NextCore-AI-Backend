from django.contrib import admin
from .models import Evidence, ClauseEvidence, AuditReport, AuditReportClause


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = [
        "evidence_number",
        "title",
        "evidence_type",
        "status",
        "uploaded_at",
        "uploaded_by",
    ]
    list_filter = ["status", "evidence_type", "uploaded_at", "evidence_date"]
    search_fields = ["evidence_number", "title", "description", "extracted_text"]
    readonly_fields = ["uploaded_at", "ner_processed_at", "reviewed_at", "file_size"]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": [
                    "tenant",
                    "evidence_number",
                    "title",
                    "description",
                    "evidence_type",
                    "tags",
                ]
            },
        ),
        ("File Upload", {"fields": ["file", "file_size", "extracted_text"]}),
        (
            "NER Processing",
            {"fields": ["ner_entities", "ner_processed_at"], "classes": ["collapse"]},
        ),
        (
            "Status & Review",
            {
                "fields": [
                    "status",
                    "uploaded_by",
                    "uploaded_at",
                    "reviewed_by",
                    "reviewed_at",
                    "reviewer_notes",
                ]
            },
        ),
        ("Dates", {"fields": ["evidence_date"]}),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return self.readonly_fields + ["uploaded_by", "evidence_number"]
        return self.readonly_fields


@admin.register(ClauseEvidence)
class ClauseEvidenceAdmin(admin.ModelAdmin):
    list_display = [
        "asqa_clause",
        "evidence",
        "mapping_type",
        "confidence_score",
        "is_verified",
        "created_at",
    ]
    list_filter = ["mapping_type", "is_verified", "created_at"]
    search_fields = [
        "asqa_clause__clause_number",
        "evidence__evidence_number",
        "rule_name",
    ]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = [
        ("Mapping", {"fields": ["asqa_clause", "evidence"]}),
        (
            "Auto-Tagging Metadata",
            {
                "fields": [
                    "mapping_type",
                    "confidence_score",
                    "matched_entities",
                    "matched_keywords",
                    "rule_name",
                    "rule_metadata",
                ]
            },
        ),
        (
            "Verification",
            {
                "fields": [
                    "is_verified",
                    "verified_by",
                    "verified_at",
                    "relevance_notes",
                ]
            },
        ),
        (
            "Timestamps",
            {"fields": ["created_at", "updated_at"], "classes": ["collapse"]},
        ),
    ]


@admin.register(AuditReport)
class AuditReportAdmin(admin.ModelAdmin):
    list_display = [
        "report_number",
        "title",
        "status",
        "compliance_percentage",
        "total_clauses",
        "created_at",
    ]
    list_filter = ["status", "created_at", "audit_period_start"]
    search_fields = ["report_number", "title", "description"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "completed_at",
        "submitted_at",
        "total_clauses",
        "clauses_with_evidence",
        "clauses_without_evidence",
        "compliance_percentage",
        "critical_clauses_count",
        "critical_clauses_covered",
        "critical_compliance_percentage",
        "total_evidence_count",
        "auto_tagged_count",
        "manually_tagged_count",
        "verified_evidence_count",
    ]
    filter_horizontal = ["asqa_standards"]

    fieldsets = [
        (
            "Basic Information",
            {"fields": ["tenant", "report_number", "title", "description"]},
        ),
        (
            "Audit Scope",
            {"fields": ["asqa_standards", "audit_period_start", "audit_period_end"]},
        ),
        ("Status", {"fields": ["status"]}),
        (
            "Compliance Metrics",
            {
                "fields": [
                    "total_clauses",
                    "clauses_with_evidence",
                    "clauses_without_evidence",
                    "compliance_percentage",
                    "critical_clauses_count",
                    "critical_clauses_covered",
                    "critical_compliance_percentage",
                ],
                "classes": ["collapse"],
            },
        ),
        (
            "Evidence Summary",
            {
                "fields": [
                    "total_evidence_count",
                    "auto_tagged_count",
                    "manually_tagged_count",
                    "verified_evidence_count",
                ],
                "classes": ["collapse"],
            },
        ),
        ("Findings & Recommendations", {"fields": ["findings", "recommendations"]}),
        (
            "Timestamps",
            {
                "fields": [
                    "created_at",
                    "created_by",
                    "updated_at",
                    "completed_at",
                    "submitted_at",
                    "submitted_by",
                ],
                "classes": ["collapse"],
            },
        ),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return self.readonly_fields + ["created_by", "report_number"]
        return self.readonly_fields


@admin.register(AuditReportClause)
class AuditReportClauseAdmin(admin.ModelAdmin):
    list_display = [
        "audit_report",
        "asqa_clause",
        "compliance_status",
        "evidence_count",
        "severity",
    ]
    list_filter = ["compliance_status", "severity", "created_at"]
    search_fields = ["asqa_clause__clause_number", "finding", "recommendation"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "evidence_count",
        "verified_evidence_count",
    ]
    filter_horizontal = ["linked_evidence"]

    fieldsets = [
        ("Audit Report & Clause", {"fields": ["audit_report", "asqa_clause"]}),
        (
            "Compliance Assessment",
            {
                "fields": [
                    "compliance_status",
                    "evidence_count",
                    "verified_evidence_count",
                ]
            },
        ),
        ("Findings", {"fields": ["finding", "severity", "recommendation"]}),
        ("Evidence", {"fields": ["linked_evidence"]}),
        (
            "Assessment Metadata",
            {
                "fields": ["assessed_by", "assessed_at", "notes"],
                "classes": ["collapse"],
            },
        ),
        (
            "Timestamps",
            {"fields": ["created_at", "updated_at"], "classes": ["collapse"]},
        ),
    ]
