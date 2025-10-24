from django.db import models
from django.contrib.auth.models import User
from tenants.models import Tenant
from django.core.validators import MinValueValidator, MaxValueValidator


class ASQAStandard(models.Model):
    """
    ASQA Standards for RTOs (Registered Training Organisations)
    Based on Standards for Registered Training Organisations (RTOs) 2015
    """
    STANDARD_TYPES = [
        ('training_assessment', 'Training and Assessment'),
        ('trainer_assessor', 'Trainer and Assessor'),
        ('educational_support', 'Educational and Support Services'),
        ('certification', 'Certification'),
        ('engagement_employer', 'Engagement with Employers'),
        ('complaints_appeals', 'Complaints and Appeals'),
        ('governance', 'Governance and Administration'),
        ('financial', 'Financial Management'),
    ]

    standard_number = models.CharField(max_length=20, unique=True, help_text="e.g., Standard 1.1")
    title = models.CharField(max_length=300)
    description = models.TextField()
    standard_type = models.CharField(max_length=50, choices=STANDARD_TYPES)
    
    # Full text of the standard
    full_text = models.TextField(help_text="Complete text of the ASQA standard")
    
    # Requirements breakdown
    requirements = models.JSONField(default=list, help_text="List of specific requirements")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(null=True, blank=True)
    version = models.CharField(max_length=20, default='2015')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asqa_standards'
        ordering = ['standard_number']
        verbose_name = 'ASQA Standard'
        verbose_name_plural = 'ASQA Standards'

    def __str__(self):
        return f"{self.standard_number} - {self.title}"


class ASQAClause(models.Model):
    """
    Individual clauses within ASQA standards for detailed comparison
    """
    standard = models.ForeignKey(ASQAStandard, on_delete=models.CASCADE, related_name='clauses')
    clause_number = models.CharField(max_length=20, help_text="e.g., 1.1, 1.2, 1.3")
    title = models.CharField(max_length=300)
    clause_text = models.TextField(help_text="Full text of the clause")
    
    # Evidence requirements
    evidence_required = models.JSONField(default=list, help_text="Types of evidence needed")
    
    # Keywords for NLP matching
    keywords = models.JSONField(default=list, help_text="Key terms for text similarity")
    
    # Compliance level
    COMPLIANCE_LEVELS = [
        ('critical', 'Critical - Must comply'),
        ('essential', 'Essential - Required'),
        ('recommended', 'Recommended - Best practice'),
    ]
    compliance_level = models.CharField(max_length=20, choices=COMPLIANCE_LEVELS, default='essential')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asqa_clauses'
        ordering = ['standard', 'clause_number']
        unique_together = [['standard', 'clause_number']]
        verbose_name = 'ASQA Clause'
        verbose_name_plural = 'ASQA Clauses'

    def __str__(self):
        return f"{self.standard.standard_number}.{self.clause_number} - {self.title}"


class Policy(models.Model):
    """
    Organisation policies to be compared against ASQA standards
    """
    POLICY_TYPES = [
        ('training_delivery', 'Training and Delivery'),
        ('assessment', 'Assessment'),
        ('student_support', 'Student Support'),
        ('complaints_appeals', 'Complaints and Appeals'),
        ('financial', 'Financial'),
        ('governance', 'Governance'),
        ('quality_assurance', 'Quality Assurance'),
        ('workplace_health_safety', 'Workplace Health and Safety'),
        ('staff_management', 'Staff Management'),
        ('facilities_resources', 'Facilities and Resources'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('archived', 'Archived'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='policies')
    
    # Policy Information
    policy_number = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    policy_type = models.CharField(max_length=50, choices=POLICY_TYPES)
    
    # Content
    content = models.TextField(help_text="Full policy content")
    version = models.CharField(max_length=20, default='1.0')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Dates
    effective_date = models.DateField(null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)
    
    # Compliance
    last_compared_at = models.DateTimeField(null=True, blank=True)
    compliance_score = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Overall compliance score (0-100)"
    )
    
    # File attachment
    file_path = models.CharField(max_length=500, blank=True, help_text="Path to uploaded policy document")
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='policies_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'policies'
        ordering = ['-created_at']
        unique_together = [['tenant', 'policy_number']]
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['policy_type']),
            models.Index(fields=['compliance_score']),
        ]
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'

    def __str__(self):
        return f"{self.policy_number} - {self.title}"


