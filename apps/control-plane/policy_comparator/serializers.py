from rest_framework import serializers
from .models import (
    ASQAStandard,
    ASQAClause,
    Policy,
    ComparisonResult,
    ComparisonSession,
)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ASQAClauseSerializer(serializers.ModelSerializer):
    compliance_level_display = serializers.CharField(
        source="get_compliance_level_display", read_only=True
    )

    class Meta:
        model = ASQAClause
        fields = [
            "id",
            "standard",
            "clause_number",
            "title",
            "clause_text",
            "evidence_required",
            "keywords",
            "compliance_level",
            "compliance_level_display",
            "is_active",
            "created_at",
            "updated_at",
        ]


class ASQAStandardSerializer(serializers.ModelSerializer):
    standard_type_display = serializers.CharField(
        source="get_standard_type_display", read_only=True
    )
    clauses = ASQAClauseSerializer(many=True, read_only=True)
    clause_count = serializers.SerializerMethodField()

    class Meta:
        model = ASQAStandard
        fields = [
            "id",
            "standard_number",
            "title",
            "description",
            "standard_type",
            "standard_type_display",
            "full_text",
            "requirements",
            "is_active",
            "effective_date",
            "version",
            "created_at",
            "updated_at",
            "clauses",
            "clause_count",
        ]

    def get_clause_count(self, obj):
        return obj.clauses.filter(is_active=True).count()


class PolicySerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source="created_by", read_only=True)
    policy_type_display = serializers.CharField(
        source="get_policy_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    # Computed fields
    comparison_count = serializers.SerializerMethodField()
    compliance_status = serializers.SerializerMethodField()

    class Meta:
        model = Policy
        fields = [
            "id",
            "tenant",
            "policy_number",
            "title",
            "description",
            "policy_type",
            "policy_type_display",
            "content",
            "version",
            "status",
            "status_display",
            "effective_date",
            "review_date",
            "last_compared_at",
            "compliance_score",
            "file_path",
            "created_by",
            "created_by_details",
            "created_at",
            "updated_at",
            "comparison_count",
            "compliance_status",
        ]
        read_only_fields = [
            "last_compared_at",
            "compliance_score",
            "created_at",
            "updated_at",
        ]

    def get_comparison_count(self, obj):
        return obj.comparison_results.count()

    def get_compliance_status(self, obj):
        if obj.compliance_score is None:
            return "not_assessed"
        elif obj.compliance_score >= 80:
            return "compliant"
        elif obj.compliance_score >= 60:
            return "needs_improvement"
        else:
            return "non_compliant"


class ComparisonResultSerializer(serializers.ModelSerializer):
    asqa_clause_details = ASQAClauseSerializer(source="asqa_clause", read_only=True)
    policy_details = PolicySerializer(source="policy", read_only=True)
    reviewed_by_details = UserSerializer(source="reviewed_by", read_only=True)
    match_type_display = serializers.CharField(
        source="get_match_type_display", read_only=True
    )

    class Meta:
        model = ComparisonResult
        fields = [
            "id",
            "policy",
            "policy_details",
            "asqa_clause",
            "asqa_clause_details",
            "similarity_score",
            "match_type",
            "match_type_display",
            "matched_text",
            "gap_description",
            "recommendations",
            "nlp_metadata",
            "keywords_matched",
            "keywords_missing",
            "has_sufficient_evidence",
            "evidence_notes",
            "is_compliant",
            "requires_action",
            "comparison_date",
            "reviewed_by",
            "reviewed_by_details",
            "reviewed_at",
        ]
        read_only_fields = ["comparison_date", "match_type"]


class ComparisonSessionSerializer(serializers.ModelSerializer):
    created_by_details = UserSerializer(source="created_by", read_only=True)
    policy_details = PolicySerializer(source="policy", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = ComparisonSession
        fields = [
            "id",
            "tenant",
            "policy",
            "policy_details",
            "session_name",
            "status",
            "status_display",
            "standards_compared",
            "total_clauses_checked",
            "compliant_count",
            "partial_match_count",
            "gap_count",
            "overall_compliance_score",
            "processing_time_seconds",
            "error_message",
            "created_by",
            "created_by_details",
            "created_at",
            "completed_at",
        ]
        read_only_fields = ["status", "created_at", "completed_at"]


class CompareRequestSerializer(serializers.Serializer):
    """Serializer for policy comparison requests"""

    policy_id = serializers.IntegerField()
    standard_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list,
        help_text="Specific ASQA standards to compare against, or all if empty",
    )
    session_name = serializers.CharField(max_length=200, required=False)
    use_nlp = serializers.BooleanField(
        default=True, help_text="Use NLP-based text similarity"
    )


class GapAnalysisSerializer(serializers.Serializer):
    """Serializer for gap analysis results"""

    clause = ASQAClauseSerializer()
    similarity_score = serializers.FloatField()
    gap_severity = serializers.CharField()
    recommendations = serializers.ListField(child=serializers.CharField())
    missing_keywords = serializers.ListField(child=serializers.CharField())
