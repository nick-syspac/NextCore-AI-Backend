from django.db import models
from django.utils import timezone
import uuid


class PDActivity(models.Model):
    """Professional Development activity records"""
    activity_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)
    
    # Trainer information
    trainer_id = models.CharField(max_length=100, db_index=True)
    trainer_name = models.CharField(max_length=200)
    trainer_role = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=200, blank=True)
    
    # Activity details
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('formal_course', 'Formal Course/Training'),
            ('workshop', 'Workshop/Seminar'),
            ('conference', 'Conference/Symposium'),
            ('webinar', 'Webinar/Online Session'),
            ('industry_placement', 'Industry Placement'),
            ('networking', 'Professional Networking'),
            ('research', 'Research/Publication'),
            ('mentoring', 'Mentoring/Coaching'),
            ('self_study', 'Self-Directed Study'),
            ('certification', 'Certification/Qualification'),
            ('teaching_observation', 'Teaching Observation'),
            ('curriculum_development', 'Curriculum Development')
        ]
    )
    
    activity_title = models.CharField(max_length=300)
    description = models.TextField()
    provider = models.CharField(max_length=200, blank=True)  # Training provider/organization
    
    # Dates and duration
    start_date = models.DateField()
    end_date = models.DateField()
    hours_completed = models.FloatField(default=0.0)
    
    # Compliance and currency
    compliance_areas = models.JSONField(default=list)
    # Example: ['Vocational Competency', 'Industry Currency', 'Teaching Skills']
    
    industry_sectors = models.JSONField(default=list)
    # Example: ['Information Technology', 'Business Services']
    
    qualification_levels = models.JSONField(default=list)
    # Example: ['Certificate IV', 'Diploma', 'Advanced Diploma']
    
    # Evidence and verification
    evidence_type = models.CharField(
        max_length=50,
        choices=[
            ('certificate', 'Certificate/Statement of Attainment'),
            ('attendance_record', 'Attendance Record'),
            ('transcript', 'Academic Transcript'),
            ('letter', 'Letter of Completion'),
            ('portfolio', 'Portfolio/Work Samples'),
            ('statutory_declaration', 'Statutory Declaration'),
            ('other', 'Other Documentation')
        ],
        blank=True
    )
    evidence_files = models.JSONField(default=list)  # File paths/URLs
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Verification'),
            ('verified', 'Verified'),
            ('rejected', 'Rejected'),
            ('expired', 'Expired')
        ],
        default='pending'
    )
    verified_by = models.CharField(max_length=200, blank=True)
    verified_date = models.DateField(null=True, blank=True)
    
    # Outcomes and reflection
    learning_outcomes = models.TextField(blank=True)
    application_to_practice = models.TextField(blank=True)
    reflection_notes = models.TextField(blank=True)
    
    # Impact on currency
    maintains_vocational_currency = models.BooleanField(default=False)
    maintains_industry_currency = models.BooleanField(default=False)
    maintains_teaching_currency = models.BooleanField(default=False)
    
    # Regulatory compliance
    meets_asqa_requirements = models.BooleanField(default=False)
    compliance_notes = models.TextField(blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('planned', 'Planned'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='planned'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['tenant', 'trainer_id', '-start_date']),
            models.Index(fields=['status', 'verification_status']),
            models.Index(fields=['activity_type', '-start_date']),
        ]
    
    def __str__(self):
        return f"{self.activity_number} - {self.activity_title}"
    
    def save(self, *args, **kwargs):
        if not self.activity_number:
            timestamp = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8].upper()
            self.activity_number = f"PD-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class TrainerProfile(models.Model):
    """Trainer professional development profile and currency tracking"""
    profile_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)
    
    # Trainer details
    trainer_id = models.CharField(max_length=100, unique=True, db_index=True)
    trainer_name = models.CharField(max_length=200)
    email = models.EmailField()
    role = models.CharField(max_length=100)
    department = models.CharField(max_length=200, blank=True)
    employment_start_date = models.DateField(null=True, blank=True)
    
    # Qualifications
    highest_qualification = models.CharField(max_length=200, blank=True)
    teaching_qualifications = models.JSONField(default=list)
    industry_qualifications = models.JSONField(default=list)
    
    # Teaching areas
    teaching_subjects = models.JSONField(default=list)
    teaching_qualification_levels = models.JSONField(default=list)
    industry_sectors = models.JSONField(default=list)
    
    # Currency requirements
    vocational_currency_required = models.BooleanField(default=True)
    industry_currency_required = models.BooleanField(default=True)
    teaching_currency_required = models.BooleanField(default=True)
    
    # Currency tracking
    total_pd_hours = models.FloatField(default=0.0)
    vocational_pd_hours = models.FloatField(default=0.0)
    industry_pd_hours = models.FloatField(default=0.0)
    teaching_pd_hours = models.FloatField(default=0.0)
    
    # Last PD dates
    last_vocational_pd = models.DateField(null=True, blank=True)
    last_industry_pd = models.DateField(null=True, blank=True)
    last_teaching_pd = models.DateField(null=True, blank=True)
    
    # Currency status
    vocational_currency_status = models.CharField(
        max_length=20,
        choices=[
            ('current', 'Current'),
            ('expiring_soon', 'Expiring Soon'),
            ('expired', 'Expired'),
            ('not_applicable', 'Not Applicable')
        ],
        default='current'
    )
    industry_currency_status = models.CharField(
        max_length=20,
        choices=[
            ('current', 'Current'),
            ('expiring_soon', 'Expiring Soon'),
            ('expired', 'Expired'),
            ('not_applicable', 'Not Applicable')
        ],
        default='current'
    )
    
    # Compliance
    meets_asqa_requirements = models.BooleanField(default=True)
    last_compliance_check = models.DateField(null=True, blank=True)
    compliance_issues = models.JSONField(default=list)
    
    # Goals and planning
    annual_pd_goal_hours = models.FloatField(default=20.0)
    current_year_hours = models.FloatField(default=0.0)
    pd_goals = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['trainer_name']
    
    def __str__(self):
        return f"{self.profile_number} - {self.trainer_name}"
    
    def save(self, *args, **kwargs):
        if not self.profile_number:
            timestamp = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:6].upper()
            self.profile_number = f"PROF-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class PDSuggestion(models.Model):
    """LLM-generated PD suggestions based on trainer profile and compliance"""
    suggestion_number = models.CharField(max_length=50, unique=True, db_index=True)
    trainer_profile = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='pd_suggestions')
    
    # Suggestion details
    suggested_activity_type = models.CharField(max_length=50)
    activity_title = models.CharField(max_length=300)
    description = models.TextField()
    rationale = models.TextField()  # Why this PD is suggested
    
    # Recommendation context
    addresses_currency_gap = models.CharField(
        max_length=50,
        choices=[
            ('vocational', 'Vocational Currency'),
            ('industry', 'Industry Currency'),
            ('teaching', 'Teaching Currency'),
            ('compliance', 'Compliance Requirement'),
            ('skill_development', 'Skill Development'),
            ('career_progression', 'Career Progression')
        ]
    )
    
    priority_level = models.CharField(
        max_length=20,
        choices=[
            ('critical', 'Critical - Compliance Risk'),
            ('high', 'High Priority'),
            ('medium', 'Medium Priority'),
            ('low', 'Low Priority')
        ],
        default='medium'
    )
    
    # Suggested providers/resources
    suggested_providers = models.JSONField(default=list)
    estimated_hours = models.FloatField(null=True, blank=True)
    estimated_cost = models.FloatField(null=True, blank=True)
    
    # Timeline
    suggested_timeframe = models.CharField(max_length=100, blank=True)
    deadline = models.DateField(null=True, blank=True)
    
    # LLM generation metadata
    generated_by_model = models.CharField(max_length=100, blank=True)
    generation_date = models.DateTimeField(auto_now_add=True)
    prompt_used = models.TextField(blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    
    # Action tracking
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending_review', 'Pending Review'),
            ('accepted', 'Accepted'),
            ('planned', 'Planned'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('dismissed', 'Dismissed')
        ],
        default='pending_review'
    )
    
    trainer_feedback = models.TextField(blank=True)
    linked_activity = models.ForeignKey(PDActivity, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority_level', '-generation_date']
    
    def __str__(self):
        return f"{self.suggestion_number} - {self.activity_title}"
    
    def save(self, *args, **kwargs):
        if not self.suggestion_number:
            timestamp = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:6].upper()
            self.suggestion_number = f"SUG-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class ComplianceRule(models.Model):
    """Compliance rules for PD requirements (ASQA, RTO-specific)"""
    rule_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)
    
    # Rule metadata
    rule_name = models.CharField(max_length=200)
    description = models.TextField()
    regulatory_source = models.CharField(
        max_length=50,
        choices=[
            ('asqa', 'ASQA Standards'),
            ('vet_quality', 'VET Quality Framework'),
            ('state_regulation', 'State Regulation'),
            ('rto_policy', 'RTO Policy'),
            ('industry_requirement', 'Industry Requirement')
        ]
    )
    reference_code = models.CharField(max_length=100, blank=True)  # e.g., "Standard 1.14"
    
    # Applicability
    applies_to_roles = models.JSONField(default=list)
    applies_to_sectors = models.JSONField(default=list)
    applies_to_qualifications = models.JSONField(default=list)
    
    # Requirements
    requirement_type = models.CharField(
        max_length=50,
        choices=[
            ('minimum_hours', 'Minimum Hours Required'),
            ('activity_type', 'Specific Activity Type'),
            ('frequency', 'Frequency Requirement'),
            ('industry_engagement', 'Industry Engagement'),
            ('qualification_maintenance', 'Qualification Maintenance')
        ]
    )
    
    requirement_details = models.JSONField(default=dict)
    # Example: {
    #   "minimum_hours": 20,
    #   "period": "annual",
    #   "activity_types": ["industry_placement", "formal_course"]
    # }
    
    # Validation
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['regulatory_source', 'rule_name']
    
    def __str__(self):
        return f"{self.rule_number} - {self.rule_name}"
    
    def save(self, *args, **kwargs):
        if not self.rule_number:
            timestamp = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:6].upper()
            self.rule_number = f"RULE-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class ComplianceCheck(models.Model):
    """Record of compliance checks against PD requirements"""
    check_number = models.CharField(max_length=50, unique=True, db_index=True)
    trainer_profile = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='compliance_checks')
    
    # Check details
    check_date = models.DateField(default=timezone.now)
    check_period_start = models.DateField()
    check_period_end = models.DateField()
    checked_by = models.CharField(max_length=200, blank=True)
    
    # Results
    overall_status = models.CharField(
        max_length=20,
        choices=[
            ('compliant', 'Fully Compliant'),
            ('at_risk', 'At Risk'),
            ('non_compliant', 'Non-Compliant')
        ]
    )
    
    rules_checked = models.JSONField(default=list)  # List of rule IDs checked
    rules_met = models.JSONField(default=list)
    rules_not_met = models.JSONField(default=list)
    
    # Findings
    compliance_score = models.FloatField(default=0.0)  # 0-100
    hours_required = models.FloatField(default=0.0)
    hours_completed = models.FloatField(default=0.0)
    hours_shortfall = models.FloatField(default=0.0)
    
    findings = models.JSONField(default=list)
    # Example: [
    #   {"rule": "RULE-123", "status": "not_met", "issue": "Only 10 hours completed, 20 required"}
    # ]
    
    recommendations = models.JSONField(default=list)
    
    # Follow-up
    requires_action = models.BooleanField(default=False)
    action_deadline = models.DateField(null=True, blank=True)
    actions_taken = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-check_date']
    
    def __str__(self):
        return f"{self.check_number} - {self.trainer_profile.trainer_name}"
    
    def save(self, *args, **kwargs):
        if not self.check_number:
            timestamp = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:6].upper()
            self.check_number = f"CHK-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)
