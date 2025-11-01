from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
import uuid
from datetime import datetime, timedelta


class EngagementHeatmap(models.Model):
    """
    Master model for student engagement heatmaps.
    Visualizes attendance, LMS usage, and discussion sentiment across time periods.
    """

    TIME_PERIOD_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("semester", "Semester"),
    ]

    RISK_LEVEL_CHOICES = [
        ("critical", "Critical - Immediate Action Required"),
        ("high", "High Risk"),
        ("medium", "Medium Risk"),
        ("low", "Low Risk"),
        ("engaged", "Fully Engaged"),
    ]

    heatmap_number = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)
    student_name = models.CharField(max_length=200)

    # Time period
    time_period = models.CharField(
        max_length=20, choices=TIME_PERIOD_CHOICES, default="weekly"
    )
    start_date = models.DateField()
    end_date = models.DateField()

    # Composite engagement score (0-100)
    overall_engagement_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Weighted composite: 40% attendance + 35% LMS + 25% sentiment",
    )

    # Component scores
    attendance_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    lms_activity_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    sentiment_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Normalized sentiment (0=very negative, 100=very positive)",
    )

    # Risk assessment
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES)
    risk_flags = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True,
        help_text="Specific risk indicators: low_attendance, inactive_lms, negative_sentiment, etc.",
    )

    # Heatmap data (JSON structure for visualization)
    heatmap_data = models.JSONField(
        default=dict,
        help_text="Daily engagement data: {date: {attendance: bool, lms_minutes: int, sentiment: float}}",
    )

    # Trends
    engagement_trend = models.CharField(
        max_length=20,
        choices=[
            ("improving", "Improving"),
            ("stable", "Stable"),
            ("declining", "Declining"),
            ("critical_decline", "Critical Decline"),
        ],
        default="stable",
    )
    change_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Percentage change from previous period",
    )

    # Intervention tracking
    alerts_triggered = models.PositiveIntegerField(default=0)
    interventions_applied = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date", "-created_at"]
        indexes = [
            models.Index(fields=["student_id", "-start_date"]),
            models.Index(fields=["risk_level", "tenant"]),
            models.Index(fields=["engagement_trend"]),
        ]
        unique_together = [["student_id", "start_date", "end_date", "time_period"]]
        verbose_name = "Engagement Heatmap"
        verbose_name_plural = "Engagement Heatmaps"

    def save(self, *args, **kwargs):
        if not self.heatmap_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:8].upper()
            self.heatmap_number = f"HEAT-{timestamp}-{unique_id}"

        # Calculate overall engagement score
        self.overall_engagement_score = (
            (self.attendance_score * 0.40)
            + (self.lms_activity_score * 0.35)
            + (self.sentiment_score * 0.25)
        )

        # Determine risk level
        if self.overall_engagement_score >= 80:
            self.risk_level = "engaged"
        elif self.overall_engagement_score >= 60:
            self.risk_level = "low"
        elif self.overall_engagement_score >= 40:
            self.risk_level = "medium"
        elif self.overall_engagement_score >= 25:
            self.risk_level = "high"
        else:
            self.risk_level = "critical"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.heatmap_number} - {self.student_name} ({self.start_date} to {self.end_date})"


class AttendanceRecord(models.Model):
    """
    Daily attendance tracking for engagement analysis.
    """

    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused"),
    ]

    record_number = models.CharField(max_length=50, unique=True, editable=False)
    heatmap = models.ForeignKey(
        EngagementHeatmap, on_delete=models.CASCADE, related_name="attendance_records"
    )
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)

    # Attendance details
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    # Session details
    session_name = models.CharField(max_length=200)
    scheduled_start = models.TimeField()
    scheduled_end = models.TimeField()
    actual_arrival = models.TimeField(null=True, blank=True)
    actual_departure = models.TimeField(null=True, blank=True)

    # Metrics
    minutes_late = models.PositiveIntegerField(default=0)
    minutes_attended = models.PositiveIntegerField(default=0)
    participation_level = models.CharField(
        max_length=20,
        choices=[
            ("high", "High Participation"),
            ("medium", "Medium Participation"),
            ("low", "Low Participation"),
            ("none", "No Participation"),
        ],
        default="medium",
    )

    # Notes
    notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["student_id", "-date"]),
            models.Index(fields=["status", "date"]),
        ]
        unique_together = [["student_id", "date", "session_name"]]
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"

    def save(self, *args, **kwargs):
        if not self.record_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.record_number = f"ATT-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.record_number} - {self.student_id} - {self.date} ({self.status})"


