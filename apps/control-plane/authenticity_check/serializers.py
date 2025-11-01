from rest_framework import serializers
from .models import (
    AuthenticityCheck,
    SubmissionAnalysis,
    PlagiarismMatch,
    MetadataVerification,
    AnomalyDetection,
)


class AnomalyDetectionSerializer(serializers.ModelSerializer):
    """Serializer for anomaly detection records"""

    anomaly_type_display = serializers.CharField(
        source="get_anomaly_type_display", read_only=True
    )
    severity_display = serializers.CharField(
        source="get_severity_display", read_only=True
    )

    class Meta:
        model = AnomalyDetection
        fields = [
            "id",
            "anomaly_number",
            "submission_analysis",
            "anomaly_type",
            "anomaly_type_display",
            "severity",
            "severity_display",
            "anomaly_data",
            "description",
            "confidence_score",
            "impact_score",
            "acknowledged",
            "false_positive",
            "resolution_notes",
            "detected_at",
        ]
        read_only_fields = ["anomaly_number", "impact_score", "detected_at"]


class MetadataVerificationSerializer(serializers.ModelSerializer):
    """Serializer for metadata verification records"""

    verification_status_display = serializers.CharField(
        source="get_verification_status_display", read_only=True
    )

    class Meta:
        model = MetadataVerification
        fields = [
            "id",
            "verification_number",
            "submission_analysis",
            "file_metadata",
            "creation_timestamp",
            "modification_timestamp",
            "modification_history",
            "author_info",
            "author_matches_student",
            "verification_status",
            "verification_status_display",
            "anomalies_detected",
            "verification_score",
            "verified_at",
        ]
        read_only_fields = [
            "verification_number",
            "verification_status",
            "verification_score",
            "verified_at",
        ]


class PlagiarismMatchSerializer(serializers.ModelSerializer):
    """Serializer for plagiarism match records"""

    match_type_display = serializers.CharField(
        source="get_match_type_display", read_only=True
    )
    severity_display = serializers.CharField(
        source="get_severity_display", read_only=True
    )

    class Meta:
        model = PlagiarismMatch
        fields = [
            "id",
            "match_number",
            "source_analysis",
            "matched_analysis",
            "similarity_score",
            "match_type",
            "match_type_display",
            "severity",
            "severity_display",
            "matched_text_segments",
            "matched_words_count",
            "matched_percentage",
            "reviewed",
            "false_positive",
            "review_notes",
            "reviewed_by",
            "reviewed_at",
            "detected_at",
        ]
        read_only_fields = ["match_number", "severity", "detected_at"]


class SubmissionAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for submission analysis records"""

    integrity_status_display = serializers.CharField(
        source="get_integrity_status_display", read_only=True
    )
    plagiarism_matches_source = PlagiarismMatchSerializer(
        many=True, read_only=True, source="plagiarism_matches_as_source"
    )
    plagiarism_matches_matched = PlagiarismMatchSerializer(
        many=True, read_only=True, source="plagiarism_matches_as_match"
    )
    metadata_verifications = MetadataVerificationSerializer(many=True, read_only=True)
    anomaly_detections = AnomalyDetectionSerializer(many=True, read_only=True)

    class Meta:
        model = SubmissionAnalysis
        fields = [
            "id",
            "analysis_number",
            "authenticity_check",
            "submission_id",
            "student_id",
            "student_name",
            "submission_content",
            "content_hash",
            "word_count",
            "character_count",
            "content_embedding",
            "plagiarism_score",
            "metadata_verification_score",
            "anomaly_score",
            "combined_integrity_score",
            "integrity_status",
            "integrity_status_display",
            "plagiarism_detected",
            "metadata_issues",
            "anomalies_found",
            "analysis_metadata",
            "analyzed_at",
            "plagiarism_matches_source",
            "plagiarism_matches_matched",
            "metadata_verifications",
            "anomaly_detections",
        ]
        read_only_fields = [
            "analysis_number",
            "content_hash",
            "word_count",
            "character_count",
            "integrity_status",
            "analyzed_at",
        ]


class SubmissionAnalysisListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing submission analyses"""

    integrity_status_display = serializers.CharField(
        source="get_integrity_status_display", read_only=True
    )

    class Meta:
        model = SubmissionAnalysis
        fields = [
            "id",
            "analysis_number",
            "submission_id",
            "student_id",
            "student_name",
            "word_count",
            "plagiarism_score",
            "metadata_verification_score",
            "anomaly_score",
            "combined_integrity_score",
            "integrity_status",
            "integrity_status_display",
            "plagiarism_detected",
            "metadata_issues",
            "anomalies_found",
            "analyzed_at",
        ]


class AuthenticityCheckSerializer(serializers.ModelSerializer):
    """Serializer for authenticity check records"""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    assessment_title = serializers.CharField(source="assessment.title", read_only=True)
    submission_analyses = SubmissionAnalysisListSerializer(many=True, read_only=True)

    class Meta:
        model = AuthenticityCheck
        fields = [
            "id",
            "check_number",
            "assessment",
            "assessment_title",
            "name",
            "description",
            "plagiarism_threshold",
            "metadata_verification_enabled",
            "anomaly_detection_enabled",
            "academic_integrity_mode",
            "status",
            "status_display",
            "total_submissions_checked",
            "plagiarism_cases_detected",
            "metadata_issues_found",
            "anomalies_detected",
            "overall_integrity_score",
            "created_at",
            "updated_at",
            "created_by",
            "submission_analyses",
        ]
        read_only_fields = [
            "check_number",
            "total_submissions_checked",
            "plagiarism_cases_detected",
            "metadata_issues_found",
            "anomalies_detected",
            "overall_integrity_score",
            "created_at",
            "updated_at",
        ]


class AuthenticityCheckListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing authenticity checks"""

    status_display = serializers.CharField(source="get_status_display", read_only=True)
    assessment_title = serializers.CharField(source="assessment.title", read_only=True)

    class Meta:
        model = AuthenticityCheck
        fields = [
            "id",
            "check_number",
            "assessment_title",
            "name",
            "status",
            "status_display",
            "total_submissions_checked",
            "plagiarism_cases_detected",
            "metadata_issues_found",
            "anomalies_detected",
            "overall_integrity_score",
            "created_at",
        ]
