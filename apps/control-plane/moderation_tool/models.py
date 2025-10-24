from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
import secrets
import json


class ModerationSession(models.Model):
    """
    A moderation session comparing assessor decisions for fairness validation.
    """
    SESSION_STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    ASSESSMENT_TYPE_CHOICES = [
        ('exam', 'Exam'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('practical', 'Practical'),
        ('portfolio', 'Portfolio'),
    ]
    
    session_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assessment_type = models.CharField(max_length=50, choices=ASSESSMENT_TYPE_CHOICES, default='exam')
    
    # Assessment details
    assessment_title = models.CharField(max_length=200)
    total_submissions = models.IntegerField(default=0)
    assessors_count = models.IntegerField(default=0)
    
    # Moderation settings
    outlier_threshold = models.FloatField(
        default=2.0,
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)],
        help_text="Standard deviations for outlier detection"
    )
    bias_sensitivity = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Sensitivity level for bias detection (1=low, 10=high)"
    )
    
    # Status
    status = models.CharField(max_length=20, choices=SESSION_STATUS_CHOICES, default='active')
    
    # Statistics
    outliers_detected = models.IntegerField(default=0)
    bias_flags_raised = models.IntegerField(default=0)
    decisions_compared = models.IntegerField(default=0)
    average_agreement_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['assessment_type']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.session_number:
            date_str = datetime.now().strftime('%Y%m%d')
            random_suffix = secrets.token_hex(3).upper()
            self.session_number = f"MOD-{date_str}-{random_suffix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.session_number} - {self.name}"
    
    def get_fairness_score(self):
        """Calculate overall fairness score (0-100)"""
        if self.decisions_compared == 0:
            return 0
        
        agreement_component = self.average_agreement_rate * 50
        outlier_penalty = min((self.outliers_detected / max(self.decisions_compared, 1)) * 25, 25)
        bias_penalty = min((self.bias_flags_raised / max(self.decisions_compared, 1)) * 25, 25)
        
        return max(0, agreement_component + 50 - outlier_penalty - bias_penalty)


