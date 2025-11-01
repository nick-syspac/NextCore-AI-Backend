from rest_framework import serializers
from .models import Rubric, RubricCriterion, RubricLevel, RubricGenerationLog


class RubricLevelSerializer(serializers.ModelSerializer):
    level_type_display = serializers.CharField(
        source="get_level_type_display", read_only=True
    )

    class Meta:
        model = RubricLevel
        fields = [
            "id",
            "level_name",
            "level_type",
            "level_type_display",
            "points",
            "description",
            "indicators",
            "examples",
            "ai_generated",
            "nlp_summary",
            "display_order",
        ]


class RubricCriterionSerializer(serializers.ModelSerializer):
    levels = RubricLevelSerializer(many=True, read_only=True)
    blooms_level_display = serializers.SerializerMethodField()

    class Meta:
        model = RubricCriterion
        fields = [
            "id",
            "criterion_number",
            "title",
            "description",
            "weight",
            "max_points",
            "maps_to_elements",
            "maps_to_performance_criteria",
            "maps_to_knowledge_evidence",
            "taxonomy_tags",
            "blooms_level",
            "blooms_level_display",
            "ai_generated",
            "ai_rationale",
            "nlp_keywords",
            "display_order",
            "levels",
        ]

    def get_blooms_level_display(self, obj):
        if obj.blooms_level:
            return obj.blooms_level.capitalize()
        return None


class RubricSerializer(serializers.ModelSerializer):
    rubric_type_display = serializers.CharField(
        source="get_rubric_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    criterion_count = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    approved_by_name = serializers.SerializerMethodField()
    assessment_title = serializers.CharField(source="assessment.title", read_only=True)
    task_question = serializers.CharField(source="task.question", read_only=True)

    class Meta:
        model = Rubric
        fields = [
            "id",
            "rubric_number",
            "title",
            "description",
            "rubric_type",
            "rubric_type_display",
            "status",
            "status_display",
            "assessment",
            "assessment_title",
            "task",
            "task_question",
            "total_points",
            "passing_score",
            "ai_generated",
            "ai_model",
            "ai_generation_time",
            "ai_generated_at",
            "nlp_summary",
            "nlp_key_points",
            "taxonomy_tags",
            "blooms_levels",
            "criterion_count",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
            "reviewed_by",
            "reviewed_by_name",
            "reviewed_at",
            "approved_by",
            "approved_by_name",
            "approved_at",
        ]
        read_only_fields = [
            "rubric_number",
            "ai_generated",
            "ai_model",
            "ai_generation_time",
            "ai_generated_at",
        ]

    def get_criterion_count(self, obj):
        return obj.get_criterion_count()

    def get_created_by_name(self, obj):
        return (
            obj.created_by.get_full_name() or obj.created_by.username
            if obj.created_by
            else None
        )

    def get_reviewed_by_name(self, obj):
        return (
            obj.reviewed_by.get_full_name() or obj.reviewed_by.username
            if obj.reviewed_by
            else None
        )

    def get_approved_by_name(self, obj):
        return (
            obj.approved_by.get_full_name() or obj.approved_by.username
            if obj.approved_by
            else None
        )


class RubricDetailSerializer(RubricSerializer):
    criteria = RubricCriterionSerializer(many=True, read_only=True)

    class Meta(RubricSerializer.Meta):
        fields = RubricSerializer.Meta.fields + ["criteria"]


class RubricGenerationRequestSerializer(serializers.Serializer):
    """Serializer for rubric generation requests"""

    assessment_id = serializers.IntegerField(required=False, allow_null=True)
    task_id = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.CharField(max_length=500, required=False)
    rubric_type = serializers.ChoiceField(
        choices=["analytic", "holistic", "checklist", "single_point"],
        default="analytic",
    )
    number_of_criteria = serializers.IntegerField(min_value=1, max_value=20, default=5)
    number_of_levels = serializers.IntegerField(min_value=2, max_value=10, default=4)
    total_points = serializers.IntegerField(min_value=1, max_value=1000, default=100)
    include_examples = serializers.BooleanField(default=True)
    enable_nlp_summary = serializers.BooleanField(default=True)
    enable_taxonomy_tagging = serializers.BooleanField(default=True)

    def validate(self, data):
        """Validate that at least assessment_id or task_id is provided"""
        if not data.get("assessment_id") and not data.get("task_id"):
            raise serializers.ValidationError(
                "Either assessment_id or task_id must be provided"
            )
        return data


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""

    total_rubrics = serializers.IntegerField()
    by_status = serializers.DictField()
    by_type = serializers.DictField()
    ai_generated_count = serializers.IntegerField()
    ai_generation_rate = serializers.FloatField()
    avg_criteria_per_rubric = serializers.FloatField()
    taxonomy_distribution = serializers.DictField()
    recent_rubrics = serializers.IntegerField()
