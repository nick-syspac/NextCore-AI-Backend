from rest_framework import serializers
from .models import (
    Intervention,
    InterventionRule,
    InterventionWorkflow,
    InterventionStep,
    InterventionOutcome,
    AuditLog,
)


class InterventionStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterventionStep
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class InterventionOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterventionOutcome
        fields = "__all__"
        read_only_fields = [
            "outcome_number",
            "improvement_percentage",
            "target_achieved",
            "created_at",
        ]


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"
        read_only_fields = ["log_number", "timestamp"]


class InterventionSerializer(serializers.ModelSerializer):
    workflow_steps = InterventionStepSerializer(many=True, read_only=True)
    outcomes = InterventionOutcomeSerializer(many=True, read_only=True)
    audit_logs = AuditLogSerializer(many=True, read_only=True)

    class Meta:
        model = Intervention
        fields = "__all__"
        read_only_fields = ["intervention_number", "created_at", "updated_at"]


class InterventionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""

    class Meta:
        model = Intervention
        fields = [
            "id",
            "intervention_number",
            "student_name",
            "intervention_type",
            "priority_level",
            "status",
            "action_taken_by",
            "action_date",
            "outcome_achieved",
            "requires_followup",
            "created_at",
        ]


class CreateInterventionRequestSerializer(serializers.Serializer):
    student_id = serializers.CharField(required=True)
    student_name = serializers.CharField(required=True)
    course_id = serializers.CharField(required=False, allow_blank=True)
    course_name = serializers.CharField(required=False, allow_blank=True)
    intervention_type = serializers.CharField(required=True)
    priority_level = serializers.CharField(required=False, default="medium")
    action_description = serializers.CharField(required=True)
    action_taken_by = serializers.CharField(required=True)
    action_taken_by_role = serializers.CharField(required=False, allow_blank=True)
    communication_method = serializers.CharField(required=False, allow_blank=True)
    communication_notes = serializers.CharField(required=False, allow_blank=True)
    trigger_type = serializers.CharField(required=False, default="manual")
    trigger_details = serializers.JSONField(required=False, default=dict)


class InterventionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterventionRule
        fields = "__all__"
        read_only_fields = [
            "rule_number",
            "last_triggered",
            "trigger_count",
            "created_at",
            "updated_at",
        ]


class EvaluateRulesRequestSerializer(serializers.Serializer):
    student_id = serializers.CharField(required=True)
    metrics = serializers.JSONField(required=True)


class InterventionWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterventionWorkflow
        fields = "__all__"
        read_only_fields = ["workflow_number", "created_at", "updated_at"]


class UpdateStepRequestSerializer(serializers.Serializer):
    step_id = serializers.IntegerField(required=True)
    status = serializers.CharField(required=True)
    completed_by = serializers.CharField(required=False, allow_blank=True)
    completion_notes = serializers.CharField(required=False, allow_blank=True)
    duration_minutes = serializers.IntegerField(required=False)
    evidence_provided = serializers.JSONField(required=False, default=list)


class RecordOutcomeRequestSerializer(serializers.Serializer):
    metric_type = serializers.CharField(required=True)
    baseline_value = serializers.FloatField(required=False)
    target_value = serializers.FloatField(required=False)
    actual_value = serializers.FloatField(required=True)
    evidence_description = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
