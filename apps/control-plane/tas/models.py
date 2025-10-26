from django.db import models
from django.contrib.auth.models import User
from tenants.models import Tenant
from django.utils import timezone
import hashlib
import json


class TASTemplate(models.Model):
    """
    Predefined TAS templates for different qualification types and AQF levels
    """
    AQF_LEVELS = [
        ('certificate_i', 'Certificate I'),
        ('certificate_ii', 'Certificate II'),
        ('certificate_iii', 'Certificate III'),
        ('certificate_iv', 'Certificate IV'),
        ('diploma', 'Diploma'),
        ('advanced_diploma', 'Advanced Diploma'),
        ('graduate_certificate', 'Graduate Certificate'),
        ('graduate_diploma', 'Graduate Diploma'),
        ('bachelor', 'Bachelor Degree'),
        ('masters', 'Masters Degree'),
    ]

    TEMPLATE_TYPES = [
        ('general', 'General Template'),
        ('trade', 'Trade/Technical'),
        ('business', 'Business/Commerce'),
        ('health', 'Health/Community Services'),
        ('creative', 'Creative Industries'),
        ('hospitality', 'Hospitality/Tourism'),
        ('technology', 'Information Technology'),
        ('education', 'Education/Training'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES, default='general')
    aqf_level = models.CharField(max_length=50, choices=AQF_LEVELS)
    
    # Template structure (JSON containing sections, prompts, and formatting)
    structure = models.JSONField(default=dict, help_text="Template structure with sections and GPT-4 prompts")
    
    # Default content and prompts
    default_sections = models.JSONField(default=list, help_text="List of default sections to include")
    gpt_prompts = models.JSONField(default=dict, help_text="GPT-4 prompts for each section")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    is_system_template = models.BooleanField(default=False, help_text="System templates cannot be deleted")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tas_templates_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tas_templates'
        ordering = ['aqf_level', 'name']
        verbose_name = 'TAS Template'
        verbose_name_plural = 'TAS Templates'

    def __str__(self):
        return f"{self.name} ({self.get_aqf_level_display()})"


class TAS(models.Model):
    """
    Training and Assessment Strategy documents with version control
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # Basic Information
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tas_documents')
    title = models.CharField(max_length=300)
    code = models.CharField(max_length=50, help_text="Qualification code (e.g., BSB50120)")
    description = models.TextField(blank=True)
    
    # Qualification Details
    qualification_name = models.CharField(max_length=300)
    aqf_level = models.CharField(max_length=50, choices=TASTemplate.AQF_LEVELS)
    training_package = models.CharField(max_length=100, blank=True)
    
    # Template and Structure
    template = models.ForeignKey(TASTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='tas_documents')
    sections = models.JSONField(default=list, help_text="Document sections with content")
    
    # Status and Workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    version = models.IntegerField(default=1)
    is_current_version = models.BooleanField(default=True)
    
    # GPT-4 Generation Metadata
    gpt_generated = models.BooleanField(default=False)
    gpt_generation_date = models.DateTimeField(null=True, blank=True)
    gpt_model_used = models.CharField(max_length=50, blank=True, help_text="GPT model version used")
    gpt_tokens_used = models.IntegerField(default=0)
    generation_time_seconds = models.FloatField(default=0.0, help_text="Time taken to generate")
    
    # Document Content
    content = models.JSONField(default=dict, help_text="Full document content including all sections")
    metadata = models.JSONField(default=dict, help_text="Additional metadata (units, assessments, etc.)")
    
    # Approval Workflow
    submitted_for_review_at = models.DateTimeField(null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tas_submitted')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tas_reviewed')
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tas_approved')
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tas_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tas_documents'
        ordering = ['-created_at']
        verbose_name = 'TAS Document'
        verbose_name_plural = 'TAS Documents'
        unique_together = [['tenant', 'code', 'version']]
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['tenant', 'code']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.code} - {self.title} (v{self.version})"

    def save(self, *args, **kwargs):
        # Auto-increment version if creating a new version of existing TAS
        if not self.pk and TAS.objects.filter(tenant=self.tenant, code=self.code).exists():
            latest = TAS.objects.filter(tenant=self.tenant, code=self.code).order_by('-version').first()
            self.version = latest.version + 1
        super().save(*args, **kwargs)

    def create_new_version(self, user):
        """Create a new version of this TAS document"""
        # Mark current versions as not current
        TAS.objects.filter(tenant=self.tenant, code=self.code, is_current_version=True).update(is_current_version=False)
        
        # Create new version
        new_version = TAS.objects.create(
            tenant=self.tenant,
            title=self.title,
            code=self.code,
            description=self.description,
            qualification_name=self.qualification_name,
            aqf_level=self.aqf_level,
            training_package=self.training_package,
            template=self.template,
            sections=self.sections,
            content=self.content,
            metadata=self.metadata,
            version=self.version + 1,
            is_current_version=True,
            created_by=user,
            status='draft',
        )
        return new_version

    def get_time_saved(self):
        """Calculate estimated time saved using GPT-4 (90% reduction)"""
        if self.gpt_generated and self.generation_time_seconds > 0:
            traditional_time = self.generation_time_seconds * 10  # If GPT saves 90%, traditional = 10x
            time_saved = traditional_time - self.generation_time_seconds
            return {
                'traditional_hours': round(traditional_time / 3600, 1),
                'gpt_hours': round(self.generation_time_seconds / 3600, 1),
                'saved_hours': round(time_saved / 3600, 1),
                'percentage_saved': 90,
            }
        return None


class TASVersion(models.Model):
    """
    Version history and change tracking for TAS documents
    """
    tas = models.ForeignKey(TAS, on_delete=models.CASCADE, related_name='version_history')
    version_number = models.IntegerField()
    
    # Change Information
    change_summary = models.TextField(help_text="Summary of changes in this version")
    changed_sections = models.JSONField(default=list, help_text="List of sections that were modified")
    
    # Diff/Comparison
    content_diff = models.JSONField(default=dict, help_text="Detailed diff of changes")
    previous_content = models.JSONField(default=dict, help_text="Snapshot of previous version content")
    new_content = models.JSONField(default=dict, help_text="Snapshot of new version content")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # GPT Regeneration tracking
    was_regenerated = models.BooleanField(default=False)
    regeneration_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'tas_versions'
        ordering = ['-version_number']
        verbose_name = 'TAS Version'
        verbose_name_plural = 'TAS Versions'
        unique_together = [['tas', 'version_number']]

    def __str__(self):
        return f"{self.tas.code} - Version {self.version_number}"


class TASGenerationLog(models.Model):
    """
    Log of GPT-4 generation attempts and results
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    tas = models.ForeignKey(TAS, on_delete=models.CASCADE, related_name='generation_logs')
    
    # Generation Request
    requested_sections = models.JSONField(default=list, help_text="Sections requested for generation")
    input_data = models.JSONField(default=dict, help_text="Input data provided to GPT-4")
    gpt_prompts = models.JSONField(default=dict, help_text="Prompts sent to GPT-4")
    
    # Generation Result
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    generated_content = models.JSONField(default=dict, help_text="Content generated by GPT-4")
    
    # Performance Metrics
    model_version = models.CharField(max_length=50, default='gpt-4')
    tokens_prompt = models.IntegerField(default=0)
    tokens_completion = models.IntegerField(default=0)
    tokens_total = models.IntegerField(default=0)
    generation_time_seconds = models.FloatField(default=0.0)
    
    # Error Handling
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tas_generation_logs'
        ordering = ['-created_at']
        verbose_name = 'TAS Generation Log'
        verbose_name_plural = 'TAS Generation Logs'

    def __str__(self):
        return f"{self.tas.code} - {self.status} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


# ============================================================================
# NEW MODELS - Course TAS & Unit TAS (High-Level Design Implementation)
# ============================================================================

class Trainer(models.Model):
    """
    Trainer/Assessor profile with qualifications, currency, and scope
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='trainers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer_profile')
    
    # Qualifications
    qualifications = models.JSONField(default=list, help_text="List of trainer qualifications")
    tae_qualification = models.CharField(max_length=100, blank=True, help_text="TAE40116 or equivalent")
    
    # Industry Currency
    industry_experience_years = models.IntegerField(default=0)
    currency_activities = models.JSONField(default=list, help_text="Recent industry currency activities")
    last_currency_date = models.DateField(null=True, blank=True)
    
    # Scope
    scope_units = models.JSONField(default=list, help_text="Unit codes the trainer is qualified to deliver")
    specializations = models.JSONField(default=list, help_text="Areas of specialization")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tas_trainers'
        unique_together = [['tenant', 'user']]
        verbose_name = 'Trainer'
        verbose_name_plural = 'Trainers'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.tenant.name}"


class Facility(models.Model):
    """
    Training facilities, equipment, and software inventory
    """
    FACILITY_TYPES = [
        ('classroom', 'Classroom'),
        ('workshop', 'Workshop'),
        ('lab', 'Laboratory'),
        ('online', 'Online Platform'),
        ('simulated', 'Simulated Environment'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='facilities')
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    location = models.CharField(max_length=300, blank=True)
    capacity = models.IntegerField(default=0)
    
    # Resources
    rooms = models.JSONField(default=list, help_text="List of rooms/spaces")
    equipment = models.JSONField(default=list, help_text="Equipment inventory")
    software = models.JSONField(default=list, help_text="Software licenses and tools")
    
    # Availability
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tas_facilities'
        ordering = ['name']
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"


class IndustryEngagement(models.Model):
    """
    Industry engagement activities and validation records
    """
    ENGAGEMENT_TYPES = [
        ('consultation', 'Industry Consultation'),
        ('validation', 'Curriculum Validation'),
        ('advisory', 'Advisory Committee'),
        ('partnership', 'Industry Partnership'),
        ('feedback', 'Employer Feedback'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='industry_engagements')
    engagement_type = models.CharField(max_length=50, choices=ENGAGEMENT_TYPES)
    
    # Engagement Details
    employer_name = models.CharField(max_length=300)
    contact_person = models.CharField(max_length=200, blank=True)
    engagement_date = models.DateField()
    
    # Outcomes
    notes = models.TextField(help_text="Summary of engagement and outcomes")
    outcomes = models.JSONField(default=list, help_text="Key outcomes and action items")
    recommendations = models.JSONField(default=list, help_text="Industry recommendations")
    
    # Links
    related_qualifications = models.JSONField(default=list, help_text="Related qualification codes")
    attachments = models.JSONField(default=list, help_text="Supporting documentation links")
    
    # Audit
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tas_industry_engagements'
        ordering = ['-engagement_date']
        verbose_name = 'Industry Engagement'
        verbose_name_plural = 'Industry Engagements'

    def __str__(self):
        return f"{self.employer_name} - {self.engagement_date}"


class CourseTAS(models.Model):
    """
    Course-level Training and Assessment Strategy
    Compliant with ASQA clauses 1.1-1.3, 1.8, 1.13-1.16, 2.2
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'In Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Core Identifiers
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='course_tas')
    qualification_code = models.CharField(max_length=50, help_text="e.g., BSB50120")
    qualification_name = models.CharField(max_length=300)
    aqf_level = models.CharField(max_length=50, choices=TASTemplate.AQF_LEVELS)
    training_package = models.CharField(max_length=100, blank=True)
    
    # TGA Snapshot
    tga_qualification_snapshot = models.JSONField(default=dict, help_text="TGA data snapshot at creation")
    tga_release_version = models.CharField(max_length=50, blank=True)
    
    # Course Structure
    core_units = models.JSONField(default=list, help_text="Core unit codes and titles")
    elective_units = models.JSONField(default=list, help_text="Selected elective unit codes and titles")
    total_units = models.IntegerField(default=0)
    
    # Delivery Model
    cohort_profile = models.TextField(help_text="Target cohort description and contextualization")
    delivery_model = models.CharField(max_length=100, help_text="Face-to-face, Online, Blended, etc.")
    total_hours = models.IntegerField(default=0, help_text="Total nominal hours")
    duration_weeks = models.IntegerField(default=52)
    
    # Clustering
    clusters = models.JSONField(default=list, help_text="Unit clusters with sequencing and hours")
    
    # Resources
    resources = models.JSONField(default=list, help_text="Facilities, equipment, materials required")
    facilities = models.ManyToManyField(Facility, blank=True, related_name='course_tas_assignments')
    
    # Assessment Overview
    assessment_overview = models.TextField(blank=True, help_text="High-level assessment strategy")
    
    # Validation & Industry
    validation_plan = models.JSONField(default=dict, help_text="Validation schedule and approach")
    industry_engagements = models.ManyToManyField(IndustryEngagement, blank=True, related_name='course_tas_links')
    
    # Compliance & Policy
    policy_links = models.JSONField(default=list, help_text="Links to RTO policies (RPL, Assessment, LLN, etc.)")
    compliance_notes = models.TextField(blank=True)
    
    # Workflow State
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    version = models.IntegerField(default=1)
    is_current_version = models.BooleanField(default=True)
    
    # Approval Workflow
    submitted_for_review_at = models.DateTimeField(null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_tas_submitted')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_tas_reviewed')
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='course_tas_approved')
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='course_tas_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tas_course_tas'
        ordering = ['-created_at']
        unique_together = [['tenant', 'qualification_code', 'version']]
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['tenant', 'qualification_code']),
        ]
        verbose_name = 'Course TAS'
        verbose_name_plural = 'Course TAS Documents'

    def __str__(self):
        return f"{self.qualification_code} - {self.qualification_name} (v{self.version})"


