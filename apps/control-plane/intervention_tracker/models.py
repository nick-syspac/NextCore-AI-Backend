from django.db import models
from django.utils import timezone
import uuid


class Intervention(models.Model):
    """Main intervention record tracking trainer actions"""

    intervention_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)

    # Student information
    student_id = models.CharField(max_length=100, db_index=True)
    student_name = models.CharField(max_length=200)
    course_id = models.CharField(max_length=100, blank=True)
    course_name = models.CharField(max_length=200, blank=True)

    # Intervention details
    intervention_type = models.CharField(
        max_length=50,
        choices=[
            ("academic_support", "Academic Support"),
            ("attendance_followup", "Attendance Follow-up"),
            ("wellbeing_check", "Wellbeing Check"),
            ("behaviour_management", "Behaviour Management"),
            ("career_guidance", "Career Guidance"),
            ("extension_approval", "Extension Approval"),
            ("special_consideration", "Special Consideration"),
            ("re_engagement", "Re-engagement"),
            ("progress_review", "Progress Review"),
            ("referral", "Referral to Services"),
        ],
    )

    priority_level = models.CharField(
        max_length=20,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("urgent", "Urgent"),
        ],
        default="medium",
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("initiated", "Initiated"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("escalated", "Escalated"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        default="initiated",
    )

    # Trigger information
    trigger_type = models.CharField(
        max_length=50,
        choices=[
            ("manual", "Manual Entry"),
            ("rule_engine", "Rule Engine Auto-trigger"),
            ("system_alert", "System Alert"),
            ("third_party", "Third Party Referral"),
        ],
        default="manual",
    )
    trigger_rule_id = models.CharField(
        max_length=100, blank=True
    )  # Which rule triggered it
    trigger_details = models.JSONField(default=dict)  # Metrics that triggered the rule

    # Action taken
    action_description = models.TextField()
    action_taken_by = models.CharField(max_length=200)  # Trainer/staff name
    action_taken_by_role = models.CharField(max_length=100, blank=True)
    action_date = models.DateTimeField(default=timezone.now)

    # Communication
    communication_method = models.CharField(
        max_length=50,
        choices=[
            ("face_to_face", "Face to Face"),
            ("phone_call", "Phone Call"),
            ("email", "Email"),
            ("video_call", "Video Call"),
            ("sms", "SMS"),
            ("written_note", "Written Note"),
            ("lms_message", "LMS Message"),
        ],
        blank=True,
    )
    communication_notes = models.TextField(blank=True)

    # Outcome tracking
    outcome_achieved = models.CharField(
        max_length=20,
        choices=[
            ("successful", "Successful"),
            ("partial", "Partially Successful"),
            ("unsuccessful", "Unsuccessful"),
            ("pending", "Pending"),
            ("not_applicable", "Not Applicable"),
        ],
        default="pending",
    )
    outcome_description = models.TextField(blank=True)
    outcome_evidence = models.JSONField(
        default=list
    )  # Links to documents, photos, etc.

    # Follow-up
    requires_followup = models.BooleanField(default=False)
    followup_date = models.DateField(null=True, blank=True)
    followup_notes = models.TextField(blank=True)

    # Referrals
    referred_to = models.CharField(
        max_length=200, blank=True
    )  # e.g., Counseling, Disability Services
    referral_accepted = models.BooleanField(null=True, blank=True)
    referral_date = models.DateField(null=True, blank=True)

    # Audit trail
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Documentation for audit
    audit_notes = models.TextField(blank=True)
    compliance_category = models.CharField(
        max_length=100, blank=True
    )  # e.g., "ASQA Requirement 1.5"
    attachments = models.JSONField(default=list)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["tenant", "student_id", "-created_at"]),
            models.Index(fields=["status", "priority_level"]),
            models.Index(fields=["trigger_type", "intervention_type"]),
        ]

    def __str__(self):
        return f"{self.intervention_number} - {self.student_name}"

    def save(self, *args, **kwargs):
        if not self.intervention_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:8].upper()
            self.intervention_number = f"INT-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class InterventionRule(models.Model):
    """Rule engine for automatic intervention triggering"""

    rule_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)

    # Rule metadata
    rule_name = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)  # Higher number = higher priority

    # Trigger conditions
    condition_type = models.CharField(
        max_length=50,
        choices=[
            ("attendance", "Attendance Threshold"),
            ("grade", "Grade Threshold"),
            ("submission", "Submission Pattern"),
            ("engagement", "Engagement Level"),
            ("risk_score", "Risk Score"),
            ("duration", "Time-based"),
            ("composite", "Multiple Conditions"),
        ],
    )

    # Condition parameters (JSON structure)
    conditions = models.JSONField(default=dict)
    # Example: {
    #   "metric": "attendance_rate",
    #   "operator": "less_than",
    #   "threshold": 75,
    #   "period": "last_2_weeks"
    # }

    # Action to take
    intervention_type = models.CharField(
        max_length=50
    )  # Maps to Intervention.intervention_type
    priority_level = models.CharField(max_length=20, default="medium")
    assigned_to_role = models.CharField(
        max_length=100, blank=True
    )  # Auto-assign to this role

    # Notification settings
    notify_staff = models.BooleanField(default=True)
    notification_recipients = models.JSONField(
        default=list
    )  # Email addresses or user IDs
    notification_template = models.TextField(blank=True)

    # Audit and compliance
    compliance_requirement = models.CharField(max_length=200, blank=True)
    last_triggered = models.DateTimeField(null=True, blank=True)
    trigger_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-priority", "rule_name"]

    def __str__(self):
        return f"{self.rule_number} - {self.rule_name}"

    def save(self, *args, **kwargs):
        if not self.rule_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.rule_number = f"RULE-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class InterventionWorkflow(models.Model):
    """Workflow steps for structured intervention processes"""

    workflow_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)

    # Workflow metadata
    workflow_name = models.CharField(max_length=200)
    description = models.TextField()
    intervention_types = models.JSONField(
        default=list
    )  # Which intervention types use this workflow
    is_active = models.BooleanField(default=True)

    # Workflow steps (ordered)
    steps = models.JSONField(default=list)
    # Example: [
    #   {
    #     "step_number": 1,
    #     "step_name": "Initial Assessment",
    #     "description": "Review student records",
    #     "required": true,
    #     "estimated_duration": 15,
    #     "fields_required": ["assessment_notes"]
    #   },
    #   ...
    # ]

    # Approval requirements
    requires_approval = models.BooleanField(default=False)
    approval_roles = models.JSONField(default=list)  # Roles that can approve

    # Documentation requirements
    required_documentation = models.JSONField(default=list)
    # Example: ["Student consent form", "Intervention plan", "Follow-up schedule"]

    # Compliance
    compliance_standard = models.CharField(max_length=200, blank=True)
    audit_requirements = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["workflow_name"]

    def __str__(self):
        return f"{self.workflow_number} - {self.workflow_name}"

    def save(self, *args, **kwargs):
        if not self.workflow_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.workflow_number = f"WF-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class InterventionStep(models.Model):
    """Track completion of workflow steps for each intervention"""

    intervention = models.ForeignKey(
        Intervention, on_delete=models.CASCADE, related_name="workflow_steps"
    )
    workflow = models.ForeignKey(
        InterventionWorkflow, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Step details
    step_number = models.IntegerField()
    step_name = models.CharField(max_length=200)
    step_description = models.TextField(blank=True)

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("skipped", "Skipped"),
            ("blocked", "Blocked"),
        ],
        default="pending",
    )

    # Completion details
    completed_by = models.CharField(max_length=200, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    completion_notes = models.TextField(blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)

    # Evidence
    evidence_provided = models.JSONField(default=list)
    attachments = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["intervention", "step_number"]
        unique_together = [["intervention", "step_number"]]

    def __str__(self):
        return f"{self.intervention.intervention_number} - Step {self.step_number}"


class InterventionOutcome(models.Model):
    """Detailed outcome tracking and analysis"""

    outcome_number = models.CharField(max_length=50, unique=True, db_index=True)
    intervention = models.ForeignKey(
        Intervention, on_delete=models.CASCADE, related_name="outcomes"
    )

    # Outcome metrics
    metric_type = models.CharField(
        max_length=50,
        choices=[
            ("attendance_improvement", "Attendance Improvement"),
            ("grade_improvement", "Grade Improvement"),
            ("engagement_increase", "Engagement Increase"),
            ("behaviour_change", "Behaviour Change"),
            ("completion_rate", "Completion Rate"),
            ("satisfaction", "Satisfaction"),
            ("custom", "Custom Metric"),
        ],
    )

    # Measurements
    baseline_value = models.FloatField(null=True, blank=True)
    target_value = models.FloatField(null=True, blank=True)
    actual_value = models.FloatField(null=True, blank=True)
    measurement_date = models.DateField(default=timezone.now)

    # Analysis
    improvement_percentage = models.FloatField(null=True, blank=True)
    target_achieved = models.BooleanField(null=True, blank=True)
    impact_rating = models.CharField(
        max_length=20,
        choices=[
            ("significant", "Significant Impact"),
            ("moderate", "Moderate Impact"),
            ("minimal", "Minimal Impact"),
            ("none", "No Impact"),
            ("negative", "Negative Impact"),
        ],
        blank=True,
    )

    # Documentation
    evidence_description = models.TextField(blank=True)
    evidence_links = models.JSONField(default=list)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-measurement_date"]

    def __str__(self):
        return f"{self.outcome_number} - {self.metric_type}"

    def save(self, *args, **kwargs):
        if not self.outcome_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.outcome_number = f"OUT-{timestamp}-{unique_id}"

        # Calculate improvement percentage
        if (
            self.baseline_value is not None
            and self.actual_value is not None
            and self.baseline_value != 0
        ):
            self.improvement_percentage = (
                (self.actual_value - self.baseline_value) / self.baseline_value
            ) * 100

        # Check if target achieved
        if self.target_value is not None and self.actual_value is not None:
            self.target_achieved = self.actual_value >= self.target_value

        super().save(*args, **kwargs)


class AuditLog(models.Model):
    """Comprehensive audit trail for compliance"""

    log_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)
    intervention = models.ForeignKey(
        Intervention, on_delete=models.CASCADE, related_name="audit_logs"
    )

    # Action details
    action_type = models.CharField(
        max_length=50,
        choices=[
            ("created", "Intervention Created"),
            ("updated", "Intervention Updated"),
            ("status_changed", "Status Changed"),
            ("step_completed", "Workflow Step Completed"),
            ("outcome_recorded", "Outcome Recorded"),
            ("document_attached", "Document Attached"),
            ("notification_sent", "Notification Sent"),
            ("escalated", "Escalated"),
            ("closed", "Closed"),
        ],
    )

    action_description = models.TextField()
    performed_by = models.CharField(max_length=200)
    performed_by_role = models.CharField(max_length=100, blank=True)

    # Changes tracked
    changes = models.JSONField(default=dict)  # Old value -> New value

    # Context
    ip_address = models.CharField(max_length=45, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["tenant", "intervention", "-timestamp"]),
            models.Index(fields=["action_type", "-timestamp"]),
        ]

    def __str__(self):
        return f"{self.log_number} - {self.action_type}"

    def save(self, *args, **kwargs):
        if not self.log_number:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.log_number = f"LOG-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)
