from django.db import models
from django.contrib.auth import get_user_model
from tenants.models import Tenant

User = get_user_model()


class MicroCredential(models.Model):
    """
    Represents a micro-credential or short course built from training package units.
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("in_review", "In Review"),
        ("approved", "Approved"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    DELIVERY_MODE_CHOICES = [
        ("online", "Online"),
        ("face_to_face", "Face to Face"),
        ("blended", "Blended"),
        ("workplace", "Workplace"),
    ]

    # Basic Information
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="micro_credentials"
    )
    title = models.CharField(max_length=500)
    code = models.CharField(max_length=100, help_text="Internal course code")
    description = models.TextField(blank=True)

    # Course Details
    duration_hours = models.PositiveIntegerField(help_text="Total duration in hours")
    delivery_mode = models.CharField(
        max_length=50, choices=DELIVERY_MODE_CHOICES, default="blended"
    )
    target_audience = models.TextField(blank=True)
    learning_outcomes = models.JSONField(
        default=list, help_text="List of learning outcomes"
    )

    # Units and Structure
    source_units = models.JSONField(
        default=list,
        help_text="List of units used: [{code, title, nominal_hours, elements}]",
    )
    compressed_content = models.JSONField(
        default=dict,
        help_text="Compressed curriculum with key competencies and assessment tasks",
    )

    # Metadata and Tagging
    tags = models.JSONField(
        default=list, help_text="Searchable tags for categorization"
    )
    skills_covered = models.JSONField(default=list, help_text="List of specific skills")
    industry_sectors = models.JSONField(
        default=list, help_text="Relevant industry sectors"
    )
    aqf_level = models.CharField(
        max_length=50, blank=True, help_text="Equivalent AQF level"
    )

    # Assessment
    assessment_strategy = models.TextField(blank=True)
    assessment_tasks = models.JSONField(
        default=list, help_text="List of assessment tasks with mapping to elements"
    )

    # Pricing and Enrollment
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    prerequisites = models.TextField(blank=True)

    # Status and Tracking
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="draft")
    gpt_generated = models.BooleanField(default=False)
    gpt_model_used = models.CharField(max_length=100, blank=True)
    generation_time_seconds = models.FloatField(null=True, blank=True)

    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_micro_credentials",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["tenant", "code"]]

    def __str__(self):
        return f"{self.code} - {self.title}"


class MicroCredentialVersion(models.Model):
    """
    Version history for micro-credentials to track changes over time.
    """

    micro_credential = models.ForeignKey(
        MicroCredential, on_delete=models.CASCADE, related_name="versions"
    )
    version_number = models.PositiveIntegerField()
    change_summary = models.TextField()
    content_snapshot = models.JSONField(
        help_text="Full snapshot of the micro-credential at this version"
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-version_number"]
        unique_together = [["micro_credential", "version_number"]]

    def __str__(self):
        return f"{self.micro_credential.code} v{self.version_number}"


class MicroCredentialEnrollment(models.Model):
    """
    Track enrollments in micro-credentials.
    """

    STATUS_CHOICES = [
        ("enrolled", "Enrolled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("withdrawn", "Withdrawn"),
    ]

    micro_credential = models.ForeignKey(
        MicroCredential, on_delete=models.CASCADE, related_name="enrollments"
    )
    student_name = models.CharField(max_length=200)
    student_email = models.EmailField()
    student_id = models.CharField(max_length=100, blank=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="enrolled")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)

    progress_data = models.JSONField(
        default=dict, help_text="Track completion of learning outcomes and assessments"
    )

    class Meta:
        ordering = ["-enrolled_at"]
        unique_together = [["micro_credential", "student_email"]]

    def __str__(self):
        return f"{self.student_name} - {self.micro_credential.title}"