class UnitTAS(models.Model):
    """
    Unit-level Training and Assessment Strategy
    Linked to Course TAS
    """
    STATUS_CHOICES = CourseTAS.STATUS_CHOICES
    
    course_tas = models.ForeignKey(CourseTAS, on_delete=models.CASCADE, related_name='unit_tas_set')
    
    # Unit Details
    unit_code = models.CharField(max_length=50)
    unit_title = models.CharField(max_length=300)
    unit_type = models.CharField(max_length=20, choices=[('core', 'Core'), ('elective', 'Elective')])
    nominal_hours = models.IntegerField(default=0)
    
    # TGA Unit Snapshot
    tga_unit_snapshot = models.JSONField(default=dict, help_text="Elements, PC, KE, FS from TGA")
    
    # Delivery Sequence
    cluster_assignment = models.CharField(max_length=100, blank=True, help_text="Which cluster/term")
    delivery_sequence = models.JSONField(default=dict, help_text="Week-by-week delivery plan")
    prerequisites = models.JSONField(default=list, help_text="Required prior units")
    
    # Assessment Plan
    assessment_plan = models.JSONField(default=list, help_text="Assessment plan summary (deprecated - use assessment_tasks relation)")
    mapping_matrix = models.JSONField(default=dict, help_text="Elements/PC/KE/FS → tasks → instruments")
    
    # Resources
    resources = models.JSONField(default=list, help_text="Specific resources for this unit")
    facilities = models.ManyToManyField(Facility, blank=True, related_name='unit_tas_assignments')
    
    # Trainers
    trainers = models.ManyToManyField(Trainer, blank=True, related_name='unit_tas_assignments')
    
    # Contextualization
    cohort_context = models.TextField(blank=True, help_text="How this unit suits the cohort")
    industry_relevance = models.TextField(blank=True)
    
    # Workflow State
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    version = models.IntegerField(default=1)
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='unit_tas_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tas_unit_tas'
        ordering = ['cluster_assignment', 'unit_code']
        unique_together = [['course_tas', 'unit_code', 'version']]
        indexes = [
            models.Index(fields=['course_tas', 'status']),
            models.Index(fields=['unit_code']),
        ]
        verbose_name = 'Unit TAS'
        verbose_name_plural = 'Unit TAS Documents'

    def __str__(self):
        return f"{self.unit_code} - {self.unit_title}"


