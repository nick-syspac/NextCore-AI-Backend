from django.db import models
from django.utils import timezone
import uuid


class TrainerQualification(models.Model):
    """Store trainer qualifications and certifications"""

    QUALIFICATION_TYPES = [
        ("certificate_iii", "Certificate III"),
        ("certificate_iv", "Certificate IV"),
        ("diploma", "Diploma"),
        ("advanced_diploma", "Advanced Diploma"),
        ("bachelor", "Bachelor Degree"),
        ("master", "Master Degree"),
        ("tae_cert_iv", "TAE40116/TAE40122"),
        ("industry_cert", "Industry Certification"),
        ("other", "Other"),
    ]

    VERIFICATION_STATUS = [
        ("verified", "Verified"),
        ("pending", "Pending Verification"),
        ("expired", "Expired"),
        ("not_verified", "Not Verified"),
    ]

    qualification_id = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100)
    trainer_id = models.CharField(max_length=100)
    trainer_name = models.CharField(max_length=200)

    # Qualification details
    qualification_type = models.CharField(max_length=50, choices=QUALIFICATION_TYPES)
    qualification_code = models.CharField(max_length=50)  # e.g., ICT40120
    qualification_name = models.CharField(max_length=300)
    issuing_organization = models.CharField(max_length=200)

    # Verification
    date_obtained = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    verification_status = models.CharField(
        max_length=20, choices=VERIFICATION_STATUS, default="pending"
    )
    verification_document = models.CharField(
        max_length=500, blank=True
    )  # File path or URL

    # Competency areas covered by this qualification
    competency_areas = models.JSONField(default=list)  # List of competency areas
    units_covered = models.JSONField(default=list)  # List of unit codes covered

    # Industry currency
    industry_experience_years = models.IntegerField(default=0)
    recent_industry_work = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant", "trainer_id"]),
            models.Index(fields=["verification_status", "expiry_date"]),
            models.Index(fields=["qualification_code"]),
        ]
        unique_together = ["tenant", "trainer_id", "qualification_code"]

    def save(self, *args, **kwargs):
        if not self.qualification_id:
            date_str = timezone.now().strftime("%Y%m%d")
            random_str = str(uuid.uuid4())[:8].upper()
            self.qualification_id = f"QUAL-{date_str}-{random_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trainer_name} - {self.qualification_name}"


class UnitOfCompetency(models.Model):
    """Store units of competency and their requirements"""

    UNIT_TYPES = [
        ("core", "Core Unit"),
        ("elective", "Elective Unit"),
        ("prerequisite", "Prerequisite"),
    ]

    unit_id = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100)

    # Unit details
    unit_code = models.CharField(max_length=50)
    unit_name = models.CharField(max_length=300)
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)
    qualification_code = models.CharField(max_length=50)  # Parent qualification

    # Requirements for delivering this unit
    required_qualifications = models.JSONField(
        default=list
    )  # List of required qualification codes
    required_competency_areas = models.JSONField(
        default=list
    )  # List of competency areas
    required_industry_experience = models.IntegerField(default=0)  # Minimum years
    requires_tae = models.BooleanField(default=True)
    requires_industry_currency = models.BooleanField(default=True)

    # Content and skills
    learning_outcomes = models.JSONField(default=list)
    assessment_methods = models.JSONField(default=list)
    technical_skills = models.JSONField(default=list)

    # Graph relationships
    prerequisite_units = models.JSONField(
        default=list
    )  # Unit codes that are prerequisites
    related_units = models.JSONField(default=list)  # Related unit codes

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant", "qualification_code"]),
            models.Index(fields=["unit_code"]),
        ]
        unique_together = ["tenant", "unit_code"]

    def save(self, *args, **kwargs):
        if not self.unit_id:
            date_str = timezone.now().strftime("%Y%m%d")
            random_str = str(uuid.uuid4())[:8].upper()
            self.unit_id = f"UNIT-{date_str}-{random_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.unit_code} - {self.unit_name}"


class TrainerAssignment(models.Model):
    """Assign trainers to units they can deliver"""

    ASSIGNMENT_STATUS = [
        ("approved", "Approved"),
        ("pending", "Pending Approval"),
        ("rejected", "Rejected"),
        ("under_review", "Under Review"),
    ]

    assignment_id = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100)

    trainer_id = models.CharField(max_length=100)
    trainer_name = models.CharField(max_length=200)
    unit = models.ForeignKey(
        UnitOfCompetency, on_delete=models.CASCADE, related_name="assignments"
    )

    # Assignment details
    assignment_status = models.CharField(
        max_length=20, choices=ASSIGNMENT_STATUS, default="pending"
    )
    assigned_date = models.DateField(auto_now_add=True)
    approved_by = models.CharField(max_length=200, blank=True)
    approved_date = models.DateField(null=True, blank=True)

    # Compliance check results
    meets_requirements = models.BooleanField(default=False)
    compliance_score = models.FloatField(default=0.0)  # 0-100
    gaps_identified = models.JSONField(default=list)  # List of gap descriptions

    # Matching qualifications
    matching_qualifications = models.JSONField(
        default=list
    )  # List of qualification IDs

    # Notes
    assignment_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant", "trainer_id"]),
            models.Index(fields=["assignment_status"]),
            models.Index(fields=["unit", "trainer_id"]),
        ]
        unique_together = ["tenant", "trainer_id", "unit"]

    def save(self, *args, **kwargs):
        if not self.assignment_id:
            date_str = timezone.now().strftime("%Y%m%d")
            random_str = str(uuid.uuid4())[:8].upper()
            self.assignment_id = f"ASSIGN-{date_str}-{random_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trainer_name} → {self.unit.unit_code}"


