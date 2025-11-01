from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
import uuid
from datetime import datetime


class LearningPathway(models.Model):
    """
    Master model for personalized learning pathways.
    Generated using collaborative filtering + embeddings to recommend optimal learning sequences.
    """

    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("paused", "Paused"),
        ("abandoned", "Abandoned"),
    ]

    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
        ("expert", "Expert"),
    ]

    pathway_number = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)
    student_name = models.CharField(max_length=200)

    # Pathway details
    pathway_name = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default="beginner"
    )
    estimated_duration_hours = models.DecimalField(
        max_digits=6, decimal_places=1, validators=[MinValueValidator(0)]
    )

    # Recommendation metadata
    recommendation_confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Confidence score from collaborative filtering algorithm (0-100%)",
    )
    similarity_score = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Cosine similarity from embedding vectors (0-1)",
    )

    # Progress tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    total_steps = models.PositiveIntegerField(default=0)
    completed_steps = models.PositiveIntegerField(default=0)
    completion_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    # Adaptive features
    personalization_factors = models.JSONField(
        default=dict,
        help_text="Factors used for personalization: learning_style, pace, interests, prior_knowledge",
    )
    similar_students = models.JSONField(
        default=list,
        help_text="Student IDs with similar learning patterns (collaborative filtering)",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["student_id", "-created_at"]),
            models.Index(fields=["status", "tenant"]),
            models.Index(fields=["difficulty_level"]),
        ]
        verbose_name = "Learning Pathway"
        verbose_name_plural = "Learning Pathways"

    def save(self, *args, **kwargs):
        if not self.pathway_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:8].upper()
            self.pathway_number = f"PATH-{timestamp}-{unique_id}"

        # Calculate completion percentage
        if self.total_steps > 0:
            self.completion_percentage = (self.completed_steps / self.total_steps) * 100

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pathway_number} - {self.pathway_name} ({self.student_name})"


class LearningStep(models.Model):
    """
    Individual learning content nodes within a pathway.
    Represents courses, modules, activities, or resources.
    """

    CONTENT_TYPE_CHOICES = [
        ("video", "Video Lesson"),
        ("reading", "Reading Material"),
        ("quiz", "Quiz/Assessment"),
        ("assignment", "Assignment"),
        ("project", "Project"),
        ("discussion", "Discussion Forum"),
        ("interactive", "Interactive Activity"),
        ("lab", "Hands-on Lab"),
    ]

    STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("skipped", "Skipped"),
    ]

    step_number = models.CharField(max_length=50, unique=True, editable=False)
    pathway = models.ForeignKey(
        LearningPathway, on_delete=models.CASCADE, related_name="steps"
    )

    # Content details
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content_url = models.URLField(blank=True)

    # Sequencing
    sequence_order = models.PositiveIntegerField()
    is_prerequisite = models.BooleanField(default=False)
    prerequisites = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Step numbers that must be completed first",
    )

    # Learning metadata
    estimated_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    difficulty_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Difficulty rating 1-5",
    )
    learning_objectives = ArrayField(models.TextField(), default=list, blank=True)

    # Tags for embeddings
    tags = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Content tags for similarity matching",
    )

    # Progress
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="not_started"
    )
    completion_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["pathway", "sequence_order"]
        unique_together = [["pathway", "sequence_order"]]
        indexes = [
            models.Index(fields=["pathway", "sequence_order"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = "Learning Step"
        verbose_name_plural = "Learning Steps"

    def save(self, *args, **kwargs):
        if not self.step_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.step_number = f"STEP-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.step_number} - {self.title}"


class StudentProgress(models.Model):
    """
    Detailed tracking of student progress through learning steps.
    Used for collaborative filtering to find similar learning patterns.
    """

    progress_number = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)
    pathway = models.ForeignKey(
        LearningPathway, on_delete=models.CASCADE, related_name="progress_records"
    )
    step = models.ForeignKey(
        LearningStep, on_delete=models.CASCADE, related_name="progress_records"
    )

    # Engagement metrics
    time_spent_minutes = models.PositiveIntegerField(default=0)
    attempts = models.PositiveIntegerField(default=0)
    completion_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    # Learning analytics
    struggle_indicators = models.JSONField(
        default=dict,
        help_text="Indicators of difficulty: multiple_attempts, extended_time, help_requests",
    )
    engagement_level = models.CharField(
        max_length=20,
        choices=[
            ("high", "High Engagement"),
            ("medium", "Medium Engagement"),
            ("low", "Low Engagement"),
        ],
        default="medium",
    )

    # Adaptive adjustments
    recommended_next_steps = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Step numbers recommended based on performance",
    )
    difficulty_adjustment = models.CharField(
        max_length=20,
        choices=[
            ("easier", "Recommend Easier"),
            ("maintain", "Maintain Level"),
            ("harder", "Recommend Harder"),
        ],
        default="maintain",
    )

    # Status
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["student_id", "pathway"]),
            models.Index(fields=["step", "is_completed"]),
        ]
        verbose_name = "Student Progress"
        verbose_name_plural = "Student Progress Records"

    def save(self, *args, **kwargs):
        if not self.progress_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.progress_number = f"PROG-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.progress_number} - {self.student_id} - {self.step.title}"


