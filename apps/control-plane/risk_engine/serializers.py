from rest_framework import serializers
from .models import (
    RiskAssessment,
    RiskFactor,
    StudentEngagementMetric,
    SentimentAnalysis,
    InterventionAction,
)


class RiskFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFactor
        fields = [
            "id",
            "factor_number",
            "factor_type",
            "factor_name",
            "description",
            "weight",
            "contribution",
            "severity",
            "current_value",
            "threshold_value",
            "threshold_exceeded",
            "trend",
            "created_at",
        ]
        read_only_fields = ["factor_number", "threshold_exceeded", "created_at"]


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentAnalysis
        fields = [
            "id",
            "analysis_number",
            "source_type",
            "text_sample",
            "sentiment_score",
            "sentiment_label",
            "confidence",
            "frustration_detected",
            "stress_detected",
            "confusion_detected",
            "disengagement_detected",
            "negative_keywords",
            "risk_indicators",
            "analysis_date",
        ]
        read_only_fields = ["analysis_number", "sentiment_label", "analysis_date"]


class InterventionActionSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(
        source="assigned_to.get_full_name", read_only=True
    )
    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )

    class Meta:
        model = InterventionAction
        fields = [
            "id",
            "action_number",
            "action_type",
            "description",
            "priority",
            "scheduled_date",
            "completed_date",
            "status",
            "assigned_to",
            "assigned_to_name",
            "outcome_notes",
            "effectiveness_rating",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["action_number", "created_at", "updated_at"]


class RiskAssessmentSerializer(serializers.ModelSerializer):
    risk_factors = RiskFactorSerializer(many=True, read_only=True)
    sentiment_analyses = SentimentAnalysisSerializer(many=True, read_only=True)
    interventions = InterventionActionSerializer(many=True, read_only=True)
    alert_acknowledged_by_name = serializers.CharField(
        source="alert_acknowledged_by.get_full_name", read_only=True
    )
    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )

    class Meta:
        model = RiskAssessment
        fields = [
            "id",
            "assessment_number",
            "student_id",
            "student_name",
            "dropout_probability",
            "risk_level",
            "risk_score",
            "engagement_score",
            "performance_score",
            "attendance_score",
            "sentiment_score",
            "model_version",
            "confidence",
            "status",
            "assessment_date",
            "last_updated",
            "alert_triggered",
            "alert_acknowledged",
            "alert_acknowledged_by",
            "alert_acknowledged_by_name",
            "alert_acknowledged_at",
            "intervention_assigned",
            "intervention_notes",
            "created_by",
            "created_by_name",
            "created_at",
            "risk_factors",
            "sentiment_analyses",
            "interventions",
        ]
        read_only_fields = [
            "assessment_number",
            "risk_level",
            "assessment_date",
            "last_updated",
            "created_at",
            "alert_triggered",
        ]


class RiskAssessmentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""

    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )
    risk_factor_count = serializers.SerializerMethodField()
    intervention_count = serializers.SerializerMethodField()

    class Meta:
        model = RiskAssessment
        fields = [
            "id",
            "assessment_number",
            "student_id",
            "student_name",
            "dropout_probability",
            "risk_level",
            "risk_score",
            "confidence",
            "status",
            "assessment_date",
            "alert_triggered",
            "alert_acknowledged",
            "intervention_assigned",
            "created_by_name",
            "risk_factor_count",
            "intervention_count",
        ]

    def get_risk_factor_count(self, obj):
        return obj.risk_factors.count()

    def get_intervention_count(self, obj):
        return obj.interventions.count()


class StudentEngagementMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEngagementMetric
        fields = [
            "id",
            "metric_number",
            "student_id",
            "student_name",
            "login_frequency",
            "time_on_platform",
            "assignment_submission_rate",
            "forum_participation",
            "peer_interaction_score",
            "last_login",
            "days_inactive",
            "activity_decline_rate",
            "overall_engagement_score",
            "measurement_date",
            "created_at",
        ]
        read_only_fields = ["metric_number", "measurement_date", "created_at"]
