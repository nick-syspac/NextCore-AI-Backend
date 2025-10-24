from django.db import models
from django.utils import timezone
import uuid


class DiaryEntry(models.Model):
    """Diary entries for teaching sessions with auto-summarization"""
    entry_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)
    
    # Trainer information
    trainer_id = models.CharField(max_length=100, db_index=True)
    trainer_name = models.CharField(max_length=200)
    
    # Session details
    session_date = models.DateField(default=timezone.now)
    session_time_start = models.TimeField(null=True, blank=True)
    session_time_end = models.TimeField(null=True, blank=True)
    session_duration_minutes = models.IntegerField(default=0)
    
    # Class/Course information
    course_name = models.CharField(max_length=300)
    course_code = models.CharField(max_length=100, blank=True)
    unit_of_competency = models.CharField(max_length=200, blank=True)
    student_count = models.IntegerField(default=0)
    delivery_mode = models.CharField(
        max_length=50,
        choices=[
            ('face_to_face', 'Face to Face'),
            ('online_live', 'Online Live'),
            ('online_self_paced', 'Online Self-Paced'),
            ('blended', 'Blended'),
            ('workplace', 'Workplace')
        ],
        default='face_to_face'
    )
    
    # Content captured
    raw_transcript = models.TextField(blank=True)  # Speech-to-text output
    manual_notes = models.TextField(blank=True)  # Trainer's manual notes
    
    # AI-generated summaries
    session_summary = models.TextField(blank=True)  # Auto-generated summary
    key_topics_covered = models.JSONField(default=list)  # List of topics
    student_engagement_notes = models.TextField(blank=True)
    challenges_encountered = models.TextField(blank=True)
    follow_up_actions = models.JSONField(default=list)  # Action items
    
    # Evidence and compliance
    learning_outcomes_addressed = models.JSONField(default=list)
    assessment_activities = models.TextField(blank=True)
    resources_used = models.JSONField(default=list)
    evidence_attachments = models.JSONField(default=list)  # File paths/URLs
    
    # Metadata
    transcription_model = models.CharField(max_length=100, blank=True)  # e.g., "whisper-1"
    summarization_model = models.CharField(max_length=100, blank=True)  # e.g., "gpt-4"
    transcription_duration_seconds = models.FloatField(null=True, blank=True)
    summarization_tokens = models.IntegerField(null=True, blank=True)
    
    # Status
    entry_status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('transcribing', 'Transcribing'),
            ('summarizing', 'Summarizing'),
            ('complete', 'Complete'),
            ('archived', 'Archived')
        ],
        default='draft'
    )
    
    is_pinned = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-session_date', '-created_at']
        indexes = [
            models.Index(fields=['tenant', 'trainer_id', '-session_date']),
            models.Index(fields=['session_date', 'entry_status']),
            models.Index(fields=['course_code', '-session_date']),
        ]
    
    def __str__(self):
        return f"{self.entry_number} - {self.course_name} ({self.session_date})"
    
    def save(self, *args, **kwargs):
        if not self.entry_number:
            timestamp = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8].upper()
            self.entry_number = f"DIARY-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class AudioRecording(models.Model):
    """Audio recordings of teaching sessions for transcription"""
    recording_number = models.CharField(max_length=50, unique=True, db_index=True)
    diary_entry = models.ForeignKey(DiaryEntry, on_delete=models.CASCADE, related_name='recordings')
    
    # Recording details
    recording_filename = models.CharField(max_length=500)
    recording_file_path = models.CharField(max_length=1000)
    recording_file_size_mb = models.FloatField(default=0.0)
    recording_duration_seconds = models.FloatField(default=0.0)
    recording_format = models.CharField(max_length=20, default='mp3')  # mp3, wav, m4a, etc.
    
    # Transcription
    transcript_text = models.TextField(blank=True)
    transcript_confidence = models.FloatField(null=True, blank=True)  # 0-1 confidence score
    transcript_language = models.CharField(max_length=10, default='en')
    
    # Processing status
    processing_status = models.CharField(
        max_length=20,
        choices=[
            ('uploaded', 'Uploaded'),
            ('queued', 'Queued for Processing'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='uploaded'
    )
    error_message = models.TextField(blank=True)
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.recording_number} - {self.recording_filename}"
    
    def save(self, *args, **kwargs):
        if not self.recording_number:
            timestamp = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:6].upper()
            self.recording_number = f"REC-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class DailySummary(models.Model):
    """Daily aggregated summary of teaching activities"""
    summary_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)
    trainer_id = models.CharField(max_length=100, db_index=True)
    trainer_name = models.CharField(max_length=200)
    
    # Summary date
    summary_date = models.DateField(db_index=True)
    
    # Statistics
    total_sessions = models.IntegerField(default=0)
    total_teaching_hours = models.FloatField(default=0.0)
    total_students = models.IntegerField(default=0)
    courses_taught = models.JSONField(default=list)
    
    # Aggregated content
    daily_highlights = models.TextField(blank=True)
    overall_student_engagement = models.TextField(blank=True)
    key_achievements = models.JSONField(default=list)
    challenges_summary = models.TextField(blank=True)
    action_items_pending = models.JSONField(default=list)
    
    # Evidence
    diary_entries_included = models.JSONField(default=list)  # List of entry IDs
    evidence_documents_created = models.IntegerField(default=0)
    
    # Generation metadata
    generated_by_model = models.CharField(max_length=100, blank=True)
    generation_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-summary_date']
        unique_together = ['tenant', 'trainer_id', 'summary_date']
    
    def __str__(self):
        return f"{self.summary_number} - {self.trainer_name} ({self.summary_date})"
    
    def save(self, *args, **kwargs):
        if not self.summary_number:
            date_str = self.summary_date.strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:6].upper()
            self.summary_number = f"DAILY-{date_str}-{unique_id}"
        super().save(*args, **kwargs)