class LMSActivity(models.Model):
    """
    Learning Management System activity tracking.
    Monitors logins, content views, assignment submissions, forum posts.
    """

    ACTIVITY_TYPE_CHOICES = [
        ("login", "Login"),
        ("content_view", "Content View"),
        ("assignment_submit", "Assignment Submission"),
        ("quiz_attempt", "Quiz Attempt"),
        ("forum_post", "Forum Post"),
        ("forum_reply", "Forum Reply"),
        ("resource_download", "Resource Download"),
        ("video_watch", "Video Watch"),
        ("chat_message", "Chat Message"),
    ]

    activity_number = models.CharField(max_length=50, unique=True, editable=False)
    heatmap = models.ForeignKey(
        EngagementHeatmap, on_delete=models.CASCADE, related_name="lms_activities"
    )
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)

    # Activity details
    date = models.DateField(db_index=True)
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPE_CHOICES)
    activity_name = models.CharField(max_length=300)

    # Time tracking
    timestamp = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=0)

    # Engagement metrics
    completion_status = models.CharField(
        max_length=20,
        choices=[
            ("completed", "Completed"),
            ("in_progress", "In Progress"),
            ("started", "Started"),
            ("abandoned", "Abandoned"),
        ],
        default="completed",
    )
    interaction_count = models.PositiveIntegerField(
        default=1, help_text="Number of clicks, views, or interactions"
    )

    # Content metadata
    course_name = models.CharField(max_length=200, blank=True)
    module_name = models.CharField(max_length=200, blank=True)

    # Quality indicators
    quality_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Score for submissions, quiz results, etc.",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["student_id", "-date"]),
            models.Index(fields=["activity_type", "date"]),
        ]
        verbose_name = "LMS Activity"
        verbose_name_plural = "LMS Activities"

    def save(self, *args, **kwargs):
        if not self.activity_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.activity_number = f"LMS-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.activity_number} - {self.activity_type} - {self.date}"


