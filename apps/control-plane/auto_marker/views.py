from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Avg, Count
import time
import re

from .models import (
    AutoMarker,
    MarkedResponse,
    MarkingCriterion,
    CriterionScore,
    MarkingLog,
)
from .serializers import (
    AutoMarkerListSerializer,
    AutoMarkerDetailSerializer,
    MarkedResponseListSerializer,
    MarkedResponseDetailSerializer,
    MarkingCriterionSerializer,
    CriterionScoreSerializer,
    MarkingLogSerializer,
    MarkResponsesRequestSerializer,
    SingleMarkRequestSerializer,
)


class AutoMarkerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AutoMarker management and marking operations
    """

    def get_queryset(self):
        tenant = self.kwargs.get("tenant_slug")
        queryset = AutoMarker.objects.filter(tenant=tenant)

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by answer type
        answer_type = self.request.query_params.get("answer_type")
        if answer_type:
            queryset = queryset.filter(answer_type=answer_type)

        # Search
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(marker_number__icontains=search)
                | Q(description__icontains=search)
            )

        return queryset.select_related("created_by").prefetch_related(
            "criteria", "responses"
        )

    def get_serializer_class(self):
        if self.action == "list":
            return AutoMarkerListSerializer
        return AutoMarkerDetailSerializer

    def perform_create(self, serializer):
        tenant = self.kwargs.get("tenant_slug")
        serializer.save(tenant=tenant, created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_responses(self, request, tenant_slug=None, pk=None):
        """
        Mark multiple responses in batch with semantic similarity
        """
        auto_marker = self.get_object()
        serializer = MarkResponsesRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        responses_data = serializer.validated_data["responses"]
        auto_mark = serializer.validated_data.get("auto_mark", True)
        enable_review_flagging = serializer.validated_data.get(
            "enable_review_flagging", True
        )

        start_time = time.time()
        marked_responses = []

        for response_data in responses_data:
            # Create response object
            response = MarkedResponse.objects.create(
                auto_marker=auto_marker,
                student_id=response_data["student_id"],
                student_name=response_data["student_name"],
                response_text=response_data["response_text"],
                status="marking",
            )

            if auto_mark:
                # Perform semantic similarity marking
                self._mark_response(response, auto_marker, enable_review_flagging)

            marked_responses.append(response)

        # Update statistics
        total_time = time.time() - start_time
        auto_marker.total_responses_marked += len(marked_responses)
        auto_marker.calculate_average_score()

        # Update average marking time
        if auto_marker.total_responses_marked > 0:
            total_marking_time = (
                auto_marker.average_marking_time
                * (auto_marker.total_responses_marked - len(marked_responses))
            ) + total_time
            auto_marker.average_marking_time = (
                total_marking_time / auto_marker.total_responses_marked
            )
        auto_marker.save()

        # Create marking log
        MarkingLog.objects.create(
            auto_marker=auto_marker,
            action="mark_batch",
            performed_by=request.user,
            similarity_model=auto_marker.similarity_model,
            model_version="1.0",
            responses_processed=len(marked_responses),
            total_time=total_time,
            details={
                "batch_size": len(marked_responses),
                "auto_mark": auto_mark,
                "review_flagging": enable_review_flagging,
            },
        )

        # Serialize responses
        response_serializer = MarkedResponseListSerializer(marked_responses, many=True)

        return Response(
            {
                "message": f"Successfully marked {len(marked_responses)} responses",
                "total_time": total_time,
                "average_time": (
                    total_time / len(marked_responses) if marked_responses else 0
                ),
                "responses": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def mark_single(self, request, tenant_slug=None, pk=None):
        """
        Mark a single response
        """
        auto_marker = self.get_object()
        serializer = SingleMarkRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_time = time.time()

        # Create response
        response = MarkedResponse.objects.create(
            auto_marker=auto_marker,
            student_id=serializer.validated_data["student_id"],
            student_name=serializer.validated_data["student_name"],
            response_text=serializer.validated_data["response_text"],
            status="marking",
        )

        if serializer.validated_data.get("auto_mark", True):
            self._mark_response(response, auto_marker, enable_review_flagging=True)

        marking_time = time.time() - start_time

        # Update statistics
        auto_marker.total_responses_marked += 1
        auto_marker.calculate_average_score()
        auto_marker.save()

        # Create log
        MarkingLog.objects.create(
            auto_marker=auto_marker,
            response=response,
            action="mark_single",
            performed_by=request.user,
            similarity_model=auto_marker.similarity_model,
            model_version="1.0",
            responses_processed=1,
            total_time=marking_time,
        )

        response_serializer = MarkedResponseDetailSerializer(response)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def _mark_response(self, response, auto_marker, enable_review_flagging=True):
        """
        Internal method to mark a response using semantic similarity
        This is a mock implementation - in production, use real NLP models
        """
        start_time = time.time()

        # Mock semantic similarity calculation
        # In production: Use sentence transformers, BERT, etc.
        similarity_score = self._calculate_semantic_similarity(
            response.response_text, auto_marker.model_answer
        )
        response.similarity_score = similarity_score

        # Keyword matching
        if auto_marker.use_keywords and auto_marker.keywords:
            keyword_score, matched, missing = self._calculate_keyword_match(
                response.response_text, auto_marker.keywords
            )
            response.keyword_match_score = keyword_score
            response.matched_keywords = matched
            response.missing_keywords = missing
        else:
            response.keyword_match_score = 0.0
            response.matched_keywords = []
            response.missing_keywords = []

        # Extract key phrases (mock)
        response.key_phrases_detected = self._extract_key_phrases(
            response.response_text
        )

        # Similarity breakdown
        response.similarity_breakdown = {
            "lexical_similarity": similarity_score * 0.4,
            "semantic_similarity": similarity_score * 0.6,
            "structure_match": (
                0.75 if len(response.response_text.split()) > 20 else 0.5
            ),
            "completeness": min(
                1.0,
                len(response.response_text.split())
                / len(auto_marker.model_answer.split()),
            ),
        }

        # Calculate marks
        response.calculate_marks()

        # Generate automated feedback
        response.automated_feedback = self._generate_feedback(response, auto_marker)

        # Update status
        response.status = "marked"
        response.marked_at = timezone.now()
        response.marking_time = time.time() - start_time

        # Review flagging
        if enable_review_flagging:
            if response.confidence_score < 0.70:
                response.requires_review = True
                response.review_reason = (
                    f"Low confidence: {response.confidence_score:.2f}"
                )
            elif len(response.missing_keywords) > len(auto_marker.keywords) / 2:
                response.requires_review = True
                response.review_reason = (
                    f"Missing {len(response.missing_keywords)} key concepts"
                )

        response.save()

        return response

    def _calculate_semantic_similarity(self, text1, text2):
        """
        Mock semantic similarity calculation
        In production: Use sentence-transformers, OpenAI embeddings, etc.
        """
        # Simple mock: based on word overlap and length ratio
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        # Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        jaccard = len(intersection) / len(union) if union else 0

        # Length ratio
        len_ratio = (
            min(len(text1), len(text2)) / max(len(text1), len(text2))
            if max(len(text1), len(text2)) > 0
            else 0
        )

        # Combined score (weighted)
        similarity = (jaccard * 0.7) + (len_ratio * 0.3)

        # Add some variance
        import random

        variance = random.uniform(-0.05, 0.15)
        similarity = max(0.0, min(1.0, similarity + variance))

        return round(similarity, 3)

    def _calculate_keyword_match(self, text, keywords):
        """Calculate keyword matching score"""
        text_lower = text.lower()
        matched = []
        missing = []

        for keyword in keywords:
            if keyword.lower() in text_lower:
                matched.append(keyword)
            else:
                missing.append(keyword)

        score = len(matched) / len(keywords) if keywords else 0.0
        return round(score, 3), matched, missing

    def _extract_key_phrases(self, text):
        """
        Mock key phrase extraction
        In production: Use spaCy, RAKE, YAKE, etc.
        """
        # Simple mock: extract longer phrases (3+ words)
        sentences = text.split(".")
        phrases = []

        for sentence in sentences[:3]:  # First 3 sentences
            words = sentence.strip().split()
            if len(words) >= 3:
                phrases.append(" ".join(words[:5]))  # First 5 words

        return phrases[:5]  # Max 5 phrases

    def _generate_feedback(self, response, auto_marker):
        """Generate automated feedback based on marking"""
        feedback_parts = []

        # Score-based feedback
        percentage = (response.marks_awarded / auto_marker.max_marks) * 100

        if percentage >= 90:
            feedback_parts.append(
                "Excellent response! Your answer demonstrates strong understanding."
            )
        elif percentage >= 70:
            feedback_parts.append(
                "Good response with solid understanding of the key concepts."
            )
        elif percentage >= 50:
            feedback_parts.append(
                "Satisfactory response. Consider expanding on key points."
            )
        else:
            feedback_parts.append(
                "Your response needs improvement. Review the model answer."
            )

        # Keyword feedback
        if response.missing_keywords:
            feedback_parts.append(
                f"Missing key concepts: {', '.join(response.missing_keywords[:3])}"
            )

        # Similarity feedback
        if response.similarity_score < 0.6:
            feedback_parts.append(
                "Try to align your response more closely with the expected answer structure."
            )

        # Length feedback
        model_length = len(auto_marker.model_answer.split())
        response_length = response.word_count
        if response_length < model_length * 0.5:
            feedback_parts.append("Consider providing more detail in your answer.")

        return " ".join(feedback_parts)

    @action(detail=True, methods=["get"])
    def statistics(self, request, tenant_slug=None, pk=None):
        """Get detailed statistics for this auto-marker"""
        auto_marker = self.get_object()
        stats = auto_marker.get_marking_statistics()

        # Add distribution data
        responses = auto_marker.responses.filter(status="marked")

        # Score distribution
        score_ranges = [
            (0, 0.3, "Low"),
            (0.3, 0.6, "Medium"),
            (0.6, 0.8, "Good"),
            (0.8, 1.0, "Excellent"),
        ]

        score_distribution = []
        for min_score, max_score, label in score_ranges:
            count = responses.filter(
                similarity_score__gte=min_score, similarity_score__lt=max_score
            ).count()
            score_distribution.append(
                {
                    "range": label,
                    "count": count,
                    "percentage": (
                        (count / responses.count() * 100)
                        if responses.count() > 0
                        else 0
                    ),
                }
            )

        stats["score_distribution"] = score_distribution
        stats["recent_responses"] = MarkedResponseListSerializer(
            responses.order_by("-marked_at")[:10], many=True
        ).data

        return Response(stats)


class MarkedResponseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing marked responses
    """

    def get_queryset(self):
        tenant = self.kwargs.get("tenant_slug")
        queryset = MarkedResponse.objects.filter(auto_marker__tenant=tenant)

        # Filter by auto-marker
        marker_id = self.request.query_params.get("marker")
        if marker_id:
            queryset = queryset.filter(auto_marker_id=marker_id)

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by review flag
        needs_review = self.request.query_params.get("needs_review")
        if needs_review == "true":
            queryset = queryset.filter(requires_review=True)

        # Filter by student
        student_id = self.request.query_params.get("student_id")
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset.select_related("auto_marker", "reviewed_by").prefetch_related(
            "criterion_scores"
        )

    def get_serializer_class(self):
        if self.action == "list":
            return MarkedResponseListSerializer
        return MarkedResponseDetailSerializer

    @action(detail=True, methods=["post"])
    def review(self, request, tenant_slug=None, pk=None):
        """Review and potentially adjust a marked response"""
        response = self.get_object()

        original_marks = response.marks_awarded
        new_marks = request.data.get("marks_awarded")
        reviewer_notes = request.data.get("reviewer_notes", "")

        if new_marks is not None:
            response.marks_awarded = float(new_marks)

        response.reviewer_notes = reviewer_notes
        response.reviewed_by = request.user
        response.reviewed_at = timezone.now()
        response.status = "reviewed"
        response.requires_review = False
        response.save()

        # Create log
        MarkingLog.objects.create(
            auto_marker=response.auto_marker,
            response=response,
            action="review_mark",
            performed_by=request.user,
            similarity_model=response.auto_marker.similarity_model,
            responses_processed=1,
            total_time=0,
            original_score=original_marks,
            new_score=response.marks_awarded,
            adjustment_reason=reviewer_notes,
        )

        serializer = self.get_serializer(response)
        return Response(serializer.data)


class MarkingCriterionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing marking criteria
    """

    serializer_class = MarkingCriterionSerializer

    def get_queryset(self):
        tenant = self.kwargs.get("tenant_slug")
        queryset = MarkingCriterion.objects.filter(auto_marker__tenant=tenant)

        # Filter by auto-marker
        marker_id = self.request.query_params.get("marker")
        if marker_id:
            queryset = queryset.filter(auto_marker_id=marker_id)

        return queryset

    def perform_create(self, serializer):
        marker_id = self.request.data.get("auto_marker")
        auto_marker = AutoMarker.objects.get(id=marker_id)

        # Ensure tenant matches
        tenant = self.kwargs.get("tenant_slug")
        if auto_marker.tenant != tenant:
            raise ValueError("Marker does not belong to this tenant")

        serializer.save(auto_marker=auto_marker)


class MarkingLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing marking logs
    """

    serializer_class = MarkingLogSerializer

    def get_queryset(self):
        tenant = self.kwargs.get("tenant_slug")
        queryset = MarkingLog.objects.filter(auto_marker__tenant=tenant)

        # Filter by auto-marker
        marker_id = self.request.query_params.get("marker")
        if marker_id:
            queryset = queryset.filter(auto_marker_id=marker_id)

        # Filter by action
        action = self.request.query_params.get("action")
        if action:
            queryset = queryset.filter(action=action)

        return queryset.select_related("auto_marker", "response", "performed_by")
