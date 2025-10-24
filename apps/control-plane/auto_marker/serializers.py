from rest_framework import serializers
from .models import AutoMarker, MarkedResponse, MarkingCriterion, CriterionScore, MarkingLog


class MarkingCriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkingCriterion
        fields = [
            'id', 'criterion_name', 'description', 'expected_content',
            'weight', 'max_points', 'criterion_keywords', 'required',
            'display_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CriterionScoreSerializer(serializers.ModelSerializer):
    criterion = MarkingCriterionSerializer(read_only=True)
    criterion_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CriterionScore
        fields = [
            'id', 'criterion', 'criterion_id', 'similarity_score',
            'points_awarded', 'matched_content', 'missing_elements',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AutoMarkerListSerializer(serializers.ModelSerializer):
    """Serializer for listing auto-markers"""
    total_responses = serializers.SerializerMethodField()
    pending_review = serializers.SerializerMethodField()
    
    class Meta:
        model = AutoMarker
        fields = [
            'id', 'marker_number', 'title', 'description', 'tenant',
            'answer_type', 'max_marks', 'status', 'similarity_model',
            'similarity_threshold', 'total_responses_marked',
            'average_similarity_score', 'average_marking_time',
            'total_responses', 'pending_review', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'marker_number', 'created_at', 'updated_at']
    
    def get_total_responses(self, obj):
        return obj.responses.count()
    
    def get_pending_review(self, obj):
        return obj.responses.filter(requires_review=True).count()


class AutoMarkerDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with nested criteria"""
    criteria = MarkingCriterionSerializer(many=True, read_only=True)
    statistics = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = AutoMarker
        fields = [
            'id', 'marker_number', 'title', 'description', 'tenant',
            'created_by', 'created_by_name', 'answer_type', 'question_text',
            'model_answer', 'max_marks', 'similarity_model',
            'similarity_threshold', 'partial_credit_enabled',
            'min_similarity_for_credit', 'use_keywords', 'keywords',
            'keyword_weight', 'total_responses_marked',
            'average_similarity_score', 'average_marking_time',
            'status', 'criteria', 'statistics', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'marker_number', 'total_responses_marked',
            'average_similarity_score', 'average_marking_time',
            'created_at', 'updated_at'
        ]
    
    def get_statistics(self, obj):
        return obj.get_marking_statistics()


class MarkedResponseListSerializer(serializers.ModelSerializer):
    """Serializer for listing marked responses"""
    auto_marker_title = serializers.CharField(source='auto_marker.title', read_only=True)
    
    class Meta:
        model = MarkedResponse
        fields = [
            'id', 'response_number', 'auto_marker', 'auto_marker_title',
            'student_id', 'student_name', 'word_count', 'similarity_score',
            'combined_score', 'marks_awarded', 'confidence_score',
            'requires_review', 'status', 'marked_at', 'created_at'
        ]
        read_only_fields = ['id', 'response_number', 'created_at']


class MarkedResponseDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for marked responses with full analysis"""
    auto_marker = AutoMarkerListSerializer(read_only=True)
    criterion_scores = CriterionScoreSerializer(many=True, read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True)
    
    class Meta:
        model = MarkedResponse
        fields = [
            'id', 'response_number', 'auto_marker', 'student_id', 'student_name',
            'response_text', 'word_count', 'similarity_score', 'keyword_match_score',
            'combined_score', 'marks_awarded', 'confidence_score',
            'matched_keywords', 'missing_keywords', 'key_phrases_detected',
            'similarity_breakdown', 'requires_review', 'review_reason',
            'automated_feedback', 'reviewer_notes', 'status', 'marking_time',
            'marked_at', 'reviewed_at', 'reviewed_by', 'reviewed_by_name',
            'criterion_scores', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'response_number', 'word_count', 'similarity_score',
            'keyword_match_score', 'combined_score', 'marks_awarded',
            'confidence_score', 'matched_keywords', 'missing_keywords',
            'key_phrases_detected', 'similarity_breakdown', 'marking_time',
            'marked_at', 'created_at', 'updated_at'
        ]


class MarkingLogSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True)
    auto_marker_title = serializers.CharField(source='auto_marker.title', read_only=True)
    
    class Meta:
        model = MarkingLog
        fields = [
            'id', 'auto_marker', 'auto_marker_title', 'response', 'action',
            'performed_by', 'performed_by_name', 'similarity_model',
            'model_version', 'responses_processed', 'total_time',
            'average_time_per_response', 'original_score', 'new_score',
            'adjustment_reason', 'details', 'timestamp'
        ]
        read_only_fields = ['id', 'average_time_per_response', 'timestamp']


class MarkResponsesRequestSerializer(serializers.Serializer):
    """Serializer for batch marking request"""
    responses = serializers.ListField(
        child=serializers.DictField(),
        help_text="List of responses to mark"
    )
    auto_mark = serializers.BooleanField(default=True)
    enable_review_flagging = serializers.BooleanField(default=True)
    
    def validate_responses(self, value):
        """Validate response format"""
        if not value:
            raise serializers.ValidationError("At least one response is required")
        
        for idx, response in enumerate(value):
            if 'student_id' not in response:
                raise serializers.ValidationError(f"Response {idx}: student_id is required")
            if 'student_name' not in response:
                raise serializers.ValidationError(f"Response {idx}: student_name is required")
            if 'response_text' not in response:
                raise serializers.ValidationError(f"Response {idx}: response_text is required")
        
        return value


class SingleMarkRequestSerializer(serializers.Serializer):
    """Serializer for marking a single response"""
    student_id = serializers.CharField(max_length=100)
    student_name = serializers.CharField(max_length=255)
    response_text = serializers.CharField()
    auto_mark = serializers.BooleanField(default=True)