class ComplianceRule(models.Model):
    """
    Compliance rules for RAG (Red/Amber/Green) checking
    """
    RULE_TYPES = [
        ('packaging', 'Packaging Rules'),
        ('trainer_scope', 'Trainer Scope'),
        ('facility_adequacy', 'Facility Adequacy'),
        ('hours_validation', 'Hours Validation'),
        ('clustering', 'Clustering Sanity'),
        ('policy', 'Policy Compliance'),
    ]
    
    SEVERITY = [
        ('red', 'Red - Blocking'),
        ('amber', 'Amber - Warning'),
        ('green', 'Green - Advisory'),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='compliance_rules', null=True, blank=True)
    rule_type = models.CharField(max_length=50, choices=RULE_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Rule Logic
    rule_logic = models.JSONField(default=dict, help_text="Rule implementation as JSON (e.g., conditions, thresholds)")
    severity = models.CharField(max_length=20, choices=SEVERITY)
    
    # ASQA Clause Reference
    asqa_clause = models.CharField(max_length=50, blank=True, help_text="e.g., 1.1, 1.13, 2.2")
    
    # Status
    is_active = models.BooleanField(default=True)
    is_system_rule = models.BooleanField(default=False, help_text="System rules cannot be deleted")
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tas_compliance_rules'
        ordering = ['rule_type', 'name']
        verbose_name = 'Compliance Rule'
        verbose_name_plural = 'Compliance Rules'

    def __str__(self):
        return f"{self.name} ({self.severity})"


class ComplianceCheck(models.Model):
    """
    Compliance check results for Course TAS and Unit TAS
    """
    ENTITY_TYPES = [
        ('course', 'Course TAS'),
        ('unit', 'Unit TAS'),
    ]
    
    STATUS = [
        ('red', 'Red - Issue Found'),
        ('amber', 'Amber - Warning'),
        ('green', 'Green - Compliant'),
    ]
    
    # Polymorphic link
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES)
    entity_id = models.IntegerField(help_text="ID of CourseTAS or UnitTAS")
    
    # Rule Applied
    rule = models.ForeignKey(ComplianceRule, on_delete=models.CASCADE, related_name='checks')
    
    # Result
    status = models.CharField(max_length=20, choices=STATUS)
    message = models.TextField(help_text="Compliance check message")
    details = models.JSONField(default=dict, help_text="Detailed check results")
    
    # Resolution
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='compliance_resolutions')
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Audit
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tas_compliance_checks'
        ordering = ['-checked_at']
        indexes = [
            models.Index(fields=['entity_type', 'entity_id', 'status']),
        ]
        verbose_name = 'Compliance Check'
        verbose_name_plural = 'Compliance Checks'

    def __str__(self):
        return f"{self.rule.name} - {self.status}"


