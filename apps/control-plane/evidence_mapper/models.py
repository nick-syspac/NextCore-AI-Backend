from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
import secrets
import json


class EvidenceMapping(models.Model):
    """
    Master evidence mapping for linking submissions to assessment criteria.
    """
    MAPPING_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    ASSESSMENT_TYPE_CHOICES = [
        ('written', 'Written Assignment'),
        ('practical', 'Practical Demonstration'),
        ('portfolio', 'Portfolio'),
        ('project', 'Project Work'),
        ('presentation', 'Presentation'),
    ]
    
    mapping_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assessment_type = models.CharField(max_length=50, choices=ASSESSMENT_TYPE_CHOICES, default='written')
    
    # Assessment details
    assessment_title = models.CharField(max_length=200)
    unit_code = models.CharField(max_length=50, blank=True)
    total_criteria = models.IntegerField(default=0)
    total_submissions = models.IntegerField(default=0)
    
    # Configuration
    auto_extract_text = models.BooleanField(default=True, help_text="Automatically extract text from submissions")
    generate_embeddings = models.BooleanField(default=True, help_text="Generate embeddings for semantic search")
    require_evidence_per_criterion = models.BooleanField(default=True)
    min_evidence_length = models.IntegerField(default=50, help_text="Minimum characters for valid evidence")
    
    # Statistics
    total_evidence_tagged = models.IntegerField(default=0)
    total_text_extracted = models.IntegerField(default=0)
    embeddings_generated = models.IntegerField(default=0)
    coverage_percentage = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    
    # Status
    status = models.CharField(max_length=20, choices=MAPPING_STATUS_CHOICES, default='active')
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['assessment_type']),
            models.Index(fields=['unit_code']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.mapping_number:
            date_str = datetime.now().strftime('%Y%m%d')
            random_suffix = secrets.token_hex(3).upper()
            self.mapping_number = f"EVM-{date_str}-{random_suffix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.mapping_number} - {self.name}"
    
    def calculate_coverage(self):
        """Calculate percentage of criteria with evidence"""
        if self.total_criteria == 0:
            return 0.0
        
        criteria_with_evidence = CriteriaTag.objects.filter(
            evidence__mapping=self
        ).values('criterion_id').distinct().count()
        
        return (criteria_with_evidence / self.total_criteria) * 100


class SubmissionEvidence(models.Model):
    """
    Individual submission with extracted text and embeddings.
    """
    EXTRACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    evidence_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    mapping = models.ForeignKey(EvidenceMapping, on_delete=models.CASCADE, related_name='submissions')
    
    # Student info
    student_id = models.CharField(max_length=100)
    student_name = models.CharField(max_length=200)
    submission_id = models.CharField(max_length=100)
    
    # Submission details
    submission_title = models.CharField(max_length=200, blank=True)
    submission_type = models.CharField(max_length=50, blank=True, help_text="e.g., PDF, DOCX, Video")
    file_path = models.CharField(max_length=500, blank=True)
    file_size_bytes = models.BigIntegerField(null=True, blank=True)
    
    # Extracted content
    extracted_text = models.TextField(blank=True, help_text="Full text extracted from submission")
    text_length = models.IntegerField(default=0)
    extraction_status = models.CharField(max_length=20, choices=EXTRACTION_STATUS_CHOICES, default='pending')
    extraction_method = models.CharField(max_length=100, blank=True, help_text="e.g., OCR, PDF parser, Speech-to-text")
    
    # Embeddings (stored as JSON array)
    text_embedding = models.JSONField(
        default=list,
        help_text="Vector embedding for semantic search"
    )
    embedding_model = models.CharField(max_length=100, blank=True, help_text="e.g., sentence-transformers")
    embedding_dimension = models.IntegerField(null=True, blank=True)
    
    # Metadata
    metadata = models.JSONField(
        default=dict,
        help_text="Additional submission metadata (language, readability, keywords, etc.)"
    )
    
    # Tagging statistics
    total_tags = models.IntegerField(default=0)
    criteria_covered = models.JSONField(default=list, help_text="List of criterion IDs with evidence")
    
    # Audit
    submitted_at = models.DateTimeField(null=True, blank=True)
    extracted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['mapping', 'student_id']),
            models.Index(fields=['extraction_status']),
            models.Index(fields=['submitted_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.evidence_number:
            date_str = datetime.now().strftime('%Y%m%d')
            random_suffix = secrets.token_hex(3).upper()
            self.evidence_number = f"EVD-{date_str}-{random_suffix}"
        
        if self.extracted_text:
            self.text_length = len(self.extracted_text)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.evidence_number} - {self.student_id}"


class CriteriaTag(models.Model):
    """
    Tagged evidence linking submission excerpts to specific criteria.
    """
    TAG_TYPE_CHOICES = [
        ('direct', 'Direct Evidence'),
        ('indirect', 'Indirect Evidence'),
        ('supporting', 'Supporting Material'),
        ('reference', 'Reference/Citation'),
    ]
    
    CONFIDENCE_LEVEL_CHOICES = [
        ('high', 'High Confidence'),
        ('medium', 'Medium Confidence'),
        ('low', 'Low Confidence'),
        ('manual', 'Manually Tagged'),
    ]
    
    tag_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    evidence = models.ForeignKey(SubmissionEvidence, on_delete=models.CASCADE, related_name='tags')
    
    # Criteria linkage
    criterion_id = models.CharField(max_length=100, help_text="Reference to assessment criterion")
    criterion_name = models.CharField(max_length=200)
    criterion_description = models.TextField(blank=True)
    
    # Tagged text
    tagged_text = models.TextField(help_text="Excerpt from submission linked to criterion")
    text_start_position = models.IntegerField(help_text="Character position in original text")
    text_end_position = models.IntegerField()
    
    # Context
    context_before = models.TextField(blank=True, help_text="Text before tagged excerpt")
    context_after = models.TextField(blank=True, help_text="Text after tagged excerpt")
    
    # Tag details
    tag_type = models.CharField(max_length=20, choices=TAG_TYPE_CHOICES, default='direct')
    confidence_level = models.CharField(max_length=20, choices=CONFIDENCE_LEVEL_CHOICES, default='manual')
    confidence_score = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Automated confidence score (0-1)"
    )
    
    # Annotations
    notes = models.TextField(blank=True, help_text="Assessor notes about this evidence")
    keywords = models.JSONField(default=list, help_text="Extracted keywords from tagged text")
    
    # Validation
    is_validated = models.BooleanField(default=False)
    validated_by = models.CharField(max_length=100, blank=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    
    # Audit
    tagged_by = models.CharField(max_length=100)
    tagged_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-tagged_at']
        indexes = [
            models.Index(fields=['evidence', 'criterion_id']),
            models.Index(fields=['tag_type']),
            models.Index(fields=['confidence_level']),
            models.Index(fields=['is_validated']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.tag_number:
            date_str = datetime.now().strftime('%Y%m%d')
            random_suffix = secrets.token_hex(3).upper()
            self.tag_number = f"TAG-{date_str}-{random_suffix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.tag_number} - {self.criterion_id}"
    
    def get_tagged_length(self):
        """Get length of tagged text"""
        return len(self.tagged_text)


class EvidenceAudit(models.Model):
    """
    Comprehensive audit trail for all evidence mapping actions.
    """
    ACTION_CHOICES = [
        ('mapping_created', 'Mapping Created'),
        ('submission_added', 'Submission Added'),
        ('text_extracted', 'Text Extracted'),
        ('embedding_generated', 'Embedding Generated'),
        ('evidence_tagged', 'Evidence Tagged'),
        ('tag_validated', 'Tag Validated'),
        ('tag_removed', 'Tag Removed'),
        ('search_performed', 'Search Performed'),
        ('export_generated', 'Export Generated'),
    ]
    
    mapping = models.ForeignKey(EvidenceMapping, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    
    # Related objects
    submission_id = models.CharField(max_length=100, blank=True)
    criterion_id = models.CharField(max_length=100, blank=True)
    tag_id = models.IntegerField(null=True, blank=True)
    
    # Action details
    action_data = models.JSONField(
        default=dict,
        help_text="Detailed data about the action performed"
    )
    
    # Changes tracking
    changes_made = models.JSONField(
        default=dict,
        help_text="Before/after values for modifications"
    )
    
    # Performance
    processing_time_ms = models.IntegerField(null=True, blank=True)
    
    # User
    performed_by = models.CharField(max_length=100)
    user_role = models.CharField(max_length=50, blank=True)
    
    # IP and context
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    
    # Audit
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['mapping', 'action']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['performed_by']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class EmbeddingSearch(models.Model):
    """
    Log of embedding-based semantic searches for analytics and optimization.
    """
    SEARCH_TYPE_CHOICES = [
        ('similarity', 'Similarity Search'),
        ('criteria_match', 'Criteria Matching'),
        ('keyword', 'Keyword Search'),
        ('hybrid', 'Hybrid Search'),
    ]
    
    search_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    mapping = models.ForeignKey(EvidenceMapping, on_delete=models.CASCADE, related_name='searches')
    
    # Search details
    search_type = models.CharField(max_length=20, choices=SEARCH_TYPE_CHOICES)
    query_text = models.TextField()
    query_embedding = models.JSONField(default=list, help_text="Vector embedding of query")
    
    # Filters applied
    filter_criteria = models.JSONField(default=dict, help_text="Additional filters (student, date range, etc.)")
    
    # Results
    results_count = models.IntegerField(default=0)
    top_results = models.JSONField(default=list, help_text="Top matching results with scores")
    
    # Performance
    search_time_ms = models.IntegerField(null=True, blank=True, help_text="Search execution time")
    
    # User
    performed_by = models.CharField(max_length=100)
    
    # Audit
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['mapping', 'search_type']),
            models.Index(fields=['timestamp']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.search_number:
            date_str = datetime.now().strftime('%Y%m%d')
            random_suffix = secrets.token_hex(3).upper()
            self.search_number = f"SRCH-{date_str}-{random_suffix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.search_number} - {self.search_type}"