class DiscussionSentiment(models.Model):
    """
    Sentiment analysis of student discussions, forum posts, and messages.
    Tracks tone, emotion, and engagement quality.
    """

    SENTIMENT_LABEL_CHOICES = [
        ("very_positive", "Very Positive"),
        ("positive", "Positive"),
        ("neutral", "Neutral"),
        ("negative", "Negative"),
        ("very_negative", "Very Negative"),
    ]

    EMOTION_CHOICES = [
        ("joy", "Joy"),
        ("interest", "Interest"),
        ("confusion", "Confusion"),
        ("frustration", "Frustration"),
        ("anxiety", "Anxiety"),
        ("anger", "Anger"),
        ("sadness", "Sadness"),
    ]

    sentiment_number = models.CharField(max_length=50, unique=True, editable=False)
    heatmap = models.ForeignKey(
        EngagementHeatmap,
        on_delete=models.CASCADE,
        related_name="discussion_sentiments",
    )
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)

    # Message details
    date = models.DateField(db_index=True)
    timestamp = models.DateTimeField()
    message_type = models.CharField(
        max_length=30,
        choices=[
            ("forum_post", "Forum Post"),
            ("forum_reply", "Forum Reply"),
            ("chat_message", "Chat Message"),
            ("email", "Email"),
            ("feedback", "Feedback"),
        ],
    )
    message_content = models.TextField()

    # Sentiment analysis
    sentiment_score = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(-1), MaxValueValidator(1)],
        help_text="Sentiment polarity: -1 (very negative) to +1 (very positive)",
    )
    sentiment_label = models.CharField(max_length=20, choices=SENTIMENT_LABEL_CHOICES)
    confidence = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Confidence in sentiment classification (0-1)",
    )

    # Emotion detection
    primary_emotion = models.CharField(
        max_length=20, choices=EMOTION_CHOICES, null=True, blank=True
    )
    emotion_scores = models.JSONField(
        default=dict,
        help_text="Emotion probabilities: {joy: 0.2, frustration: 0.6, ...}",
    )

    # Engagement indicators
    word_count = models.PositiveIntegerField(default=0)
    question_count = models.PositiveIntegerField(default=0)
    exclamation_count = models.PositiveIntegerField(default=0)

    # Risk keywords
    negative_keywords = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Detected negative or concerning keywords",
    )
    help_seeking_keywords = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Keywords indicating student needs help",
    )

    # Context
    discussion_topic = models.CharField(max_length=300, blank=True)
    reply_count = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["student_id", "-date"]),
            models.Index(fields=["sentiment_label", "date"]),
        ]
        verbose_name = "Discussion Sentiment"
        verbose_name_plural = "Discussion Sentiments"

    def save(self, *args, **kwargs):
        if not self.sentiment_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.sentiment_number = f"SENT-{timestamp}-{unique_id}"

        # Auto-assign sentiment label based on score
        if self.sentiment_score >= 0.5:
            self.sentiment_label = "very_positive"
        elif self.sentiment_score >= 0.1:
            self.sentiment_label = "positive"
        elif self.sentiment_score >= -0.1:
            self.sentiment_label = "neutral"
        elif self.sentiment_score >= -0.5:
            self.sentiment_label = "negative"
        else:
            self.sentiment_label = "very_negative"

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.sentiment_number} - {self.sentiment_label} ({self.sentiment_score})"
        )


class EngagementAlert(models.Model):
    """
    Automated alerts for engagement risks.
    Visual risk dashboard flags.
    """

    ALERT_TYPE_CHOICES = [
        ("attendance", "Attendance Warning"),
        ("lms_inactivity", "LMS Inactivity"),
        ("negative_sentiment", "Negative Sentiment Detected"),
        ("participation_drop", "Participation Drop"),
        ("overall_engagement", "Overall Engagement Risk"),
        ("discussion_silence", "Discussion Silence"),
        ("deadline_approaching", "Deadline Approaching"),
    ]

    SEVERITY_CHOICES = [
        ("critical", "Critical"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("acknowledged", "Acknowledged"),
        ("resolved", "Resolved"),
        ("dismissed", "Dismissed"),
    ]

    alert_number = models.CharField(max_length=50, unique=True, editable=False)
    heatmap = models.ForeignKey(
        EngagementHeatmap, on_delete=models.CASCADE, related_name="engagement_alerts"
    )
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)
    student_name = models.CharField(max_length=200)

    # Alert details
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    title = models.CharField(max_length=300)
    description = models.TextField()

    # Metrics that triggered alert
    trigger_metrics = models.JSONField(
        default=dict,
        help_text="Metrics that triggered this alert: {attendance_score: 45, days_absent: 5}",
    )

    # Recommendations
    recommended_actions = ArrayField(
        models.TextField(),
        default=list,
        blank=True,
        help_text="Suggested interventions",
    )

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    acknowledged_by = models.CharField(max_length=200, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["student_id", "-created_at"]),
            models.Index(fields=["status", "severity"]),
            models.Index(fields=["alert_type", "tenant"]),
        ]
        verbose_name = "Engagement Alert"
        verbose_name_plural = "Engagement Alerts"

    def save(self, *args, **kwargs):
        if not self.alert_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.alert_number = f"ALERT-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alert_number} - {self.alert_type} - {self.severity}"
