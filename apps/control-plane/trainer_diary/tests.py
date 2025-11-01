from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import (
    DiaryEntry,
    AudioRecording,
    DailySummary,
    EvidenceDocument,
    TranscriptionJob,
)


class DiaryEntryModelTest(TestCase):
    def setUp(self):
        self.diary_entry = DiaryEntry.objects.create(
            tenant="test-tenant",
            trainer_id="trainer-001",
            trainer_name="John Smith",
            session_date=timezone.now().date(),
            course_name="Certificate IV in Training and Assessment",
            course_code="TAE40116",
            student_count=15,
            session_duration_minutes=180,
            delivery_mode="face_to_face",
            entry_status="draft",
        )

    def test_diary_entry_creation(self):
        """Test diary entry is created with auto-generated entry number"""
        self.assertIsNotNone(self.diary_entry.entry_number)
        self.assertTrue(self.diary_entry.entry_number.startswith("DIARY-"))
        self.assertEqual(self.diary_entry.trainer_name, "John Smith")
        self.assertEqual(self.diary_entry.student_count, 15)

    def test_diary_entry_str(self):
        """Test diary entry string representation"""
        expected = f"{self.diary_entry.entry_number} - {self.diary_entry.course_name} ({self.diary_entry.session_date})"
        self.assertEqual(str(self.diary_entry), expected)


class AudioRecordingModelTest(TestCase):
    def setUp(self):
        self.diary_entry = DiaryEntry.objects.create(
            tenant="test-tenant",
            trainer_id="trainer-001",
            trainer_name="John Smith",
            session_date=timezone.now().date(),
            course_name="Certificate IV in Training and Assessment",
            student_count=15,
            session_duration_minutes=180,
        )

        self.recording = AudioRecording.objects.create(
            diary_entry=self.diary_entry,
            recording_filename="session_recording.mp3",
            recording_file_path="/uploads/audio/session_recording.mp3",
            recording_file_size_mb=5.2,
            recording_duration_seconds=1800,
            recording_format="mp3",
            processing_status="uploaded",
        )

    def test_recording_creation(self):
        """Test audio recording is created with auto-generated number"""
        self.assertIsNotNone(self.recording.recording_number)
        self.assertTrue(self.recording.recording_number.startswith("REC-"))
        self.assertEqual(self.recording.recording_format, "mp3")

    def test_recording_relationship(self):
        """Test relationship between recording and diary entry"""
        self.assertEqual(self.recording.diary_entry, self.diary_entry)
        self.assertEqual(self.diary_entry.recordings.count(), 1)


class DailySummaryModelTest(TestCase):
    def setUp(self):
        today = timezone.now().date()
        self.daily_summary = DailySummary.objects.create(
            tenant="test-tenant",
            trainer_id="trainer-001",
            trainer_name="John Smith",
            summary_date=today,
            total_sessions=3,
            total_teaching_hours=6.0,
            total_students=45,
            courses_taught=["Course A", "Course B"],
        )

    def test_daily_summary_creation(self):
        """Test daily summary is created with auto-generated number"""
        self.assertIsNotNone(self.daily_summary.summary_number)
        self.assertTrue(self.daily_summary.summary_number.startswith("DAILY-"))
        self.assertEqual(self.daily_summary.total_sessions, 3)
        self.assertEqual(self.daily_summary.total_teaching_hours, 6.0)

    def test_unique_trainer_date(self):
        """Test unique constraint on trainer and date"""
        with self.assertRaises(Exception):
            DailySummary.objects.create(
                tenant="test-tenant",
                trainer_id="trainer-001",
                trainer_name="John Smith",
                summary_date=self.daily_summary.summary_date,
            )


class EvidenceDocumentModelTest(TestCase):
    def setUp(self):
        self.diary_entry = DiaryEntry.objects.create(
            tenant="test-tenant",
            trainer_id="trainer-001",
            trainer_name="John Smith",
            session_date=timezone.now().date(),
            course_name="Certificate IV in Training and Assessment",
            student_count=15,
            session_duration_minutes=180,
        )

        self.evidence_doc = EvidenceDocument.objects.create(
            diary_entry=self.diary_entry,
            document_type="teaching_evidence",
            document_title="Teaching Evidence - Session 1",
            document_content="# Evidence\n\nThis is the evidence content.",
            document_format="markdown",
            generated_by="John Smith",
            generation_method="auto_ai",
        )

    def test_evidence_document_creation(self):
        """Test evidence document is created with auto-generated number"""
        self.assertIsNotNone(self.evidence_doc.document_number)
        self.assertTrue(self.evidence_doc.document_number.startswith("DOC-"))
        self.assertEqual(self.evidence_doc.document_type, "teaching_evidence")


class TranscriptionJobModelTest(TestCase):
    def setUp(self):
        diary_entry = DiaryEntry.objects.create(
            tenant="test-tenant",
            trainer_id="trainer-001",
            trainer_name="John Smith",
            session_date=timezone.now().date(),
            course_name="Certificate IV in Training and Assessment",
            student_count=15,
            session_duration_minutes=180,
        )

        recording = AudioRecording.objects.create(
            diary_entry=diary_entry,
            recording_filename="session_recording.mp3",
            recording_file_path="/uploads/audio/session_recording.mp3",
            recording_file_size_mb=5.2,
            recording_duration_seconds=1800,
        )

        self.job = TranscriptionJob.objects.create(
            audio_recording=recording,
            transcription_engine="whisper",
            language="en",
            job_status="pending",
        )

    def test_transcription_job_creation(self):
        """Test transcription job is created with auto-generated number"""
        self.assertIsNotNone(self.job.job_number)
        self.assertTrue(self.job.job_number.startswith("JOB-"))
        self.assertEqual(self.job.transcription_engine, "whisper")
        self.assertEqual(self.job.job_status, "pending")
