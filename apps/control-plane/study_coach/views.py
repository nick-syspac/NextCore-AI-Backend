from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Q
from datetime import datetime, timedelta
import random

from .models import (
    ChatSession,
    ChatMessage,
    KnowledgeDocument,
    CoachingInsight,
    CoachConfiguration,
)
from .serializers import (
    ChatSessionSerializer,
    ChatSessionListSerializer,
    ChatMessageSerializer,
    KnowledgeDocumentSerializer,
    CoachingInsightSerializer,
    CoachConfigurationSerializer,
    SendMessageRequestSerializer,
    GenerateInsightsRequestSerializer,
)


class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

    def get_queryset(self):
        tenant = self.kwargs.get("tenant_slug")
        queryset = ChatSession.objects.filter(tenant=tenant)

        # Filter by student
        student_id = self.request.query_params.get("student_id")
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ChatSessionListSerializer
        return ChatSessionSerializer

    @action(detail=False, methods=["post"])
    def send_message(self, request, tenant_slug=None):
        """Send a message and get AI coach response"""
        serializer = SendMessageRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Get or create session
        session_id = data.get("session_id")
        if session_id:
            session = ChatSession.objects.get(id=session_id, tenant=tenant_slug)
        else:
            session = ChatSession.objects.create(
                tenant=tenant_slug,
                student_id=data["student_id"],
                student_name=data["student_name"],
                subject=data.get("subject", ""),
                topic=data.get("topic", ""),
                session_type=data.get("session_type", "general_chat"),
            )

        # Create student message
        student_message = ChatMessage.objects.create(
            session=session,
            role="student",
            content=data["message"],
            sentiment=self._analyze_sentiment(data["message"]),
            intent_detected=self._detect_intent(data["message"]),
        )

        # Retrieve relevant context from vector DB
        context = self._retrieve_context(
            tenant_slug, data["message"], data.get("subject", ""), data.get("topic", "")
        )

        # Generate AI coach response
        coach_response = self._generate_coach_response(
            tenant_slug, session, data["message"], context
        )

        # Create coach message
        coach_message = ChatMessage.objects.create(
            session=session,
            role="coach",
            content=coach_response["content"],
            model_used=coach_response["model"],
            prompt_tokens=coach_response.get("prompt_tokens", 0),
            completion_tokens=coach_response.get("completion_tokens", 0),
            total_tokens=coach_response.get("total_tokens", 0),
            response_time_ms=coach_response.get("response_time_ms", 0),
            context_used=context["context_summary"],
            vector_search_results=context["documents"],
            relevance_scores=context["scores"],
        )

        # Update session
        session.message_count += 2
        session.save()

        return Response(
            {
                "session": ChatSessionSerializer(session).data,
                "student_message": ChatMessageSerializer(student_message).data,
                "coach_message": ChatMessageSerializer(coach_message).data,
                "context_retrieved": len(context["documents"]),
            }
        )

    @action(detail=True, methods=["post"])
    def rate_session(self, request, pk=None, tenant_slug=None):
        """Rate a completed session"""
        session = self.get_object()
        rating = request.data.get("rating")
        feedback = request.data.get("feedback", "")

        if not rating or not (1 <= int(rating) <= 5):
            return Response(
                {"error": "Rating must be between 1 and 5"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session.satisfaction_rating = int(rating)
        session.student_feedback = feedback
        session.status = "completed"
        session.completed_at = timezone.now()
        session.save()

        return Response(ChatSessionSerializer(session).data)

    @action(detail=False, methods=["get"])
    def dashboard(self, request, tenant_slug=None):
        """Get dashboard statistics"""
        student_id = request.query_params.get("student_id")

        queryset = ChatSession.objects.filter(tenant=tenant_slug)
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        # Calculate stats
        total_sessions = queryset.count()
        active_sessions = queryset.filter(status="active").count()

        avg_satisfaction = (
            queryset.filter(satisfaction_rating__isnull=False).aggregate(
                avg=Avg("satisfaction_rating")
            )["avg"]
            or 0.0
        )

        total_messages = (
            queryset.aggregate(total=models.Sum("message_count"))["total"] or 0
        )

        # Session type breakdown
        session_types = (
            queryset.values("session_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Recent sessions
        recent_sessions = queryset[:5]

        return Response(
            {
                "total_sessions": total_sessions,
                "active_sessions": active_sessions,
                "average_satisfaction": round(avg_satisfaction, 2),
                "total_messages": total_messages,
                "session_type_breakdown": list(session_types),
                "recent_sessions": ChatSessionListSerializer(
                    recent_sessions, many=True
                ).data,
            }
        )

    def _analyze_sentiment(self, message):
        """Analyze message sentiment (simplified)"""
        negative_words = [
            "confused",
            "stuck",
            "hard",
            "difficult",
            "frustrated",
            "don't understand",
            "help",
            "struggling",
        ]
        positive_words = [
            "thanks",
            "thank you",
            "great",
            "helpful",
            "understand",
            "clear",
            "got it",
            "makes sense",
        ]

        message_lower = message.lower()

        negative_count = sum(1 for word in negative_words if word in message_lower)
        positive_count = sum(1 for word in positive_words if word in message_lower)

        if negative_count > positive_count:
            if negative_count >= 3:
                return "frustrated"
            return "confused"
        elif positive_count > negative_count:
            return "positive"

        return "neutral"

    def _detect_intent(self, message):
        """Detect message intent"""
        message_lower = message.lower()

        if any(
            word in message_lower
            for word in ["?", "what", "how", "why", "when", "where"]
        ):
            return "question"
        elif any(word in message_lower for word in ["explain", "clarify", "elaborate"]):
            return "clarification"
        elif any(
            word in message_lower for word in ["example", "show me", "demonstrate"]
        ):
            return "example_request"
        elif any(word in message_lower for word in ["thanks", "thank you"]):
            return "acknowledgment"

        return "statement"

    def _retrieve_context(self, tenant, query, subject, topic):
        """Retrieve relevant context from vector DB (simulated)"""
        # In production, this would use actual vector similarity search
        # For now, return relevant documents based on subject/topic

        documents = KnowledgeDocument.objects.filter(tenant=tenant)

        if subject:
            documents = documents.filter(subject__icontains=subject)

        if topic:
            documents = documents.filter(
                Q(topic__icontains=topic) | Q(content__icontains=topic)
            )

        # Simulate vector search with top K results
        top_docs = documents[:5]

        # Update retrieval stats
        for doc in top_docs:
            doc.retrieval_count += 1
            doc.last_retrieved_at = timezone.now()
            doc.save()

        return {
            "context_summary": {
                "documents_found": top_docs.count(),
                "subjects": list(set(d.subject for d in top_docs)),
                "types": list(set(d.document_type for d in top_docs)),
            },
            "documents": [
                {
                    "id": doc.id,
                    "title": doc.title,
                    "type": doc.document_type,
                    "excerpt": doc.content[:200],
                }
                for doc in top_docs
            ],
            "scores": [round(0.9 - i * 0.1, 2) for i in range(len(top_docs))],
        }

    def _generate_coach_response(self, tenant, session, message, context):
        """Generate AI coach response (simulated LLM call)"""
        # In production, this would call actual LLM API (OpenAI, Anthropic, etc.)
        # For now, generate contextual responses based on message content

        config = CoachConfiguration.objects.filter(tenant=tenant).first()
        model = config.primary_model if config else "gpt-4"

        message_lower = message.lower()

        # Generate response based on message intent
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            response = f"Hello! I'm your AI study coach, available 24/7 to help you succeed. What would you like to work on today?"
        elif "help" in message_lower and any(
            word in message_lower for word in ["homework", "assignment"]
        ):
            response = "I'd be happy to help with your homework! Let's work through this together. Can you tell me which specific part you're finding challenging? I'll guide you step-by-step."
        elif any(word in message_lower for word in ["explain", "what is", "what are"]):
            concept = (
                message.split("explain")[-1].strip()
                if "explain" in message_lower
                else "this concept"
            )
            response = (
                f"Great question! Let me explain {concept}. "
                + f"I've found {len(context['documents'])} relevant resources to help. "
                + "The key idea is understanding how the components work together. Would you like me to break it down further?"
            )
        elif "exam" in message_lower or "test" in message_lower:
            response = (
                "Let's prepare you for success on your exam! I can help with:\n"
                + "• Reviewing key concepts\n• Practice problems\n• Study strategies\n• Time management\n\nWhat area would you like to focus on first?"
            )
        elif any(
            word in message_lower for word in ["stuck", "confused", "don't understand"]
        ):
            response = (
                "No worries - that's what I'm here for! Let's break this down into smaller pieces. "
                + "Can you tell me which specific part is confusing? Sometimes a different explanation or example can make it click."
            )
        elif any(word in message_lower for word in ["thanks", "thank you"]):
            response = (
                "You're very welcome! I'm glad I could help. Remember, I'm here 24/7 whenever you need support. "
                + "Is there anything else you'd like to work on?"
            )
        else:
            response = (
                f"I understand you're asking about this topic. Based on the course materials I have access to, "
                + f"there are several important aspects to consider. Would you like me to explain the fundamentals first, "
                + "or would you prefer to dive into a specific area?"
            )

        # Simulate LLM metrics
        prompt_tokens = len(message.split()) * 2 + 100  # Simplified
        completion_tokens = len(response.split()) * 2

        return {
            "content": response,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "response_time_ms": random.randint(500, 2000),
        }


class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        tenant = self.kwargs.get("tenant_slug")
        session_id = self.request.query_params.get("session_id")

        queryset = ChatMessage.objects.filter(session__tenant=tenant)

        if session_id:
            queryset = queryset.filter(session_id=session_id)

        return queryset


class KnowledgeDocumentViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeDocument.objects.all()
    serializer_class = KnowledgeDocumentSerializer

    def get_queryset(self):
        tenant = self.kwargs.get("tenant_slug")
        return KnowledgeDocument.objects.filter(tenant=tenant)

    def perform_create(self, serializer):
        tenant = self.kwargs.get("tenant_slug")
        serializer.save(tenant=tenant)


class CoachingInsightViewSet(viewsets.ModelViewSet):
    queryset = CoachingInsight.objects.all()
    serializer_class = CoachingInsightSerializer

    def get_queryset(self):
        tenant = self.kwargs.get("tenant_slug")
        return CoachingInsight.objects.filter(tenant=tenant)

    @action(detail=False, methods=["post"])
    def generate_insights(self, request, tenant_slug=None):
        """Generate insights for a student"""
        serializer = GenerateInsightsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        student_id = data["student_id"]
        time_period = data.get("time_period", timezone.now().strftime("%Y-%m"))

        # Get sessions for the period
        sessions = ChatSession.objects.filter(
            tenant=tenant_slug,
            student_id=student_id,
            created_at__month=int(time_period.split("-")[1]),
            created_at__year=int(time_period.split("-")[0]),
        )

        # Calculate metrics
        total_sessions = sessions.count()
        total_messages = (
            sessions.aggregate(total=models.Sum("message_count"))["total"] or 0
        )
        total_duration = (
            sessions.aggregate(total=models.Sum("total_duration_minutes"))["total"] or 0
        )

        avg_session_length = (
            (total_duration / total_sessions) if total_sessions > 0 else 0
        )

        # Session type distribution
        session_type_dist = {}
        for session in sessions:
            session_type_dist[session.session_type] = (
                session_type_dist.get(session.session_type, 0) + 1
            )

        # Most discussed subjects and topics
        subjects = [s.subject for s in sessions if s.subject]
        topics = [s.topic for s in sessions if s.topic]

        from collections import Counter

        most_discussed_subjects = [
            item for item, count in Counter(subjects).most_common(5)
        ]
        most_discussed_topics = [item for item, count in Counter(topics).most_common(5)]

        # Satisfaction metrics
        rated_sessions = sessions.filter(satisfaction_rating__isnull=False)
        avg_satisfaction = (
            rated_sessions.aggregate(avg=Avg("satisfaction_rating"))["avg"] or 0.0
        )

        # Create or update insight
        insight, created = CoachingInsight.objects.update_or_create(
            tenant=tenant_slug,
            student_id=student_id,
            time_period=time_period,
            defaults={
                "total_sessions": total_sessions,
                "total_messages": total_messages,
                "total_duration_minutes": total_duration,
                "average_session_length": round(avg_session_length, 2),
                "session_type_distribution": session_type_dist,
                "most_discussed_subjects": most_discussed_subjects,
                "most_discussed_topics": most_discussed_topics,
                "average_satisfaction": round(avg_satisfaction, 2),
                "sessions_with_feedback": rated_sessions.count(),
            },
        )

        return Response(CoachingInsightSerializer(insight).data)


class CoachConfigurationViewSet(viewsets.ModelViewSet):
    queryset = CoachConfiguration.objects.all()
    serializer_class = CoachConfigurationSerializer

    def get_queryset(self):
        tenant = self.kwargs.get("tenant_slug")
        return CoachConfiguration.objects.filter(tenant=tenant)

    def perform_create(self, serializer):
        tenant = self.kwargs.get("tenant_slug")
        serializer.save(tenant=tenant)


# Import models for aggregation
from django.db import models