class PathwayRecommendation(models.Model):
    """
    Collaborative filtering recommendations for learning pathways.
    Uses user-item matrix and embeddings for personalized suggestions.
    """

    ALGORITHM_CHOICES = [
        ("collaborative_filtering", "Collaborative Filtering"),
        ("content_based", "Content-Based"),
        ("hybrid", "Hybrid (CF + Embeddings)"),
    ]

    recommendation_number = models.CharField(max_length=50, unique=True, editable=False)
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)
    student_name = models.CharField(max_length=200)

    # Recommendation details
    recommended_pathway = models.ForeignKey(
        LearningPathway, on_delete=models.CASCADE, related_name="recommendations"
    )
    algorithm_used = models.CharField(
        max_length=30, choices=ALGORITHM_CHOICES, default="hybrid"
    )

    # Scoring
    recommendation_score = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Overall recommendation score (0-1)",
    )
    collaborative_score = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Score from collaborative filtering",
    )
    embedding_similarity = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Cosine similarity from content embeddings",
    )

    # Collaborative filtering metadata
    similar_students_count = models.PositiveIntegerField(default=0)
    similar_students_list = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True,
        help_text="Student IDs with similar learning patterns",
    )
    common_pathways = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Pathway numbers completed by similar students",
    )

    # Reasoning
    recommendation_reasons = models.JSONField(
        default=list, help_text="Human-readable reasons for recommendation"
    )

    # User feedback
    is_accepted = models.BooleanField(null=True, blank=True)
    feedback_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="User rating of recommendation (1-5)",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="Recommendation expiry date")

    class Meta:
        ordering = ["-recommendation_score", "-created_at"]
        indexes = [
            models.Index(fields=["student_id", "-created_at"]),
            models.Index(fields=["is_accepted"]),
        ]
        verbose_name = "Pathway Recommendation"
        verbose_name_plural = "Pathway Recommendations"

    def save(self, *args, **kwargs):
        if not self.recommendation_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:8].upper()
            self.recommendation_number = f"REC-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.recommendation_number} - {self.student_name} - {self.recommended_pathway.pathway_name}"


class ContentEmbedding(models.Model):
    """
    Vector embeddings for learning content.
    Used for semantic similarity and content-based recommendations.
    """

    embedding_number = models.CharField(max_length=50, unique=True, editable=False)
    step = models.OneToOneField(
        LearningStep, on_delete=models.CASCADE, related_name="embedding"
    )

    # Embedding vector (stored as array)
    embedding_vector = ArrayField(
        models.FloatField(),
        default=list,
        help_text="384-dimensional embedding vector from sentence-transformers",
    )
    embedding_dimension = models.PositiveIntegerField(default=384)

    # Metadata for embedding generation
    model_name = models.CharField(
        max_length=100,
        default="all-MiniLM-L6-v2",
        help_text="Name of the embedding model used",
    )
    text_content = models.TextField(
        help_text="Text used to generate embedding (title + description + objectives)"
    )

    # Similarity cache (top 10 most similar content)
    similar_content = models.JSONField(
        default=list,
        help_text="Cached list of similar step_numbers with similarity scores",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["step"]),
        ]
        verbose_name = "Content Embedding"
        verbose_name_plural = "Content Embeddings"

    def save(self, *args, **kwargs):
        if not self.embedding_number:
            timestamp = datetime.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.embedding_number = f"EMB-{timestamp}-{unique_id}"

        self.embedding_dimension = len(self.embedding_vector)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.embedding_number} - {self.step.title}"