class CompetencyGap(models.Model):
    """Identified gaps between trainer qualifications and unit requirements"""

    GAP_SEVERITY = [
        ("critical", "Critical - Cannot Deliver"),
        ("high", "High - Requires Upskilling"),
        ("medium", "Medium - Recommended Upskilling"),
        ("low", "Low - Minor Gap"),
    ]

    GAP_TYPES = [
        ("missing_qualification", "Missing Required Qualification"),
        ("expired_qualification", "Expired Qualification"),
        ("insufficient_experience", "Insufficient Industry Experience"),
        ("missing_tae", "Missing TAE Qualification"),
        ("missing_currency", "Missing Industry Currency"),
        ("competency_mismatch", "Competency Area Mismatch"),
        ("skill_gap", "Technical Skill Gap"),
    ]

    gap_id = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100)

    trainer_id = models.CharField(max_length=100)
    trainer_name = models.CharField(max_length=200)
    unit = models.ForeignKey(
        UnitOfCompetency, on_delete=models.CASCADE, related_name="gaps"
    )
    assignment = models.ForeignKey(
        TrainerAssignment,
        on_delete=models.CASCADE,
        related_name="gaps",
        null=True,
        blank=True,
    )

    # Gap details
    gap_type = models.CharField(max_length=50, choices=GAP_TYPES)
    gap_severity = models.CharField(max_length=20, choices=GAP_SEVERITY)
    gap_description = models.TextField()

    # What's missing
    required_qualification = models.CharField(max_length=100, blank=True)
    required_competency = models.CharField(max_length=200, blank=True)
    required_experience_years = models.IntegerField(null=True, blank=True)

    # Current state
    current_qualifications = models.JSONField(
        default=list
    )  # What trainer currently has

    # Resolution
    is_resolved = models.BooleanField(default=False)
    resolution_date = models.DateField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    # Recommendations
    recommended_action = models.TextField()
    estimated_resolution_time = models.CharField(
        max_length=100, blank=True
    )  # e.g., "6 months"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant", "trainer_id"]),
            models.Index(fields=["gap_severity", "is_resolved"]),
            models.Index(fields=["unit"]),
        ]

    def save(self, *args, **kwargs):
        if not self.gap_id:
            date_str = timezone.now().strftime("%Y%m%d")
            random_str = str(uuid.uuid4())[:8].upper()
            self.gap_id = f"GAP-{date_str}-{random_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trainer_name} - {self.gap_type} for {self.unit.unit_code}"


class QualificationMapping(models.Model):
    """Graph-based mapping between qualifications and competencies"""

    mapping_id = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100)

    # Source qualification
    source_qualification_code = models.CharField(max_length=50)
    source_qualification_name = models.CharField(max_length=300)

    # Target competency areas
    competency_areas = models.JSONField(default=list)  # List of competency areas

    # Matching strength (graph weight)
    match_strength = models.FloatField(default=0.0)  # 0-1, higher = stronger match
    match_confidence = models.FloatField(default=0.0)  # 0-1, confidence in the mapping

    # Equivalency information
    equivalent_qualifications = models.JSONField(
        default=list
    )  # List of equivalent qualification codes
    superseded_by = models.CharField(max_length=50, blank=True)
    supersedes = models.CharField(max_length=50, blank=True)

    # Units coverage
    units_covered = models.JSONField(
        default=list
    )  # Unit codes covered by this qualification
    units_partially_covered = models.JSONField(default=list)  # Partially covered units

    # Metadata
    mapping_source = models.CharField(
        max_length=100, default="manual"
    )  # manual, training.gov.au, ml_model
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant", "source_qualification_code"]),
            models.Index(fields=["match_strength"]),
        ]
        unique_together = ["tenant", "source_qualification_code"]

    def save(self, *args, **kwargs):
        if not self.mapping_id:
            date_str = timezone.now().strftime("%Y%m%d")
            random_str = str(uuid.uuid4())[:8].upper()
            self.mapping_id = f"MAP-{date_str}-{random_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.source_qualification_code} mapping"


class ComplianceCheck(models.Model):
    """Compliance check runs for trainer matrix validation"""

    CHECK_STATUS = [
        ("pending", "Pending"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    check_id = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100)

    # Check details
    check_type = models.CharField(
        max_length=50, default="full_matrix"
    )  # full_matrix, trainer, unit, qualification
    check_status = models.CharField(
        max_length=20, choices=CHECK_STATUS, default="pending"
    )

    # Scope
    trainer_ids = models.JSONField(
        default=list
    )  # List of trainer IDs to check (empty = all)
    unit_codes = models.JSONField(
        default=list
    )  # List of unit codes to check (empty = all)

    # Results summary
    total_assignments_checked = models.IntegerField(default=0)
    compliant_assignments = models.IntegerField(default=0)
    non_compliant_assignments = models.IntegerField(default=0)
    gaps_found = models.IntegerField(default=0)

    # Severity breakdown
    critical_gaps = models.IntegerField(default=0)
    high_gaps = models.IntegerField(default=0)
    medium_gaps = models.IntegerField(default=0)
    low_gaps = models.IntegerField(default=0)

    # Compliance score
    overall_compliance_score = models.FloatField(default=0.0)  # 0-100

    # Report
    report_summary = models.TextField(blank=True)
    detailed_results = models.JSONField(
        default=dict
    )  # Detailed breakdown by trainer/unit
    recommendations = models.JSONField(default=list)  # List of recommended actions

    # Execution details
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    execution_time_seconds = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant", "check_status"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.check_id:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            random_str = str(uuid.uuid4())[:6].upper()
            self.check_id = f"CHECK-{timestamp}-{random_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compliance Check {self.check_id} - {self.check_status}"
