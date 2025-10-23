from django.db import models
from django.contrib.auth.models import User
from tenants.models import Tenant
from django.utils import timezone


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
