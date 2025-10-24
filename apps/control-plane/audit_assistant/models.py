from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
import os
import uuid

User = get_user_model()


def evidence_upload_path(instance, filename):
    """Generate upload path for evidence files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('evidence', str(instance.tenant.id), filename)


class Evidence(models.Model):
    """
    Evidence documents uploaded for ASQA compliance audits.
    Supports file uploads with NER processing for auto-tagging.
    """
    EVIDENCE_TYPE_CHOICES = [
        ('policy', 'Policy Document'),
        ('procedure', 'Procedure'),
        ('record', 'Record/Log'),
        ('template', 'Template/Form'),
        ('certificate', 'Certificate'),
        ('qualification', 'Qualification Document'),
        ('training_material', 'Training Material'),
        ('assessment', 'Assessment Document'),
        ('quality_assurance', 'Quality Assurance Document'),
        ('financial', 'Financial Document'),
        ('contract', 'Contract/Agreement'),
        ('correspondence', 'Correspondence'),
        ('meeting_minutes', 'Meeting Minutes'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('processing', 'Processing NER'),
        ('tagged', 'Auto-Tagged'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Basic info
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name='evidence_documents')
    evidence_number = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    evidence_type = models.CharField(max_length=50, choices=EVIDENCE_TYPE_CHOICES)
    
    # File upload
    file = models.FileField(
        upload_to=evidence_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'doc', 'xlsx', 'xls', 'txt', 'jpg', 'jpeg', 'png'])],
        help_text="Supported formats: PDF, Word, Excel, Text, Images"
    )
    file_size = models.IntegerField(null=True, blank=True, help_text="File size in bytes")
    extracted_text = models.TextField(blank=True, help_text="Text extracted from uploaded file")
    
    # NER processing
    ner_entities = models.JSONField(
        default=list,
        help_text="Named entities extracted: {entity: str, type: str, start: int, end: int}"
    )
    ner_processed_at = models.DateTimeField(null=True, blank=True)
    
    # Auto-tagging
    auto_tagged_clauses = models.ManyToManyField(
        'policy_comparator.ASQAClause',
        through='ClauseEvidence',
        related_name='evidence_documents',
        help_text="ASQA clauses automatically tagged via NER"
    )
    
    # Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    tags = models.JSONField(default=list, help_text="Custom tags for categorization")
    
    # Dates
    evidence_date = models.DateField(help_text="Date the evidence was created/issued")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_evidence')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_evidence')
    
    # Review notes
    reviewer_notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'evidence'
        verbose_name = 'Evidence Document'
        verbose_name_plural = 'Evidence Documents'
        ordering = ['-uploaded_at']
        unique_together = [['tenant', 'evidence_number']]
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['evidence_type']),
            models.Index(fields=['evidence_date']),
        ]
    
    def __str__(self):
        return f"{self.evidence_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.file and not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class ClauseEvidence(models.Model):
    """
    Many-to-many relationship between ASQA clauses and evidence documents.
    Tracks auto-tagging confidence and manual review status.
    """
    MAPPING_TYPE_CHOICES = [
        ('auto_ner', 'Auto-tagged (NER)'),
        ('auto_rule', 'Auto-tagged (Rule-based)'),
        ('manual', 'Manual Assignment'),
        ('suggested', 'Suggested Match'),
    ]
    
    # Relationships
    asqa_clause = models.ForeignKey('policy_comparator.ASQAClause', on_delete=models.CASCADE)
    evidence = models.ForeignKey(Evidence, on_delete=models.CASCADE)
    
    # Auto-tagging metadata
    mapping_type = models.CharField(max_length=20, choices=MAPPING_TYPE_CHOICES)
    confidence_score = models.FloatField(
        default=0.0,
        help_text="Confidence score (0.0-1.0) for auto-tagged matches"
    )
    matched_entities = models.JSONField(
        default=list,
        help_text="NER entities that triggered this mapping: [{entity: str, type: str}]"
    )
    matched_keywords = models.JSONField(
        default=list,
        help_text="Keywords that matched between clause and evidence"
    )
    
    # Rule mapping metadata
    rule_name = models.CharField(max_length=100, blank=True, help_text="Name of rule that triggered mapping")
    rule_metadata = models.JSONField(default=dict, help_text="Additional rule processing data")
    
    # Manual review
    is_verified = models.BooleanField(default=False, help_text="Manually verified by reviewer")
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Relevance
    relevance_notes = models.TextField(blank=True, help_text="Notes on evidence relevance to clause")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clause_evidence'
        verbose_name = 'Clause Evidence Mapping'
        verbose_name_plural = 'Clause Evidence Mappings'
        ordering = ['-confidence_score', '-created_at']
        unique_together = [['asqa_clause', 'evidence']]
        indexes = [
            models.Index(fields=['mapping_type']),
            models.Index(fields=['confidence_score']),
            models.Index(fields=['is_verified']),
        ]
    
    def __str__(self):
        return f"{self.asqa_clause.clause_number} - {self.evidence.evidence_number}"


class AuditReport(models.Model):
    """
    Clause-by-clause audit reports showing evidence coverage.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('submitted', 'Submitted to ASQA'),
    ]
    
    # Basic info
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name='audit_reports')
    report_number = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Audit scope
    asqa_standards = models.ManyToManyField(
        'policy_comparator.ASQAStandard',
        related_name='audit_reports',
        help_text="ASQA standards included in this audit"
    )
    audit_period_start = models.DateField(help_text="Start date of audit period")
    audit_period_end = models.DateField(help_text="End date of audit period")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Compliance metrics
    total_clauses = models.IntegerField(default=0)
    clauses_with_evidence = models.IntegerField(default=0)
    clauses_without_evidence = models.IntegerField(default=0)
    compliance_percentage = models.FloatField(default=0.0, help_text="Percentage of clauses with evidence")
    
    # Critical clause tracking
    critical_clauses_count = models.IntegerField(default=0)
    critical_clauses_covered = models.IntegerField(default=0)
    critical_compliance_percentage = models.FloatField(default=0.0)
    
    # Evidence summary
    total_evidence_count = models.IntegerField(default=0)
    auto_tagged_count = models.IntegerField(default=0, help_text="Evidence auto-tagged via NER")
    manually_tagged_count = models.IntegerField(default=0)
    verified_evidence_count = models.IntegerField(default=0)
    
    # Report metadata
    findings = models.JSONField(
        default=list,
        help_text="List of findings: [{clause: str, finding: str, severity: str, recommendation: str}]"
    )
    recommendations = models.JSONField(default=list, help_text="Overall recommendations")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_audit_reports')
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='submitted_audit_reports')
    
    class Meta:
        db_table = 'audit_reports'
        verbose_name = 'Audit Report'
        verbose_name_plural = 'Audit Reports'
        ordering = ['-created_at']
        unique_together = [['tenant', 'report_number']]
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['audit_period_start', 'audit_period_end']),
            models.Index(fields=['compliance_percentage']),
        ]
    
    def __str__(self):
        return f"{self.report_number} - {self.title}"
    
    def calculate_metrics(self):
        """Calculate compliance metrics based on clause evidence mappings"""
        from policy_comparator.models import ASQAClause
        
        # Get all clauses for included standards
        all_clauses = ASQAClause.objects.filter(
            standard__in=self.asqa_standards.all()
        )
        
        self.total_clauses = all_clauses.count()
        
        # Count clauses with evidence
        clauses_with_evidence = all_clauses.filter(
            evidence_documents__evidence__tenant=self.tenant,
            evidence_documents__evidence__status__in=['tagged', 'reviewed', 'approved']
        ).distinct().count()
        
        self.clauses_with_evidence = clauses_with_evidence
        self.clauses_without_evidence = self.total_clauses - clauses_with_evidence
        
        # Calculate compliance percentage
        if self.total_clauses > 0:
            self.compliance_percentage = round((clauses_with_evidence / self.total_clauses) * 100, 2)
        else:
            self.compliance_percentage = 0.0
        
        # Critical clause metrics
        critical_clauses = all_clauses.filter(compliance_level='critical')
        self.critical_clauses_count = critical_clauses.count()
        
        critical_with_evidence = critical_clauses.filter(
            evidence_documents__evidence__tenant=self.tenant,
            evidence_documents__evidence__status__in=['tagged', 'reviewed', 'approved']
        ).distinct().count()
        
        self.critical_clauses_covered = critical_with_evidence
        
        if self.critical_clauses_count > 0:
            self.critical_compliance_percentage = round(
                (critical_with_evidence / self.critical_clauses_count) * 100, 2
            )
        else:
            self.critical_compliance_percentage = 0.0
        
        # Evidence summary
        evidence_docs = Evidence.objects.filter(
            tenant=self.tenant,
            auto_tagged_clauses__standard__in=self.asqa_standards.all()
        ).distinct()
        
        self.total_evidence_count = evidence_docs.count()
        self.auto_tagged_count = ClauseEvidence.objects.filter(
            evidence__in=evidence_docs,
            mapping_type__in=['auto_ner', 'auto_rule']
        ).values('evidence').distinct().count()
        
        self.manually_tagged_count = ClauseEvidence.objects.filter(
            evidence__in=evidence_docs,
            mapping_type='manual'
        ).values('evidence').distinct().count()
        
        self.verified_evidence_count = ClauseEvidence.objects.filter(
            evidence__in=evidence_docs,
            is_verified=True
        ).values('evidence').distinct().count()
        
        self.save()


