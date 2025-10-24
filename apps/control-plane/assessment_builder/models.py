from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import json


class Assessment(models.Model):
    """
    Main assessment document generated from unit codes.
    Contains tasks, instructions, and compliance mappings.
    """
    ASSESSMENT_TYPE_CHOICES = [
        ('knowledge', 'Knowledge Assessment'),
        ('practical', 'Practical Assessment'),
        ('project', 'Project Assessment'),
        ('portfolio', 'Portfolio Assessment'),
        ('observation', 'Observation Checklist'),
        ('case_study', 'Case Study'),
        ('simulation', 'Simulation/Role Play'),
        ('integrated', 'Integrated Assessment'),
        ('written', 'Written Assessment'),
        ('oral', 'Oral Assessment'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generating', 'Generating with AI'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name='assessments')
    assessment_number = models.CharField(max_length=50, unique=True, editable=False)
    
    # Unit information
    unit_code = models.CharField(max_length=50, help_text="Training package unit code (e.g., BSBWHS211)")
    unit_title = models.CharField(max_length=300)
    training_package = models.CharField(max_length=100, blank=True, help_text="e.g., BSB - Business Services")
    unit_release = models.CharField(max_length=20, blank=True, help_text="Release number")
    
    # Assessment details
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES)
    title = models.CharField(max_length=300)
    version = models.CharField(max_length=20, default='1.0')
    
    # Generated content
    instructions = models.TextField(
        blank=True,
        help_text="AI-generated assessment instructions"
    )
    context = models.TextField(
        blank=True,
        help_text="Assessment context and scenario"
    )
    conditions = models.TextField(
        blank=True,
        help_text="Assessment conditions (equipment, resources, etc.)"
    )
    
    # AI generation metadata
    ai_generated = models.BooleanField(default=False)
    ai_model = models.CharField(max_length=50, blank=True, help_text="e.g., GPT-4")
    ai_prompt = models.TextField(blank=True, help_text="Prompt used for generation")
    ai_generation_time = models.FloatField(null=True, blank=True, help_text="Generation time in seconds")
    ai_generated_at = models.DateTimeField(null=True, blank=True)
    
    # Bloom's Taxonomy analysis
    blooms_analysis = models.JSONField(
        default=dict,
        blank=True,
        help_text="Bloom's taxonomy verb analysis: {level: count}"
    )
    blooms_distribution = models.JSONField(
        default=dict,
        blank=True,
        help_text="Distribution percentages across Bloom's levels"
    )
    dominant_blooms_level = models.CharField(
        max_length=20,
        blank=True,
        help_text="Most prominent Bloom's level"
    )
    
    # Compliance
    is_compliant = models.BooleanField(default=False)
    compliance_score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Overall compliance score (0-100)"
    )
    compliance_notes = models.TextField(blank=True)
    
    # Mapping to unit requirements
    elements_covered = models.JSONField(
        default=list,
        blank=True,
        help_text="List of unit elements covered"
    )
    performance_criteria_covered = models.JSONField(
        default=list,
        blank=True,
        help_text="List of performance criteria covered"
    )
    knowledge_evidence_covered = models.JSONField(
        default=list,
        blank=True,
        help_text="List of knowledge evidence items covered"
    )
    performance_evidence_covered = models.JSONField(
        default=list,
        blank=True,
        help_text="List of performance evidence items covered"
    )
    
    # Assessment duration
    estimated_duration_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Estimated completion time in hours"
    )
    
    # Status and workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Review and approval
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_assessments'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_assessments'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_assessments')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['unit_code']),
            models.Index(fields=['assessment_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.assessment_number} - {self.unit_code} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.assessment_number:
            # Generate unique assessment number
            from django.utils.crypto import get_random_string
            today = timezone.now()
            self.assessment_number = f"ASM-{today.strftime('%Y%m%d')}-{get_random_string(6, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
        super().save(*args, **kwargs)
    
    def get_task_count(self):
        """Get total number of tasks"""
        return self.tasks.count()
    
    def get_total_questions(self):
        """Get total number of questions across all tasks"""
        return sum(task.question_count for task in self.tasks.all())
    
    def calculate_blooms_distribution(self):
        """Calculate Bloom's taxonomy distribution across all tasks"""
        from collections import Counter
        
        all_verbs = []
        for task in self.tasks.all():
            all_verbs.extend(task.blooms_verbs or [])
        
        if not all_verbs:
            return {}
        
        # Count by Bloom's level
        level_counts = Counter()
        blooms_levels = {
            'remember': ['list', 'define', 'tell', 'describe', 'identify', 'show', 'label', 'collect', 'examine', 'tabulate', 'quote', 'name', 'who', 'when', 'where'],
            'understand': ['summarize', 'describe', 'interpret', 'contrast', 'predict', 'associate', 'distinguish', 'estimate', 'differentiate', 'discuss', 'extend', 'explain'],
            'apply': ['apply', 'demonstrate', 'calculate', 'complete', 'illustrate', 'show', 'solve', 'examine', 'modify', 'relate', 'change', 'classify', 'experiment', 'discover'],
            'analyze': ['analyze', 'separate', 'order', 'explain', 'connect', 'classify', 'arrange', 'divide', 'compare', 'select', 'explain', 'infer'],
            'evaluate': ['assess', 'decide', 'rank', 'grade', 'test', 'measure', 'recommend', 'convince', 'select', 'judge', 'explain', 'discriminate', 'support', 'conclude', 'compare', 'summarize'],
            'create': ['design', 'formulate', 'build', 'invent', 'create', 'compose', 'generate', 'derive', 'modify', 'develop', 'construct', 'produce', 'plan', 'devise'],
        }
        
        for verb in all_verbs:
            verb_lower = verb.lower()
            for level, level_verbs in blooms_levels.items():
                if verb_lower in level_verbs:
                    level_counts[level] += 1
                    break
        
        total = sum(level_counts.values())
        if total == 0:
            return {}
        
        distribution = {
            level: round((count / total) * 100, 1)
            for level, count in level_counts.items()
        }
        
        return distribution


class AssessmentTask(models.Model):
    """
    Individual task within an assessment.
    Can be a question, activity, or practical demonstration.
    """
    TASK_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('short_answer', 'Short Answer'),
        ('long_answer', 'Long Answer/Essay'),
        ('case_study', 'Case Study'),
        ('practical', 'Practical Demonstration'),
        ('project', 'Project Task'),
        ('portfolio', 'Portfolio Item'),
        ('observation', 'Observation'),
        ('presentation', 'Presentation'),
        ('role_play', 'Role Play/Simulation'),
    ]
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='tasks')
    task_number = models.CharField(max_length=20, help_text="e.g., '1', '1a', 'A.1'")
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    
    # Task content
    question = models.TextField(help_text="The task question or instruction")
    context = models.TextField(
        blank=True,
        help_text="Additional context, scenario, or information for the task"
    )
    
    # AI generation
    ai_generated = models.BooleanField(default=False)
    ai_rationale = models.TextField(
        blank=True,
        help_text="AI explanation of why this task was generated"
    )
    
    # Bloom's Taxonomy
    blooms_level = models.CharField(
        max_length=20,
        blank=True,
        help_text="Primary Bloom's taxonomy level"
    )
    blooms_verbs = models.JSONField(
        default=list,
        blank=True,
        help_text="Bloom's taxonomy verbs detected in this task"
    )
    
    # Mapping to unit
    maps_to_elements = models.JSONField(
        default=list,
        blank=True,
        help_text="Unit elements this task addresses"
    )
    maps_to_performance_criteria = models.JSONField(
        default=list,
        blank=True,
        help_text="Performance criteria this task addresses"
    )
    maps_to_knowledge_evidence = models.JSONField(
        default=list,
        blank=True,
        help_text="Knowledge evidence this task addresses"
    )
    
    # Task metadata
    question_count = models.IntegerField(
        default=1,
        help_text="Number of sub-questions (for multi-part tasks)"
    )
    estimated_time_minutes = models.IntegerField(
        null=True,
        blank=True,
        help_text="Estimated completion time in minutes"
    )
    
    # Marking
    marks_available = models.IntegerField(
        null=True,
        blank=True,
        help_text="Total marks for this task"
    )
    
    # Order
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['assessment', 'display_order', 'task_number']
        indexes = [
            models.Index(fields=['assessment', 'display_order']),
        ]
    
    def __str__(self):
        return f"Task {self.task_number} - {self.task_type}"


