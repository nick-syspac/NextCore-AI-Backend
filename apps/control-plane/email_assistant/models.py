from django.db import models
from django.utils import timezone
import uuid


class StudentMessage(models.Model):
    """Incoming student queries/messages that need replies"""

    MESSAGE_TYPES = [
        ("email", "Email"),
        ("lms", "LMS Message"),
        ("sms", "SMS"),
        ("chat", "Live Chat"),
        ("form", "Contact Form"),
    ]

    PRIORITY_LEVELS = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("new", "New"),
        ("draft_generated", "Draft Generated"),
        ("replied", "Replied"),
        ("archived", "Archived"),
    ]

    message_number = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100, db_index=True)

    # Student information
    student_name = models.CharField(max_length=200)
    student_email = models.EmailField()
    student_id = models.CharField(max_length=50, blank=True)

    # Message details
    message_type = models.CharField(
        max_length=20, choices=MESSAGE_TYPES, default="email"
    )
    subject = models.CharField(max_length=500)
    message_body = models.TextField()
    received_date = models.DateTimeField(default=timezone.now)

    # Classification
    priority = models.CharField(
        max_length=20, choices=PRIORITY_LEVELS, default="medium"
    )
    category = models.CharField(
        max_length=100, blank=True
    )  # e.g., "Assessment Query", "Enrollment", "Technical Support"
    detected_sentiment = models.CharField(
        max_length=50, blank=True
    )  # positive, negative, neutral, frustrated
    detected_topics = models.JSONField(
        default=list, blank=True
    )  # ["assessment", "deadline", "extension"]

    # Status
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="new")
    requires_human_review = models.BooleanField(default=False)

    # Context
    conversation_thread = models.ForeignKey(
        "ConversationThread",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    previous_message_count = models.IntegerField(default=0)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-received_date"]
        indexes = [
            models.Index(fields=["tenant", "status"]),
            models.Index(fields=["priority", "-received_date"]),
            models.Index(fields=["student_email", "-received_date"]),
        ]

    def save(self, *args, **kwargs):
        if not self.message_number:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            random_part = str(uuid.uuid4())[:6].upper()
            self.message_number = f"MSG-{timestamp}-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.message_number} - {self.student_name}: {self.subject[:50]}"


class DraftReply(models.Model):
    """AI-generated draft replies to student messages"""

    GENERATION_STATUS = [
        ("generating", "Generating"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    draft_number = models.CharField(max_length=50, unique=True, editable=False)
    student_message = models.ForeignKey(
        StudentMessage, on_delete=models.CASCADE, related_name="drafts"
    )

    # Generated content
    reply_body = models.TextField()
    reply_subject = models.CharField(max_length=500, blank=True)

    # Generation settings
    tone_used = models.CharField(
        max_length=50
    )  # professional, friendly, empathetic, formal, casual
    formality_level = models.IntegerField(default=3)  # 1-5 scale
    include_greeting = models.BooleanField(default=True)
    include_signature = models.BooleanField(default=True)

    # Template usage
    template_used = models.ForeignKey(
        "MessageTemplate", on_delete=models.SET_NULL, null=True, blank=True
    )

    # Quality metrics
    confidence_score = models.FloatField(default=0.0)  # 0-1, how confident the AI is
    readability_score = models.FloatField(default=0.0)  # Flesch reading ease
    word_count = models.IntegerField(default=0)
    estimated_reading_time_seconds = models.IntegerField(default=0)

    # User interaction
    was_edited = models.BooleanField(default=False)
    was_sent = models.BooleanField(default=False)
    was_rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True)

    # Generation metadata
    generation_status = models.CharField(
        max_length=20, choices=GENERATION_STATUS, default="completed"
    )
    generation_time_ms = models.IntegerField(default=0)
    llm_model_used = models.CharField(max_length=100, default="gpt-4")
    generation_prompt = models.TextField(blank=True)

    # Timestamps
    generated_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-generated_at"]
        indexes = [
            models.Index(fields=["student_message", "-generated_at"]),
            models.Index(fields=["was_sent", "-generated_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.draft_number:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            random_part = str(uuid.uuid4())[:6].upper()
            self.draft_number = f"DRAFT-{timestamp}-{random_part}"
        if self.reply_body:
            self.word_count = len(self.reply_body.split())
            self.estimated_reading_time_seconds = int(
                (self.word_count / 200) * 60
            )  # 200 words per minute
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.draft_number} for {self.student_message.message_number}"


class MessageTemplate(models.Model):
    """Reusable message templates for common queries"""

    TEMPLATE_TYPES = [
        ("assessment", "Assessment Query"),
        ("enrollment", "Enrollment"),
        ("technical", "Technical Support"),
        ("extension", "Extension Request"),
        ("general", "General Query"),
        ("complaint", "Complaint"),
        ("feedback", "Feedback"),
    ]

    template_number = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100, db_index=True)

    # Template details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)

    # Content
    template_body = models.TextField()
    placeholders = models.JSONField(
        default=list, blank=True
    )  # ["{student_name}", "{due_date}", "{unit_code}"]

    # Tone settings
    default_tone = models.CharField(max_length=50, default="professional")
    formality_level = models.IntegerField(default=3)

    # Usage tracking
    usage_count = models.IntegerField(default=0)
    success_rate = models.FloatField(
        default=0.0
    )  # % of times used template was sent without major edits
    last_used_at = models.DateTimeField(null=True, blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_system_template = models.BooleanField(default=False)  # Pre-built vs user-created

    # Metadata
    created_by = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-usage_count", "name"]
        indexes = [
            models.Index(fields=["tenant", "template_type"]),
            models.Index(fields=["is_active", "-usage_count"]),
        ]

    def save(self, *args, **kwargs):
        if not self.template_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            random_part = str(uuid.uuid4())[:6].upper()
            self.template_number = f"TMPL-{timestamp}-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.template_type})"


class ConversationThread(models.Model):
    """Groups related messages in a conversation"""

    thread_number = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100, db_index=True)

    # Participants
    student_email = models.EmailField()
    student_name = models.CharField(max_length=200)

    # Thread details
    subject = models.CharField(max_length=500)
    message_count = models.IntegerField(default=0)
    first_message_date = models.DateTimeField(default=timezone.now)
    last_message_date = models.DateTimeField(default=timezone.now)

    # Status
    is_active = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)

    # Context
    primary_category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_message_date"]
        indexes = [
            models.Index(fields=["tenant", "is_active"]),
            models.Index(fields=["student_email", "-last_message_date"]),
        ]

    def save(self, *args, **kwargs):
        if not self.thread_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            random_part = str(uuid.uuid4())[:6].upper()
            self.thread_number = f"THREAD-{timestamp}-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.thread_number} - {self.subject[:50]}"


class ToneProfile(models.Model):
    """Custom tone profiles for different scenarios"""

    profile_number = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100, db_index=True)

    # Profile details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Tone settings
    tone_descriptor = models.CharField(
        max_length=50
    )  # professional, friendly, empathetic, formal
    formality_level = models.IntegerField(
        default=3
    )  # 1 (very casual) to 5 (very formal)
    empathy_level = models.IntegerField(
        default=3
    )  # 1 (neutral) to 5 (highly empathetic)
    brevity_level = models.IntegerField(default=3)  # 1 (very brief) to 5 (detailed)

    # Style guidelines
    use_contractions = models.BooleanField(default=True)  # "can't" vs "cannot"
    use_emojis = models.BooleanField(default=False)
    greeting_style = models.CharField(max_length=100, default="Hi {name},")
    closing_style = models.CharField(max_length=100, default="Best regards,")

    # Use cases
    recommended_for = models.JSONField(
        default=list, blank=True
    )  # ["complaints", "technical_support"]

    # Usage tracking
    usage_count = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_default", "-usage_count", "name"]
        indexes = [
            models.Index(fields=["tenant", "is_active"]),
        ]

    def save(self, *args, **kwargs):
        if not self.profile_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            random_part = str(uuid.uuid4())[:6].upper()
            self.profile_number = f"TONE-{timestamp}-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.tone_descriptor})"


class ReplyHistory(models.Model):
    """Track all sent replies for analytics and learning"""

    history_number = models.CharField(max_length=50, unique=True, editable=False)

    # References
    student_message = models.ForeignKey(
        StudentMessage, on_delete=models.CASCADE, related_name="reply_history"
    )
    draft_reply = models.ForeignKey(
        DraftReply, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Final sent version
    final_reply_body = models.TextField()
    final_subject = models.CharField(max_length=500)

    # Timing metrics
    time_to_first_draft_seconds = models.IntegerField(
        default=0
    )  # From message received to first draft
    time_to_send_seconds = models.IntegerField(
        default=0
    )  # From message received to sent
    edit_count = models.IntegerField(default=0)  # How many times draft was edited

    # Efficiency metrics
    estimated_manual_time_seconds = models.IntegerField(
        default=300
    )  # Estimated time if done manually (5 min default)
    time_saved_seconds = models.IntegerField(default=0)  # manual - actual
    time_saved_percentage = models.FloatField(default=0.0)

    # Trainer info
    sent_by = models.CharField(max_length=200)
    sent_at = models.DateTimeField(default=timezone.now)

    # Quality feedback (optional)
    student_responded = models.BooleanField(default=False)
    student_satisfied = models.BooleanField(null=True, blank=True)
    follow_up_required = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sent_at"]
        verbose_name_plural = "Reply histories"
        indexes = [
            models.Index(fields=["-sent_at"]),
            models.Index(fields=["sent_by", "-sent_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.history_number:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            random_part = str(uuid.uuid4())[:6].upper()
            self.history_number = f"HIST-{timestamp}-{random_part}"

        # Calculate time saved
        if self.time_to_send_seconds > 0 and self.estimated_manual_time_seconds > 0:
            self.time_saved_seconds = (
                self.estimated_manual_time_seconds - self.time_to_send_seconds
            )
            if self.estimated_manual_time_seconds > 0:
                self.time_saved_percentage = (
                    self.time_saved_seconds / self.estimated_manual_time_seconds
                ) * 100

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.history_number} - Reply sent by {self.sent_by}"
