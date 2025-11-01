"""
Extended CIR models for comprehensive improvement tracking.
Extends the existing ImprovementAction model with additional entities for
workflow steps, verification, compliance tracking, and AI-assisted operations.
"""

from __future__ import annotations

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

User = get_user_model()


class ActionStep(models.Model):
    """
    Individual steps/tasks within an improvement action for detailed workflow tracking.
    """

    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("blocked", "Blocked"),
        ("cancelled", "Cancelled"),
    ]

    # Relationships
    improvement_action = models.ForeignKey(
        "continuous_improvement.ImprovementAction",
        on_delete=models.CASCADE,
        related_name="steps",
    )

    # Step details
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sequence_order = models.IntegerField(default=0, help_text="Order of execution")

    # Assignment & status
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_action_steps",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="not_started"
    )

    # Timeline
    due_date = models.DateField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Progress & evidence
    progress_notes = models.TextField(blank=True)
    evidence_refs = models.JSONField(
        default=list, help_text="References to evidence documents/files"
    )

    # Blocking issues
    is_blocked = models.BooleanField(default=False)
    blocker_description = models.TextField(blank=True)
    blocker_resolved_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cir_action_steps"
        verbose_name = "Action Step"
        verbose_name_plural = "Action Steps"
        ordering = ["improvement_action", "sequence_order", "created_at"]
        indexes = [
            models.Index(fields=["improvement_action", "status"]),
            models.Index(fields=["owner"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self):
        return f"{self.improvement_action.action_number} - Step {self.sequence_order}: {self.title}"

    @property
    def is_overdue(self):
        """Check if step is overdue"""
        if self.status in ["completed", "cancelled"]:
            return False
        if self.due_date:
            return timezone.now().date() > self.due_date
        return False


class Comment(models.Model):
    """
    Comments/notes on improvement actions for collaboration and audit trail.
    """

    VISIBILITY_CHOICES = [
        ("internal", "Internal Only"),
        ("restricted", "Restricted"),
        ("auditor", "Visible to Auditors"),
        ("public", "Public"),
    ]

    # Relationships
    improvement_action = models.ForeignKey(
        "continuous_improvement.ImprovementAction",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    # Comment details
    body = models.TextField()
    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default="internal"
    )

    # Optional parent for threaded comments
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    # Mentions & notifications
    mentioned_users = models.ManyToManyField(
        User, blank=True, related_name="mentioned_in_comments"
    )

    # Metadata
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="improvement_comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    class Meta:
        db_table = "cir_comments"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["improvement_action", "created_at"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return f"Comment on {self.improvement_action.action_number} by {self.author}"


class Attachment(models.Model):
    """
    File attachments linked to improvement actions.
    """

    KIND_CHOICES = [
        ("document", "Document"),
        ("image", "Image"),
        ("evidence", "Evidence"),
        ("report", "Report"),
        ("correspondence", "Correspondence"),
        ("other", "Other"),
    ]

    # Relationships
    improvement_action = models.ForeignKey(
        "continuous_improvement.ImprovementAction",
        on_delete=models.CASCADE,
        related_name="file_attachments",
    )

    # File details
    file_uri = models.CharField(max_length=500, help_text="S3 URI or file path")
    filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(null=True, blank=True, help_text="Size in bytes")
    mime_type = models.CharField(max_length=100, blank=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="document")

    # Security & integrity
    sha256_hash = models.CharField(
        max_length=64, blank=True, help_text="File integrity hash"
    )

    # Metadata
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="uploaded_attachments"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cir_attachments"
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["improvement_action"]),
            models.Index(fields=["kind"]),
        ]

    def __str__(self):
        return f"{self.filename} - {self.improvement_action.action_number}"


class Verification(models.Model):
    """
    Verification records for completed improvement actions.
    """

    OUTCOME_CHOICES = [
        ("verified", "Verified - Effective"),
        ("verified_partial", "Verified - Partially Effective"),
        ("not_verified", "Not Verified"),
        ("requires_rework", "Requires Rework"),
    ]

    # Relationships
    improvement_action = models.ForeignKey(
        "continuous_improvement.ImprovementAction",
        on_delete=models.CASCADE,
        related_name="verifications",
    )

    # Verification details
    outcome = models.CharField(max_length=30, choices=OUTCOME_CHOICES)
    notes = models.TextField(help_text="Verification findings and observations")

    # Evidence
    evidence_reviewed = models.JSONField(
        default=list, help_text="List of evidence items reviewed"
    )

    # Effectiveness assessment
    effectiveness_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Effectiveness rating 1-5",
    )

    # Follow-up
    requires_followup = models.BooleanField(default=False)
    followup_actions = models.TextField(blank=True)
    followup_due_date = models.DateField(null=True, blank=True)

    # Verifier
    verifier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="conducted_verifications",
    )
    verified_at = models.DateTimeField(default=timezone.now)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cir_verifications"
        verbose_name = "Verification"
        verbose_name_plural = "Verifications"
        ordering = ["-verified_at"]
        indexes = [
            models.Index(fields=["improvement_action", "verified_at"]),
            models.Index(fields=["outcome"]),
            models.Index(fields=["requires_followup"]),
        ]

    def __str__(self):
        return f"Verification of {self.improvement_action.action_number} - {self.get_outcome_display()}"


