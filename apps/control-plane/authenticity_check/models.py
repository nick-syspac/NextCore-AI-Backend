from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import hashlib
import json
from datetime import datetime


class AuthenticityCheck(models.Model):
    """Master model for authenticity checking with plagiarism and integrity analysis"""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("flagged", "Flagged"),
        ("reviewed", "Reviewed"),
    ]

    check_number = models.CharField(max_length=50, unique=True, editable=False)
    assessment = models.ForeignKey(
        "assessment_builder.Assessment",
        on_delete=models.CASCADE,
        related_name="authenticity_checks",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Configuration
    plagiarism_threshold = models.FloatField(
        default=0.7,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Similarity threshold for plagiarism detection (0.0-1.0)",
    )
    metadata_verification_enabled = models.BooleanField(default=True)
    anomaly_detection_enabled = models.BooleanField(default=True)
    academic_integrity_mode = models.BooleanField(
        default=True, help_text="Enable strict academic integrity compliance"
    )

    # Status and statistics
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_submissions_checked = models.IntegerField(default=0)
    plagiarism_cases_detected = models.IntegerField(default=0)
    metadata_issues_found = models.IntegerField(default=0)
    anomalies_detected = models.IntegerField(default=0)
    overall_integrity_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Overall integrity score (0-100)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="authenticity_checks_created",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Authenticity Check"
        verbose_name_plural = "Authenticity Checks"

    def __str__(self):
        return f"{self.check_number} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.check_number:
            date_str = timezone.now().strftime("%Y%m%d")
            last_check = (
                AuthenticityCheck.objects.filter(
                    check_number__startswith=f"AUTH-{date_str}-"
                )
                .order_by("-check_number")
                .first()
            )

            if last_check:
                last_number = int(last_check.check_number.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.check_number = f"AUTH-{date_str}-{new_number:06d}"

        super().save(*args, **kwargs)

    def calculate_overall_score(self):
        """Calculate overall integrity score based on all analyses"""
        analyses = self.submission_analyses.all()
        if not analyses:
            return 0.0

        total_score = sum(a.combined_integrity_score for a in analyses)
        self.overall_integrity_score = total_score / len(analyses)
        self.save(update_fields=["overall_integrity_score"])
        return self.overall_integrity_score


class SubmissionAnalysis(models.Model):
    """Individual submission analysis with plagiarism, metadata, and anomaly scores"""

    INTEGRITY_STATUS_CHOICES = [
        ("pass", "Pass"),
        ("warning", "Warning"),
        ("fail", "Fail"),
        ("under_review", "Under Review"),
    ]

    analysis_number = models.CharField(max_length=50, unique=True, editable=False)
    authenticity_check = models.ForeignKey(
        AuthenticityCheck, on_delete=models.CASCADE, related_name="submission_analyses"
    )
    submission_id = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100, blank=True)
    student_name = models.CharField(max_length=255, blank=True)

    # Content analysis
    submission_content = models.TextField()
    content_hash = models.CharField(max_length=64, editable=False)
    word_count = models.IntegerField(default=0)
    character_count = models.IntegerField(default=0)

    # Embeddings for comparison
    content_embedding = models.JSONField(
        default=list,
        help_text="384-dimensional embedding vector for similarity comparison",
    )

    # Scores
    plagiarism_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Plagiarism similarity score (0.0-1.0)",
    )
    metadata_verification_score = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Metadata verification score (0-100)",
    )
    anomaly_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Anomaly detection score (0-100, higher is more suspicious)",
    )
    combined_integrity_score = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Combined integrity score (0-100)",
    )

    # Analysis results
    integrity_status = models.CharField(
        max_length=20, choices=INTEGRITY_STATUS_CHOICES, default="pass"
    )
    plagiarism_detected = models.BooleanField(default=False)
    metadata_issues = models.BooleanField(default=False)
    anomalies_found = models.BooleanField(default=False)

    # Additional data
    analysis_metadata = models.JSONField(
        default=dict,
        help_text="Additional analysis metadata (language, typing patterns, etc.)",
    )

    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-analyzed_at"]
        verbose_name = "Submission Analysis"
        verbose_name_plural = "Submission Analyses"

    def __str__(self):
        return f"{self.analysis_number} - {self.student_name or self.submission_id}"

    def save(self, *args, **kwargs):
        if not self.analysis_number:
            date_str = timezone.now().strftime("%Y%m%d")
            last_analysis = (
                SubmissionAnalysis.objects.filter(
                    analysis_number__startswith=f"ANA-{date_str}-"
                )
                .order_by("-analysis_number")
                .first()
            )

            if last_analysis:
                last_number = int(last_analysis.analysis_number.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.analysis_number = f"ANA-{date_str}-{new_number:06d}"

        # Generate content hash
        if self.submission_content and not self.content_hash:
            self.content_hash = hashlib.sha256(
                self.submission_content.encode("utf-8")
            ).hexdigest()

        # Calculate word and character counts
        if self.submission_content:
            self.word_count = len(self.submission_content.split())
            self.character_count = len(self.submission_content)

        super().save(*args, **kwargs)

    def calculate_combined_score(self):
        """Calculate combined integrity score from individual scores"""
        # Lower is better for plagiarism and anomalies
        plagiarism_penalty = self.plagiarism_score * 100
        anomaly_penalty = self.anomaly_score

        # Start with 100 and subtract penalties
        score = 100.0
        score -= plagiarism_penalty * 0.5  # 50% weight for plagiarism
        score -= (
            100 - self.metadata_verification_score
        ) * 0.2  # 20% weight for metadata
        score -= anomaly_penalty * 0.3  # 30% weight for anomalies

        self.combined_integrity_score = max(0.0, min(100.0, score))

        # Update integrity status
        if self.combined_integrity_score >= 80:
            self.integrity_status = "pass"
        elif self.combined_integrity_score >= 60:
            self.integrity_status = "warning"
        else:
            self.integrity_status = "fail"

        self.save(update_fields=["combined_integrity_score", "integrity_status"])
        return self.combined_integrity_score


class PlagiarismMatch(models.Model):
    """Detected plagiarism matches between submissions"""

    MATCH_TYPE_CHOICES = [
        ("exact", "Exact Match"),
        ("paraphrased", "Paraphrased"),
        ("structural", "Structural Similarity"),
        ("embedding", "Embedding Similarity"),
    ]

    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    match_number = models.CharField(max_length=50, unique=True, editable=False)
    source_analysis = models.ForeignKey(
        SubmissionAnalysis,
        on_delete=models.CASCADE,
        related_name="plagiarism_matches_as_source",
    )
    matched_analysis = models.ForeignKey(
        SubmissionAnalysis,
        on_delete=models.CASCADE,
        related_name="plagiarism_matches_as_match",
    )

    similarity_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Similarity score between submissions (0.0-1.0)",
    )
    match_type = models.CharField(
        max_length=20, choices=MATCH_TYPE_CHOICES, default="embedding"
    )
    severity = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, default="medium"
    )

    # Matched content details
    matched_text_segments = models.JSONField(
        default=list, help_text="List of matched text segments with positions"
    )
    matched_words_count = models.IntegerField(default=0)
    matched_percentage = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Percentage of text that matches",
    )

    # Review status
    reviewed = models.BooleanField(default=False)
    false_positive = models.BooleanField(default=False)
    review_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-similarity_score", "-detected_at"]
        verbose_name = "Plagiarism Match"
        verbose_name_plural = "Plagiarism Matches"

    def __str__(self):
        return f"{self.match_number} - {self.similarity_score:.2%} similarity"

    def save(self, *args, **kwargs):
        if not self.match_number:
            date_str = timezone.now().strftime("%Y%m%d")
            last_match = (
                PlagiarismMatch.objects.filter(
                    match_number__startswith=f"PLG-{date_str}-"
                )
                .order_by("-match_number")
                .first()
            )

            if last_match:
                last_number = int(last_match.match_number.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.match_number = f"PLG-{date_str}-{new_number:06d}"

        # Determine severity based on similarity score
        if self.similarity_score >= 0.9:
            self.severity = "critical"
        elif self.similarity_score >= 0.75:
            self.severity = "high"
        elif self.similarity_score >= 0.6:
            self.severity = "medium"
        else:
            self.severity = "low"

        super().save(*args, **kwargs)


class MetadataVerification(models.Model):
    """Verification of submission metadata for authenticity"""

    VERIFICATION_STATUS_CHOICES = [
        ("verified", "Verified"),
        ("suspicious", "Suspicious"),
        ("anomalous", "Anomalous"),
        ("failed", "Failed"),
    ]

    verification_number = models.CharField(max_length=50, unique=True, editable=False)
    submission_analysis = models.ForeignKey(
        SubmissionAnalysis,
        on_delete=models.CASCADE,
        related_name="metadata_verifications",
    )

    # File metadata
    file_metadata = models.JSONField(
        default=dict,
        help_text="Complete file metadata (EXIF, document properties, etc.)",
    )
    creation_timestamp = models.DateTimeField(null=True, blank=True)
    modification_timestamp = models.DateTimeField(null=True, blank=True)
    modification_history = models.JSONField(
        default=list, help_text="History of file modifications"
    )

    # Author information
    author_info = models.JSONField(
        default=dict, help_text="Author metadata from file (if available)"
    )
    author_matches_student = models.BooleanField(null=True, blank=True)

    # Verification results
    verification_status = models.CharField(
        max_length=20, choices=VERIFICATION_STATUS_CHOICES, default="verified"
    )
    anomalies_detected = models.JSONField(
        default=list, help_text="List of detected metadata anomalies"
    )
    verification_score = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Verification score (0-100)",
    )

    # Timestamps
    verified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-verified_at"]
        verbose_name = "Metadata Verification"
        verbose_name_plural = "Metadata Verifications"

    def __str__(self):
        return f"{self.verification_number} - {self.verification_status}"

    def save(self, *args, **kwargs):
        if not self.verification_number:
            date_str = timezone.now().strftime("%Y%m%d")
            last_verification = (
                MetadataVerification.objects.filter(
                    verification_number__startswith=f"VER-{date_str}-"
                )
                .order_by("-verification_number")
                .first()
            )

            if last_verification:
                last_number = int(last_verification.verification_number.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.verification_number = f"VER-{date_str}-{new_number:06d}"

        # Determine verification status based on anomalies
        if self.anomalies_detected:
            anomaly_count = len(self.anomalies_detected)
            if anomaly_count >= 3:
                self.verification_status = "failed"
                self.verification_score = max(0, 100 - (anomaly_count * 30))
            elif anomaly_count >= 2:
                self.verification_status = "anomalous"
                self.verification_score = max(0, 100 - (anomaly_count * 20))
            else:
                self.verification_status = "suspicious"
                self.verification_score = max(0, 100 - (anomaly_count * 15))
        else:
            self.verification_status = "verified"
            self.verification_score = 100.0

        super().save(*args, **kwargs)


class AnomalyDetection(models.Model):
    """Detection of behavioral and pattern anomalies in submissions"""

    ANOMALY_TYPE_CHOICES = [
        ("typing_speed", "Unusual Typing Speed"),
        ("paste_events", "Excessive Paste Events"),
        ("time_gaps", "Suspicious Time Gaps"),
        ("behavioral", "Behavioral Anomaly"),
        ("pattern", "Pattern Anomaly"),
        ("statistical", "Statistical Anomaly"),
    ]

    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    anomaly_number = models.CharField(max_length=50, unique=True, editable=False)
    submission_analysis = models.ForeignKey(
        SubmissionAnalysis, on_delete=models.CASCADE, related_name="anomaly_detections"
    )

    anomaly_type = models.CharField(max_length=20, choices=ANOMALY_TYPE_CHOICES)
    severity = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, default="medium"
    )

    # Anomaly details
    anomaly_data = models.JSONField(
        default=dict, help_text="Detailed anomaly data and evidence"
    )
    description = models.TextField()
    confidence_score = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Confidence in anomaly detection (0.0-1.0)",
    )

    # Impact
    impact_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Impact on integrity score (0-100)",
    )

    # Review
    acknowledged = models.BooleanField(default=False)
    false_positive = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)

    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-severity", "-detected_at"]
        verbose_name = "Anomaly Detection"
        verbose_name_plural = "Anomaly Detections"

    def __str__(self):
        return f"{self.anomaly_number} - {self.get_anomaly_type_display()} ({self.severity})"

    def save(self, *args, **kwargs):
        if not self.anomaly_number:
            date_str = timezone.now().strftime("%Y%m%d")
            last_anomaly = (
                AnomalyDetection.objects.filter(
                    anomaly_number__startswith=f"ANM-{date_str}-"
                )
                .order_by("-anomaly_number")
                .first()
            )

            if last_anomaly:
                last_number = int(last_anomaly.anomaly_number.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.anomaly_number = f"ANM-{date_str}-{new_number:06d}"

        # Calculate impact score based on severity and confidence
        severity_multiplier = {
            "low": 0.25,
            "medium": 0.5,
            "high": 0.75,
            "critical": 1.0,
        }
        self.impact_score = (
            severity_multiplier.get(self.severity, 0.5) * self.confidence_score * 100
        )

        super().save(*args, **kwargs)
