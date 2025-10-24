from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from datetime import datetime


class FeedbackTemplate(models.Model):
    """
    Template for generating personalized feedback with sentiment control
    """
    
    SENTIMENT_CHOICES = [
        ('encouraging', 'Encouraging'),
        ('constructive', 'Constructive'),
        ('neutral', 'Neutral'),
        ('direct', 'Direct'),
        ('motivational', 'Motivational'),
    ]
    
    TONE_CHOICES = [
        ('formal', 'Formal'),
        ('conversational', 'Conversational'),
        ('supportive', 'Supportive'),
        ('professional', 'Professional'),
        ('friendly', 'Friendly'),
    ]
    
    FEEDBACK_TYPE_CHOICES = [
        ('formative', 'Formative'),
        ('summative', 'Summative'),
        ('diagnostic', 'Diagnostic'),
        ('peer', 'Peer Review'),
        ('self_assessment', 'Self-Assessment'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    # Identification
    template_number = models.CharField(max_length=50, unique=True, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Tenant and ownership
    tenant = models.CharField(max_length=100, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_templates')
    
    # Template configuration
    feedback_type = models.CharField(max_length=50, choices=FEEDBACK_TYPE_CHOICES, default='formative')
    sentiment = models.CharField(max_length=50, choices=SENTIMENT_CHOICES, default='constructive')
    tone = models.CharField(max_length=50, choices=TONE_CHOICES, default='professional')
    
    # Rubric mapping
    rubric = models.ForeignKey('rubric_generator.Rubric', on_delete=models.SET_NULL, null=True, blank=True)
    maps_to_criteria = models.JSONField(default=list, blank=True, help_text="List of rubric criterion IDs")
    
    # Personalization settings
    include_student_name = models.BooleanField(default=True)
    include_strengths = models.BooleanField(default=True)
    include_improvements = models.BooleanField(default=True)
    include_next_steps = models.BooleanField(default=True)
    include_encouragement = models.BooleanField(default=True)
    
    # Content structure
    opening_template = models.TextField(default="Dear {student_name},", help_text="Opening statement template")
    strengths_template = models.TextField(default="Your strengths include: {strengths}", blank=True)
    improvements_template = models.TextField(default="Areas for improvement: {improvements}", blank=True)
    next_steps_template = models.TextField(default="Next steps: {next_steps}", blank=True)
    closing_template = models.TextField(default="Keep up the great work!", blank=True)
    
    # Sentiment controls
    positivity_level = models.IntegerField(
        default=7,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="1=Very Critical, 10=Very Positive"
    )
    directness_level = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="1=Very Indirect, 10=Very Direct"
    )
    formality_level = models.IntegerField(
        default=7,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="1=Very Casual, 10=Very Formal"
    )
    
    # Performance tracking
    total_feedback_generated = models.IntegerField(default=0)
    average_generation_time = models.FloatField(default=0.0, help_text="Average time in seconds")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['feedback_type']),
            models.Index(fields=['created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.template_number:
            # Generate unique template number: FBT-YYYYMMDD-XXXXXX
            today = datetime.now().strftime('%Y%m%d')
            random_suffix = uuid.uuid4().hex[:6].upper()
            self.template_number = f"FBT-{today}-{random_suffix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.template_number} - {self.name}"
    
    def get_sentiment_description(self):
        """Get human-readable sentiment description"""
        descriptions = {
            1: "Very critical and direct",
            2: "Critical but fair",
            3: "Somewhat critical",
            4: "Balanced critical",
            5: "Neutral and balanced",
            6: "Somewhat positive",
            7: "Positive and encouraging",
            8: "Very encouraging",
            9: "Highly motivational",
            10: "Extremely positive"
        }
        return descriptions.get(self.positivity_level, "Balanced")


class GeneratedFeedback(models.Model):
    """
    Generated personalized feedback for students
    """
    
    STATUS_CHOICES = [
        ('generating', 'Generating'),
        ('generated', 'Generated'),
        ('reviewed', 'Reviewed'),
        ('delivered', 'Delivered'),
        ('revised', 'Revised'),
    ]
    
    # Identification
    feedback_number = models.CharField(max_length=50, unique=True, editable=False)
    template = models.ForeignKey(FeedbackTemplate, on_delete=models.CASCADE, related_name='generated_feedbacks')
    
    # Student information
    student_id = models.CharField(max_length=100, db_index=True)
    student_name = models.CharField(max_length=255)
    
    # Assessment context
    assessment_title = models.CharField(max_length=255, blank=True)
    score = models.FloatField(null=True, blank=True)
    max_score = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=10, blank=True)
    
    # Rubric mapping (if used)
    rubric_scores = models.JSONField(default=dict, blank=True, help_text="Scores per rubric criterion")
    
    # Generated content
    feedback_text = models.TextField()
    strengths_identified = models.JSONField(default=list, blank=True)
    improvements_identified = models.JSONField(default=list, blank=True)
    next_steps_suggested = models.JSONField(default=list, blank=True)
    
    # Sentiment analysis
    sentiment_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
        help_text="Sentiment: -1 (negative) to +1 (positive)"
    )
    tone_consistency = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="How well tone matches template settings"
    )
    
    # Personalization metrics
    word_count = models.IntegerField(default=0)
    reading_level = models.CharField(max_length=50, blank=True, help_text="e.g., Grade 10, University")
    personalization_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="How personalized the feedback is"
    )
    
    # Review and delivery
    requires_review = models.BooleanField(default=False, db_index=True)
    review_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_feedbacks')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivery_method = models.CharField(max_length=50, blank=True, help_text="email, LMS, portal, etc.")
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='generating', db_index=True)
    generation_time = models.FloatField(default=0.0, help_text="Time to generate in seconds")
    generated_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['template', 'status']),
            models.Index(fields=['student_id']),
            models.Index(fields=['requires_review']),
            models.Index(fields=['generated_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.feedback_number:
            # Generate unique feedback number: FDB-YYYYMMDD-XXXXXX
            today = datetime.now().strftime('%Y%m%d')
            random_suffix = uuid.uuid4().hex[:6].upper()
            self.feedback_number = f"FDB-{today}-{random_suffix}"
        
        # Calculate word count
        if self.feedback_text:
            self.word_count = len(self.feedback_text.split())
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.feedback_number} - {self.student_name}"
    
    def get_percentage_score(self):
        """Calculate percentage score"""
        if self.score is not None and self.max_score and self.max_score > 0:
            return (self.score / self.max_score) * 100
        return None


class FeedbackCriterion(models.Model):
    """
    Individual feedback criteria mapped to rubric criteria
    """
    template = models.ForeignKey(FeedbackTemplate, on_delete=models.CASCADE, related_name='criteria')
    
    # Criterion details
    criterion_name = models.CharField(max_length=255)
    description = models.TextField()
    
    # Rubric mapping
    rubric_criterion = models.ForeignKey(
        'rubric_generator.RubricCriterion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Feedback templates for different performance levels
    excellent_feedback = models.TextField(help_text="Feedback for excellent performance")
    good_feedback = models.TextField(help_text="Feedback for good performance")
    satisfactory_feedback = models.TextField(help_text="Feedback for satisfactory performance")
    needs_improvement_feedback = models.TextField(help_text="Feedback for needs improvement")
    
    # Weighting
    weight = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Importance of this criterion"
    )
    
    # Display
    display_order = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'created_at']
        verbose_name_plural = "Feedback Criteria"
    
    def __str__(self):
        return f"{self.criterion_name} ({self.weight * 100}%)"
    
    def get_feedback_for_score(self, score_percentage):
        """Get appropriate feedback based on score"""
        if score_percentage >= 85:
            return self.excellent_feedback
        elif score_percentage >= 70:
            return self.good_feedback
        elif score_percentage >= 50:
            return self.satisfactory_feedback
        else:
            return self.needs_improvement_feedback


