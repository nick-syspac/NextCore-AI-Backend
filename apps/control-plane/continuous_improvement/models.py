from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# Import extended CIR models
from .models_cir import (
    ActionStep,
    Comment,
    Attachment,
    Verification,
    ClauseLink,
    SLAPolicy,
    KPISnapshot,
    TaxonomyLabel,
    AIRun,
    Embedding,
)

__all__ = [
    "ImprovementCategory",
    "ImprovementAction",
    "ActionTracking",
    "ImprovementReview",
    "ActionStep",
    "Comment",
    "Attachment",
    "Verification",
    "ClauseLink",
    "SLAPolicy",
    "KPISnapshot",
    "TaxonomyLabel",
    "AIRun",
    "Embedding",
]


class ImprovementCategory(models.Model):
    """
    Categories for organizing improvement actions aligned with ASQA standards.
    """

    CATEGORY_TYPE_CHOICES = [
        ("training_assessment", "Training & Assessment"),
        ("trainer_qualifications", "Trainer & Assessor Qualifications"),
        ("student_support", "Student Support Services"),
        ("facilities_equipment", "Facilities & Equipment"),
        ("admin_records", "Administration & Records"),
        ("compliance_governance", "Compliance & Governance"),
        ("marketing_recruitment", "Marketing & Recruitment"),
        ("financial_management", "Financial Management"),
        ("quality_assurance", "Quality Assurance"),
        ("stakeholder_engagement", "Stakeholder Engagement"),
        ("continuous_improvement", "Continuous Improvement"),
        ("other", "Other"),
    ]

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="improvement_categories",
    )
    name = models.CharField(max_length=200)
    category_type = models.CharField(max_length=50, choices=CATEGORY_TYPE_CHOICES)
    description = models.TextField(blank=True)
    color_code = models.CharField(
        max_length=7, default="#3B82F6", help_text="Hex color code for UI display"
    )

    # ASQA alignment
    related_standards = models.JSONField(
        default=list, help_text="List of ASQA standard numbers this category relates to"
    )

    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_categories"
    )

    class Meta:
        db_table = "improvement_categories"
        verbose_name = "Improvement Category"
        verbose_name_plural = "Improvement Categories"
        ordering = ["name"]
        unique_together = [["tenant", "name"]]
        indexes = [
            models.Index(fields=["tenant", "is_active"]),
            models.Index(fields=["category_type"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"


class ImprovementAction(models.Model):
    """
    Individual improvement actions tracked in the continuous improvement register.
    Includes AI classification and summarization capabilities.
    """

    PRIORITY_CHOICES = [
        ("critical", "Critical"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    STATUS_CHOICES = [
        ("identified", "Identified"),
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    SOURCE_CHOICES = [
        ("audit", "Audit Finding"),
        ("complaint", "Complaint"),
        ("feedback", "Stakeholder Feedback"),
        ("self_assessment", "Self Assessment"),
        ("staff_suggestion", "Staff Suggestion"),
        ("student_feedback", "Student Feedback"),
        ("industry_feedback", "Industry Feedback"),
        ("regulator_feedback", "Regulator Feedback"),
        ("data_analysis", "Data Analysis"),
        ("benchmarking", "Benchmarking"),
        ("other", "Other"),
    ]

    # Basic info
    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="improvement_actions"
    )
    action_number = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField(
        help_text="Detailed description of the improvement action"
    )

    # Classification
    category = models.ForeignKey(
        ImprovementCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="actions",
    )
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="medium"
    )
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)

    # AI Classification & Summarization
    ai_classified_category = models.CharField(
        max_length=50,
        blank=True,
        help_text="AI-suggested category based on content analysis",
    )
    ai_classification_confidence = models.FloatField(
        default=0.0, help_text="Confidence score (0.0-1.0) for AI classification"
    )
    ai_summary = models.TextField(
        blank=True, help_text="AI-generated summary of the action"
    )
    ai_keywords = models.JSONField(
        default=list, help_text="AI-extracted keywords from description"
    )
    ai_related_standards = models.JSONField(
        default=list, help_text="AI-identified ASQA standards related to this action"
    )
    ai_processed_at = models.DateTimeField(null=True, blank=True)

    # Status & Timeline
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="identified"
    )
    identified_date = models.DateField(default=timezone.now)
    planned_start_date = models.DateField(null=True, blank=True)
    target_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)

    # Assignment
    responsible_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responsible_improvement_actions",
    )
    supporting_staff = models.ManyToManyField(
        User,
        blank=True,
        related_name="supporting_improvement_actions",
        help_text="Additional staff supporting this action",
    )

    # Implementation details
    root_cause = models.TextField(blank=True, help_text="Root cause analysis")
    proposed_solution = models.TextField(blank=True)
    resources_required = models.TextField(blank=True)
    estimated_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    actual_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Effectiveness & Impact
    success_criteria = models.TextField(blank=True, help_text="How to measure success")
    expected_impact = models.TextField(blank=True)
    actual_impact = models.TextField(blank=True, help_text="Post-implementation impact")
    effectiveness_rating = models.IntegerField(
        null=True, blank=True, help_text="Rating 1-5 after completion"
    )

    # Compliance tracking
    compliance_status = models.CharField(
        max_length=20,
        choices=[
            ("compliant", "Compliant"),
            ("at_risk", "At Risk"),
            ("overdue", "Overdue"),
            ("completed", "Completed"),
        ],
        default="compliant",
    )
    is_critical_compliance = models.BooleanField(
        default=False, help_text="Critical for maintaining RTO registration"
    )

    # Review & Approval
    requires_approval = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_improvement_actions",
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    tags = models.JSONField(default=list, help_text="Custom tags for filtering")
    attachments = models.JSONField(
        default=list, help_text="List of attachment URLs/metadata"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_improvement_actions",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "improvement_actions"
        verbose_name = "Improvement Action"
        verbose_name_plural = "Improvement Actions"
        ordering = ["-created_at"]
        unique_together = [["tenant", "action_number"]]
        indexes = [
            models.Index(fields=["tenant", "status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["compliance_status"]),
            models.Index(fields=["target_completion_date"]),
            models.Index(fields=["responsible_person"]),
        ]

    def __str__(self):
        return f"{self.action_number} - {self.title}"

    def save(self, *args, **kwargs):
        # Auto-update compliance status based on dates
        if self.status == "completed" and self.actual_completion_date:
            self.compliance_status = "completed"
        elif self.target_completion_date:
            today = timezone.now().date()
            days_until_due = (self.target_completion_date - today).days

            if days_until_due < 0:
                self.compliance_status = "overdue"
            elif days_until_due <= 7:
                self.compliance_status = "at_risk"
            else:
                self.compliance_status = "compliant"

        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Check if action is overdue"""
        if self.status in ["completed", "cancelled"]:
            return False
        if self.target_completion_date:
            return timezone.now().date() > self.target_completion_date
        return False

    @property
    def days_until_due(self):
        """Calculate days until target completion"""
        if self.target_completion_date:
            delta = self.target_completion_date - timezone.now().date()
            return delta.days
        return None

    @property
    def progress_percentage(self):
        """Calculate progress based on status and tracking"""
        status_progress = {
            "identified": 10,
            "planned": 25,
            "in_progress": 50,
            "on_hold": 50,
            "completed": 100,
            "cancelled": 0,
        }
        return status_progress.get(self.status, 0)


class ActionTracking(models.Model):
    """
    Track progress updates and milestones for improvement actions.
    """

    UPDATE_TYPE_CHOICES = [
        ("progress", "Progress Update"),
        ("milestone", "Milestone Achieved"),
        ("issue", "Issue/Blocker"),
        ("resource_change", "Resource Change"),
        ("timeline_change", "Timeline Change"),
        ("status_change", "Status Change"),
        ("completion", "Completion"),
        ("review", "Review"),
    ]

    # Relationships
    improvement_action = models.ForeignKey(
        ImprovementAction, on_delete=models.CASCADE, related_name="tracking_updates"
    )

    # Update details
    update_type = models.CharField(max_length=30, choices=UPDATE_TYPE_CHOICES)
    update_text = models.TextField(help_text="Description of the update")

    # Progress tracking
    progress_percentage = models.IntegerField(
        null=True, blank=True, help_text="Overall progress (0-100)"
    )
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)

    # Issues & blockers
    is_blocker = models.BooleanField(default=False)
    blocker_resolved = models.BooleanField(default=False)
    blocker_resolution = models.TextField(blank=True)

    # Evidence & attachments
    evidence_provided = models.JSONField(
        default=list, help_text="Evidence of progress (file URLs, references)"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "action_tracking"
        verbose_name = "Action Tracking Update"
        verbose_name_plural = "Action Tracking Updates"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["improvement_action", "created_at"]),
            models.Index(fields=["update_type"]),
            models.Index(fields=["is_blocker"]),
        ]

    def __str__(self):
        return f"{self.improvement_action.action_number} - {self.get_update_type_display()}"


class ImprovementReview(models.Model):
    """
    Periodic reviews of the continuous improvement register.
    """

    REVIEW_TYPE_CHOICES = [
        ("monthly", "Monthly Review"),
        ("quarterly", "Quarterly Review"),
        ("annual", "Annual Review"),
        ("ad_hoc", "Ad-hoc Review"),
    ]

    # Basic info
    tenant = models.ForeignKey(
        "tenants.Tenant", on_delete=models.CASCADE, related_name="improvement_reviews"
    )
    review_number = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPE_CHOICES)
    review_date = models.DateField()

    # Review scope
    actions_reviewed = models.ManyToManyField(
        ImprovementAction, related_name="reviews", blank=True
    )
    review_period_start = models.DateField()
    review_period_end = models.DateField()

    # Summary statistics
    total_actions_reviewed = models.IntegerField(default=0)
    actions_completed = models.IntegerField(default=0)
    actions_on_track = models.IntegerField(default=0)
    actions_at_risk = models.IntegerField(default=0)
    actions_overdue = models.IntegerField(default=0)

    # AI-generated insights
    ai_summary = models.TextField(
        blank=True, help_text="AI-generated summary of review findings"
    )
    ai_trends = models.JSONField(
        default=list, help_text="AI-identified trends and patterns"
    )
    ai_recommendations = models.JSONField(
        default=list, help_text="AI-generated recommendations"
    )

    # Review outcomes
    key_findings = models.TextField(blank=True)
    areas_of_concern = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    action_items = models.JSONField(
        default=list, help_text="New actions arising from review"
    )

    # Review participants
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="conducted_reviews"
    )
    attendees = models.ManyToManyField(
        User, blank=True, related_name="attended_reviews"
    )

    # Approval & distribution
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_reviews",
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    notes = models.TextField(blank=True)
    attachments = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "improvement_reviews"
        verbose_name = "Improvement Review"
        verbose_name_plural = "Improvement Reviews"
        ordering = ["-review_date"]
        unique_together = [["tenant", "review_number"]]
        indexes = [
            models.Index(fields=["tenant", "review_date"]),
            models.Index(fields=["review_type"]),
        ]

    def __str__(self):
        return f"{self.review_number} - {self.title}"

    def calculate_statistics(self):
        """Calculate review statistics from included actions"""
        actions = self.actions_reviewed.all()

        self.total_actions_reviewed = actions.count()
        self.actions_completed = actions.filter(status="completed").count()
        self.actions_on_track = actions.filter(compliance_status="compliant").count()
        self.actions_at_risk = actions.filter(compliance_status="at_risk").count()
        self.actions_overdue = actions.filter(compliance_status="overdue").count()

        self.save()
