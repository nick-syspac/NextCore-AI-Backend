from django.db import models
from django.utils import timezone
import uuid


class ChatSession(models.Model):
    """Chat session for student-coach interactions"""

    session_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)
    student_name = models.CharField(max_length=200)

    # Session metadata
    subject = models.CharField(max_length=200, blank=True)
    topic = models.CharField(max_length=200, blank=True)
    session_type = models.CharField(
        max_length=50,
        choices=[
            ("homework_help", "Homework Help"),
            ("concept_review", "Concept Review"),
            ("exam_prep", "Exam Preparation"),
            ("project_guidance", "Project Guidance"),
            ("career_advice", "Career Advice"),
            ("study_tips", "Study Tips"),
            ("general_chat", "General Chat"),
        ],
        default="general_chat",
    )

    # Session status
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("paused", "Paused"),
            ("completed", "Completed"),
            ("archived", "Archived"),
        ],
        default="active",
    )

    # Session analytics
    message_count = models.IntegerField(default=0)
    total_duration_minutes = models.IntegerField(default=0)
    satisfaction_rating = models.IntegerField(null=True, blank=True)  # 1-5 stars
    student_feedback = models.TextField(blank=True)

    # Context tracking
    referenced_materials = models.JSONField(
        default=list
    )  # Course materials, documents, etc.
    key_concepts_discussed = models.JSONField(default=list)
    follow_up_needed = models.BooleanField(default=False)
    follow_up_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["tenant", "student_id", "-created_at"]),
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.session_number} - {self.student_name}"

    def save(self, *args, **kwargs):
        if not self.session_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:8].upper()
            self.session_number = f"CHAT-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    """Individual messages in a chat session"""

    message_number = models.CharField(max_length=50, unique=True, db_index=True)
    session = models.ForeignKey(
        ChatSession, on_delete=models.CASCADE, related_name="messages"
    )

    # Message content
    role = models.CharField(
        max_length=20,
        choices=[("student", "Student"), ("coach", "AI Coach"), ("system", "System")],
    )
    content = models.TextField()

    # LLM metadata (for coach messages)
    model_used = models.CharField(max_length=100, blank=True)  # e.g., gpt-4, claude-3
    prompt_tokens = models.IntegerField(null=True, blank=True)
    completion_tokens = models.IntegerField(null=True, blank=True)
    total_tokens = models.IntegerField(null=True, blank=True)
    response_time_ms = models.IntegerField(null=True, blank=True)

    # Context and retrieval
    context_used = models.JSONField(default=dict)  # Retrieved context from vector DB
    vector_search_results = models.JSONField(default=list)  # Top K similar documents
    relevance_scores = models.JSONField(default=list)  # Similarity scores

    # Message metadata
    sentiment = models.CharField(
        max_length=20,
        choices=[
            ("positive", "Positive"),
            ("neutral", "Neutral"),
            ("confused", "Confused"),
            ("frustrated", "Frustrated"),
            ("negative", "Negative"),
        ],
        blank=True,
    )
    intent_detected = models.CharField(
        max_length=200, blank=True
    )  # question, clarification, etc.

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.message_number} - {self.role}"

    def save(self, *args, **kwargs):
        if not self.message_number:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            unique_id = str(uuid.uuid4())[:6].upper()
            self.message_number = f"MSG-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class KnowledgeDocument(models.Model):
    """Documents stored in vector DB for contextual retrieval"""

    document_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)

    # Document metadata
    title = models.CharField(max_length=300)
    document_type = models.CharField(
        max_length=50,
        choices=[
            ("syllabus", "Syllabus"),
            ("lecture_notes", "Lecture Notes"),
            ("textbook", "Textbook Chapter"),
            ("assignment", "Assignment"),
            ("study_guide", "Study Guide"),
            ("faq", "FAQ"),
            ("policy", "Policy Document"),
            ("resource", "Learning Resource"),
        ],
    )
    subject = models.CharField(max_length=200)
    topic = models.CharField(max_length=200, blank=True)

    # Content
    content = models.TextField()
    summary = models.TextField(blank=True)
    keywords = models.JSONField(default=list)

    # Vector DB integration
    vector_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )  # ID in vector DB
    embedding_model = models.CharField(max_length=100, default="all-MiniLM-L6-v2")
    chunk_size = models.IntegerField(default=512)
    chunks_count = models.IntegerField(default=1)

    # Usage tracking
    retrieval_count = models.IntegerField(default=0)
    average_relevance_score = models.FloatField(default=0.0)
    last_retrieved_at = models.DateTimeField(null=True, blank=True)

    # Access control
    visibility = models.CharField(
        max_length=20,
        choices=[
            ("public", "Public"),
            ("course_specific", "Course Specific"),
            ("restricted", "Restricted"),
        ],
        default="course_specific",
    )
    course_ids = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["tenant", "subject", "document_type"]),
            models.Index(fields=["vector_id"]),
        ]

    def __str__(self):
        return f"{self.document_number} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.document_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:8].upper()
            self.document_number = f"DOC-{timestamp}-{unique_id}"
        if not self.vector_id:
            self.vector_id = f"vec_{uuid.uuid4().hex}"
        super().save(*args, **kwargs)


class CoachingInsight(models.Model):
    """Analytics and insights from coaching sessions"""

    insight_number = models.CharField(max_length=50, unique=True, db_index=True)
    tenant = models.CharField(max_length=100, db_index=True)
    student_id = models.CharField(max_length=100, db_index=True)
    time_period = models.CharField(max_length=50)  # e.g., "2024-10"

    # Engagement metrics
    total_sessions = models.IntegerField(default=0)
    total_messages = models.IntegerField(default=0)
    total_duration_minutes = models.IntegerField(default=0)
    average_session_length = models.FloatField(default=0.0)

    # Session type breakdown
    session_type_distribution = models.JSONField(default=dict)  # {type: count}

    # Performance indicators
    most_discussed_subjects = models.JSONField(default=list)
    most_discussed_topics = models.JSONField(default=list)
    knowledge_gaps_identified = models.JSONField(default=list)

    # Sentiment analysis
    average_sentiment_score = models.FloatField(default=0.0)  # -1 to 1
    sentiment_trend = models.CharField(
        max_length=20,
        choices=[
            ("improving", "Improving"),
            ("stable", "Stable"),
            ("declining", "Declining"),
        ],
        default="stable",
    )

    # Satisfaction metrics
    average_satisfaction = models.FloatField(default=0.0)  # 1-5 stars
    sessions_with_feedback = models.IntegerField(default=0)

    # Recommendations
    recommended_resources = models.JSONField(default=list)
    follow_up_actions = models.JSONField(default=list)
    at_risk_indicators = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["tenant", "student_id", "time_period"]]

    def __str__(self):
        return f"{self.insight_number} - Student {self.student_id}"

    def save(self, *args, **kwargs):
        if not self.insight_number:
            timestamp = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4())[:8].upper()
            self.insight_number = f"INSIGHT-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class CoachConfiguration(models.Model):
    """Configuration for AI coach behavior"""

    tenant = models.CharField(max_length=100, unique=True, db_index=True)

    # LLM settings
    primary_model = models.CharField(max_length=100, default="gpt-4")
    fallback_model = models.CharField(max_length=100, default="gpt-3.5-turbo")
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=500)

    # Personality and tone
    coaching_style = models.CharField(
        max_length=50,
        choices=[
            ("encouraging", "Encouraging & Supportive"),
            ("socratic", "Socratic Questioning"),
            ("direct", "Direct & Concise"),
            ("adaptive", "Adaptive to Student"),
        ],
        default="encouraging",
    )
    personality_traits = models.JSONField(
        default=list
    )  # patient, empathetic, motivating

    # Behavior rules
    system_prompt = models.TextField(default="You are a helpful AI study coach.")
    response_guidelines = models.JSONField(default=list)
    prohibited_topics = models.JSONField(default=list)

    # Vector DB settings
    vector_db_enabled = models.BooleanField(default=True)
    top_k_results = models.IntegerField(default=5)
    similarity_threshold = models.FloatField(default=0.7)

    # Safety and moderation
    content_filter_enabled = models.BooleanField(default=True)
    profanity_filter = models.BooleanField(default=True)
    escalation_keywords = models.JSONField(default=list)  # Crisis detection

    # Availability
    available_24_7 = models.BooleanField(default=True)
    business_hours_only = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, default="UTC")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Coach Config - {self.tenant}"