class AssessmentTask(models.Model):
    """
    Assessment tasks linked to Unit TAS
    """
    TASK_TYPES = [
        ('knowledge', 'Knowledge Assessment'),
        ('practical', 'Practical Demonstration'),
        ('project', 'Project'),
        ('portfolio', 'Portfolio'),
        ('observation', 'Workplace Observation'),
        ('case_study', 'Case Study'),
        ('simulation', 'Simulation'),
    ]
    
    unit_tas = models.ForeignKey(UnitTAS, on_delete=models.CASCADE, related_name='assessment_tasks')
    
    # Task Details
    task_number = models.IntegerField()
    task_name = models.CharField(max_length=300)
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    description = models.TextField()
    
    # Mapping
    elements_covered = models.JSONField(default=list, help_text="Element codes covered")
    performance_criteria_covered = models.JSONField(default=list, help_text="PC codes covered")
    knowledge_evidence_covered = models.JSONField(default=list, help_text="KE items covered")
    foundation_skills_covered = models.JSONField(default=list, help_text="FS items covered")
    
    # Instructions
    instructions = models.TextField(blank=True)
    resources_required = models.JSONField(default=list)
    time_allowed = models.CharField(max_length=100, blank=True)
    
    # Instruments
    instruments = models.JSONField(default=list, help_text="Assessment instruments/tools used")
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tas_assessment_tasks'
        ordering = ['unit_tas', 'task_number']
        unique_together = [['unit_tas', 'task_number']]
        verbose_name = 'Assessment Task'
        verbose_name_plural = 'Assessment Tasks'

    def __str__(self):
        return f"{self.unit_tas.unit_code} - Task {self.task_number}: {self.task_name}"