class ClauseLink(models.Model):
    """
    Links between improvement actions and compliance clauses (ASQA, ISO, etc.).
    Tracks both AI-suggested and manually assigned clause relationships.
    """

    SOURCE_CHOICES = [
        ("ai", "AI-Suggested"),
        ("human", "Manually Assigned"),
    ]

    # Relationships
    improvement_action = models.ForeignKey(
        "continuous_improvement.ImprovementAction",
        on_delete=models.CASCADE,
        related_name="clause_links",
    )
    clause = models.ForeignKey(
        "policy_comparator.ASQAClause",
        on_delete=models.CASCADE,
        related_name="improvement_links",
    )

    # Link metadata
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    confidence = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Confidence score for AI suggestions (0.0-1.0)",
    )

    # Rationale
    rationale = models.TextField(
        blank=True, help_text="Explanation for the clause link"
    )

    # Review status
    reviewed = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_clause_links",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_clause_links"
    )

    class Meta:
        db_table = "cir_clause_links"
        verbose_name = "Clause Link"
        verbose_name_plural = "Clause Links"
        unique_together = [["improvement_action", "clause"]]
        ordering = ["-confidence", "-created_at"]
        indexes = [
            models.Index(fields=["improvement_action"]),
            models.Index(fields=["clause"]),
            models.Index(fields=["source", "confidence"]),
        ]

    def __str__(self):
        return f"{self.improvement_action.action_number} → {self.clause.clause_number}"


class SLAPolicy(models.Model):
    """
    Service Level Agreement policies for improvement action timelines.
    Defines target completion times based on priority, type, or category.
    """

    # Relationships
    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="sla_policies"
    )

    # Policy details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Target timeline
    target_days = models.IntegerField(help_text="Target completion time in days")

    # Applicability rules (JSON query filter)
    applies_to_priorities = models.JSONField(
        default=list, help_text="List of priorities this policy applies to"
    )
    applies_to_sources = models.JSONField(
        default=list, help_text="List of source types this policy applies to"
    )
    applies_to_categories = models.JSONField(
        default=list, help_text="List of category IDs this policy applies to"
    )

    # Escalation
    warning_days_before = models.IntegerField(
        default=7, help_text="Days before due date to trigger warning"
    )
    escalate_on_breach = models.BooleanField(
        default=True, help_text="Auto-escalate when SLA is breached"
    )
    escalation_recipients = models.JSONField(
        default=list, help_text="User IDs to notify on escalation"
    )

    # Status
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_sla_policies"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cir_sla_policies"
        verbose_name = "SLA Policy"
        verbose_name_plural = "SLA Policies"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["tenant", "is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.target_days} days)"

    def applies_to_action(self, action) -> bool:
        """Check if this SLA policy applies to a given improvement action."""
        # Check priority
        if (
            self.applies_to_priorities
            and action.priority not in self.applies_to_priorities
        ):
            return False

        # Check source
        if self.applies_to_sources and action.source not in self.applies_to_sources:
            return False

        # Check category
        if self.applies_to_categories and action.category_id:
            if action.category_id not in self.applies_to_categories:
                return False

        return True


class KPISnapshot(models.Model):
    """
    Periodic snapshots of key performance indicators for compliance tracking.
    Stores point-in-time metrics for trend analysis and reporting.
    """

    PERIOD_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("annual", "Annual"),
    ]

    # Relationships
    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="kpi_snapshots"
    )

    # Period & timing
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    computed_at = models.DateTimeField(default=timezone.now)

    # Core metrics
    metric_key = models.CharField(max_length=100, help_text="Metric identifier")
    metric_value = models.DecimalField(
        max_digits=12, decimal_places=2, help_text="Numeric metric value"
    )
    metric_unit = models.CharField(
        max_length=50,
        blank=True,
        help_text="Unit of measurement (%, count, days, etc.)",
    )

    # Additional context
    metadata = models.JSONField(
        default=dict, help_text="Additional metric metadata and breakdown"
    )

    # Comparison
    previous_value = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    variance_percentage = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "cir_kpi_snapshots"
        verbose_name = "KPI Snapshot"
        verbose_name_plural = "KPI Snapshots"
        ordering = ["-period_end", "metric_key"]
        unique_together = [["tenant", "metric_key", "period", "period_end"]]
        indexes = [
            models.Index(fields=["tenant", "metric_key", "period_end"]),
            models.Index(fields=["period"]),
        ]

    def __str__(self):
        return f"{self.metric_key}: {self.metric_value} ({self.period} ending {self.period_end})"


