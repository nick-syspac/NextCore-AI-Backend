from rest_framework import serializers
from .models import Evidence, ClauseEvidence, AuditReport, AuditReportClause
from policy_comparator.models import ASQAClause, ASQAStandard


class EvidenceSerializer(serializers.ModelSerializer):
    """Serializer for evidence documents"""

    uploaded_by_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    tagged_clauses_count = serializers.SerializerMethodField()
    auto_tagged_count = serializers.SerializerMethodField()

    class Meta:
        model = Evidence
        fields = [
            "id",
            "evidence_number",
            "title",
            "description",
            "evidence_type",
            "file",
            "file_url",
            "file_name",
            "file_size",
            "extracted_text",
            "ner_entities",
            "ner_processed_at",
            "status",
            "tags",
            "evidence_date",
            "uploaded_at",
            "uploaded_by",
            "uploaded_by_name",
            "reviewed_at",
            "reviewed_by",
            "reviewed_by_name",
            "reviewer_notes",
            "tagged_clauses_count",
            "auto_tagged_count",
        ]
        read_only_fields = [
            "uploaded_at",
            "ner_processed_at",
            "file_size",
            "extracted_text",
        ]

    def get_uploaded_by_name(self, obj):
        return obj.uploaded_by.get_full_name() if obj.uploaded_by else None

    def get_reviewed_by_name(self, obj):
        return obj.reviewed_by.get_full_name() if obj.reviewed_by else None

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None

    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.split("/")[-1]
        return None

    def get_tagged_clauses_count(self, obj):
        return obj.auto_tagged_clauses.count()

    def get_auto_tagged_count(self, obj):
        return ClauseEvidence.objects.filter(
            evidence=obj, mapping_type__in=["auto_ner", "auto_rule"]
        ).count()