class ImmutableSnapshot(models.Model):
    """
    Immutable audit snapshot of approved Course TAS
    Sealed with checksum for compliance evidence
    """
    course_tas = models.ForeignKey(CourseTAS, on_delete=models.CASCADE, related_name='snapshots')
    
    # Snapshot Content
    snapshot_data = models.JSONField(help_text="Complete frozen state of CourseTAS and all UnitTAS")
    version = models.IntegerField()
    
    # Integrity
    checksum = models.CharField(max_length=64, help_text="SHA-256 hash of snapshot data")
    
    # Metadata
    snapshot_reason = models.CharField(max_length=100, help_text="e.g., 'Initial Approval', 'Version Update'")
    evidence_pack_links = models.JSONField(default=list, help_text="Links to supporting evidence")
    
    # Audit Trail
    sealed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sealed_at = models.DateTimeField(auto_now_add=True)
    
    # Auditor Access
    auditor_link_token = models.CharField(max_length=100, blank=True, help_text="Secure token for auditor access")
    auditor_link_expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tas_immutable_snapshots'
        ordering = ['-sealed_at']
        verbose_name = 'Immutable Snapshot'
        verbose_name_plural = 'Immutable Snapshots'

    def __str__(self):
        return f"{self.course_tas.qualification_code} v{self.version} - {self.sealed_at.strftime('%Y-%m-%d')}"
    
    def calculate_checksum(self):
        """Calculate SHA-256 checksum of snapshot data"""
        snapshot_json = json.dumps(self.snapshot_data, sort_keys=True)
        return hashlib.sha256(snapshot_json.encode()).hexdigest()
    
    def verify_integrity(self):
        """Verify snapshot has not been tampered with"""
        return self.checksum == self.calculate_checksum()
    
    def save(self, *args, **kwargs):
        """Auto-calculate checksum on save"""
        if not self.checksum and self.snapshot_data:
            self.checksum = self.calculate_checksum()
        super().save(*args, **kwargs)


