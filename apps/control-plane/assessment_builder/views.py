from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
import re
import time

from .models import (
    Assessment,
    AssessmentTask,
    AssessmentCriteria,
    AssessmentGenerationLog,
)
from .serializers import (
    AssessmentSerializer,
    AssessmentDetailSerializer,
    AssessmentTaskSerializer,
    AssessmentCriteriaSerializer,
    AssessmentGenerationRequestSerializer,
    DashboardStatsSerializer,
)


class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        queryset = Assessment.objects.filter(tenant=tenant)

        # Filters
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        assessment_type = self.request.query_params.get("assessment_type")
        if assessment_type:
            queryset = queryset.filter(assessment_type=assessment_type)

        unit_code = self.request.query_params.get("unit_code")
        if unit_code:
            queryset = queryset.filter(unit_code__icontains=unit_code)

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AssessmentDetailSerializer
        return AssessmentSerializer

    @action(detail=False, methods=["post"])
    def generate_assessment(self, request):
        """
        Generate assessment using GPT-4 from unit code
        """
        serializer = AssessmentGenerationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Create assessment record
        assessment = Assessment.objects.create(
            tenant=request.tenant,
            unit_code=data["unit_code"],
            unit_title=data["unit_title"],
            training_package=data.get("training_package", ""),
            assessment_type=data["assessment_type"],
            title=f"{data['unit_title']} - Assessment",
            status="generating",
            created_by=request.user,
            elements_covered=data.get("elements", []),
            performance_criteria_covered=data.get("performance_criteria", []),
            knowledge_evidence_covered=data.get("knowledge_evidence", []),
            performance_evidence_covered=data.get("performance_evidence", []),
        )

        start_time = time.time()

        try:
            # Generate assessment content with mock GPT-4
            generation_result = self._generate_with_ai(
                assessment, data["number_of_tasks"], data.get("include_context", True)
            )

            generation_time = time.time() - start_time

            # Update assessment with generated content
            assessment.instructions = generation_result["instructions"]
            assessment.context = generation_result["context"]
            assessment.conditions = generation_result["conditions"]
            assessment.ai_generated = True
            assessment.ai_model = "GPT-4 (Mock)"
            assessment.ai_generation_time = generation_time
            assessment.ai_generated_at = timezone.now()
            assessment.status = "review"
            assessment.save()

            # Create tasks
            for i, task_data in enumerate(generation_result["tasks"], 1):
                task = AssessmentTask.objects.create(
                    assessment=assessment,
                    task_number=str(i),
                    task_type=task_data["type"],
                    question=task_data["question"],
                    context=task_data.get("context", ""),
                    ai_generated=True,
                    ai_rationale=task_data.get("rationale", ""),
                    blooms_level=task_data["blooms_level"],
                    blooms_verbs=task_data["blooms_verbs"],
                    maps_to_elements=task_data.get("maps_to_elements", []),
                    maps_to_performance_criteria=task_data.get(
                        "maps_to_performance_criteria", []
                    ),
                    question_count=1,
                    estimated_time_minutes=task_data.get("estimated_time", 10),
                    display_order=i,
                )

            # Analyze Bloom's taxonomy for entire assessment
            blooms_dist = assessment.calculate_blooms_distribution()
            assessment.blooms_distribution = blooms_dist
            if blooms_dist:
                assessment.dominant_blooms_level = max(blooms_dist, key=blooms_dist.get)
            assessment.save()

            # Create generation log
            AssessmentGenerationLog.objects.create(
                assessment=assessment,
                action="generate_full",
                ai_model="GPT-4 (Mock)",
                prompt_used=generation_result.get("prompt", ""),
                tokens_used=generation_result.get("tokens", 0),
                generation_time=generation_time,
                success=True,
                performed_by=request.user,
            )

            serializer = AssessmentDetailSerializer(assessment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            assessment.status = "draft"
            assessment.save()

            AssessmentGenerationLog.objects.create(
                assessment=assessment,
                action="generate_full",
                ai_model="GPT-4 (Mock)",
                prompt_used="",
                generation_time=time.time() - start_time,
                success=False,
                error_message=str(e),
                performed_by=request.user,
            )

            return Response(
                {"error": f"Assessment generation failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _generate_with_ai(self, assessment, num_tasks, include_context):
        """
        Mock GPT-4 generation - in production, this would call OpenAI API
        """
        # Mock generation based on unit code and type
        unit_code = assessment.unit_code
        unit_title = assessment.unit_title
        assessment_type = assessment.assessment_type

        # Generate instructions
        instructions = f"""
# Assessment Instructions for {unit_code}

This assessment is designed to evaluate your competency in {unit_title}.

## Instructions to Candidates:
1. Read all questions carefully before beginning
2. Answer all questions to the best of your ability
3. Ensure responses demonstrate your knowledge and skills
4. You may refer to workplace documentation and resources
5. Ask your assessor if you need clarification

## Submission Requirements:
- Complete all tasks within the specified timeframe
- Ensure all responses are legible and clearly marked
- Submit all required evidence and documentation
"""

        # Generate context
        context = (
            f"""
This assessment covers the unit {unit_code} - {unit_title}.

You will be assessed on your ability to demonstrate the required knowledge and skills 
outlined in the unit of competency. This assessment includes a combination of questions 
and practical tasks that align with workplace requirements.
"""
            if include_context
            else ""
        )

        # Generate conditions
        conditions = """
## Assessment Conditions:
- Assessment to be conducted in a simulated or actual workplace environment
- Access to workplace documentation, policies, and resources
- Standard workplace equipment and materials
- Reasonable adjustments available for candidates with special needs
"""

        # Generate tasks with Bloom's taxonomy
        tasks = []
        blooms_levels = [
            "remember",
            "understand",
            "apply",
            "analyze",
            "evaluate",
            "create",
        ]

        # Mock task templates based on assessment type
        if assessment_type == "knowledge":
            task_types = ["short_answer", "long_answer", "multiple_choice"]
        elif assessment_type == "practical":
            task_types = ["practical", "observation", "case_study"]
        else:
            task_types = ["short_answer", "case_study", "practical"]

        for i in range(num_tasks):
            # Distribute across Bloom's levels
            blooms_level = blooms_levels[min(i % 6, 5)]
            task_type = task_types[i % len(task_types)]

            # Detect Bloom's verbs
            blooms_verbs = self._get_blooms_verbs(blooms_level)
            primary_verb = blooms_verbs[0]

            # Generate question based on Bloom's level
            question = self._generate_question(
                unit_title, primary_verb, blooms_level, i + 1
            )

            tasks.append(
                {
                    "type": task_type,
                    "question": question,
                    "context": f"This task assesses your ability to {blooms_level} concepts related to {unit_title}.",
                    "rationale": f'Generated to assess {blooms_level} level understanding using "{primary_verb}" verb',
                    "blooms_level": blooms_level,
                    "blooms_verbs": blooms_verbs[:3],  # Top 3 verbs
                    "maps_to_elements": (
                        assessment.elements_covered[:1]
                        if assessment.elements_covered
                        else []
                    ),
                    "maps_to_performance_criteria": (
                        assessment.performance_criteria_covered[:2]
                        if assessment.performance_criteria_covered
                        else []
                    ),
                    "estimated_time": (
                        10 if task_type in ["short_answer", "multiple_choice"] else 20
                    ),
                }
            )

        return {
            "instructions": instructions.strip(),
            "context": context.strip(),
            "conditions": conditions.strip(),
            "tasks": tasks,
            "prompt": f"Generate assessment for {unit_code}",
            "tokens": 1500,
        }

    def _get_blooms_verbs(self, level):
        """
        Get Bloom's taxonomy verbs for a given level
        """
        blooms_verb_map = {
            "remember": [
                "list",
                "define",
                "describe",
                "identify",
                "name",
                "recall",
                "recognize",
            ],
            "understand": [
                "explain",
                "summarize",
                "interpret",
                "classify",
                "compare",
                "discuss",
            ],
            "apply": ["apply", "demonstrate", "implement", "use", "execute", "solve"],
            "analyze": [
                "analyze",
                "differentiate",
                "examine",
                "investigate",
                "categorize",
            ],
            "evaluate": [
                "evaluate",
                "assess",
                "judge",
                "critique",
                "justify",
                "recommend",
            ],
            "create": ["create", "design", "develop", "formulate", "construct", "plan"],
        }
        return blooms_verb_map.get(level, ["describe"])

    def _generate_question(self, unit_title, verb, blooms_level, question_num):
        """
        Generate a question based on Bloom's taxonomy level
        """
        templates = {
            "remember": f"{verb.capitalize()} the key components of {unit_title}.",
            "understand": f"{verb.capitalize()} how {unit_title} principles apply in the workplace.",
            "apply": f"{verb.capitalize()} your knowledge of {unit_title} to solve a workplace scenario.",
            "analyze": f"{verb.capitalize()} the relationship between different aspects of {unit_title}.",
            "evaluate": f"{verb.capitalize()} the effectiveness of different approaches to {unit_title}.",
            "create": f"{verb.capitalize()} a plan or solution that demonstrates {unit_title} competency.",
        }

        base_question = templates.get(
            blooms_level, f"{verb.capitalize()} aspects of {unit_title}."
        )

        return f"**Question {question_num}:** {base_question}"

    @action(detail=True, methods=["post"])
    def analyze_blooms(self, request, pk=None):
        """
        Analyze Bloom's taxonomy distribution in assessment
        """
        assessment = self.get_object()

        blooms_dist = assessment.calculate_blooms_distribution()
        assessment.blooms_distribution = blooms_dist

        if blooms_dist:
            assessment.dominant_blooms_level = max(blooms_dist, key=blooms_dist.get)

        assessment.save()

        return Response(
            {
                "blooms_distribution": blooms_dist,
                "dominant_level": assessment.dominant_blooms_level,
            }
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """
        Approve assessment for publishing
        """
        assessment = self.get_object()

        assessment.status = "approved"
        assessment.approved_by = request.user
        assessment.approved_at = timezone.now()
        assessment.save()

        serializer = self.get_serializer(assessment)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def dashboard_stats(self, request):
        """
        Get dashboard statistics
        """
        tenant = request.tenant
        thirty_days_ago = timezone.now() - timedelta(days=30)

        assessments = Assessment.objects.filter(tenant=tenant)
        recent = assessments.filter(created_at__gte=thirty_days_ago)

        # Calculate Bloom's distribution across all assessments
        all_blooms = {}
        for assessment in assessments:
            if assessment.blooms_distribution:
                for level, percentage in assessment.blooms_distribution.items():
                    all_blooms[level] = all_blooms.get(level, 0) + percentage

        # Average out the distribution
        total_assessments_with_blooms = sum(
            1 for a in assessments if a.blooms_distribution
        )
        if total_assessments_with_blooms > 0:
            blooms_distribution = {
                level: round(count / total_assessments_with_blooms, 1)
                for level, count in all_blooms.items()
            }
        else:
            blooms_distribution = {}

        stats = {
            "total_assessments": assessments.count(),
            "by_status": dict(
                assessments.values("status")
                .annotate(count=Count("id"))
                .values_list("status", "count")
            ),
            "by_type": dict(
                assessments.values("assessment_type")
                .annotate(count=Count("id"))
                .values_list("assessment_type", "count")
            ),
            "ai_generated_count": assessments.filter(ai_generated=True).count(),
            "ai_generation_rate": 0.0,
            "avg_compliance_score": assessments.aggregate(avg=Avg("compliance_score"))[
                "avg"
            ]
            or 0,
            "avg_tasks_per_assessment": 0.0,
            "blooms_distribution": blooms_distribution,
            "recent_assessments": recent.count(),
        }

        if stats["total_assessments"] > 0:
            stats["ai_generation_rate"] = round(
                (stats["ai_generated_count"] / stats["total_assessments"]) * 100, 1
            )

            # Calculate average tasks
            total_tasks = sum(a.get_task_count() for a in assessments)
            stats["avg_tasks_per_assessment"] = round(
                total_tasks / stats["total_assessments"], 1
            )

        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)


class AssessmentTaskViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentTaskSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        queryset = AssessmentTask.objects.filter(assessment__tenant=tenant)

        # Filter by assessment
        assessment_id = self.request.query_params.get("assessment")
        if assessment_id:
            queryset = queryset.filter(assessment_id=assessment_id)

        return queryset


class AssessmentCriteriaViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentCriteriaSerializer

    def get_queryset(self):
        tenant = self.request.tenant
        queryset = AssessmentCriteria.objects.filter(assessment__tenant=tenant)

        # Filter by assessment
        assessment_id = self.request.query_params.get("assessment")
        if assessment_id:
            queryset = queryset.filter(assessment_id=assessment_id)

        return queryset