class FeedbackLog(models.Model):
    """
    Audit log for feedback generation and delivery
    """
    
    ACTION_CHOICES = [
        ('generate_single', 'Generate Single'),
        ('generate_batch', 'Generate Batch'),
        ('review', 'Review Feedback'),
        ('revise', 'Revise Feedback'),
        ('deliver', 'Deliver Feedback'),
        ('template_update', 'Update Template'),
    ]
    
    # Reference
    template = models.ForeignKey(FeedbackTemplate, on_delete=models.CASCADE, related_name='logs')
    feedback = models.ForeignKey(GeneratedFeedback, on_delete=models.CASCADE, null=True, blank=True, related_name='logs')
    
    # Action details
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, db_index=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Generation metrics
    feedbacks_generated = models.IntegerField(default=1)
    total_time = models.FloatField(help_text="Total processing time in seconds")
    average_time_per_feedback = models.FloatField(default=0.0)
    
    # Sentiment metrics
    average_sentiment = models.FloatField(null=True, blank=True)
    average_personalization = models.FloatField(null=True, blank=True)
    
    # Changes (for revisions)
    changes_made = models.TextField(blank=True)
    previous_version = models.TextField(blank=True)
    
    # Additional details
    details = models.JSONField(default=dict, blank=True)
    
    # Metadata
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['template', 'action']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.template.template_number} at {self.timestamp}"
    
    def save(self, *args, **kwargs):
        if self.feedbacks_generated > 0:
            self.average_time_per_feedback = self.total_time / self.feedbacks_generated
        super().save(*args, **kwargs)
