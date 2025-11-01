from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from tenants.models import Tenant
from assessment_builder.models import Assessment, AssessmentTask

User = get_user_model()


class Rubric(models.Model):
    """
    Marking rubric for assessments or individual tasks
    """

    RUBRIC_TYPE_CHOICES = [
        ("analytic", "Analytic"),  # Separate criteria with levels
        ("holistic", "Holistic"),  # Single overall assessment
        ("checklist", "Checklist"),  # Simple yes/no criteria
        ("single_point", "Single Point"),  # Focus on meeting standard
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("generating", "Generating"),
        ("review", "In Review"),
        ("approved", "Approved"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    # Core fields
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="rubrics")
    rubric_number = models.CharField(max_length=50, unique=True, editable=False)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    rubric_type = models.CharField(
        max_length=20, choices=RUBRIC_TYPE_CHOICES, default="analytic"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    # Links to assessments/tasks
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="rubrics",
        null=True,
        blank=True,
        help_text="Assessment this rubric is for",
    )
    task = models.ForeignKey(
        AssessmentTask,
        on_delete=models.CASCADE,
        related_name="rubrics",
        null=True,
        blank=True,
        help_text="Specific task this rubric is for (optional)",
    )

    # Rubric structure
    total_points = models.IntegerField(
        default=100, help_text="Maximum points achievable"
    )
    passing_score = models.IntegerField(default=50, help_text="Minimum points to pass")

    # AI Generation metadata
    ai_generated = models.BooleanField(default=False)
    ai_model = models.CharField(max_length=100, blank=True)
    ai_prompt = models.TextField(blank=True)
    ai_generation_time = models.FloatField(
        null=True, blank=True, help_text="Generation time in seconds"
    )
    ai_generated_at = models.DateTimeField(null=True, blank=True)

    # NLP Summarization
    nlp_summary = models.TextField(
        blank=True, help_text="NLP-generated summary of rubric purpose"
    )
    nlp_key_points = models.JSONField(
        default=list, blank=True, help_text="Extracted key assessment points"
    )

    # Taxonomy Tagging
    taxonomy_tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Educational taxonomy tags (Bloom's, SOLO, etc.)",
    )
    blooms_levels = models.JSONField(
        default=dict, blank=True, help_text="Distribution of Bloom's levels in criteria"
    )

    # Metadata
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_rubrics"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Review workflow
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_rubrics",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_rubrics",
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["tenant", "status"]),
            models.Index(fields=["rubric_type"]),
            models.Index(fields=["assessment"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.rubric_number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.rubric_number:
            # Generate rubric number: RUB-YYYYMMDD-XXXXXX
            from datetime import datetime

            date_str = datetime.now().strftime("%Y%m%d")
            # Get count of rubrics created today
            today_start = timezone.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            count = Rubric.objects.filter(created_at__gte=today_start).count()
            self.rubric_number = f"RUB-{date_str}-{str(count + 1).zfill(6)}"
        super().save(*args, **kwargs)

    def get_criterion_count(self):
        """Get total number of criteria"""
        return self.criteria.count()

    def calculate_taxonomy_distribution(self):
        """Calculate distribution of taxonomy tags across criteria"""
        from collections import Counter

        all_tags = []
        for criterion in self.criteria.all():
            all_tags.extend(criterion.taxonomy_tags or [])

        if not all_tags:
            return {}

        tag_counts = Counter(all_tags)
        total = sum(tag_counts.values())

        distribution = {
            tag: round((count / total) * 100, 1) for tag, count in tag_counts.items()
        }
        return distribution


class RubricCriterion(models.Model):
    """
    Individual criterion within a rubric
    """

    rubric = models.ForeignKey(
        Rubric, on_delete=models.CASCADE, related_name="criteria"
    )
    criterion_number = models.CharField(max_length=20, help_text="e.g., 1, 1.1, A")
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    # Weight and scoring
    weight = models.IntegerField(default=1, help_text="Weight of this criterion")
    max_points = models.IntegerField(
        default=10, help_text="Maximum points for this criterion"
    )

    # Links to unit requirements
    maps_to_elements = models.JSONField(default=list, blank=True)
    maps_to_performance_criteria = models.JSONField(default=list, blank=True)
    maps_to_knowledge_evidence = models.JSONField(default=list, blank=True)

    # Taxonomy tagging
    taxonomy_tags = models.JSONField(
        default=list,
        blank=True,
        help_text='Tags like "Bloom\'s: Apply", "SOLO: Relational"',
    )
    blooms_level = models.CharField(
        max_length=20, blank=True, help_text="Primary Bloom's level for this criterion"
    )

    # AI metadata
    ai_generated = models.BooleanField(default=False)
    ai_rationale = models.TextField(
        blank=True, help_text="Why this criterion was generated"
    )
    nlp_keywords = models.JSONField(
        default=list, blank=True, help_text="NLP-extracted keywords"
    )

    # Ordering
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["rubric", "display_order"]
        indexes = [
            models.Index(fields=["rubric", "display_order"]),
        ]

    def __str__(self):
        return f"{self.rubric.rubric_number} - {self.criterion_number}: {self.title}"


class RubricLevel(models.Model):
    """
    Performance level definition for a criterion (e.g., Excellent, Good, Satisfactory, Poor)
    """

    LEVEL_CHOICES = [
        ("exemplary", "Exemplary"),
        ("proficient", "Proficient"),
        ("competent", "Competent"),
        ("developing", "Developing"),
        ("unsatisfactory", "Unsatisfactory"),
        ("not_demonstrated", "Not Demonstrated"),
    ]

    criterion = models.ForeignKey(
        RubricCriterion, on_delete=models.CASCADE, related_name="levels"
    )
    level_name = models.CharField(
        max_length=50, help_text="e.g., Excellent, Good, Satisfactory"
    )
    level_type = models.CharField(max_length=30, choices=LEVEL_CHOICES, blank=True)
    points = models.IntegerField(help_text="Points awarded for this level")
    description = models.TextField(
        help_text="What performance looks like at this level"
    )

    # Examples and indicators
    indicators = models.JSONField(
        default=list,
        blank=True,
        help_text="Specific indicators of this performance level",
    )
    examples = models.TextField(
        blank=True, help_text="Example responses or work at this level"
    )

    # AI generation
    ai_generated = models.BooleanField(default=False)
    nlp_summary = models.TextField(
        blank=True, help_text="NLP summary of level description"
    )

    # Ordering
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["criterion", "-points"]  # Highest points first
        indexes = [
            models.Index(fields=["criterion", "display_order"]),
        ]

    def __str__(self):
        return (
            f"{self.criterion.criterion_number} - {self.level_name} ({self.points} pts)"
        )


class RubricGenerationLog(models.Model):
    """
    Audit log for rubric generation activities
    """

    ACTION_CHOICES = [
        ("generate_full", "Generate Full Rubric"),
        ("generate_criterion", "Generate Single Criterion"),
        ("generate_levels", "Generate Performance Levels"),
        ("nlp_summarize", "NLP Summarization"),
        ("tag_taxonomy", "Taxonomy Tagging"),
        ("regenerate", "Regenerate"),
    ]

    rubric = models.ForeignKey(
        Rubric, on_delete=models.CASCADE, related_name="generation_logs"
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)

    # AI/NLP details
    ai_model = models.CharField(max_length=100, blank=True)
    nlp_model = models.CharField(max_length=100, blank=True)
    prompt_used = models.TextField(blank=True)
    response_text = models.TextField(blank=True)

    # Metrics
    tokens_used = models.IntegerField(default=0)
    generation_time = models.FloatField(help_text="Time in seconds")

    # Result
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    # Audit
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    performed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-performed_at"]
        indexes = [
            models.Index(fields=["rubric", "performed_at"]),
        ]

    def __str__(self):
        return f"{self.rubric.rubric_number} - {self.action} at {self.performed_at}"