class EvidenceDocument(models.Model):
    """Evidence documents generated from diary entries"""
    document_number = models.CharField(max_length=50, unique=True, db_index=True)
    diary_entry = models.ForeignKey(DiaryEntry, on_delete=models.CASCADE, related_name='evidence_docs')
    
    # Document details
    document_type = models.CharField(
        max_length=50,
        choices=[
            ('session_plan', 'Session Plan'),
            ('attendance_record', 'Attendance Record'),
            ('teaching_evidence', 'Teaching Evidence'),
            ('assessment_record', 'Assessment Record'),
            ('student_feedback', 'Student Feedback Summary'),
            ('compliance_report', 'Compliance Report'),
            ('professional_reflection', 'Professional Reflection')
        ]
    )
    
    document_title = models.CharField(max_length=300)
    document_content = models.TextField()  # Formatted content
    document_format = models.CharField(
        max_length=20,
        choices=[
            ('markdown', 'Markdown'),
            ('html', 'HTML'),
            ('pdf', 'PDF'),
            ('docx', 'Word Document')
        ],
        default='markdown'
    )
    
    # File storage
    file_path = models.CharField(max_length=1000, blank=True)
    file_size_kb = models.FloatField(null=True, blank=True)
    
    # Metadata
    generated_by = models.CharField(max_length=200)  # User or system
    generation_method = models.CharField(
        max_length=50,
        choices=[
            ('auto_ai', 'Auto-generated by AI'),
            ('template', 'Generated from Template'),
            ('manual', 'Manually Created')
        ],
        default='auto_ai'
    )
    
    # Compliance
    meets_compliance_standards = models.BooleanField(default=True)
    compliance_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.document_number} - {self.document_title}"
    
    def save(self, *args, **kwargs):
        if not self.document_number:
            timestamp = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:6].upper()
            self.document_number = f"DOC-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class TranscriptionJob(models.Model):
    """Queue for managing speech-to-text transcription jobs"""
    job_number = models.CharField(max_length=50, unique=True, db_index=True)
    audio_recording = models.ForeignKey(AudioRecording, on_delete=models.CASCADE, related_name='transcription_jobs')
    
    # Job details
    job_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )
    
    # Processing configuration
    transcription_engine = models.CharField(
        max_length=50,
        choices=[
            ('whisper', 'OpenAI Whisper'),
            ('google_stt', 'Google Speech-to-Text'),
            ('azure_stt', 'Azure Speech Service'),
            ('aws_transcribe', 'AWS Transcribe')
        ],
        default='whisper'
    )
    language = models.CharField(max_length=10, default='en')
    enable_speaker_diarization = models.BooleanField(default=False)
    enable_punctuation = models.BooleanField(default=True)
    
    # Results
    transcript_result = models.TextField(blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    processing_time_seconds = models.FloatField(null=True, blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.job_number} - {self.job_status}"
    
    def save(self, *args, **kwargs):
        if not self.job_number:
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4())[:6].upper()
            self.job_number = f"JOB-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)