class ClauseEvidenceSerializer(serializers.ModelSerializer):
    """Serializer for clause-evidence mappings"""

    clause_number = serializers.CharField(
        source="asqa_clause.clause_number", read_only=True
    )
    clause_title = serializers.CharField(source="asqa_clause.title", read_only=True)
    clause_compliance_level = serializers.CharField(
        source="asqa_clause.compliance_level", read_only=True
    )
    evidence_number = serializers.CharField(
        source="evidence.evidence_number", read_only=True
    )
    evidence_title = serializers.CharField(source="evidence.title", read_only=True)
    evidence_type = serializers.CharField(
        source="evidence.evidence_type", read_only=True
    )
    verified_by_name = serializers.SerializerMethodField()
    mapping_type_display = serializers.CharField(
        source="get_mapping_type_display", read_only=True
    )

    class Meta:
        model = ClauseEvidence
        fields = [
            "id",
            "asqa_clause",
            "clause_number",
            "clause_title",
            "clause_compliance_level",
            "evidence",
            "evidence_number",
            "evidence_title",
            "evidence_type",
            "mapping_type",
            "mapping_type_display",
            "confidence_score",
            "matched_entities",
            "matched_keywords",
            "rule_name",
            "rule_metadata",
            "is_verified",
            "verified_by",
            "verified_by_name",
            "verified_at",
            "relevance_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_verified_by_name(self, obj):
        return obj.verified_by.get_full_name() if obj.verified_by else None


class AuditReportClauseSerializer(serializers.ModelSerializer):
    """Serializer for audit report clause entries"""

    clause_number = serializers.CharField(
        source="asqa_clause.clause_number", read_only=True
    )
    clause_title = serializers.CharField(source="asqa_clause.title", read_only=True)
    clause_text = serializers.CharField(
        source="asqa_clause.clause_text", read_only=True
    )
    clause_compliance_level = serializers.CharField(
        source="asqa_clause.compliance_level", read_only=True
    )
    standard_name = serializers.CharField(
        source="asqa_clause.standard.title", read_only=True
    )
    assessed_by_name = serializers.SerializerMethodField()
    evidence_details = serializers.SerializerMethodField()
    compliance_status_display = serializers.CharField(
        source="get_compliance_status_display", read_only=True
    )

    class Meta:
        model = AuditReportClause
        fields = [
            "id",
            "asqa_clause",
            "clause_number",
            "clause_title",
            "clause_text",
            "clause_compliance_level",
            "standard_name",
            "compliance_status",
            "compliance_status_display",
            "evidence_count",
            "verified_evidence_count",
            "evidence_details",
            "finding",
            "severity",
            "recommendation",
            "assessed_by",
            "assessed_by_name",
            "assessed_at",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "evidence_count",
            "verified_evidence_count",
            "created_at",
            "updated_at",
        ]

    def get_assessed_by_name(self, obj):
        return obj.assessed_by.get_full_name() if obj.assessed_by else None

    def get_evidence_details(self, obj):
        evidence = obj.linked_evidence.all()[:5]  # Limit to 5 for performance
        return EvidenceSerializer(evidence, many=True, context=self.context).data


class AuditReportSerializer(serializers.ModelSerializer):
    """Serializer for audit reports"""

    created_by_name = serializers.SerializerMethodField()
    submitted_by_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    standards_count = serializers.SerializerMethodField()
    clause_entries_count = serializers.SerializerMethodField()
    standards_details = serializers.SerializerMethodField()

    class Meta:
        model = AuditReport
        fields = [
            "id",
            "report_number",
            "title",
            "description",
            "asqa_standards",
            "standards_count",
            "standards_details",
            "audit_period_start",
            "audit_period_end",
            "status",
            "status_display",
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
            "findings",
            "recommendations",
            "created_at",
            "created_by",
            "created_by_name",
            "updated_at",
            "completed_at",
            "submitted_at",
            "submitted_by",
            "submitted_by_name",
            "clause_entries_count",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
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

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def get_submitted_by_name(self, obj):
        return obj.submitted_by.get_full_name() if obj.submitted_by else None

    def get_standards_count(self, obj):
        return obj.asqa_standards.count()

    def get_clause_entries_count(self, obj):
        return obj.clause_entries.count()

    def get_standards_details(self, obj):
        standards = obj.asqa_standards.all()
        return [
            {
                "id": s.id,
                "standard_number": s.standard_number,
                "title": s.title,
                "standard_type": s.standard_type,
            }
            for s in standards
        ]


class AuditReportDetailSerializer(AuditReportSerializer):
    """Detailed serializer with clause entries"""

    clause_entries = AuditReportClauseSerializer(many=True, read_only=True)

    class Meta(AuditReportSerializer.Meta):
        fields = AuditReportSerializer.Meta.fields + ["clause_entries"]


class EvidenceUploadSerializer(serializers.Serializer):
    """Serializer for evidence upload with NER processing"""

    evidence_number = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    evidence_type = serializers.ChoiceField(choices=Evidence.EVIDENCE_TYPE_CHOICES)
    file = serializers.FileField()
    evidence_date = serializers.DateField()
    tags = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    auto_tag = serializers.BooleanField(
        default=True, help_text="Enable auto-tagging via NER"
    )


class ClauseEvidenceGapSerializer(serializers.Serializer):
    """Serializer for clause evidence gap analysis"""

    asqa_clause = serializers.PrimaryKeyRelatedField(queryset=ASQAClause.objects.all())
    clause_number = serializers.CharField(
        source="asqa_clause.clause_number", read_only=True
    )
    clause_title = serializers.CharField(source="asqa_clause.title", read_only=True)
    compliance_level = serializers.CharField(
        source="asqa_clause.compliance_level", read_only=True
    )
    evidence_count = serializers.IntegerField(read_only=True)
    verified_evidence_count = serializers.IntegerField(read_only=True)
    has_sufficient_evidence = serializers.BooleanField(read_only=True)
    gap_severity = serializers.CharField(read_only=True)
    recommendations = serializers.ListField(read_only=True)
