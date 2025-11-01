from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

User = get_user_model()


class RiskAssessment(models.Model):
    """Master risk assessment tracking dropout predictions"""

    RISK_LEVEL_CHOICES = [
        ("low", "Low Risk"),
        ("medium", "Medium Risk"),
        ("high", "High Risk"),
        ("critical", "Critical Risk"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("monitoring", "Monitoring"),
        ("intervention_required", "Intervention Required"),
        ("resolved", "Resolved"),
        ("dropped_out", "Dropped Out"),
    ]

    assessment_number = models.CharField(max_length=50, unique=True, editable=False)
    student_id = models.CharField(max_length=100)
    student_name = models.CharField(max_length=255)

    # Risk scores
    dropout_probability = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Predicted dropout probability (0.0 - 1.0)",
    )
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES)
    risk_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Overall risk score (0-100)",
    )

    # Component scores
    engagement_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Engagement level score",
    )
    performance_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Academic performance score",
    )
    attendance_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Attendance rate score",
    )
    sentiment_score = models.FloatField(
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
        help_text="Sentiment analysis score (-1.0 to 1.0)",
    )

    # Model information
    model_version = models.CharField(max_length=50, default="logistic_v1.0")
    confidence = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Model confidence percentage",
    )

    # Status and metadata
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="active")
    assessment_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # Alert tracking
    alert_triggered = models.BooleanField(default=False)
    alert_acknowledged = models.BooleanField(default=False)
    alert_acknowledged_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acknowledged_alerts",
    )
    alert_acknowledged_at = models.DateTimeField(null=True, blank=True)

    # Intervention tracking
    intervention_assigned = models.BooleanField(default=False)
    intervention_notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="risk_assessments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-assessment_date", "-created_at"]
        indexes = [
            models.Index(fields=["student_id", "-assessment_date"]),
            models.Index(fields=["risk_level", "status"]),
            models.Index(fields=["alert_triggered", "alert_acknowledged"]),
        ]

    def save(self, *args, **kwargs):
        if not self.assessment_number:
            # Generate assessment number: RISK-YYYYMMDD-XXXXXX
            today = datetime.now()
            date_str = today.strftime("%Y%m%d")
            count = RiskAssessment.objects.filter(
                assessment_number__startswith=f"RISK-{date_str}"
            ).count()
            self.assessment_number = f"RISK-{date_str}-{str(count + 1).zfill(6)}"

        # Auto-assign risk level based on dropout probability
        if self.dropout_probability >= 0.75:
            self.risk_level = "critical"
        elif self.dropout_probability >= 0.50:
            self.risk_level = "high"
        elif self.dropout_probability >= 0.25:
            self.risk_level = "medium"
        else:
            self.risk_level = "low"

        # Trigger alert for high and critical risk
        if self.risk_level in ["high", "critical"] and not self.alert_triggered:
            self.alert_triggered = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.assessment_number} - {self.student_name} ({self.risk_level})"


class RiskFactor(models.Model):
    """Individual risk factors contributing to dropout prediction"""

    FACTOR_TYPE_CHOICES = [
        ("academic", "Academic Performance"),
        ("attendance", "Attendance"),
        ("engagement", "Engagement"),
        ("behavioral", "Behavioral"),
        ("socioeconomic", "Socioeconomic"),
        ("personal", "Personal Circumstances"),
        ("sentiment", "Sentiment Analysis"),
    ]

    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    factor_number = models.CharField(max_length=50, unique=True, editable=False)
    assessment = models.ForeignKey(
        RiskAssessment, on_delete=models.CASCADE, related_name="risk_factors"
    )

    factor_type = models.CharField(max_length=20, choices=FACTOR_TYPE_CHOICES)
    factor_name = models.CharField(max_length=255)
    description = models.TextField()

    # Factor metrics
    weight = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Factor weight in model (0.0 - 1.0)",
    )
    contribution = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Contribution to overall risk (%)",
    )
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)

    # Data points
    current_value = models.FloatField(help_text="Current measured value")
    threshold_value = models.FloatField(help_text="Risk threshold value")
    threshold_exceeded = models.BooleanField(default=False)

    # Trend analysis
    trend = models.CharField(
        max_length=20,
        choices=[
            ("improving", "Improving"),
            ("stable", "Stable"),
            ("declining", "Declining"),
            ("critical_decline", "Critical Decline"),
        ],
        default="stable",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-contribution", "-weight"]

    def save(self, *args, **kwargs):
        if not self.factor_number:
            # Generate factor number: RF-YYYYMMDD-XXXXXX
            today = datetime.now()
            date_str = today.strftime("%Y%m%d")
            count = RiskFactor.objects.filter(
                factor_number__startswith=f"RF-{date_str}"
            ).count()
            self.factor_number = f"RF-{date_str}-{str(count + 1).zfill(6)}"

        # Determine if threshold is exceeded
        self.threshold_exceeded = self.current_value < self.threshold_value

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.factor_number} - {self.factor_name}"


