from rest_framework import serializers
from .models import (
    EngagementHeatmap, AttendanceRecord, LMSActivity,
    DiscussionSentiment, EngagementAlert
)


class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = [
            'id', 'record_number', 'tenant', 'student_id', 'date', 'status',
            'session_name', 'scheduled_start', 'scheduled_end', 'actual_arrival',
            'actual_departure', 'minutes_late', 'minutes_attended',
            'participation_level', 'notes', 'created_at'
        ]
        read_only_fields = ['record_number', 'created_at']


class LMSActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LMSActivity
        fields = [
            'id', 'activity_number', 'tenant', 'student_id', 'date',
            'activity_type', 'activity_name', 'timestamp', 'duration_minutes',
            'completion_status', 'interaction_count', 'course_name',
            'module_name', 'quality_score', 'created_at'
        ]
        read_only_fields = ['activity_number', 'created_at']


class DiscussionSentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussionSentiment
        fields = [
            'id', 'sentiment_number', 'tenant', 'student_id', 'date',
            'timestamp', 'message_type', 'message_content', 'sentiment_score',
            'sentiment_label', 'confidence', 'primary_emotion', 'emotion_scores',
            'word_count', 'question_count', 'exclamation_count',
            'negative_keywords', 'help_seeking_keywords', 'discussion_topic',
            'reply_count', 'created_at'
        ]
        read_only_fields = ['sentiment_number', 'sentiment_label', 'created_at']


class EngagementAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngagementAlert
        fields = [
            'id', 'alert_number', 'tenant', 'student_id', 'student_name',
            'alert_type', 'severity', 'title', 'description', 'trigger_metrics',
            'recommended_actions', 'status', 'acknowledged_by', 'acknowledged_at',
            'resolved_at', 'resolution_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['alert_number', 'created_at', 'updated_at']


class EngagementHeatmapSerializer(serializers.ModelSerializer):
    attendance_records = AttendanceRecordSerializer(many=True, read_only=True)
    lms_activities = LMSActivitySerializer(many=True, read_only=True)
    discussion_sentiments = DiscussionSentimentSerializer(many=True, read_only=True)
    engagement_alerts = EngagementAlertSerializer(many=True, read_only=True)
    
    class Meta:
        model = EngagementHeatmap
        fields = [
            'id', 'heatmap_number', 'tenant', 'student_id', 'student_name',
            'time_period', 'start_date', 'end_date', 'overall_engagement_score',
            'attendance_score', 'lms_activity_score', 'sentiment_score',
            'risk_level', 'risk_flags', 'heatmap_data', 'engagement_trend',
            'change_percentage', 'alerts_triggered', 'interventions_applied',
            'created_at', 'updated_at', 'attendance_records', 'lms_activities',
            'discussion_sentiments', 'engagement_alerts'
        ]
        read_only_fields = ['heatmap_number', 'overall_engagement_score', 'risk_level', 'created_at', 'updated_at']


class HeatmapGenerationRequestSerializer(serializers.Serializer):
    """Serializer for heatmap generation requests"""
    student_id = serializers.CharField(max_length=100)
    student_name = serializers.CharField(max_length=200)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    time_period = serializers.ChoiceField(
        choices=['daily', 'weekly', 'monthly', 'semester'],
        default='weekly'
    )
