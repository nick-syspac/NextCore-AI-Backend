from rest_framework import serializers
from .models import (
    ChatSession,
    ChatMessage,
    KnowledgeDocument,
    CoachingInsight,
    CoachConfiguration,
)


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = "__all__"
        read_only_fields = ["message_number", "created_at"]


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = "__all__"
        read_only_fields = ["session_number", "created_at", "updated_at"]


class ChatSessionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""

    message_count = serializers.IntegerField()

    class Meta:
        model = ChatSession
        fields = [
            "id",
            "session_number",
            "student_name",
            "subject",
            "topic",
            "session_type",
            "status",
            "message_count",
            "satisfaction_rating",
            "created_at",
            "updated_at",
        ]


class SendMessageRequestSerializer(serializers.Serializer):
    session_id = serializers.IntegerField(required=False)
    student_id = serializers.CharField(required=True)
    student_name = serializers.CharField(required=True)
    message = serializers.CharField(required=True)
    subject = serializers.CharField(required=False, allow_blank=True)
    topic = serializers.CharField(required=False, allow_blank=True)
    session_type = serializers.CharField(required=False, default="general_chat")


class KnowledgeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeDocument
        fields = "__all__"
        read_only_fields = [
            "document_number",
            "vector_id",
            "retrieval_count",
            "average_relevance_score",
            "last_retrieved_at",
            "created_at",
            "updated_at",
        ]


class CoachingInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachingInsight
        fields = "__all__"
        read_only_fields = ["insight_number", "created_at", "updated_at"]


class GenerateInsightsRequestSerializer(serializers.Serializer):
    student_id = serializers.CharField(required=True)
    time_period = serializers.CharField(required=False)


class CoachConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachConfiguration
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
