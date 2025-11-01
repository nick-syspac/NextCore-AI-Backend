from rest_framework import serializers
from .models import (
    DiaryEntry,
    AudioRecording,
    DailySummary,
    EvidenceDocument,
    TranscriptionJob,
)


class AudioRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioRecording
        fields = "__all__"
        read_only_fields = ["recording_number", "uploaded_at", "processed_at"]


class DiaryEntrySerializer(serializers.ModelSerializer):
    recordings = AudioRecordingSerializer(many=True, read_only=True)

    class Meta:
        model = DiaryEntry
        fields = "__all__"
        read_only_fields = ["entry_number", "created_at", "updated_at"]


class DiaryEntryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing diary entries"""

    recordings_count = serializers.SerializerMethodField()

    class Meta:
        model = DiaryEntry
        fields = [
            "id",
            "entry_number",
            "trainer_name",
            "session_date",
            "course_name",
            "session_duration_minutes",
            "student_count",
            "entry_status",
            "recordings_count",
            "created_at",
        ]

    def get_recordings_count(self, obj):
        return obj.recordings.count()


class DailySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySummary
        fields = "__all__"
        read_only_fields = ["summary_number", "generation_date"]


class EvidenceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceDocument
        fields = "__all__"
        read_only_fields = ["document_number", "created_at"]


class TranscriptionJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionJob
        fields = "__all__"
        read_only_fields = ["job_number", "created_at", "started_at", "completed_at"]


# Request/Response Serializers


class UploadAudioRequestSerializer(serializers.Serializer):
    """Request serializer for audio upload"""

    diary_entry_id = serializers.IntegerField()
    audio_file = serializers.FileField()
    recording_filename = serializers.CharField(max_length=500)
    language = serializers.CharField(max_length=10, default="en")


class UploadAudioResponseSerializer(serializers.Serializer):
    """Response serializer for audio upload"""

    recording_id = serializers.IntegerField()
    recording_number = serializers.CharField()
    status = serializers.CharField()
    message = serializers.CharField()


class TranscribeAudioRequestSerializer(serializers.Serializer):
    """Request serializer for transcription"""

    recording_id = serializers.IntegerField()
    transcription_engine = serializers.ChoiceField(
        choices=["whisper", "google_stt", "azure_stt", "aws_transcribe"],
        default="whisper",
    )
    language = serializers.CharField(max_length=10, default="en")
    enable_speaker_diarization = serializers.BooleanField(default=False)


class TranscribeAudioResponseSerializer(serializers.Serializer):
    """Response serializer for transcription"""

    job_id = serializers.IntegerField()
    job_number = serializers.CharField()
    status = serializers.CharField()
    transcript = serializers.CharField(allow_blank=True)
    message = serializers.CharField()


class GenerateSummaryRequestSerializer(serializers.Serializer):
    """Request serializer for AI summary generation"""

    diary_entry_id = serializers.IntegerField()
    include_transcript = serializers.BooleanField(default=True)
    include_manual_notes = serializers.BooleanField(default=True)
    summary_style = serializers.ChoiceField(
        choices=["brief", "detailed", "evidence_focused"], default="detailed"
    )


class GenerateSummaryResponseSerializer(serializers.Serializer):
    """Response serializer for AI summary generation"""

    diary_entry_id = serializers.IntegerField()
    session_summary = serializers.CharField()
    key_topics_covered = serializers.ListField(child=serializers.CharField())
    follow_up_actions = serializers.ListField(child=serializers.CharField())
    model_used = serializers.CharField()
    tokens_used = serializers.IntegerField()


class CreateDailySummaryRequestSerializer(serializers.Serializer):
    """Request serializer for creating daily summary"""

    trainer_id = serializers.CharField(max_length=100)
    summary_date = serializers.DateField()
    include_draft_entries = serializers.BooleanField(default=False)


class CreateDailySummaryResponseSerializer(serializers.Serializer):
    """Response serializer for daily summary creation"""

    summary_id = serializers.IntegerField()
    summary_number = serializers.CharField()
    total_sessions = serializers.IntegerField()
    total_teaching_hours = serializers.FloatField()
    message = serializers.CharField()


class GenerateEvidenceRequestSerializer(serializers.Serializer):
    """Request serializer for evidence document generation"""

    diary_entry_id = serializers.IntegerField()
    document_type = serializers.ChoiceField(
        choices=[
            "session_plan",
            "attendance_record",
            "teaching_evidence",
            "assessment_record",
            "student_feedback",
            "compliance_report",
            "professional_reflection",
        ]
    )
    document_format = serializers.ChoiceField(
        choices=["markdown", "html", "pdf", "docx"], default="markdown"
    )
    include_attachments = serializers.BooleanField(default=True)


class GenerateEvidenceResponseSerializer(serializers.Serializer):
    """Response serializer for evidence document generation"""

    document_id = serializers.IntegerField()
    document_number = serializers.CharField()
    document_title = serializers.CharField()
    document_content = serializers.CharField()
    file_path = serializers.CharField(allow_blank=True)
    message = serializers.CharField()


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""

    total_entries = serializers.IntegerField()
    entries_this_week = serializers.IntegerField()
    entries_this_month = serializers.IntegerField()
    total_teaching_hours = serializers.FloatField()
    total_students_taught = serializers.IntegerField()
    total_recordings = serializers.IntegerField()
    pending_transcriptions = serializers.IntegerField()
    daily_summaries_count = serializers.IntegerField()
    evidence_documents_count = serializers.IntegerField()
    recent_entries = DiaryEntryListSerializer(many=True)
    courses_taught = serializers.ListField(child=serializers.CharField())


class ExportEvidenceRequestSerializer(serializers.Serializer):
    """Request serializer for evidence export"""

    trainer_id = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    export_format = serializers.ChoiceField(
        choices=["pdf", "docx", "excel", "json"], default="pdf"
    )
    include_transcripts = serializers.BooleanField(default=True)
    include_summaries = serializers.BooleanField(default=True)
    include_evidence_docs = serializers.BooleanField(default=True)


class ExportEvidenceResponseSerializer(serializers.Serializer):
    """Response serializer for evidence export"""

    export_file_path = serializers.CharField()
    export_file_size_mb = serializers.FloatField()
    total_entries = serializers.IntegerField()
    date_range = serializers.CharField()
    message = serializers.CharField()
