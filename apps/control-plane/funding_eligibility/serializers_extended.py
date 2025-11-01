"""
Serializers for extended funding eligibility models.
"""

from rest_framework import serializers
from .models_extended import (
    Jurisdiction,
    Ruleset,
    RulesetArtifact,
    ReferenceTable,
    EligibilityRequest,
    ExternalLookup,
    EligibilityDecision,
    DecisionOverride,
    EvidenceAttachment,
    WebhookEndpoint,
    WebhookDelivery,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    """Minimal user representation"""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
        read_only_fields = fields


class JurisdictionSerializer(serializers.ModelSerializer):
    """Jurisdiction serializer"""

    class Meta:
        model = Jurisdiction
        fields = "__all__"


class RulesetArtifactSerializer(serializers.ModelSerializer):
    """Ruleset artifact serializer"""

    class Meta:
        model = RulesetArtifact
        fields = ["id", "type", "name", "blob", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class RulesetSerializer(serializers.ModelSerializer):
    """Ruleset serializer with artifacts"""

    artifacts = RulesetArtifactSerializer(many=True, read_only=True)
    created_by_details = UserMinimalSerializer(source="created_by", read_only=True)

    class Meta:
        model = Ruleset
        fields = [
            "id",
            "version",
            "jurisdiction_code",
            "status",
            "checksum",
            "description",
            "changelog",
            "artifacts",
            "created_by",
            "created_by_details",
            "created_at",
            "activated_at",
            "retired_at",
        ]
        read_only_fields = [
            "id",
            "checksum",
            "created_at",
            "activated_at",
            "retired_at",
        ]


class RulesetMinimalSerializer(serializers.ModelSerializer):
    """Minimal ruleset representation"""

    class Meta:
        model = Ruleset
        fields = ["id", "version", "jurisdiction_code", "status"]


class ReferenceTableSerializer(serializers.ModelSerializer):
    """Reference table serializer"""

    class Meta:
        model = ReferenceTable
        fields = [
            "id",
            "namespace",
            "version",
            "data",
            "source",
            "checksum",
            "valid_from",
            "valid_until",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "checksum", "created_at", "updated_at"]


class ExternalLookupSerializer(serializers.ModelSerializer):
    """External lookup serializer"""

    class Meta:
        model = ExternalLookup
        fields = [
            "id",
            "request",
            "provider",
            "request_data",
            "response_data",
            "status",
            "error_message",
            "latency_ms",
            "cached_until",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "response_data",
            "status",
            "error_message",
            "latency_ms",
            "cached_until",
            "created_at",
        ]


class EvidenceAttachmentSerializer(serializers.ModelSerializer):
    """Evidence attachment serializer"""

    uploaded_by_details = UserMinimalSerializer(source="uploaded_by", read_only=True)
    verifier_details = UserMinimalSerializer(source="verifier", read_only=True)

    class Meta:
        model = EvidenceAttachment
        fields = [
            "id",
            "request",
            "file_uri",
            "filename",
            "file_size",
            "mime_type",
            "type",
            "verified",
            "verifier",
            "verifier_details",
            "verified_at",
            "verification_notes",
            "uploaded_by",
            "uploaded_by_details",
            "uploaded_at",
        ]
        read_only_fields = [
            "id",
            "file_uri",
            "file_size",
            "uploaded_by",
            "uploaded_at",
        ]


class DecisionOverrideSerializer(serializers.ModelSerializer):
    """Decision override serializer"""

    approver_details = UserMinimalSerializer(source="approver", read_only=True)

    class Meta:
        model = DecisionOverride
        fields = [
            "id",
            "decision",
            "reason_code",
            "justification",
            "final_outcome",
            "approver",
            "approver_details",
            "approved_at",
            "policy_version",
            "evidence_refs",
        ]
        read_only_fields = ["id", "approver", "approved_at"]


class EligibilityDecisionSerializer(serializers.ModelSerializer):
    """Eligibility decision serializer"""

    ruleset_details = RulesetMinimalSerializer(source="ruleset", read_only=True)
    decided_by_user_details = UserMinimalSerializer(
        source="decided_by_user", read_only=True
    )
    overrides = DecisionOverrideSerializer(many=True, read_only=True)

    class Meta:
        model = EligibilityDecision
        fields = [
            "id",
            "request",
            "ruleset",
            "ruleset_details",
            "outcome",
            "reasons",
            "clause_refs",
            "decision_data",
            "explanation",
            "decided_by",
            "decided_by_user",
            "decided_by_user_details",
            "decided_at",
            "overrides",
        ]
        read_only_fields = [
            "id",
            "decided_by",
            "decided_by_user",
            "decided_at",
        ]


class EligibilityRequestSerializer(serializers.ModelSerializer):
    """Eligibility request serializer"""

    requested_by_details = UserMinimalSerializer(source="requested_by", read_only=True)
    external_lookups = ExternalLookupSerializer(many=True, read_only=True)
    decision = EligibilityDecisionSerializer(read_only=True)
    attachments = EvidenceAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = EligibilityRequest
        fields = [
            "id",
            "tenant",
            "person_id",
            "course_id",
            "jurisdiction_code",
            "input",
            "evidence_refs",
            "status",
            "requested_at",
            "evaluated_at",
            "requested_by",
            "requested_by_details",
            "metadata",
            "external_lookups",
            "decision",
            "attachments",
        ]
        read_only_fields = [
            "id",
            "status",
            "requested_at",
            "evaluated_at",
            "requested_by",
        ]


class EligibilityRequestListSerializer(serializers.ModelSerializer):
    """List view for eligibility requests"""

    requested_by_details = UserMinimalSerializer(source="requested_by", read_only=True)
    outcome = serializers.SerializerMethodField()

    class Meta:
        model = EligibilityRequest
        fields = [
            "id",
            "person_id",
            "course_id",
            "jurisdiction_code",
            "status",
            "outcome",
            "requested_at",
            "evaluated_at",
            "requested_by_details",
        ]
        read_only_fields = fields

    def get_outcome(self, obj):
        """Get decision outcome if available"""
        if hasattr(obj, "decision"):
            return obj.decision.outcome
        return None


class WebhookEndpointSerializer(serializers.ModelSerializer):
    """Webhook endpoint serializer"""

    class Meta:
        model = WebhookEndpoint
        fields = [
            "id",
            "tenant",
            "name",
            "target",
            "url",
            "secret",
            "events",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {"secret": {"write_only": True}}


class WebhookDeliverySerializer(serializers.ModelSerializer):
    """Webhook delivery serializer"""

    endpoint_details = WebhookEndpointSerializer(source="endpoint", read_only=True)

    class Meta:
        model = WebhookDelivery
        fields = [
            "id",
            "endpoint",
            "endpoint_details",
            "event_type",
            "payload",
            "status_code",
            "response_body",
            "error_message",
            "attempt_count",
            "last_attempt_at",
            "delivered_at",
            "created_at",
        ]
        read_only_fields = fields


# Request/Response serializers for API actions


class CreateEligibilityRequestSerializer(serializers.Serializer):
    """Serializer for creating eligibility requests"""

    person_id = serializers.CharField(max_length=100)
    course_id = serializers.CharField(max_length=100)
    jurisdiction_code = serializers.CharField(max_length=10)
    input = serializers.JSONField()
    metadata = serializers.JSONField(required=False, default=dict)


class EvaluateRequestSerializer(serializers.Serializer):
    """Serializer for triggering evaluation"""

    force = serializers.BooleanField(default=False)
    ruleset_id = serializers.IntegerField(required=False)


class CreateOverrideSerializer(serializers.Serializer):
    """Serializer for creating decision overrides"""

    decision_id = serializers.IntegerField()
    reason_code = serializers.CharField(max_length=50)
    justification = serializers.CharField()
    final_outcome = serializers.ChoiceField(
        choices=["eligible", "ineligible", "review"]
    )
    policy_version = serializers.CharField(max_length=20)
    evidence_refs = serializers.JSONField(required=False, default=list)


class UploadEvidenceSerializer(serializers.Serializer):
    """Serializer for uploading evidence"""

    request_id = serializers.IntegerField()
    type = serializers.ChoiceField(
        choices=[
            "id",
            "concession",
            "residency",
            "visa",
            "qualification",
            "employment",
            "income",
            "other",
        ]
    )
    file = serializers.FileField()


class ActivateRulesetSerializer(serializers.Serializer):
    """Serializer for activating rulesets"""

    ruleset_id = serializers.IntegerField()