class EvidencePack(models.Model):
    """
    Evidence pack for audit trail
    Links to industry engagement, validation, policies, etc.
    """
    course_tas = models.ForeignKey(CourseTAS, on_delete=models.CASCADE, related_name='evidence_packs')
    snapshot = models.OneToOneField(ImmutableSnapshot, on_delete=models.CASCADE, null=True, blank=True, related_name='evidence_pack')
    
    # Pack Contents
    industry_engagement_links = models.JSONField(default=list, help_text="Links to IndustryEngagement records")
    validation_evidence = models.JSONField(default=list, help_text="Validation meeting notes, reports")
    policy_documents = models.JSONField(default=list, help_text="Linked RTO policy documents")
    trainer_credentials = models.JSONField(default=list, help_text="Trainer qualifications and currency evidence")
    facility_documentation = models.JSONField(default=list, help_text="Facility and resource evidence")
    change_log = models.JSONField(default=list, help_text="History of changes and justifications")
    
    # Metadata
    compiled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    compiled_at = models.DateTimeField(auto_now_add=True)
    
    # Export
    export_file_path = models.CharField(max_length=500, blank=True, help_text="Path to exported evidence bundle")

    class Meta:
        db_table = 'tas_evidence_packs'
        ordering = ['-compiled_at']
        verbose_name = 'Evidence Pack'
        verbose_name_plural = 'Evidence Packs'

    def __str__(self):
        return f"Evidence Pack - {self.course_tas.qualification_code}"


class QualificationCache(models.Model):
    """
    Cached qualification and units data from training.gov.au
    Populated via management command and refreshed periodically
    """
    qualification_code = models.CharField(max_length=20, unique=True, db_index=True)
    qualification_title = models.CharField(max_length=500)
    training_package = models.CharField(max_length=20, blank=True)
    aqf_level = models.CharField(max_length=50, blank=True)
    
    # Packaging rules and structure
    packaging_rules = models.TextField(blank=True)
    has_groupings = models.BooleanField(default=False)
    
    # Units data (stored as JSON)
    groupings = models.JSONField(
        default=list,
        help_text="List of groupings with units: [{name, type, required, units: [{code, title, type}]}]"
    )
    
    # Metadata
    source = models.CharField(
        max_length=50, 
        default='training.gov.au',
        help_text="Data source (training.gov.au, manual, etc.)"
    )
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    release_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'tas_qualification_cache'
        ordering = ['qualification_code']
        verbose_name = 'Qualification Cache'
        verbose_name_plural = 'Qualification Cache'
        indexes = [
            models.Index(fields=['qualification_code', 'is_active']),
            models.Index(fields=['training_package']),
        ]
    
    def __str__(self):
        return f"{self.qualification_code} - {self.qualification_title}"
    
    def get_units_data(self):
        """Return the units data structure for API responses"""
        return {
            'qualification_code': self.qualification_code,
            'qualification_title': self.qualification_title,
            'packaging_rules': self.packaging_rules,
            'has_groupings': self.has_groupings,
            'groupings': self.groupings
        }
