"""
Extended models for comprehensive Funding Eligibility system.
Implements rules engine, jurisdiction connectors, decision store, and webhook integration.
"""
from __future__ import annotations

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import hashlib
import json

User = get_user_model()


class Jurisdiction(models.Model):
    """
    Australian jurisdictions with active funding programs.
    """
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    default_ruleset = models.ForeignKey(
        'Ruleset',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    
    # Configuration
    config = models.JSONField(
        default=dict,
        help_text="Jurisdiction-specific configuration"
    )
    
    class Meta:
        db_table = 'funding_jurisdictions'
        verbose_name = 'Jurisdiction'
        verbose_name_plural = 'Jurisdictions'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Ruleset(models.Model):
    """
    Versioned rulesets for eligibility evaluation.
    Immutable once activated to ensure reproducibility.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('retired', 'Retired'),
    ]
    
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20, help_text="Semantic version (e.g., 1.7.2)")
    jurisdiction_code = models.CharField(max_length=10)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    # Checksum for integrity
    checksum = models.CharField(max_length=64, editable=False, help_text="SHA256 of rule content")
    
    # Metadata
    description = models.TextField(blank=True)
    changelog = models.TextField(blank=True, help_text="Changes from previous version")
    
    # Audit
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_rulesets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    retired_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'funding_rulesets'
        unique_together = [['jurisdiction_code', 'version']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['jurisdiction_code', 'status']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.jurisdiction_code} v{self.version} [{self.status}]"
    
    def save(self, *args, **kwargs):
        # Generate checksum if not set
        if not self.checksum and hasattr(self, 'artifacts'):
            content = ''.join([a.blob for a in self.artifacts.all()])
            self.checksum = hashlib.sha256(content.encode()).hexdigest()
        super().save(*args, **kwargs)
    
    def activate(self):
        """Activate this ruleset and retire others for same jurisdiction"""
        if self.status != 'draft':
            raise ValidationError("Only draft rulesets can be activated")
        
        # Retire active rulesets
        Ruleset.objects.filter(
            jurisdiction_code=self.jurisdiction_code,
            status='active'
        ).update(status='retired', retired_at=timezone.now())
        
        # Activate this ruleset
        self.status = 'active'
        self.activated_at = timezone.now()
        self.save()


class RulesetArtifact(models.Model):
    """
    Rule content for a ruleset (JSONLogic, Rego, etc.).
    """
    TYPE_CHOICES = [
        ('jsonlogic', 'JSONLogic'),
        ('rego', 'Open Policy Agent (Rego)'),
        ('python', 'Python Expression'),
    ]
    
    ruleset = models.ForeignKey(
        Ruleset,
        on_delete=models.CASCADE,
        related_name='artifacts'
    )
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100, help_text="Artifact name/identifier")
    blob = models.TextField(help_text="Rule content")
    
    # Metadata
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'funding_ruleset_artifacts'
        unique_together = [['ruleset', 'name']]
    
    def __str__(self):
        return f"{self.ruleset} - {self.name}"


class ReferenceTable(models.Model):
    """
    Reference data for rule evaluation (concession types, postcode mappings, caps, etc.).
    """
    namespace = models.CharField(max_length=100, help_text="Data namespace (e.g., 'vic.concessions')")
    version = models.CharField(max_length=20)
    
    data = models.JSONField(help_text="Reference data as JSON")
    
    # Source tracking
    source = models.CharField(max_length=200, help_text="Data source URL or description")
    checksum = models.CharField(max_length=64, help_text="SHA256 of data")
    
    # Validity
    valid_from = models.DateField(default=timezone.now)
    valid_until = models.DateField(null=True, blank=True)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'funding_reference_tables'
        unique_together = [['namespace', 'version']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['namespace', 'valid_from', 'valid_until']),
        ]
    
    def __str__(self):
        return f"{self.namespace} v{self.version}"
    
    def save(self, *args, **kwargs):
        # Generate checksum
        data_str = json.dumps(self.data, sort_keys=True)
        self.checksum = hashlib.sha256(data_str.encode()).hexdigest()
        super().save(*args, **kwargs)


class EligibilityRequest(models.Model):
    """
    Request for eligibility evaluation.
    Immutable input snapshot for audit trail.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('evaluating', 'Evaluating'),
        ('evaluated', 'Evaluated'),
        ('error', 'Error'),
    ]
    
    id = models.AutoField(primary_key=True)
    
    # Tenant & user
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='eligibility_requests'
    )
    person_id = models.CharField(max_length=100, help_text="Person identifier in SMS/LMS")
    course_id = models.CharField(max_length=100, help_text="Course identifier")
    
    # Jurisdiction
    jurisdiction_code = models.CharField(max_length=10)
    
    # Input snapshot (immutable)
    input = models.JSONField(
        help_text="Complete input data for evaluation"
    )
    
    # Evidence attachments
    evidence_refs = models.JSONField(
        default=list,
        help_text="References to attached evidence documents"
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='eligibility_requests'
    )
    metadata = models.JSONField(default=dict, help_text="Additional metadata")
    
    class Meta:
        db_table = 'funding_eligibility_requests'
        ordering = ['-requested_at']
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['person_id']),
            models.Index(fields=['jurisdiction_code']),
            models.Index(fields=['requested_at']),
        ]
    
    def __str__(self):
        return f"REQ-{self.id} ({self.jurisdiction_code})"