class AssessorDecision(models.Model):
    """
    Individual assessor's marking decision for moderation comparison.
    """
    GRADE_CHOICES = [
        ('HD', 'High Distinction'),
        ('D', 'Distinction'),
        ('C', 'Credit'),
        ('P', 'Pass'),
        ('F', 'Fail'),
        ('NYC', 'Not Yet Competent'),
        ('C', 'Competent'),
    ]
    
    decision_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    session = models.ForeignKey(ModerationSession, on_delete=models.CASCADE, related_name='decisions')
    
    # Student info
    student_id = models.CharField(max_length=100)
    student_name = models.CharField(max_length=200, blank=True)
    submission_id = models.CharField(max_length=100)
    
    # Assessor info
    assessor_id = models.CharField(max_length=100)
    assessor_name = models.CharField(max_length=200)
    
    # Decision details
    score = models.FloatField(validators=[MinValueValidator(0)])
    max_score = models.FloatField(validators=[MinValueValidator(0)])
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    
    # Detailed scoring (JSON)
    criterion_scores = models.JSONField(
        default=dict,
        help_text="Dictionary of criterion_id -> score"
    )
    
    # Flags
    is_outlier = models.BooleanField(default=False)
    has_bias_flag = models.BooleanField(default=False)
    requires_review = models.BooleanField(default=False)
    
    # Justification
    comments = models.TextField(blank=True)
    marking_time_minutes = models.IntegerField(null=True, blank=True)
    
    # Audit
    marked_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-marked_at']
        indexes = [
            models.Index(fields=['session', 'student_id']),
            models.Index(fields=['assessor_id']),
            models.Index(fields=['is_outlier']),
            models.Index(fields=['has_bias_flag']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.decision_number:
            date_str = datetime.now().strftime('%Y%m%d')
            random_suffix = secrets.token_hex(3).upper()
            self.decision_number = f"DEC-{date_str}-{random_suffix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.decision_number} - {self.assessor_name} -> {self.student_id}"
    
    def get_percentage_score(self):
        """Calculate percentage score"""
        if self.max_score == 0:
            return 0
        return (self.score / self.max_score) * 100


class OutlierDetection(models.Model):
    """
    Detected outliers in assessor decisions with statistical analysis.
    """
    OUTLIER_TYPE_CHOICES = [
        ('high_scorer', 'High Scorer'),
        ('low_scorer', 'Low Scorer'),
        ('inconsistent', 'Inconsistent'),
        ('statistical', 'Statistical Anomaly'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    outlier_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    session = models.ForeignKey(ModerationSession, on_delete=models.CASCADE, related_name='outliers')
    decision = models.ForeignKey(AssessorDecision, on_delete=models.CASCADE, related_name='outlier_flags')
    
    # Outlier details
    outlier_type = models.CharField(max_length=50, choices=OUTLIER_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    
    # Statistical measures
    z_score = models.FloatField(help_text="Standard deviations from mean")
    deviation_percentage = models.FloatField(help_text="Percentage deviation from average")
    expected_score = models.FloatField()
    actual_score = models.FloatField()
    
    # Comparison data
    cohort_mean = models.FloatField()
    cohort_std_dev = models.FloatField()
    assessor_mean = models.FloatField(help_text="Assessor's average score across all submissions")
    
    # Analysis
    explanation = models.TextField()
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Confidence in outlier detection (0-1)"
    )
    
    # Resolution
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    resolved_by = models.CharField(max_length=100, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Audit
    detected_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-severity', '-detected_at']
        indexes = [
            models.Index(fields=['session', 'severity']),
            models.Index(fields=['is_resolved']),
            models.Index(fields=['detected_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.outlier_number:
            date_str = datetime.now().strftime('%Y%m%d')
            random_suffix = secrets.token_hex(3).upper()
            self.outlier_number = f"OUT-{date_str}-{random_suffix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.outlier_number} - {self.outlier_type} ({self.severity})"


class BiasScore(models.Model):
    """
    Bias detection and scoring for assessor fairness analysis.
    """
    BIAS_TYPE_CHOICES = [
        ('leniency', 'Leniency Bias'),
        ('severity', 'Severity Bias'),
        ('central_tendency', 'Central Tendency Bias'),
        ('halo_effect', 'Halo Effect'),
        ('recency', 'Recency Bias'),
        ('demographic', 'Demographic Bias'),
        ('timing', 'Timing Bias'),
    ]
    
    bias_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    session = models.ForeignKey(ModerationSession, on_delete=models.CASCADE, related_name='bias_scores')
    
    # Target
    assessor_id = models.CharField(max_length=100)
    assessor_name = models.CharField(max_length=200)
    
    # Bias details
    bias_type = models.CharField(max_length=50, choices=BIAS_TYPE_CHOICES)
    bias_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Bias score (0=no bias, 1=severe bias)"
    )
    
    # Statistical evidence
    sample_size = models.IntegerField(help_text="Number of decisions analyzed")
    mean_difference = models.FloatField(help_text="Difference from cohort mean")
    std_dev_ratio = models.FloatField(help_text="Ratio to cohort standard deviation")
    
    # Detailed analysis
    evidence = models.JSONField(
        default=dict,
        help_text="Statistical evidence and patterns detected"
    )
    affected_students = models.JSONField(
        default=list,
        help_text="List of student IDs affected by bias"
    )
    
    # Validation
    is_validated = models.BooleanField(default=False)
    validation_notes = models.TextField(blank=True)
    validated_by = models.CharField(max_length=100, blank=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    
    # Recommendations
    recommendation = models.TextField(help_text="Action recommended to address bias")
    severity_level = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Severity level (1=minor, 10=critical)"
    )
    
    # Audit
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-bias_score', '-calculated_at']
        indexes = [
            models.Index(fields=['session', 'assessor_id']),
            models.Index(fields=['bias_type']),
            models.Index(fields=['is_validated']),
            models.Index(fields=['calculated_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.bias_number:
            date_str = datetime.now().strftime('%Y%m%d')
            random_suffix = secrets.token_hex(3).upper()
            self.bias_number = f"BIAS-{date_str}-{random_suffix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.bias_number} - {self.bias_type} ({self.bias_score:.2f})"
    
    def get_severity_label(self):
        """Get human-readable severity label"""
        if self.severity_level <= 3:
            return "Minor"
        elif self.severity_level <= 6:
            return "Moderate"
        elif self.severity_level <= 8:
            return "Significant"
        else:
            return "Critical"


class ModerationLog(models.Model):
    """
    Audit log for moderation actions and comparisons.
    """
    ACTION_CHOICES = [
        ('session_created', 'Session Created'),
        ('decision_added', 'Decision Added'),
        ('outlier_detected', 'Outlier Detected'),
        ('bias_calculated', 'Bias Calculated'),
        ('comparison_run', 'Comparison Run'),
        ('validation_completed', 'Validation Completed'),
        ('session_completed', 'Session Completed'),
    ]
    
    session = models.ForeignKey(ModerationSession, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    
    # Metrics
    decisions_processed = models.IntegerField(default=0)
    outliers_found = models.IntegerField(default=0)
    bias_flags = models.IntegerField(default=0)
    
    # Performance
    processing_time_ms = models.IntegerField(null=True, blank=True)
    
    # User
    performed_by = models.CharField(max_length=100, blank=True)
    
    # Audit
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['session', 'action']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
