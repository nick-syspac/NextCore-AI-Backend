from django.db import models
from django.utils import timezone
import uuid


class TrainerProfile(models.Model):
    """Extended trainer profile for industry currency verification"""

    profile_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)

    # Trainer information
    trainer_id = models.CharField(max_length=100, db_index=True)
    trainer_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    # Social profiles
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    personal_website = models.URLField(blank=True)

    # Industry details
    primary_industry = models.CharField(max_length=200, blank=True)
    specializations = models.JSONField(default=list)  # List of specializations
    years_experience = models.IntegerField(default=0)

    # Currency status
    last_verified_date = models.DateField(null=True, blank=True)
    currency_status = models.CharField(
        max_length=20,
        choices=[
            ("current", "Current"),
            ("expiring_soon", "Expiring Soon"),
            ("expired", "Expired"),
            ("not_verified", "Not Verified"),
        ],
        default="not_verified",
    )
    currency_score = models.FloatField(default=0.0)  # 0-100 score

    # Verification settings
    auto_verify_enabled = models.BooleanField(default=True)
    verification_frequency_days = models.IntegerField(default=90)
    next_verification_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        unique_together = ["tenant", "trainer_id"]
        indexes = [
            models.Index(fields=["tenant", "trainer_id"]),
            models.Index(fields=["currency_status", "-last_verified_date"]),
        ]

    def __str__(self):
        return f"{self.profile_number} - {self.trainer_name}"

    def save(self, *args, **kwargs):
        if not self.profile_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:8].upper()
            self.profile_number = f"PROFILE-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class VerificationScan(models.Model):
    """Scan jobs for verifying industry currency"""

    scan_number = models.CharField(max_length=50, unique=True, db_index=True)
    trainer_profile = models.ForeignKey(
        TrainerProfile, on_delete=models.CASCADE, related_name="scans"
    )

    # Scan configuration
    scan_type = models.CharField(
        max_length=20,
        choices=[
            ("manual", "Manual Scan"),
            ("scheduled", "Scheduled Scan"),
            ("automatic", "Automatic Scan"),
        ],
        default="manual",
    )
    sources_to_scan = models.JSONField(
        default=list
    )  # ['linkedin', 'github', 'twitter']

    # Scan status
    scan_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("scanning", "Scanning"),
            ("extracting", "Extracting Entities"),
            ("analyzing", "Analyzing"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ],
        default="pending",
    )

    # Results summary
    total_items_found = models.IntegerField(default=0)
    relevant_items_count = models.IntegerField(default=0)
    currency_score = models.FloatField(default=0.0)

    # Processing metadata
    scan_duration_seconds = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["trainer_profile", "-created_at"]),
            models.Index(fields=["scan_status", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.scan_number} - {self.scan_status}"

    def save(self, *args, **kwargs):
        if not self.scan_number:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.scan_number = f"SCAN-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class LinkedInActivity(models.Model):
    """LinkedIn activities extracted from profile"""

    activity_number = models.CharField(max_length=50, unique=True, db_index=True)
    verification_scan = models.ForeignKey(
        VerificationScan, on_delete=models.CASCADE, related_name="linkedin_activities"
    )

    # Activity details
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ("post", "Post/Article"),
            ("comment", "Comment"),
            ("share", "Share"),
            ("certification", "Certification"),
            ("course", "Course Completion"),
            ("project", "Project"),
            ("position", "Work Position"),
            ("skill_endorsement", "Skill Endorsement"),
        ],
    )

    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)

    # Date information
    activity_date = models.DateField(null=True, blank=True)
    date_text = models.CharField(max_length=200, blank=True)  # Raw date text

    # Extracted entities
    skills_mentioned = models.JSONField(default=list)
    technologies = models.JSONField(default=list)
    companies = models.JSONField(default=list)
    keywords = models.JSONField(default=list)

    # Relevance scoring
    relevance_score = models.FloatField(default=0.0)  # 0-1 score
    is_industry_relevant = models.BooleanField(default=False)
    relevance_reasoning = models.TextField(blank=True)

    # Metadata
    raw_data = models.JSONField(default=dict)
    extracted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-activity_date", "-extracted_at"]
        indexes = [
            models.Index(fields=["verification_scan", "-activity_date"]),
            models.Index(fields=["is_industry_relevant", "-relevance_score"]),
        ]

    def __str__(self):
        return f"{self.activity_number} - {self.activity_type}: {self.title[:50]}"

    def save(self, *args, **kwargs):
        if not self.activity_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.activity_number = f"LI-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class GitHubActivity(models.Model):
    """GitHub activities extracted from profile"""

    activity_number = models.CharField(max_length=50, unique=True, db_index=True)
    verification_scan = models.ForeignKey(
        VerificationScan, on_delete=models.CASCADE, related_name="github_activities"
    )

    # Activity details
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ("repository", "Repository"),
            ("commit", "Commit"),
            ("pull_request", "Pull Request"),
            ("issue", "Issue"),
            ("contribution", "Contribution"),
            ("gist", "Gist"),
            ("star", "Star"),
        ],
    )

    repository_name = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)

    # Date information
    activity_date = models.DateField(null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True)

    # Repository metadata
    language = models.CharField(max_length=100, blank=True)
    languages_used = models.JSONField(default=list)
    topics = models.JSONField(default=list)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)

    # Extracted entities
    technologies = models.JSONField(default=list)
    frameworks = models.JSONField(default=list)
    keywords = models.JSONField(default=list)

    # Relevance scoring
    relevance_score = models.FloatField(default=0.0)  # 0-1 score
    is_industry_relevant = models.BooleanField(default=False)
    relevance_reasoning = models.TextField(blank=True)

    # Activity metrics
    commits_count = models.IntegerField(default=0)
    contributions_count = models.IntegerField(default=0)

    # Metadata
    raw_data = models.JSONField(default=dict)
    extracted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-activity_date", "-extracted_at"]
        indexes = [
            models.Index(fields=["verification_scan", "-activity_date"]),
            models.Index(fields=["is_industry_relevant", "-relevance_score"]),
        ]

    def __str__(self):
        return f"{self.activity_number} - {self.activity_type}: {self.repository_name or self.title[:50]}"

    def save(self, *args, **kwargs):
        if not self.activity_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.activity_number = f"GH-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class CurrencyEvidence(models.Model):
    """Generated evidence documents for industry currency"""

    evidence_number = models.CharField(max_length=50, unique=True, db_index=True)
    trainer_profile = models.ForeignKey(
        TrainerProfile, on_delete=models.CASCADE, related_name="currency_evidence"
    )
    verification_scan = models.ForeignKey(
        VerificationScan, on_delete=models.CASCADE, related_name="evidence_documents"
    )

    # Evidence details
    evidence_type = models.CharField(
        max_length=50,
        choices=[
            ("linkedin_summary", "LinkedIn Activity Summary"),
            ("github_summary", "GitHub Activity Summary"),
            ("combined_report", "Combined Currency Report"),
            ("timeline", "Activity Timeline"),
            ("skills_matrix", "Skills Matrix"),
            ("currency_certificate", "Currency Certificate"),
        ],
    )

    title = models.CharField(max_length=300)
    content = models.TextField()  # Markdown or HTML content

    # Date range covered
    evidence_start_date = models.DateField(null=True, blank=True)
    evidence_end_date = models.DateField(null=True, blank=True)

    # Metrics included
    total_activities = models.IntegerField(default=0)
    relevant_activities = models.IntegerField(default=0)
    currency_score = models.FloatField(default=0.0)

    # Evidence metadata
    linkedin_activities_included = models.JSONField(
        default=list
    )  # List of activity IDs
    github_activities_included = models.JSONField(default=list)  # List of activity IDs

    # File storage
    file_format = models.CharField(
        max_length=20,
        choices=[
            ("markdown", "Markdown"),
            ("html", "HTML"),
            ("pdf", "PDF"),
            ("json", "JSON"),
        ],
        default="markdown",
    )
    file_path = models.CharField(max_length=1000, blank=True)
    file_size_kb = models.FloatField(null=True, blank=True)

    # Compliance
    meets_rto_standards = models.BooleanField(default=True)
    compliance_notes = models.TextField(blank=True)

    # Status
    is_approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=200, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["trainer_profile", "-created_at"]),
            models.Index(fields=["verification_scan", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.evidence_number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.evidence_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.evidence_number = f"EVIDENCE-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class EntityExtraction(models.Model):
    """NLP entity extraction results"""

    extraction_number = models.CharField(max_length=50, unique=True, db_index=True)
    verification_scan = models.ForeignKey(
        VerificationScan, on_delete=models.CASCADE, related_name="entity_extractions"
    )

    # Source information
    source_type = models.CharField(
        max_length=20,
        choices=[
            ("linkedin", "LinkedIn"),
            ("github", "GitHub"),
            ("twitter", "Twitter"),
            ("website", "Website"),
        ],
    )
    source_url = models.URLField(blank=True)
    source_text = models.TextField()

    # Extracted entities
    entities = models.JSONField(default=dict)  # {entity_type: [entities]}
    # Example: {
    #   "PERSON": ["John Doe"],
    #   "ORG": ["Microsoft", "Google"],
    #   "TECH": ["Python", "React", "Docker"],
    #   "SKILL": ["Machine Learning", "Web Development"],
    #   "DATE": ["2024", "January 2024"]
    # }

    # Confidence scores
    extraction_confidence = models.FloatField(default=0.0)  # 0-1
    entity_count = models.IntegerField(default=0)

    # Processing metadata
    nlp_model_used = models.CharField(
        max_length=100, blank=True
    )  # e.g., "spacy-en_core_web_lg"
    processing_time_ms = models.FloatField(null=True, blank=True)

    extracted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-extracted_at"]
        indexes = [
            models.Index(fields=["verification_scan", "source_type"]),
        ]

    def __str__(self):
        return f"{self.extraction_number} - {self.source_type}: {self.entity_count} entities"

    def save(self, *args, **kwargs):
        if not self.extraction_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.extraction_number = f"EXTRACT-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)