class StudentEngagementMetric(models.Model):
    """Student engagement data for risk modeling"""

    metric_number = models.CharField(max_length=50, unique=True, editable=False)
    student_id = models.CharField(max_length=100, db_index=True)
    student_name = models.CharField(max_length=255)

    # Engagement metrics
    login_frequency = models.IntegerField(help_text="Logins per week")
    time_on_platform = models.FloatField(help_text="Hours per week")
    assignment_submission_rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Assignment submission rate (%)",
    )
    forum_participation = models.IntegerField(help_text="Forum posts/comments count")
    peer_interaction_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Peer interaction score",
    )

    # Activity patterns
    last_login = models.DateTimeField(null=True, blank=True)
    days_inactive = models.IntegerField(default=0)
    activity_decline_rate = models.FloatField(
        default=0.0, help_text="Week-over-week decline %"
    )

    # Engagement score
    overall_engagement_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Composite engagement score",
    )

    measurement_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-measurement_date"]
        indexes = [
            models.Index(fields=["student_id", "-measurement_date"]),
        ]

    def save(self, *args, **kwargs):
        if not self.metric_number:
            # Generate metric number: ENG-YYYYMMDD-XXXXXX
            today = datetime.now()
            date_str = today.strftime("%Y%m%d")
            count = StudentEngagementMetric.objects.filter(
                metric_number__startswith=f"ENG-{date_str}"
            ).count()
            self.metric_number = f"ENG-{date_str}-{str(count + 1).zfill(6)}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.metric_number} - {self.student_name}"


class SentimentAnalysis(models.Model):
    """Sentiment analysis of student communications for risk assessment"""

    SENTIMENT_CHOICES = [
        ("very_negative", "Very Negative"),
        ("negative", "Negative"),
        ("neutral", "Neutral"),
        ("positive", "Positive"),
        ("very_positive", "Very Positive"),
    ]

    analysis_number = models.CharField(max_length=50, unique=True, editable=False)
    assessment = models.ForeignKey(
        RiskAssessment, on_delete=models.CASCADE, related_name="sentiment_analyses"
    )

    # Source information
    source_type = models.CharField(
        max_length=50,
        choices=[
            ("email", "Email"),
            ("forum_post", "Forum Post"),
            ("chat", "Chat Message"),
            ("feedback", "Feedback Form"),
            ("survey", "Survey Response"),
        ],
    )
    text_sample = models.TextField(help_text="Sample text analyzed")

    # Sentiment scores
    sentiment_score = models.FloatField(
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
        help_text="Sentiment score (-1.0 = very negative, 1.0 = very positive)",
    )
    sentiment_label = models.CharField(max_length=20, choices=SENTIMENT_CHOICES)
    confidence = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Sentiment model confidence",
    )

    # Emotion detection
    frustration_detected = models.BooleanField(default=False)
    stress_detected = models.BooleanField(default=False)
    confusion_detected = models.BooleanField(default=False)
    disengagement_detected = models.BooleanField(default=False)

    # Keywords and patterns
    negative_keywords = models.JSONField(default=list, blank=True)
    risk_indicators = models.JSONField(default=list, blank=True)

    analysis_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-analysis_date"]
        verbose_name_plural = "Sentiment analyses"

    def save(self, *args, **kwargs):
        if not self.analysis_number:
            # Generate analysis number: SENT-YYYYMMDD-XXXXXX
            today = datetime.now()
            date_str = today.strftime("%Y%m%d")
            count = SentimentAnalysis.objects.filter(
                analysis_number__startswith=f"SENT-{date_str}"
            ).count()
            self.analysis_number = f"SENT-{date_str}-{str(count + 1).zfill(6)}"

        # Auto-assign sentiment label based on score
        if self.sentiment_score <= -0.6:
            self.sentiment_label = "very_negative"
        elif self.sentiment_score <= -0.2:
            self.sentiment_label = "negative"
        elif self.sentiment_score <= 0.2:
            self.sentiment_label = "neutral"
        elif self.sentiment_score <= 0.6:
            self.sentiment_label = "positive"
        else:
            self.sentiment_label = "very_positive"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.analysis_number} - {self.sentiment_label}"


class InterventionAction(models.Model):
    """Intervention actions taken for at-risk students"""

    ACTION_TYPE_CHOICES = [
        ("email_outreach", "Email Outreach"),
        ("phone_call", "Phone Call"),
        ("meeting_scheduled", "Meeting Scheduled"),
        ("counseling_referral", "Counseling Referral"),
        ("academic_support", "Academic Support"),
        ("mentoring", "Mentoring Assignment"),
        ("course_adjustment", "Course Adjustment"),
        ("financial_support", "Financial Support Referral"),
    ]

    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    action_number = models.CharField(max_length=50, unique=True, editable=False)
    assessment = models.ForeignKey(
        RiskAssessment, on_delete=models.CASCADE, related_name="interventions"
    )

    action_type = models.CharField(max_length=30, choices=ACTION_TYPE_CHOICES)
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("urgent", "Urgent"),
        ],
        default="medium",
    )

    # Scheduling
    scheduled_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")

    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_interventions",
    )

    # Outcomes
    outcome_notes = models.TextField(blank=True)
    effectiveness_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text="Effectiveness rating (1-5)",
    )

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_interventions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_date", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.action_number:
            # Generate action number: INT-YYYYMMDD-XXXXXX
            today = datetime.now()
            date_str = today.strftime("%Y%m%d")
            count = InterventionAction.objects.filter(
                action_number__startswith=f"INT-{date_str}"
            ).count()
            self.action_number = f"INT-{date_str}-{str(count + 1).zfill(6)}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action_number} - {self.action_type}"