class ExternalLookup(models.Model):
    """
    External API lookups with caching.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('error', 'Error'),
        ('timeout', 'Timeout'),
    ]
    
    request = models.ForeignKey(
        EligibilityRequest,
        on_delete=models.CASCADE,
        related_name='external_lookups'
    )
    
    # Provider
    provider = models.CharField(max_length=100, help_text="API provider (USI, visa, etc.)")
    
    # Request/response
    request_data = models.JSONField()
    response_data = models.JSONField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    # Performance
    latency_ms = models.IntegerField(null=True, blank=True)
    
    # Caching
    cached_until = models.DateTimeField(null=True, blank=True)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'funding_external_lookups'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['request', 'provider']),
            models.Index(fields=['provider', 'status']),
            models.Index(fields=['cached_until']),
        ]
    
    def __str__(self):
        return f"{self.provider} lookup for {self.request}"


class EligibilityDecision(models.Model):
    """
    Final eligibility decision for a request.
    Immutable once created.
    """
    OUTCOME_CHOICES = [
        ('eligible', 'Eligible'),
        ('ineligible', 'Ineligible'),
        ('review', 'Manual Review Required'),
    ]
    
    id = models.AutoField(primary_key=True)
    
    request = models.OneToOneField(
        EligibilityRequest,
        on_delete=models.CASCADE,
        related_name='decision'
    )
    
    # Ruleset used
    ruleset = models.ForeignKey(
        Ruleset,
        on_delete=models.PROTECT,
        related_name='decisions'
    )
    
    # Outcome
    outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES)
    
    # Reasons & clauses
    reasons = models.JSONField(
        default=list,
        help_text="Reason codes for the decision"
    )
    clause_refs = models.JSONField(
        default=list,
        help_text="Relevant clause/policy references"
    )
    
    # Full decision data
    decision_data = models.JSONField(
        help_text="Complete decision output from rules engine"
    )
    
    # Human-readable explanation
    explanation = models.TextField(blank=True)
    
    # Decision maker
    decided_by = models.CharField(
        max_length=20,
        choices=[('system', 'System'), ('user', 'User')],
        default='system'
    )
    decided_by_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eligibility_decisions'
    )
    
    # Timestamp
    decided_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'funding_eligibility_decisions'
        ordering = ['-decided_at']
        indexes = [
            models.Index(fields=['request']),
            models.Index(fields=['outcome']),
            models.Index(fields=['ruleset']),
        ]
    
    def __str__(self):
        return f"Decision for {self.request}: {self.get_outcome_display()}"


class DecisionOverride(models.Model):
    """
    Manual override of automated decisions.
    """
    decision = models.ForeignKey(
        EligibilityDecision,
        on_delete=models.CASCADE,
        related_name='overrides'
    )
    
    # Override details
    reason_code = models.CharField(max_length=50)
    justification = models.TextField(help_text="Detailed justification for override")
    final_outcome = models.CharField(
        max_length=20,
        choices=EligibilityDecision.OUTCOME_CHOICES
    )
    
    # Approval
    approver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='funding_decision_overrides'
    )
    approved_at = models.DateTimeField(auto_now_add=True)
    
    # Policy reference
    policy_version = models.CharField(
        max_length=20,
        help_text="Override policy version applied"
    )
    
    # Supporting evidence
    evidence_refs = models.JSONField(default=list)
    
    class Meta:
        db_table = 'funding_decision_overrides'
        ordering = ['-approved_at']
        indexes = [
            models.Index(fields=['decision']),
            models.Index(fields=['approver']),
        ]
    
    def __str__(self):
        return f"Override for {self.decision} by {self.approver}"


class EvidenceAttachment(models.Model):
    """
    Evidence documents attached to eligibility requests.
    """
    TYPE_CHOICES = [
        ('id', 'ID Document'),
        ('concession', 'Concession Card'),
        ('residency', 'Proof of Residency'),
        ('visa', 'Visa Document'),
        ('qualification', 'Prior Qualification'),
        ('employment', 'Employment Proof'),
        ('income', 'Income Statement'),
        ('other', 'Other'),
    ]
    
    request = models.ForeignKey(
        EligibilityRequest,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    
    # File details
    file_uri = models.CharField(max_length=500, help_text="S3/storage URI")
    filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(help_text="Size in bytes")
    mime_type = models.CharField(max_length=100)
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Verification
    verified = models.BooleanField(default=False)
    verifier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='funding_verified_evidence'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    
    # Upload
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='funding_uploaded_evidence'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'funding_evidence_attachments'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['request', 'type']),
            models.Index(fields=['verified']),
        ]
    
    def __str__(self):
        return f"{self.get_type_display()} for {self.request}"


class WebhookEndpoint(models.Model):
    """
    Webhook configuration for SMS/LMS integration.
    """
    TARGET_CHOICES = [
        ('sms', 'Student Management System'),
        ('lms', 'Learning Management System'),
        ('other', 'Other System'),
    ]
    
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='webhook_endpoints'
    )
    
    # Configuration
    name = models.CharField(max_length=200)
    target = models.CharField(max_length=20, choices=TARGET_CHOICES)
    url = models.URLField()
    secret = models.CharField(max_length=255, help_text="HMAC secret for signing")
    
    # Events to send
    events = models.JSONField(
        default=list,
        help_text="Event types to send (e.g., ['decision.finalized', 'override.approved'])"
    )
    
    # Status
    active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'funding_webhook_endpoints'
        indexes = [
            models.Index(fields=['tenant', 'active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.target})"


class WebhookDelivery(models.Model):
    """
    Webhook delivery attempts and results.
    """
    endpoint = models.ForeignKey(
        WebhookEndpoint,
        on_delete=models.CASCADE,
        related_name='deliveries'
    )
    
    # Event
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    
    # Delivery
    status_code = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    
    # Timing
    attempt_count = models.IntegerField(default=1)
    last_attempt_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'funding_webhook_deliveries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['endpoint', 'event_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.event_type} to {self.endpoint}"
