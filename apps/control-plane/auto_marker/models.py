from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from datetime import datetime


class AutoMarker(models.Model):
    """
    Auto-Marker configuration for automated grading with semantic similarity
    """
    
    ANSWER_TYPE_CHOICES = [
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
        ('paragraph', 'Paragraph'),
        ('definition', 'Definition'),
        ('explanation', 'Explanation'),
    ]
    
    SIMILARITY_MODEL_CHOICES = [
        ('sentence_transformers', 'Sentence Transformers'),
        ('word2vec', 'Word2Vec'),
        ('bert', 'BERT'),
        ('openai_embeddings', 'OpenAI Embeddings'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    # Identification
    marker_number = models.CharField(max_length=50, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Tenant and ownership
    tenant = models.CharField(max_length=100, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_markers')
    
    # Configuration
    answer_type = models.CharField(max_length=50, choices=ANSWER_TYPE_CHOICES, default='short_answer')
    question_text = models.TextField(help_text="The question being asked")
    model_answer = models.TextField(help_text="The ideal/model answer for comparison")
    max_marks = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    # Semantic similarity settings
    similarity_model = models.CharField(max_length=50, choices=SIMILARITY_MODEL_CHOICES, default='sentence_transformers')
    similarity_threshold = models.FloatField(
        default=0.70,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Minimum similarity score for full marks (0.0-1.0)"
    )
    partial_credit_enabled = models.BooleanField(default=True)
    min_similarity_for_credit = models.FloatField(
        default=0.40,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Minimum similarity for partial credit"
    )
    
    # Marking criteria
    use_keywords = models.BooleanField(default=True, help_text="Enable keyword matching")
    keywords = models.JSONField(default=list, blank=True, help_text="Required keywords for full marks")
    keyword_weight = models.FloatField(
        default=0.20,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Weight of keyword matching in final score"
    )
    
    # Performance tracking
    total_responses_marked = models.IntegerField(default=0)
    average_similarity_score = models.FloatField(default=0.0)
    average_marking_time = models.FloatField(default=0.0, help_text="Average time in seconds")
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['answer_type']),
            models.Index(fields=['created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.marker_number:
            # Generate unique marker number: AMK-YYYYMMDD-XXXXXX
            today = datetime.now().strftime('%Y%m%d')
            random_suffix = uuid.uuid4().hex[:6].upper()
            self.marker_number = f"AMK-{today}-{random_suffix}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.marker_number} - {self.title}"
    
    def calculate_average_score(self):
        """Calculate average similarity score from all responses"""
        responses = self.responses.filter(status='marked')
        if responses.exists():
            total = sum(r.similarity_score for r in responses)
            self.average_similarity_score = total / responses.count()
            self.save()
        return self.average_similarity_score
    
    def get_marking_statistics(self):
        """Get comprehensive marking statistics"""
        responses = self.responses.filter(status='marked')
        total = responses.count()
        
        if total == 0:
            return {
                'total_marked': 0,
                'avg_similarity': 0.0,
                'avg_marks': 0.0,
                'high_confidence': 0,
                'needs_review': 0,
            }
        
        return {
            'total_marked': total,
            'avg_similarity': sum(r.similarity_score for r in responses) / total,
            'avg_marks': sum(r.marks_awarded for r in responses) / total,
            'high_confidence': responses.filter(confidence_score__gte=0.85).count(),
            'needs_review': responses.filter(requires_review=True).count(),
            'pass_rate': responses.filter(marks_awarded__gte=self.max_marks * 0.5).count() / total * 100,
        }


class MarkedResponse(models.Model):
    """
    Student responses marked by the auto-marker with semantic similarity scores
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('marking', 'Marking'),
        ('marked', 'Marked'),
        ('reviewed', 'Reviewed'),
        ('disputed', 'Disputed'),
    ]
    
    # Identification
    response_number = models.CharField(max_length=50, unique=True, editable=False)
    auto_marker = models.ForeignKey(AutoMarker, on_delete=models.CASCADE, related_name='responses')
    
    # Student information
    student_id = models.CharField(max_length=100, db_index=True)
    student_name = models.CharField(max_length=255)
    
    # Response content
    response_text = models.TextField()
    word_count = models.IntegerField(default=0)
    
    # Semantic similarity scores
    similarity_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Semantic similarity to model answer (0.0-1.0)"
    )
    keyword_match_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Keyword matching score (0.0-1.0)"
    )
    combined_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Weighted combination of similarity and keyword scores"
    )
    
    # Marking results
    marks_awarded = models.FloatField(default=0.0)
    confidence_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Confidence in the automated marking"
    )
    
    # Analysis details
    matched_keywords = models.JSONField(default=list, blank=True)
    missing_keywords = models.JSONField(default=list, blank=True)
    key_phrases_detected = models.JSONField(default=list, blank=True)
    similarity_breakdown = models.JSONField(default=dict, blank=True, help_text="Detailed similarity analysis")
    
    # Review and feedback
    requires_review = models.BooleanField(default=False, db_index=True)
    review_reason = models.CharField(max_length=255, blank=True)
    automated_feedback = models.TextField(blank=True)
    reviewer_notes = models.TextField(blank=True)
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    marking_time = models.FloatField(default=0.0, help_text="Time taken to mark in seconds")
    marked_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_responses')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['auto_marker', 'status']),
            models.Index(fields=['student_id']),
            models.Index(fields=['requires_review']),
            models.Index(fields=['marked_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.response_number:
            # Generate unique response number: RSP-YYYYMMDD-XXXXXX
            today = datetime.now().strftime('%Y%m%d')
            random_suffix = uuid.uuid4().hex[:6].upper()
            self.response_number = f"RSP-{today}-{random_suffix}"
        
        # Calculate word count
        if self.response_text:
            self.word_count = len(self.response_text.split())
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.response_number} - {self.student_name}"
    
    def calculate_marks(self):
        """Calculate marks based on similarity and keyword scores"""
        marker = self.auto_marker
        
        # Combine similarity and keyword scores
        if marker.use_keywords and marker.keywords:
            self.combined_score = (
                self.similarity_score * (1 - marker.keyword_weight) +
                self.keyword_match_score * marker.keyword_weight
            )
        else:
            self.combined_score = self.similarity_score
        
        # Award marks based on combined score
        if self.combined_score >= marker.similarity_threshold:
            # Full marks
            self.marks_awarded = marker.max_marks
            self.confidence_score = self.combined_score
        elif marker.partial_credit_enabled and self.combined_score >= marker.min_similarity_for_credit:
            # Partial marks - linear scaling
            score_range = marker.similarity_threshold - marker.min_similarity_for_credit
            normalized_score = (self.combined_score - marker.min_similarity_for_credit) / score_range
            self.marks_awarded = marker.max_marks * normalized_score
            self.confidence_score = self.combined_score * 0.8  # Lower confidence for partial credit
        else:
            # Below minimum threshold
            self.marks_awarded = 0
            self.confidence_score = 0.5  # Low confidence
        
        # Flag for review if confidence is low
        if self.confidence_score < 0.70:
            self.requires_review = True
            self.review_reason = f"Low confidence score: {self.confidence_score:.2f}"
        
        self.save()
        return self.marks_awarded


class MarkingCriterion(models.Model):
    """
    Individual marking criteria for detailed assessment
    """
    auto_marker = models.ForeignKey(AutoMarker, on_delete=models.CASCADE, related_name='criteria')
    
    # Criterion details
    criterion_name = models.CharField(max_length=255)
    description = models.TextField()
    expected_content = models.TextField(help_text="Expected content for this criterion")
    
    # Scoring
    weight = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Weight of this criterion (0.0-1.0)"
    )
    max_points = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Keywords for this criterion
    criterion_keywords = models.JSONField(default=list, blank=True)
    required = models.BooleanField(default=False, help_text="Is this criterion required?")
    
    # Ordering
    display_order = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'created_at']
        verbose_name_plural = "Marking Criteria"
    
    def __str__(self):
        return f"{self.criterion_name} ({self.weight * 100}%)"


class CriterionScore(models.Model):
    """
    Score for individual criterion in a marked response
    """
    response = models.ForeignKey(MarkedResponse, on_delete=models.CASCADE, related_name='criterion_scores')
    criterion = models.ForeignKey(MarkingCriterion, on_delete=models.CASCADE)
    
    # Scores
    similarity_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    points_awarded = models.FloatField(default=0.0)
    
    # Analysis
    matched_content = models.TextField(blank=True)
    missing_elements = models.JSONField(default=list, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['criterion__display_order']
    
    def __str__(self):
        return f"{self.criterion.criterion_name}: {self.points_awarded}/{self.criterion.max_points}"


class MarkingLog(models.Model):
    """
    Audit log for marking actions and AI model usage
    """
    
    ACTION_CHOICES = [
        ('mark_single', 'Mark Single Response'),
        ('mark_batch', 'Mark Batch'),
        ('review_mark', 'Review Mark'),
        ('adjust_score', 'Adjust Score'),
        ('recalculate', 'Recalculate Scores'),
        ('model_update', 'Update Model Answer'),
    ]
    
    # Reference
    auto_marker = models.ForeignKey(AutoMarker, on_delete=models.CASCADE, related_name='logs')
    response = models.ForeignKey(MarkedResponse, on_delete=models.CASCADE, null=True, blank=True, related_name='logs')
    
    # Action details
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, db_index=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # AI/Model information
    similarity_model = models.CharField(max_length=100)
    model_version = models.CharField(max_length=50, blank=True)
    
    # Performance metrics
    responses_processed = models.IntegerField(default=1)
    total_time = models.FloatField(help_text="Total processing time in seconds")
    average_time_per_response = models.FloatField(default=0.0)
    
    # Score changes (for review/adjust actions)
    original_score = models.FloatField(null=True, blank=True)
    new_score = models.FloatField(null=True, blank=True)
    adjustment_reason = models.TextField(blank=True)
    
    # Additional details
    details = models.JSONField(default=dict, blank=True)
    
    # Metadata
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['auto_marker', 'action']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.action} - {self.auto_marker.marker_number} at {self.timestamp}"
    
    def save(self, *args, **kwargs):
        if self.responses_processed > 0:
            self.average_time_per_response = self.total_time / self.responses_processed
        super().save(*args, **kwargs)