class AssessmentCriteria(models.Model):
    """
    Marking criteria and benchmarks for assessment tasks.
    Links to unit performance criteria and knowledge evidence.
    """
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='criteria')
    task = models.ForeignKey(
        AssessmentTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='criteria',
        help_text="Optional: Link to specific task"
    )
    
    # Criteria details
    criterion_number = models.CharField(max_length=20)
    criterion_text = models.TextField(help_text="What the student must demonstrate")
    
    # Mapping to unit
    unit_element = models.CharField(max_length=100, blank=True)
    performance_criterion = models.CharField(max_length=100, blank=True)
    knowledge_evidence = models.CharField(max_length=100, blank=True)
    
    # Assessment guidance
    satisfactory_evidence = models.TextField(
        blank=True,
        help_text="What constitutes satisfactory performance"
    )
    not_satisfactory_evidence = models.TextField(
        blank=True,
        help_text="What would be unsatisfactory"
    )
    
    # AI generated
    ai_generated = models.BooleanField(default=False)
    
    # Order
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['assessment', 'display_order', 'criterion_number']
        verbose_name_plural = 'Assessment Criteria'
    
    def __str__(self):
        return f"Criterion {self.criterion_number}"


class AssessmentGenerationLog(models.Model):
    """
    Audit log for AI generation activities.
    """
    ACTION_CHOICES = [
        ('generate_full', 'Full Assessment Generated'),
        ('generate_task', 'Task Generated'),
        ('generate_criteria', 'Criteria Generated'),
        ('analyze_blooms', 'Bloom\'s Analysis Performed'),
        ('regenerate', 'Content Regenerated'),
    ]
    
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='generation_logs')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    
    # Generation details
    ai_model = models.CharField(max_length=50)
    prompt_used = models.TextField()
    response_text = models.TextField(blank=True)
    tokens_used = models.IntegerField(null=True, blank=True)
    generation_time = models.FloatField(help_text="Time in seconds")
    
    # Results
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    performed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-performed_at']
        indexes = [
            models.Index(fields=['assessment', 'performed_at']),
        ]
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.assessment.assessment_number}"
