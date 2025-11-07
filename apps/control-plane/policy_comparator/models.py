from django.db import models
from django.contrib.auth.models import User
from tenants.models import Tenant
from django.core.validators import MinValueValidator, MaxValueValidator
from pgvector.django import VectorField
import hashlib


class Document(models.Model):
    """
    Uploaded policy documents with versioning support
    """

    SOURCE_TYPES = [
        ("pdf", "PDF"),
        ("docx", "Word Document"),
        ("html", "HTML"),
        ("txt", "Plain Text"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending Upload"),
        ("uploading", "Uploading"),
        ("processing", "Processing"),
        ("ready", "Ready"),
        ("failed", "Failed"),
        ("archived", "Archived"),
    ]

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="policy_documents"
    )

    title = models.CharField(max_length=500)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    s3_uri = models.CharField(max_length=1000, help_text="S3 path to original file")
    sha256 = models.CharField(
        max_length=64, db_index=True, help_text="File hash for deduplication"
    )

    language = models.CharField(max_length=10, default="en")
    pages = models.IntegerField(null=True, blank=True)
    word_count = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    error_message = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="uploaded_documents"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "policy_documents"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["tenant", "status"]),
            models.Index(fields=["sha256"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.source_type})"


class DocumentVersion(models.Model):
    """
    Version history for documents
    """

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="versions"
    )
    version_no = models.IntegerField()
    s3_uri = models.CharField(max_length=1000)
    sha256 = models.CharField(max_length=64, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document_versions"
        ordering = ["-version_no"]
        unique_together = [["document", "version_no"]]

    def __str__(self):
        return f"{self.document.title} v{self.version_no}"


class DocumentChunk(models.Model):
    """
    Text chunks from documents for embedding and comparison
    """

    document_version = models.ForeignKey(
        DocumentVersion, on_delete=models.CASCADE, related_name="chunks"
    )
    chunk_idx = models.IntegerField(help_text="Sequential index of chunk")

    text = models.TextField()
    tokens = models.IntegerField(help_text="Token count for this chunk")
    section_path = models.CharField(
        max_length=500,
        blank=True,
        help_text="Heading path, e.g., '1. Introduction > 1.1 Purpose'",
    )

    page_from = models.IntegerField(null=True, blank=True)
    page_to = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "document_chunks"
        ordering = ["document_version", "chunk_idx"]
        indexes = [
            models.Index(fields=["document_version", "chunk_idx"]),
        ]

    def __str__(self):
        return f"{self.document_version} chunk {self.chunk_idx}"


class AsqaClausePack(models.Model):
    """
    Versioned packs of ASQA clauses (global or tenant-specific)
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("review", "Under Review"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Null for global ASQA packs",
    )
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "asqa_clause_packs"
        ordering = ["-published_at"]
        unique_together = [["tenant", "name", "version"]]

    def __str__(self):
        return f"{self.name} v{self.version}"


class ASQAStandard(models.Model):
    """
    ASQA Standards for RTOs (Registered Training Organisations)
    Supports both:
    - Standards for Registered Training Organisations (RTOs) 2015
    - Standards for Registered Training Organisations (RTOs) 2025 (effective 1 July 2025)
    """

    # 2015 Standard Types (Legacy)
    STANDARD_TYPES_2015 = [
        ("training_assessment", "Training and Assessment"),
        ("trainer_assessor", "Trainer and Assessor"),
        ("educational_support", "Educational and Support Services"),
        ("certification", "Certification"),
        ("engagement_employer", "Engagement with Employers"),
        ("complaints_appeals", "Complaints and Appeals"),
        ("governance", "Governance and Administration"),
        ("financial", "Financial Management"),
    ]
    
    # 2025 Standard Types (Current)
    STANDARD_TYPES_2025 = [
        # Outcome Standards
        ("qa1_training_assessment", "Quality Area 1 - Training and Assessment"),
        ("qa2_student_support", "Quality Area 2 - VET Student Support"),
        ("qa3_workforce", "Quality Area 3 - VET Workforce"),
        ("qa4_governance", "Quality Area 4 - Governance"),
        # Compliance Requirements
        ("compliance_information", "Compliance - Information and Transparency"),
        ("compliance_integrity", "Compliance - Integrity of NRT Products"),
        ("compliance_accountability", "Compliance - Accountability"),
        ("compliance_fit_proper", "Compliance - Fit and Proper Person"),
        # Credential Policy
        ("credential_policy", "Credential Policy"),
    ]
    
    STANDARD_TYPES = STANDARD_TYPES_2015 + STANDARD_TYPES_2025
    
    STANDARD_CATEGORIES = [
        ("outcome", "Outcome Standard"),
        ("compliance", "Compliance Requirement"),
        ("credential", "Credential Policy"),
        ("legacy_2015", "2015 Standard"),
    ]
    
    VERSIONS = [
        ("2015", "Standards for RTOs 2015"),
        ("2025", "Standards for RTOs 2025"),
    ]

    standard_number = models.CharField(
        max_length=20, db_index=True, help_text="e.g., Standard 1.1 (2015) or QA1.1 (2025)"
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    standard_type = models.CharField(max_length=50, choices=STANDARD_TYPES)
    
    # New field for 2025 standards structure
    standard_category = models.CharField(
        max_length=20, 
        choices=STANDARD_CATEGORIES,
        default="legacy_2015",
        help_text="Classification within 2025 standards framework"
    )
    
    # Quality Area (for 2025 Outcome Standards)
    quality_area = models.IntegerField(
        null=True, 
        blank=True,
        help_text="Quality Area number (1-4) for 2025 Outcome Standards"
    )

    # Full text of the standard
    full_text = models.TextField(help_text="Complete text of the ASQA standard")

    # Requirements breakdown
    requirements = models.JSONField(
        default=list, help_text="List of specific requirements"
    )

    # Metadata
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=20, choices=VERSIONS, default="2025")
    
    # Official ASQA links
    asqa_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Link to official ASQA documentation"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "asqa_standards"
        ordering = ["version", "quality_area", "standard_number"]
        verbose_name = "ASQA Standard"
        verbose_name_plural = "ASQA Standards"
        indexes = [
            models.Index(fields=["version", "is_active"]),
            models.Index(fields=["standard_category"]),
            models.Index(fields=["quality_area"]),
        ]
        # Allow same standard_number for different versions
        unique_together = [["standard_number", "version"]]

    def __str__(self):
        if self.version == "2025" and self.quality_area:
            return f"QA{self.quality_area} {self.standard_number} - {self.title} (2025)"
        return f"{self.standard_number} - {self.title} ({self.version})"


class ASQAClause(models.Model):
    """
    Individual clauses within ASQA standards for detailed comparison
    """

    standard = models.ForeignKey(
        ASQAStandard, on_delete=models.CASCADE, related_name="clauses"
    )
    clause_number = models.CharField(max_length=20, help_text="e.g., 1.1, 1.2, 1.3")
    title = models.CharField(max_length=300)
    clause_text = models.TextField(help_text="Full text of the clause")

    # Evidence requirements
    evidence_required = models.JSONField(
        default=list, help_text="Types of evidence needed"
    )

    # Keywords for NLP matching
    keywords = models.JSONField(default=list, help_text="Key terms for text similarity")

    # Compliance level
    COMPLIANCE_LEVELS = [
        ("critical", "Critical - Must comply"),
        ("essential", "Essential - Required"),
        ("recommended", "Recommended - Best practice"),
    ]
    compliance_level = models.CharField(
        max_length=20, choices=COMPLIANCE_LEVELS, default="essential"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "asqa_clauses"
        ordering = ["standard", "clause_number"]
        unique_together = [["standard", "clause_number"]]
        verbose_name = "ASQA Clause"
        verbose_name_plural = "ASQA Clauses"

    def __str__(self):
        return f"{self.standard.standard_number}.{self.clause_number} - {self.title}"


class Policy(models.Model):
    """
    Organisation policies to be compared against ASQA standards
    """

    POLICY_TYPES = [
        ("training_delivery", "Training and Delivery"),
        ("assessment", "Assessment"),
        ("student_support", "Student Support"),
        ("complaints_appeals", "Complaints and Appeals"),
        ("financial", "Financial"),
        ("governance", "Governance"),
        ("quality_assurance", "Quality Assurance"),
        ("workplace_health_safety", "Workplace Health and Safety"),
        ("staff_management", "Staff Management"),
        ("facilities_resources", "Facilities and Resources"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("under_review", "Under Review"),
        ("approved", "Approved"),
        ("archived", "Archived"),
    ]

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="policies"
    )

    # Policy Information
    policy_number = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    policy_type = models.CharField(max_length=50, choices=POLICY_TYPES)

    # Content
    content = models.TextField(help_text="Full policy content")
    version = models.CharField(max_length=20, default="1.0")

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    # Dates
    effective_date = models.DateField(null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)

    # Compliance
    last_compared_at = models.DateTimeField(null=True, blank=True)
    compliance_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Overall compliance score (0-100)",
    )

    # File attachment
    file_path = models.CharField(
        max_length=500, blank=True, help_text="Path to uploaded policy document"
    )

    # Audit
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="policies_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "policies"
        ordering = ["-created_at"]
        unique_together = [["tenant", "policy_number"]]
        indexes = [
            models.Index(fields=["tenant", "status"]),
            models.Index(fields=["policy_type"]),
            models.Index(fields=["compliance_score"]),
        ]
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return f"{self.policy_number} - {self.title}"


class ComparisonResult(models.Model):
    """
    Results of NLP-based policy comparison against ASQA clauses
    """

    MATCH_TYPES = [
        ("full", "Full Match"),
        ("partial", "Partial Match"),
        ("weak", "Weak Match"),
        ("no_match", "No Match"),
    ]

    policy = models.ForeignKey(
        Policy, on_delete=models.CASCADE, related_name="comparison_results"
    )
    asqa_clause = models.ForeignKey(
        ASQAClause, on_delete=models.CASCADE, related_name="comparison_results"
    )

    # NLP Similarity Scores
    similarity_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Text similarity score (0.0 - 1.0)",
    )

    # Match classification
    match_type = models.CharField(max_length=20, choices=MATCH_TYPES)

    # Analysis
    matched_text = models.TextField(blank=True, help_text="Relevant text from policy")
    gap_description = models.TextField(
        blank=True, help_text="Description of compliance gap"
    )

    # Recommendations
    recommendations = models.JSONField(
        default=list, help_text="Suggestions to improve compliance"
    )

    # NLP Analysis Details
    nlp_metadata = models.JSONField(default=dict, help_text="NLP processing metadata")
    keywords_matched = models.JSONField(
        default=list, help_text="Keywords found in policy"
    )
    keywords_missing = models.JSONField(
        default=list, help_text="Keywords missing from policy"
    )

    # Evidence
    has_sufficient_evidence = models.BooleanField(default=False)
    evidence_notes = models.TextField(blank=True)

    # Status
    is_compliant = models.BooleanField(
        default=False, help_text="Meets ASQA requirements"
    )
    requires_action = models.BooleanField(
        default=False, help_text="Action needed to achieve compliance"
    )

    # Audit
    comparison_date = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_comparisons",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "comparison_results"
        ordering = ["-similarity_score"]
        unique_together = [["policy", "asqa_clause"]]
        indexes = [
            models.Index(fields=["policy", "similarity_score"]),
            models.Index(fields=["is_compliant"]),
            models.Index(fields=["requires_action"]),
        ]
        verbose_name = "Comparison Result"
        verbose_name_plural = "Comparison Results"

    def __str__(self):
        return f"{self.policy.policy_number} vs {self.asqa_clause.clause_number} - {self.similarity_score:.2f}"

    def save(self, *args, **kwargs):
        # Auto-classify match type based on similarity score
        if self.similarity_score >= 0.8:
            self.match_type = "full"
            self.is_compliant = True
        elif self.similarity_score >= 0.6:
            self.match_type = "partial"
            self.requires_action = True
        elif self.similarity_score >= 0.4:
            self.match_type = "weak"
            self.requires_action = True
        else:
            self.match_type = "no_match"
            self.requires_action = True

        super().save(*args, **kwargs)


class ComparisonSession(models.Model):
    """
    Track batch comparison sessions
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="comparison_sessions"
    )
    policy = models.ForeignKey(
        Policy, on_delete=models.CASCADE, related_name="comparison_sessions"
    )

    # Session metadata
    session_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Standards compared
    standards_compared = models.JSONField(
        default=list, help_text="List of ASQA standard IDs compared"
    )

    # Results summary
    total_clauses_checked = models.IntegerField(default=0)
    compliant_count = models.IntegerField(default=0)
    partial_match_count = models.IntegerField(default=0)
    gap_count = models.IntegerField(default=0)

    # Overall score
    overall_compliance_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )

    # Performance metrics
    processing_time_seconds = models.FloatField(default=0.0)

    # Error handling
    error_message = models.TextField(blank=True)

    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "comparison_sessions"
        ordering = ["-created_at"]
        verbose_name = "Comparison Session"
        verbose_name_plural = "Comparison Sessions"

    def __str__(self):
        return f"{self.session_name} - {self.status}"

    def calculate_compliance_score(self):
        """Calculate overall compliance score"""
        if self.total_clauses_checked == 0:
            return 0.0

        # Weight different match types
        score = (
            (self.compliant_count * 100)
            + (self.partial_match_count * 60)
            + (self.gap_count * 0)
        ) / self.total_clauses_checked

        self.overall_compliance_score = round(score, 2)
        return self.overall_compliance_score
