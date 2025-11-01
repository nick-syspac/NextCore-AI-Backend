from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
from datetime import datetime
import random
import math

from .models import (
    EvidenceMapping,
    SubmissionEvidence,
    CriteriaTag,
    EvidenceAudit,
    EmbeddingSearch,
)
from .serializers import (
    EvidenceMappingSerializer,
    SubmissionEvidenceSerializer,
    SubmissionEvidenceDetailSerializer,
    CriteriaTagSerializer,
    EvidenceAuditSerializer,
    EmbeddingSearchSerializer,
    TagEvidenceRequestSerializer,
    ExtractTextRequestSerializer,
    SearchEmbeddingsRequestSerializer,
)


class EvidenceMappingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing evidence mappings with coverage tracking.
    """

    queryset = EvidenceMapping.objects.all()
    serializer_class = EvidenceMappingSerializer

    @action(detail=True, methods=["get"])
    def coverage_report(self, request, pk=None):
        """
        Generate coverage report showing criteria with/without evidence.
        """
        mapping = self.get_object()

        # Get all unique criteria that have evidence
        criteria_with_evidence = (
            CriteriaTag.objects.filter(evidence__mapping=mapping)
            .values("criterion_id", "criterion_name")
            .annotate(tag_count=models.Count("id"))
            .order_by("criterion_id")
        )

        # Calculate statistics
        total_tags = CriteriaTag.objects.filter(evidence__mapping=mapping).count()
        validated_tags = CriteriaTag.objects.filter(
            evidence__mapping=mapping, is_validated=True
        ).count()

        coverage_data = {
            "mapping_id": mapping.id,
            "mapping_number": mapping.mapping_number,
            "total_criteria": mapping.total_criteria,
            "criteria_with_evidence": len(criteria_with_evidence),
            "coverage_percentage": mapping.calculate_coverage(),
            "total_tags": total_tags,
            "validated_tags": validated_tags,
            "validation_rate": (
                (validated_tags / total_tags * 100) if total_tags > 0 else 0
            ),
            "criteria_breakdown": list(criteria_with_evidence),
        }

        return Response(coverage_data)


class SubmissionEvidenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing submission evidence with text extraction and embedding generation.
    """

    queryset = SubmissionEvidence.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SubmissionEvidenceDetailSerializer
        return SubmissionEvidenceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        mapping_id = self.request.query_params.get("mapping_id")
        if mapping_id:
            queryset = queryset.filter(mapping_id=mapping_id)
        return queryset

    @action(detail=True, methods=["post"])
    def extract_text(self, request, pk=None):
        """
        Extract text from submission and optionally generate embeddings.
        """
        submission = self.get_object()
        serializer = ExtractTextRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        extraction_method = serializer.validated_data.get("extraction_method", "mock")
        generate_embedding = serializer.validated_data.get("generate_embedding", True)

        start_time = datetime.now()

        # Mock text extraction (in production, use actual OCR/parser)
        if not submission.extracted_text:
            mock_paragraphs = [
                "This assignment demonstrates a comprehensive understanding of the key concepts covered in the unit.",
                "The research methodology employed follows industry best practices and shows critical thinking.",
                "Evidence of practical application is clearly presented through detailed case studies.",
                "The analysis incorporates relevant theoretical frameworks and demonstrates synthesis of multiple sources.",
                "Recommendations are well-justified and aligned with the findings presented throughout the document.",
                "The conclusion effectively summarizes the key learnings and their practical implications.",
            ]

            submission.extracted_text = "\n\n".join(
                random.sample(mock_paragraphs, k=random.randint(3, 6))
            )
            submission.text_length = len(submission.extracted_text)
            submission.extraction_status = "completed"
            submission.extraction_method = extraction_method
            submission.extracted_at = timezone.now()

            # Mock metadata extraction
            submission.metadata = {
                "language": "en",
                "readability_score": random.randint(60, 90),
                "word_count": len(submission.extracted_text.split()),
                "sentence_count": submission.extracted_text.count("."),
                "keywords": ["analysis", "methodology", "evidence", "research"],
            }

        # Generate mock embedding (in production, use sentence-transformers or similar)
        if generate_embedding and not submission.text_embedding:
            embedding_dimension = 384
            submission.text_embedding = [
                random.random() for _ in range(embedding_dimension)
            ]
            submission.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
            submission.embedding_dimension = embedding_dimension

            # Update mapping statistics
            submission.mapping.embeddings_generated += 1
            submission.mapping.save()

        submission.save()

        # Update mapping statistics
        submission.mapping.total_text_extracted += 1
        submission.mapping.save()

        # Log extraction
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        EvidenceAudit.objects.create(
            mapping=submission.mapping,
            action="text_extracted",
            description=f"Extracted text from submission {submission.evidence_number}",
            submission_id=submission.submission_id,
            action_data={
                "text_length": submission.text_length,
                "extraction_method": extraction_method,
                "embedding_generated": generate_embedding,
            },
            processing_time_ms=int(processing_time),
            performed_by=(
                request.user.username if request.user.is_authenticated else "system"
            ),
        )

        return Response(
            {
                "status": "success",
                "extracted_text_length": submission.text_length,
                "embedding_generated": bool(submission.text_embedding),
                "embedding_dimension": submission.embedding_dimension,
                "metadata": submission.metadata,
            }
        )

    @action(detail=True, methods=["post"])
    def tag_evidence(self, request, pk=None):
        """
        Tag specific text excerpt to a criterion.
        """
        submission = self.get_object()
        serializer = TagEvidenceRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # Extract context (100 chars before and after)
        context_size = 100
        start_pos = data["text_start_position"]
        end_pos = data["text_end_position"]

        context_before = submission.extracted_text[
            max(0, start_pos - context_size) : start_pos
        ]
        context_after = submission.extracted_text[
            end_pos : min(len(submission.extracted_text), end_pos + context_size)
        ]

        # Extract keywords from tagged text
        tagged_words = data["tagged_text"].lower().split()
        common_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
        }
        keywords = [
            word for word in tagged_words if len(word) > 3 and word not in common_words
        ][:10]

        # Create tag
        tag = CriteriaTag.objects.create(
            evidence=submission,
            criterion_id=data["criterion_id"],
            criterion_name=data["criterion_name"],
            criterion_description=data.get("criterion_description", ""),
            tagged_text=data["tagged_text"],
            text_start_position=start_pos,
            text_end_position=end_pos,
            context_before=context_before,
            context_after=context_after,
            tag_type=data.get("tag_type", "direct"),
            confidence_level="manual",
            confidence_score=1.0,
            notes=data.get("notes", ""),
            keywords=keywords,
            tagged_by=data["tagged_by"],
        )

        # Update submission statistics
        submission.total_tags += 1
        if data["criterion_id"] not in submission.criteria_covered:
            submission.criteria_covered.append(data["criterion_id"])
        submission.save()

        # Update mapping statistics
        submission.mapping.total_evidence_tagged += 1
        submission.mapping.coverage_percentage = submission.mapping.calculate_coverage()
        submission.mapping.save()

        # Log tagging
        EvidenceAudit.objects.create(
            mapping=submission.mapping,
            action="evidence_tagged",
            description=f"Tagged evidence for criterion {data['criterion_id']}",
            submission_id=submission.submission_id,
            criterion_id=data["criterion_id"],
            tag_id=tag.id,
            action_data={
                "tag_number": tag.tag_number,
                "tag_type": tag.tag_type,
                "text_length": len(data["tagged_text"]),
            },
            performed_by=data["tagged_by"],
        )

        return Response(CriteriaTagSerializer(tag).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def search_embeddings(self, request):
        """
        Search submissions using embedding similarity.
        """
        serializer = SearchEmbeddingsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data["query"]
        search_type = serializer.validated_data["search_type"]
        limit = serializer.validated_data["limit"]
        min_similarity = serializer.validated_data["min_similarity"]

        start_time = datetime.now()

        # Generate query embedding (mock)
        query_embedding = [random.random() for _ in range(384)]

        # Get all submissions with embeddings
        submissions = SubmissionEvidence.objects.exclude(text_embedding=[])

        # Calculate cosine similarity (mock implementation)
        results = []
        for submission in submissions:
            if submission.text_embedding:
                # Mock similarity score
                similarity = random.uniform(0.3, 0.95)

                if similarity >= min_similarity:
                    results.append(
                        {
                            "submission_id": submission.id,
                            "evidence_number": submission.evidence_number,
                            "student_id": submission.student_id,
                            "student_name": submission.student_name,
                            "similarity_score": round(similarity, 3),
                            "text_preview": (
                                submission.extracted_text[:200] + "..."
                                if len(submission.extracted_text) > 200
                                else submission.extracted_text
                            ),
                            "total_tags": submission.total_tags,
                        }
                    )

        # Sort by similarity and limit
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        results = results[:limit]

        # Log search
        search_time = (datetime.now() - start_time).total_seconds() * 1000

        mapping_id = request.query_params.get("mapping_id")
        if mapping_id:
            try:
                mapping = EvidenceMapping.objects.get(id=mapping_id)
                EmbeddingSearch.objects.create(
                    mapping=mapping,
                    search_type=search_type,
                    query_text=query,
                    query_embedding=query_embedding,
                    results_count=len(results),
                    top_results=results[:5],
                    search_time_ms=int(search_time),
                    performed_by=(
                        request.user.username
                        if request.user.is_authenticated
                        else "anonymous"
                    ),
                )
            except EvidenceMapping.DoesNotExist:
                pass

        return Response(
            {
                "query": query,
                "search_type": search_type,
                "results_count": len(results),
                "search_time_ms": int(search_time),
                "results": results,
            }
        )


class CriteriaTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing criteria tags.
    """

    queryset = CriteriaTag.objects.all()
    serializer_class = CriteriaTagSerializer

    @action(detail=True, methods=["post"])
    def validate_tag(self, request, pk=None):
        """Validate a criteria tag."""
        tag = self.get_object()
        tag.is_validated = True
        tag.validated_by = request.data.get("validated_by", "system")
        tag.validated_at = timezone.now()
        tag.save()

        # Log validation
        EvidenceAudit.objects.create(
            mapping=tag.evidence.mapping,
            action="tag_validated",
            description=f"Validated tag {tag.tag_number}",
            submission_id=tag.evidence.submission_id,
            criterion_id=tag.criterion_id,
            tag_id=tag.id,
            performed_by=tag.validated_by,
        )

        return Response(CriteriaTagSerializer(tag).data)


class EvidenceAuditViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing evidence audit logs (read-only).
    """

    queryset = EvidenceAudit.objects.all()
    serializer_class = EvidenceAuditSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        mapping_id = self.request.query_params.get("mapping_id")
        if mapping_id:
            queryset = queryset.filter(mapping_id=mapping_id)
        return queryset


class EmbeddingSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing embedding search logs (read-only).
    """

    queryset = EmbeddingSearch.objects.all()
    serializer_class = EmbeddingSearchSerializer