class ComparisonResult(models.Model):
    """
    Results of NLP-based policy comparison against ASQA clauses
    """
    MATCH_TYPES = [
        ('full', 'Full Match'),
        ('partial', 'Partial Match'),
        ('weak', 'Weak Match'),
        ('no_match', 'No Match'),
    ]

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='comparison_results')
    asqa_clause = models.ForeignKey(ASQAClause, on_delete=models.CASCADE, related_name='comparison_results')
    
    # NLP Similarity Scores
    similarity_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Text similarity score (0.0 - 1.0)"
    )
    
    # Match classification
    match_type = models.CharField(max_length=20, choices=MATCH_TYPES)
    
    # Analysis
    matched_text = models.TextField(blank=True, help_text="Relevant text from policy")
    gap_description = models.TextField(blank=True, help_text="Description of compliance gap")
    
    # Recommendations
    recommendations = models.JSONField(default=list, help_text="Suggestions to improve compliance")
    
    # NLP Analysis Details
    nlp_metadata = models.JSONField(default=dict, help_text="NLP processing metadata")
    keywords_matched = models.JSONField(default=list, help_text="Keywords found in policy")
    keywords_missing = models.JSONField(default=list, help_text="Keywords missing from policy")
    
    # Evidence
    has_sufficient_evidence = models.BooleanField(default=False)
    evidence_notes = models.TextField(blank=True)
    
    # Status
    is_compliant = models.BooleanField(default=False, help_text="Meets ASQA requirements")
    requires_action = models.BooleanField(default=False, help_text="Action needed to achieve compliance")
    
    # Audit
    comparison_date = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_comparisons')
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'comparison_results'
        ordering = ['-similarity_score']
        unique_together = [['policy', 'asqa_clause']]
        indexes = [
            models.Index(fields=['policy', 'similarity_score']),
            models.Index(fields=['is_compliant']),
            models.Index(fields=['requires_action']),
        ]
        verbose_name = 'Comparison Result'
        verbose_name_plural = 'Comparison Results'

    def __str__(self):
        return f"{self.policy.policy_number} vs {self.asqa_clause.clause_number} - {self.similarity_score:.2f}"

    def save(self, *args, **kwargs):
        # Auto-classify match type based on similarity score
        if self.similarity_score >= 0.8:
            self.match_type = 'full'
            self.is_compliant = True
        elif self.similarity_score >= 0.6:
            self.match_type = 'partial'
            self.requires_action = True
        elif self.similarity_score >= 0.4:
            self.match_type = 'weak'
            self.requires_action = True
        else:
            self.match_type = 'no_match'
            self.requires_action = True
        
        super().save(*args, **kwargs)


class ComparisonSession(models.Model):
    """
    Track batch comparison sessions
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='comparison_sessions')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='comparison_sessions')
    
    # Session metadata
    session_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Standards compared
    standards_compared = models.JSONField(default=list, help_text="List of ASQA standard IDs compared")
    
    # Results summary
    total_clauses_checked = models.IntegerField(default=0)
    compliant_count = models.IntegerField(default=0)
    partial_match_count = models.IntegerField(default=0)
    gap_count = models.IntegerField(default=0)
    
    # Overall score
    overall_compliance_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
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
        db_table = 'comparison_sessions'
        ordering = ['-created_at']
        verbose_name = 'Comparison Session'
        verbose_name_plural = 'Comparison Sessions'

    def __str__(self):
        return f"{self.session_name} - {self.status}"

    def calculate_compliance_score(self):
        """Calculate overall compliance score"""
        if self.total_clauses_checked == 0:
            return 0.0
        
        # Weight different match types
        score = (
            (self.compliant_count * 100) +
            (self.partial_match_count * 60) +
            (self.gap_count * 0)
        ) / self.total_clauses_checked
        
        self.overall_compliance_score = round(score, 2)
        return self.overall_compliance_score
