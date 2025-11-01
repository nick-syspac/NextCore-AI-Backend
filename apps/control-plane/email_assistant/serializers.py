from rest_framework import serializers
from .models import (
    StudentMessage,
    DraftReply,
    MessageTemplate,
    ConversationThread,
    ToneProfile,
    ReplyHistory,
)


# Model Serializers
class StudentMessageSerializer(serializers.ModelSerializer):
    drafts_count = serializers.SerializerMethodField()

    class Meta:
        model = StudentMessage
        fields = "__all__"

    def get_drafts_count(self, obj):
        return obj.drafts.count()


class StudentMessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMessage
        fields = [
            "id",
            "message_number",
            "student_name",
            "subject",
            "message_type",
            "priority",
            "status",
            "received_date",
            "detected_sentiment",
        ]


class DraftReplySerializer(serializers.ModelSerializer):
    student_message_details = StudentMessageListSerializer(
        source="student_message", read_only=True
    )

    class Meta:
        model = DraftReply
        fields = "__all__"


class DraftReplyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftReply
        fields = [
            "id",
            "draft_number",
            "tone_used",
            "confidence_score",
            "was_sent",
            "generated_at",
            "word_count",
        ]


class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = "__all__"


class MessageTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = [
            "id",
            "template_number",
            "name",
            "template_type",
            "usage_count",
            "is_active",
        ]


class ConversationThreadSerializer(serializers.ModelSerializer):
    messages_count = serializers.SerializerMethodField()

    class Meta:
        model = ConversationThread
        fields = "__all__"

    def get_messages_count(self, obj):
        return obj.messages.count()


class ToneProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToneProfile
        fields = "__all__"


class ReplyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyHistory
        fields = "__all__"


# Request/Response Serializers
class GenerateReplyRequestSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    tone = serializers.ChoiceField(
        choices=["professional", "friendly", "empathetic", "formal", "casual"],
        default="professional",
    )
    formality_level = serializers.IntegerField(min_value=1, max_value=5, default=3)
    include_greeting = serializers.BooleanField(default=True)
    include_signature = serializers.BooleanField(default=True)
    template_id = serializers.IntegerField(required=False, allow_null=True)
    additional_context = serializers.CharField(required=False, allow_blank=True)
    max_words = serializers.IntegerField(default=200, min_value=50, max_value=1000)


class GenerateReplyResponseSerializer(serializers.Serializer):
    draft_id = serializers.IntegerField()
    draft_number = serializers.CharField()
    reply_body = serializers.CharField()
    reply_subject = serializers.CharField()
    confidence_score = serializers.FloatField()
    word_count = serializers.IntegerField()
    generation_time_ms = serializers.IntegerField()
    message = serializers.CharField()


class RefineToneRequestSerializer(serializers.Serializer):
    draft_id = serializers.IntegerField()
    new_tone = serializers.ChoiceField(
        choices=["professional", "friendly", "empathetic", "formal", "casual"]
    )
    formality_adjustment = serializers.IntegerField(
        required=False, min_value=-2, max_value=2
    )
    make_shorter = serializers.BooleanField(default=False)
    make_longer = serializers.BooleanField(default=False)
    add_empathy = serializers.BooleanField(default=False)
    specific_instructions = serializers.CharField(required=False, allow_blank=True)


class RefineToneResponseSerializer(serializers.Serializer):
    draft_id = serializers.IntegerField()
    original_reply = serializers.CharField()
    refined_reply = serializers.CharField()
    original_word_count = serializers.IntegerField()
    refined_word_count = serializers.IntegerField()
    tone_used = serializers.CharField()
    changes_made = serializers.ListField(child=serializers.CharField())
    message = serializers.CharField()


class SaveTemplateRequestSerializer(serializers.Serializer):
    draft_id = serializers.IntegerField(required=False, allow_null=True)
    template_body = serializers.CharField()
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    template_type = serializers.ChoiceField(
        choices=[
            "assessment",
            "enrollment",
            "technical",
            "extension",
            "general",
            "complaint",
            "feedback",
        ]
    )
    default_tone = serializers.CharField(default="professional")
    placeholders = serializers.ListField(child=serializers.CharField(), required=False)


class SaveTemplateResponseSerializer(serializers.Serializer):
    template_id = serializers.IntegerField()
    template_number = serializers.CharField()
    name = serializers.CharField()
    template_type = serializers.CharField()
    placeholders = serializers.ListField(child=serializers.CharField())
    message = serializers.CharField()


class SuggestRepliesRequestSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    num_suggestions = serializers.IntegerField(default=3, min_value=1, max_value=5)
    variety = serializers.BooleanField(
        default=True
    )  # Generate replies with different tones


class SuggestRepliesResponseSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    suggestions = serializers.ListField(child=serializers.DictField())
    message = serializers.CharField()


class AnalyzeSentimentRequestSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    analyze_urgency = serializers.BooleanField(default=True)
    extract_topics = serializers.BooleanField(default=True)


class AnalyzeSentimentResponseSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    sentiment = serializers.CharField()
    sentiment_score = serializers.FloatField()
    urgency_level = serializers.CharField()
    detected_topics = serializers.ListField(child=serializers.CharField())
    recommended_tone = serializers.CharField()
    recommended_priority = serializers.CharField()
    analysis_details = serializers.DictField()
    message = serializers.CharField()


class SendReplyRequestSerializer(serializers.Serializer):
    draft_id = serializers.IntegerField()
    final_reply_body = serializers.CharField()
    final_subject = serializers.CharField()
    sent_by = serializers.CharField(max_length=200)
    edit_count = serializers.IntegerField(default=0)


class SendReplyResponseSerializer(serializers.Serializer):
    history_id = serializers.IntegerField()
    history_number = serializers.CharField()
    time_saved_seconds = serializers.IntegerField()
    time_saved_percentage = serializers.FloatField()
    message = serializers.CharField()


class DashboardStatsSerializer(serializers.Serializer):
    total_messages = serializers.IntegerField()
    new_messages = serializers.IntegerField()
    draft_generated = serializers.IntegerField()
    replied_messages = serializers.IntegerField()

    total_drafts = serializers.IntegerField()
    drafts_sent = serializers.IntegerField()
    drafts_rejected = serializers.IntegerField()
    avg_confidence_score = serializers.FloatField()

    total_templates = serializers.IntegerField()
    active_templates = serializers.IntegerField()

    total_time_saved_hours = serializers.FloatField()
    avg_time_saved_per_reply_seconds = serializers.IntegerField()
    time_saved_percentage = serializers.FloatField()
    total_replies_sent = serializers.IntegerField()

    messages_by_priority = serializers.DictField()
    messages_by_sentiment = serializers.DictField()
    recent_messages = StudentMessageListSerializer(many=True)
    recent_drafts = DraftReplyListSerializer(many=True)
    top_templates = MessageTemplateListSerializer(many=True)