class AuditReportClause(models.Model):
    """
    Individual clause entries in an audit report with evidence status.
    """
    COMPLIANCE_STATUS_CHOICES = [
        ('compliant', 'Compliant'),
        ('partial', 'Partially Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('not_assessed', 'Not Assessed'),
    ]
    
    # Relationships
    audit_report = models.ForeignKey(AuditReport, on_delete=models.CASCADE, related_name='clause_entries')
    asqa_clause = models.ForeignKey('policy_comparator.ASQAClause', on_delete=models.CASCADE)
    
    # Compliance assessment
    compliance_status = models.CharField(max_length=20, choices=COMPLIANCE_STATUS_CHOICES, default='not_assessed')
    evidence_count = models.IntegerField(default=0)
    verified_evidence_count = models.IntegerField(default=0)
    
    # Findings
    finding = models.TextField(blank=True, help_text="Audit finding for this clause")
    severity = models.CharField(
        max_length=20,
        choices=[
            ('critical', 'Critical'),
            ('major', 'Major'),
            ('minor', 'Minor'),
            ('observation', 'Observation'),
        ],
        blank=True
    )
    recommendation = models.TextField(blank=True)
    
    # Evidence references
    linked_evidence = models.ManyToManyField(Evidence, related_name='audit_clause_entries', blank=True)
    
    # Assessment metadata
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    assessed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'audit_report_clauses'
        verbose_name = 'Audit Report Clause'
        verbose_name_plural = 'Audit Report Clauses'
        ordering = ['asqa_clause__clause_number']
        unique_together = [['audit_report', 'asqa_clause']]
        indexes = [
            models.Index(fields=['compliance_status']),
            models.Index(fields=['severity']),
        ]
    
    def __str__(self):
        return f"{self.audit_report.report_number} - {self.asqa_clause.clause_number}"
    
    def update_evidence_counts(self):
        """Update evidence counts for this clause"""
        clause_evidence = ClauseEvidence.objects.filter(
            asqa_clause=self.asqa_clause,
            evidence__tenant=self.audit_report.tenant,
            evidence__status__in=['tagged', 'reviewed', 'approved']
        )
        
        self.evidence_count = clause_evidence.count()
        self.verified_evidence_count = clause_evidence.filter(is_verified=True).count()
        
        # Auto-determine compliance status based on evidence
        if self.evidence_count == 0:
            self.compliance_status = 'non_compliant'
        elif self.verified_evidence_count >= 2:  # At least 2 verified evidence items
            self.compliance_status = 'compliant'
        elif self.evidence_count >= 1:
            self.compliance_status = 'partial'
        else:
            self.compliance_status = 'not_assessed'
        
        self.save()