class TaxonomyLabel(models.Model):
    """
    Configurable taxonomy labels for classification (types, origins, etc.).
    Enables tenant-specific classification schemes.
    """

    # Relationships
    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="taxonomy_labels"
    )

    # Label details
    key = models.CharField(
        max_length=100, help_text="Label key (e.g., 'type:non-conformance')"
    )
    name = models.CharField(max_length=200, help_text="Display name")
    description = models.TextField(blank=True)

    # Visual
    color = models.CharField(
        max_length=7, default="#6B7280", help_text="Hex color code"
    )
    icon = models.CharField(max_length=50, blank=True, help_text="Icon identifier")

    # Categorization
    category = models.CharField(
        max_length=50, help_text="Label category (type, origin, risk, etc.)"
    )

    # Status
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cir_taxonomy_labels"
        verbose_name = "Taxonomy Label"
        verbose_name_plural = "Taxonomy Labels"
        unique_together = [["tenant", "key"]]
        ordering = ["category", "name"]
        indexes = [
            models.Index(fields=["tenant", "category", "is_active"]),
        ]

    def __str__(self):
        return f"{self.category}: {self.name}"


class AIRun(models.Model):
    """
    Audit log for AI operations (classification, summarization, clause linking).
    Tracks model performance, costs, and provides explainability.
    """

    TASK_TYPE_CHOICES = [
        ("classify", "Classification"),
        ("summarize", "Summarization"),
        ("clause_link", "Clause Linking"),
        ("sentiment", "Sentiment Analysis"),
        ("extract", "Entity Extraction"),
        ("embed", "Embedding Generation"),
    ]

    # Relationships
    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="ai_runs"
    )

    # Target entity
    target_entity = models.CharField(
        max_length=50, help_text="Entity type (improvement_action, etc.)"
    )
    target_id = models.IntegerField(help_text="Entity primary key")

    # Task details
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)

    # Input/output
    input_ref = models.TextField(blank=True, help_text="Reference to input data")
    output_json = models.JSONField(default=dict, help_text="AI output/predictions")

    # Performance metrics
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    tokens_used = models.IntegerField(null=True, blank=True)
    latency_ms = models.IntegerField(
        null=True, blank=True, help_text="Response time in ms"
    )

    # Model info
    model_name = models.CharField(max_length=100, blank=True)
    model_version = models.CharField(max_length=50, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cir_ai_runs"
        verbose_name = "AI Run"
        verbose_name_plural = "AI Runs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["tenant", "task_type", "created_at"]),
            models.Index(fields=["target_entity", "target_id"]),
            models.Index(fields=["success"]),
        ]

    def __str__(self):
        status = "✓" if self.success else "✗"
        return f"{status} {self.get_task_type_display()} for {self.target_entity}#{self.target_id}"


class Embedding(models.Model):
    """
    Vector embeddings for semantic search and similarity matching.
    Requires PostgreSQL with pgvector extension.
    """

    # Relationships
    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="embeddings"
    )

    # Target entity
    entity = models.CharField(max_length=50, help_text="Entity type")
    entity_id = models.IntegerField(help_text="Entity primary key")

    # Vector data
    # Note: In production, replace JSONField with pgvector's VectorField
    # from pgvector.django import VectorField
    # vector = VectorField(dimensions=1536)
    vector = models.JSONField(help_text="Embedding vector (placeholder for pgvector)")

    # Model info
    model = models.CharField(max_length=100, help_text="Embedding model used")
    dimension = models.IntegerField(help_text="Vector dimensions")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cir_embeddings"
        verbose_name = "Embedding"
        verbose_name_plural = "Embeddings"
        unique_together = [["tenant", "entity", "entity_id", "model"]]
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["tenant", "entity", "entity_id"]),
        ]
        # In production with pgvector:
        # indexes = [
        #     models.Index(fields=['tenant', 'entity', 'entity_id']),
        #     IvfflatIndex(
        #         name='embedding_vector_idx',
        #         fields=['vector'],
        #         lists=100,
        #         opclasses=['vector_cosine_ops']
        #     ),
        # ]

    def __str__(self):
        return f"Embedding for {self.entity}#{self.entity_id} ({self.model})"
