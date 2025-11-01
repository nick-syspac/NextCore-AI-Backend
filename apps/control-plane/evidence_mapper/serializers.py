from rest_framework import serializers
from .models import (
    EvidenceMapping,
    SubmissionEvidence,
    CriteriaTag,
    EvidenceAudit,
    EmbeddingSearch,
)


class EvidenceMappingSerializer(serializers.ModelSerializer):
    coverage_percentage_calculated = serializers.SerializerMethodField()

    class Meta:
        model = EvidenceMapping
        fields = "__all__"
        read_only_fields = (
            "mapping_number",
            "created_at",
            "updated_at",
            "total_evidence_tagged",
            "total_text_extracted",
            "embeddings_generated",
            "coverage_percentage",
        )

    def get_coverage_percentage_calculated(self, obj):
        return obj.calculate_coverage()


class SubmissionEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionEvidence
        fields = "__all__"
        read_only_fields = (
            "evidence_number",
            "created_at",
            "text_length",
            "total_tags",
            "extracted_at",
        )


class SubmissionEvidenceDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = SubmissionEvidence
        fields = "__all__"
        read_only_fields = (
            "evidence_number",
            "created_at",
            "text_length",
            "total_tags",
            "extracted_at",
        )

    def get_tags(self, obj):
        tags = obj.tags.all()
        return CriteriaTagSerializer(tags, many=True).data


class CriteriaTagSerializer(serializers.ModelSerializer):
    tagged_length = serializers.SerializerMethodField()

    class Meta:
        model = CriteriaTag
        fields = "__all__"
        read_only_fields = ("tag_number", "tagged_at")

    def get_tagged_length(self, obj):
        return obj.get_tagged_length()


class EvidenceAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceAudit
        fields = "__all__"
        read_only_fields = ("timestamp",)


class EmbeddingSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbeddingSearch
        fields = "__all__"
        read_only_fields = ("search_number", "timestamp")


# Request serializers
class TagEvidenceRequestSerializer(serializers.Serializer):
    criterion_id = serializers.CharField(required=True)
    criterion_name = serializers.CharField(required=True)
    criterion_description = serializers.CharField(required=False, allow_blank=True)
    tagged_text = serializers.CharField(required=True)
    text_start_position = serializers.IntegerField(required=True)
    text_end_position = serializers.IntegerField(required=True)
    tag_type = serializers.ChoiceField(
        choices=CriteriaTag.TAG_TYPE_CHOICES, default="direct"
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    tagged_by = serializers.CharField(required=True)


class ExtractTextRequestSerializer(serializers.Serializer):
    extraction_method = serializers.CharField(required=False, default="mock")
    generate_embedding = serializers.BooleanField(default=True)


class SearchEmbeddingsRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
    search_type = serializers.ChoiceField(
        choices=EmbeddingSearch.SEARCH_TYPE_CHOICES, default="similarity"
    )
    limit = serializers.IntegerField(default=10, min_value=1, max_value=100)
    min_similarity = serializers.FloatField(default=0.5, min_value=0.0, max_value=1.0)
