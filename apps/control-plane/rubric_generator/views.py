from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
import time
import re

from .models import Rubric, RubricCriterion, RubricLevel, RubricGenerationLog
from .serializers import (
    RubricSerializer,
    RubricDetailSerializer,
    RubricCriterionSerializer,
    RubricLevelSerializer,
    RubricGenerationRequestSerializer,
    DashboardStatsSerializer,
)
from assessment_builder.models import Assessment, AssessmentTask


class RubricViewSet(viewsets.ModelViewSet):
    serializer_class = RubricSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        queryset = Rubric.objects.filter(tenant=tenant)

        # Filters
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        rubric_type = self.request.query_params.get("rubric_type")
        if rubric_type:
            queryset = queryset.filter(rubric_type=rubric_type)

        assessment_id = self.request.query_params.get("assessment")
        if assessment_id:
            queryset = queryset.filter(assessment_id=assessment_id)

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RubricDetailSerializer
        return RubricSerializer

    @action(detail=False, methods=["post"])
    def generate_rubric(self, request):
        """
        Generate rubric using NLP summarization and taxonomy tagging
        """
        serializer = RubricGenerationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Get assessment or task
        assessment = None
        task = None

        if data.get("assessment_id"):
            try:
                assessment = Assessment.objects.get(
                    id=data["assessment_id"], tenant=request.tenant
                )
            except Assessment.DoesNotExist:
                return Response(
                    {"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND
                )

        if data.get("task_id"):
            try:
                task = AssessmentTask.objects.get(
                    id=data["task_id"], assessment__tenant=request.tenant
                )
                assessment = task.assessment
            except AssessmentTask.DoesNotExist:
                return Response(
                    {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
                )

        # Generate title if not provided
        title = data.get("title")
        if not title:
            if task:
                title = f"Rubric for {task.task_number}: {task.question[:50]}"
            elif assessment:
                title = f"Rubric for {assessment.unit_code} - {assessment.title}"

        # Create rubric record
        rubric = Rubric.objects.create(
            tenant=request.tenant,
            title=title,
            rubric_type=data["rubric_type"],
            assessment=assessment,
            task=task,
            total_points=data["total_points"],
            passing_score=int(data["total_points"] * 0.5),  # 50% default
            status="generating",
            created_by=request.user,
        )

        start_time = time.time()

        try:
            # Generate rubric content
            generation_result = self._generate_with_nlp(
                rubric,
                assessment,
                task,
                data["number_of_criteria"],
                data["number_of_levels"],
                data["include_examples"],
                data["enable_nlp_summary"],
                data["enable_taxonomy_tagging"],
            )

            generation_time = time.time() - start_time

            # Update rubric with generated content
            rubric.description = generation_result["description"]
            rubric.ai_generated = True
            rubric.ai_model = "GPT-4 + NLP (Mock)"
            rubric.ai_generation_time = generation_time
            rubric.ai_generated_at = timezone.now()

            if data["enable_nlp_summary"]:
                rubric.nlp_summary = generation_result["nlp_summary"]
                rubric.nlp_key_points = generation_result["nlp_key_points"]

            if data["enable_taxonomy_tagging"]:
                rubric.taxonomy_tags = generation_result["taxonomy_tags"]
                rubric.blooms_levels = generation_result["blooms_levels"]

            rubric.status = "review"
            rubric.save()

            # Create criteria and levels
            for i, criterion_data in enumerate(generation_result["criteria"], 1):
                criterion = RubricCriterion.objects.create(
                    rubric=rubric,
                    criterion_number=str(i),
                    title=criterion_data["title"],
                    description=criterion_data["description"],
                    weight=criterion_data["weight"],
                    max_points=criterion_data["max_points"],
                    maps_to_elements=criterion_data.get("maps_to_elements", []),
                    maps_to_performance_criteria=criterion_data.get(
                        "maps_to_performance_criteria", []
                    ),
                    taxonomy_tags=criterion_data.get("taxonomy_tags", []),
                    blooms_level=criterion_data.get("blooms_level", ""),
                    ai_generated=True,
                    ai_rationale=criterion_data.get("rationale", ""),
                    nlp_keywords=criterion_data.get("nlp_keywords", []),
                    display_order=i,
                )

                # Create performance levels for this criterion
                for level_data in criterion_data["levels"]:
                    RubricLevel.objects.create(
                        criterion=criterion,
                        level_name=level_data["name"],
                        level_type=level_data["type"],
                        points=level_data["points"],
                        description=level_data["description"],
                        indicators=level_data.get("indicators", []),
                        examples=level_data.get("examples", ""),
                        ai_generated=True,
                        nlp_summary=level_data.get("nlp_summary", ""),
                        display_order=level_data["order"],
                    )

            # Create generation log
            RubricGenerationLog.objects.create(
                rubric=rubric,
                action="generate_full",
                ai_model="GPT-4 + NLP (Mock)",
                nlp_model="spaCy + NLTK (Mock)",
                prompt_used=generation_result.get("prompt", ""),
                tokens_used=generation_result.get("tokens", 0),
                generation_time=generation_time,
                success=True,
                performed_by=request.user,
            )

            serializer = RubricDetailSerializer(rubric)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            rubric.status = "draft"
            rubric.save()

            RubricGenerationLog.objects.create(
                rubric=rubric,
                action="generate_full",
                ai_model="GPT-4 + NLP (Mock)",
                generation_time=time.time() - start_time,
                success=False,
                error_message=str(e),
                performed_by=request.user,
            )

            return Response(
                {"error": f"Rubric generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _generate_with_nlp(
        self,
        rubric,
        assessment,
        task,
        num_criteria,
        num_levels,
        include_examples,
        enable_nlp,
        enable_taxonomy,
    ):
        """
        Mock NLP-based rubric generation
        In production, this would use actual NLP libraries (spaCy, NLTK) and GPT-4
        """
        # Gather context
        context = []
        if assessment:
            context.append(f"Unit: {assessment.unit_code} - {assessment.unit_title}")
            if assessment.elements_covered:
                context.extend(assessment.elements_covered)

        if task:
            context.append(f"Task: {task.question}")

        # Generate description
        description = f"""
This rubric provides a structured marking guide for assessing student performance.
It uses {num_levels} performance levels across {num_criteria} key criteria to ensure
consistent, transparent, and fair assessment.
""".strip()

        # NLP Summarization (mock)
        nlp_summary = ""
        nlp_key_points = []
        if enable_nlp:
            nlp_summary = self._generate_nlp_summary(context, num_criteria)
            nlp_key_points = self._extract_key_points(context)

        # Taxonomy tagging (mock)
        taxonomy_tags = []
        blooms_levels = {}
        if enable_taxonomy:
            taxonomy_tags = self._generate_taxonomy_tags(assessment, task)
            blooms_levels = self._calculate_blooms_distribution(num_criteria)

        # Generate criteria
        criteria = []
        points_per_criterion = rubric.total_points // num_criteria

        # Define performance levels
        level_definitions = self._get_performance_levels(
            num_levels, points_per_criterion
        )

        # Generate criteria based on context
        criterion_templates = self._get_criterion_templates(
            assessment, task, num_criteria
        )

        for i, template in enumerate(criterion_templates[:num_criteria]):
            criterion_data = {
                "title": template["title"],
                "description": template["description"],
                "weight": 1,
                "max_points": points_per_criterion,
                "maps_to_elements": (
                    assessment.elements_covered[:1]
                    if assessment and assessment.elements_covered
                    else []
                ),
                "maps_to_performance_criteria": (
                    assessment.performance_criteria_covered[:2]
                    if assessment and assessment.performance_criteria_covered
                    else []
                ),
                "taxonomy_tags": template.get("taxonomy_tags", []),
                "blooms_level": template.get("blooms_level", ""),
                "rationale": template.get("rationale", ""),
                "nlp_keywords": template.get("nlp_keywords", []),
                "levels": [],
            }

            # Add performance levels for this criterion
            for level_def in level_definitions:
                level_data = {
                    "name": level_def["name"],
                    "type": level_def["type"],
                    "points": level_def["points"],
                    "description": self._customize_level_description(
                        template["title"], level_def["template"]
                    ),
                    "indicators": level_def.get("indicators", []),
                    "examples": (
                        level_def.get("example_template", "")
                        if include_examples
                        else ""
                    ),
                    "nlp_summary": level_def.get("nlp_summary", ""),
                    "order": level_def["order"],
                }
                criterion_data["levels"].append(level_data)

            criteria.append(criterion_data)

        return {
            "description": description,
            "nlp_summary": nlp_summary,
            "nlp_key_points": nlp_key_points,
            "taxonomy_tags": taxonomy_tags,
            "blooms_levels": blooms_levels,
            "criteria": criteria,
            "prompt": f'Generate rubric for {assessment.unit_code if assessment else "task"}',
            "tokens": 2000,
        }

    def _generate_nlp_summary(self, context, num_criteria):
        """Generate NLP summary of rubric purpose"""
        summary = f"""
This rubric assesses {num_criteria} key competency areas. It provides clear performance 
descriptors to guide both assessors and students. The criteria are designed to measure 
achievement of learning outcomes through observable indicators.
""".strip()
        return summary

    def _extract_key_points(self, context):
        """Extract key points using NLP (mock)"""
        # In production, use spaCy or NLTK for actual extraction
        return [
            "Clear performance descriptors",
            "Observable assessment criteria",
            "Aligned to unit requirements",
            "Multiple performance levels",
            "Consistent marking standards",
        ]

    def _generate_taxonomy_tags(self, assessment, task):
        """Generate educational taxonomy tags"""
        tags = ["Bloom's Taxonomy", "Competency-Based"]

        if assessment and assessment.blooms_distribution:
            # Add dominant Bloom's level
            blooms_dist = assessment.blooms_distribution
            if blooms_dist:
                dominant = max(blooms_dist, key=blooms_dist.get)
                tags.append(f"Bloom's: {dominant.capitalize()}")

        if task and task.blooms_level:
            tags.append(f"Bloom's: {task.blooms_level.capitalize()}")

        tags.extend(["SOLO Taxonomy", "RTO Compliance"])

        return tags

    def _calculate_blooms_distribution(self, num_criteria):
        """Calculate mock Bloom's distribution across criteria"""
        # Distribute criteria across Bloom's levels
        levels = ["remember", "understand", "apply", "analyze", "evaluate", "create"]
        distribution = {}

        for i, level in enumerate(levels):
            # Simple distribution: higher levels get fewer criteria
            weight = max(1, num_criteria - i)
            distribution[level] = round(
                (weight / sum(range(1, num_criteria + 1))) * 100, 1
            )

        return distribution

    def _get_performance_levels(self, num_levels, max_points):
        """Define performance level structure"""
        if num_levels == 4:
            return [
                {
                    "name": "Exemplary",
                    "type": "exemplary",
                    "points": max_points,
                    "template": "Exceeds expectations with exceptional quality",
                    "indicators": [
                        "Comprehensive coverage",
                        "Deep understanding",
                        "Innovation demonstrated",
                    ],
                    "nlp_summary": "Exceptional performance beyond requirements",
                    "order": 1,
                },
                {
                    "name": "Proficient",
                    "type": "proficient",
                    "points": int(max_points * 0.75),
                    "template": "Meets all expectations with good quality",
                    "indicators": [
                        "Complete coverage",
                        "Clear understanding",
                        "Competent application",
                    ],
                    "nlp_summary": "Solid performance meeting all requirements",
                    "order": 2,
                },
                {
                    "name": "Developing",
                    "type": "developing",
                    "points": int(max_points * 0.5),
                    "template": "Partially meets expectations, needs improvement",
                    "indicators": [
                        "Partial coverage",
                        "Basic understanding",
                        "Some gaps",
                    ],
                    "nlp_summary": "Adequate but incomplete performance",
                    "order": 3,
                },
                {
                    "name": "Unsatisfactory",
                    "type": "unsatisfactory",
                    "points": 0,
                    "template": "Does not meet expectations",
                    "indicators": [
                        "Minimal coverage",
                        "Limited understanding",
                        "Significant gaps",
                    ],
                    "nlp_summary": "Performance below acceptable standards",
                    "order": 4,
                },
            ]
        elif num_levels == 5:
            return [
                {
                    "name": "Exemplary",
                    "type": "exemplary",
                    "points": max_points,
                    "template": "Outstanding performance",
                    "order": 1,
                },
                {
                    "name": "Proficient",
                    "type": "proficient",
                    "points": int(max_points * 0.8),
                    "template": "Strong performance",
                    "order": 2,
                },
                {
                    "name": "Competent",
                    "type": "competent",
                    "points": int(max_points * 0.6),
                    "template": "Satisfactory performance",
                    "order": 3,
                },
                {
                    "name": "Developing",
                    "type": "developing",
                    "points": int(max_points * 0.4),
                    "template": "Needs improvement",
                    "order": 4,
                },
                {
                    "name": "Unsatisfactory",
                    "type": "unsatisfactory",
                    "points": 0,
                    "template": "Below standard",
                    "order": 5,
                },
            ]
        else:
            # Default 3 levels
            return [
                {
                    "name": "Proficient",
                    "type": "proficient",
                    "points": max_points,
                    "template": "Meets all requirements",
                    "order": 1,
                },
                {
                    "name": "Developing",
                    "type": "developing",
                    "points": int(max_points * 0.5),
                    "template": "Partially meets requirements",
                    "order": 2,
                },
                {
                    "name": "Unsatisfactory",
                    "type": "unsatisfactory",
                    "points": 0,
                    "template": "Does not meet requirements",
                    "order": 3,
                },
            ]

    def _get_criterion_templates(self, assessment, task, num_criteria):
        """Generate criterion templates based on context"""
        templates = [
            {
                "title": "Knowledge and Understanding",
                "description": "Demonstrates knowledge of key concepts and principles",
                "blooms_level": "understand",
                "taxonomy_tags": ["Bloom's: Understand", "Knowledge"],
                "nlp_keywords": [
                    "knowledge",
                    "understanding",
                    "concepts",
                    "principles",
                ],
                "rationale": "Assesses foundational knowledge required for competency",
            },
            {
                "title": "Application of Skills",
                "description": "Applies knowledge to practical situations",
                "blooms_level": "apply",
                "taxonomy_tags": ["Bloom's: Apply", "Skills"],
                "nlp_keywords": ["apply", "practical", "skills", "demonstrate"],
                "rationale": "Evaluates ability to use knowledge in context",
            },
            {
                "title": "Analysis and Problem Solving",
                "description": "Analyzes situations and develops solutions",
                "blooms_level": "analyze",
                "taxonomy_tags": ["Bloom's: Analyze", "Problem Solving"],
                "nlp_keywords": ["analyze", "problem", "solution", "critical thinking"],
                "rationale": "Measures analytical and problem-solving capabilities",
            },
            {
                "title": "Quality and Accuracy",
                "description": "Produces work that is accurate and meets quality standards",
                "blooms_level": "evaluate",
                "taxonomy_tags": ["Bloom's: Evaluate", "Quality"],
                "nlp_keywords": ["quality", "accuracy", "standards", "precision"],
                "rationale": "Assesses attention to detail and quality standards",
            },
            {
                "title": "Communication and Presentation",
                "description": "Communicates ideas clearly and professionally",
                "blooms_level": "create",
                "taxonomy_tags": ["Bloom's: Create", "Communication"],
                "nlp_keywords": [
                    "communication",
                    "presentation",
                    "clarity",
                    "professional",
                ],
                "rationale": "Evaluates communication effectiveness",
            },
        ]

        # Extend if more criteria needed
        while len(templates) < num_criteria:
            templates.append(
                {
                    "title": f"Additional Criterion {len(templates) + 1}",
                    "description": "Additional assessment criterion",
                    "blooms_level": "apply",
                    "taxonomy_tags": ["General Competency"],
                    "nlp_keywords": ["competency", "performance"],
                    "rationale": "Supplementary assessment criterion",
                }
            )

        return templates

    def _customize_level_description(self, criterion_title, level_template):
        """Customize level description based on criterion"""
        return f"{criterion_title}: {level_template}"

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """Approve rubric for publishing"""
        rubric = self.get_object()

        rubric.status = "approved"
        rubric.approved_by = request.user
        rubric.approved_at = timezone.now()
        rubric.save()

        serializer = self.get_serializer(rubric)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def dashboard_stats(self, request):
        """Get dashboard statistics"""
        tenant = request.tenant
        thirty_days_ago = timezone.now() - timedelta(days=30)

        rubrics = Rubric.objects.filter(tenant=tenant)
        recent = rubrics.filter(created_at__gte=thirty_days_ago)

        # Calculate taxonomy distribution
        all_tags = []
        for rubric in rubrics:
            all_tags.extend(rubric.taxonomy_tags or [])

        from collections import Counter

        tag_counts = Counter(all_tags)
        total_tags = sum(tag_counts.values())
        taxonomy_distribution = (
            {
                tag: round((count / total_tags) * 100, 1)
                for tag, count in tag_counts.items()
            }
            if total_tags > 0
            else {}
        )

        stats = {
            "total_rubrics": rubrics.count(),
            "by_status": dict(
                rubrics.values("status")
                .annotate(count=Count("id"))
                .values_list("status", "count")
            ),
            "by_type": dict(
                rubrics.values("rubric_type")
                .annotate(count=Count("id"))
                .values_list("rubric_type", "count")
            ),
            "ai_generated_count": rubrics.filter(ai_generated=True).count(),
            "ai_generation_rate": 0.0,
            "avg_criteria_per_rubric": 0.0,
            "taxonomy_distribution": taxonomy_distribution,
            "recent_rubrics": recent.count(),
        }

        if stats["total_rubrics"] > 0:
            stats["ai_generation_rate"] = round(
                (stats["ai_generated_count"] / stats["total_rubrics"]) * 100, 1
            )

            # Calculate average criteria
            total_criteria = sum(r.get_criterion_count() for r in rubrics)
            stats["avg_criteria_per_rubric"] = round(
                total_criteria / stats["total_rubrics"], 1
            )

        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)


class RubricCriterionViewSet(viewsets.ModelViewSet):
    serializer_class = RubricCriterionSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        queryset = RubricCriterion.objects.filter(rubric__tenant=tenant)

        rubric_id = self.request.query_params.get("rubric")
        if rubric_id:
            queryset = queryset.filter(rubric_id=rubric_id)

        return queryset


class RubricLevelViewSet(viewsets.ModelViewSet):
    serializer_class = RubricLevelSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        queryset = RubricLevel.objects.filter(criterion__rubric__tenant=tenant)

        criterion_id = self.request.query_params.get("criterion")
        if criterion_id:
            queryset = queryset.filter(criterion_id=criterion_id)

        return queryset
