from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q, Avg, F
from datetime import datetime, timedelta
import re

from .models import (
    ImprovementCategory,
    ImprovementAction,
    ActionTracking,
    ImprovementReview,
)
from .serializers import (
    ImprovementCategorySerializer,
    ImprovementActionSerializer,
    ImprovementActionDetailSerializer,
    ActionTrackingSerializer,
    ImprovementReviewSerializer,
    AIClassificationRequestSerializer,
    DashboardStatsSerializer,
)


class ImprovementCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing improvement categories
    """

    serializer_class = ImprovementCategorySerializer

    def get_queryset(self):
        tenant_id = self.kwargs.get("tenant_id")
        return ImprovementCategory.objects.filter(tenant_id=tenant_id).prefetch_related(
            "actions"
        )


class ImprovementActionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for improvement actions with AI classification and tracking
    """

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ImprovementActionDetailSerializer
        return ImprovementActionSerializer

    def get_queryset(self):
        tenant_id = self.kwargs.get("tenant_id")
        queryset = (
            ImprovementAction.objects.filter(tenant_id=tenant_id)
            .select_related(
                "category", "responsible_person", "created_by", "approved_by"
            )
            .prefetch_related("tracking_updates", "supporting_staff")
        )

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by priority
        priority_filter = self.request.query_params.get("priority")
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        # Filter by compliance
        compliance_filter = self.request.query_params.get("compliance_status")
        if compliance_filter:
            queryset = queryset.filter(compliance_status=compliance_filter)

        # Filter by category
        category_filter = self.request.query_params.get("category")
        if category_filter:
            queryset = queryset.filter(category_id=category_filter)

        # Filter overdue
        if self.request.query_params.get("overdue") == "true":
            queryset = queryset.filter(
                target_completion_date__lt=timezone.now().date(),
                status__in=["identified", "planned", "in_progress"],
            )

        return queryset

    def perform_create(self, serializer):
        tenant_id = self.kwargs.get("tenant_id")
        action = serializer.save(tenant_id=tenant_id, created_by=self.request.user)

        # Trigger AI classification if description provided
        if action.description:
            self._classify_action(action)

    @action(detail=True, methods=["post"])
    def classify(self, request, tenant_id=None, pk=None):
        """
        Trigger AI classification and summarization for an action
        """
        action = self.get_object()

        # Run AI classification
        classification_result = self._classify_action(action)

        return Response(
            {
                "message": "AI classification complete",
                "classification": classification_result,
                "action": ImprovementActionSerializer(
                    action, context={"request": request}
                ).data,
            }
        )

    @action(detail=False, methods=["post"])
    def classify_text(self, request, tenant_id=None):
        """
        Classify text without creating an action (for preview)
        """
        serializer = AIClassificationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        classification = self._classify_text(
            serializer.validated_data["description"],
            serializer.validated_data.get("title", ""),
            serializer.validated_data.get("root_cause", ""),
        )

        return Response(classification)

    @action(detail=True, methods=["post"])
    def add_tracking(self, request, tenant_id=None, pk=None):
        """
        Add a tracking update to an improvement action
        """
        action = self.get_object()

        tracking = ActionTracking.objects.create(
            improvement_action=action,
            update_type=request.data.get("update_type", "progress"),
            update_text=request.data.get("update_text", ""),
            progress_percentage=request.data.get("progress_percentage"),
            is_blocker=request.data.get("is_blocker", False),
            evidence_provided=request.data.get("evidence_provided", []),
            created_by=request.user,
        )

        # If status change, update the action
        if request.data.get("new_status"):
            tracking.old_status = action.status
            tracking.new_status = request.data["new_status"]
            tracking.save()

            action.status = request.data["new_status"]
            if request.data["new_status"] == "completed":
                action.actual_completion_date = timezone.now().date()
            action.save()

        return Response(
            ActionTrackingSerializer(tracking, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, tenant_id=None, pk=None):
        """
        Approve an improvement action
        """
        action = self.get_object()

        if action.approved_at:
            return Response(
                {"error": "Action already approved"}, status=status.HTTP_400_BAD_REQUEST
            )

        action.approved_by = request.user
        action.approved_at = timezone.now()
        action.save()

        # Add tracking update
        ActionTracking.objects.create(
            improvement_action=action,
            update_type="review",
            update_text=f"Action approved by {request.user.get_full_name()}",
            created_by=request.user,
        )

        return Response(
            ImprovementActionSerializer(action, context={"request": request}).data
        )

    @action(detail=False, methods=["get"])
    def dashboard_stats(self, request, tenant_id=None):
        """
        Get dashboard statistics for real-time compliance tracking
        """
        actions = self.get_queryset()

        # Basic counts
        total_actions = actions.count()

        # By status
        by_status = dict(
            actions.values("status")
            .annotate(count=Count("id"))
            .values_list("status", "count")
        )

        # By priority
        by_priority = dict(
            actions.values("priority")
            .annotate(count=Count("id"))
            .values_list("priority", "count")
        )

        # By compliance status
        by_compliance = dict(
            actions.values("compliance_status")
            .annotate(count=Count("id"))
            .values_list("compliance_status", "count")
        )

        # Overdue and at-risk
        overdue_count = actions.filter(compliance_status="overdue").count()
        at_risk_count = actions.filter(compliance_status="at_risk").count()

        # Completion rate
        completed_count = actions.filter(status="completed").count()
        completion_rate = (
            (completed_count / total_actions * 100) if total_actions > 0 else 0
        )

        # Average days to complete
        completed_actions = actions.filter(
            status="completed",
            actual_completion_date__isnull=False,
            identified_date__isnull=False,
        )
        avg_days = 0
        if completed_actions.exists():
            total_days = sum(
                [
                    (action.actual_completion_date - action.identified_date).days
                    for action in completed_actions
                ]
            )
            avg_days = total_days / completed_actions.count()

        # Critical compliance
        critical_compliance_count = actions.filter(is_critical_compliance=True).count()

        # Recent completions (last 30 days)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_completions = actions.filter(
            status="completed", actual_completion_date__gte=thirty_days_ago
        ).count()

        stats = {
            "total_actions": total_actions,
            "by_status": by_status,
            "by_priority": by_priority,
            "by_compliance": by_compliance,
            "overdue_count": overdue_count,
            "at_risk_count": at_risk_count,
            "completion_rate": round(completion_rate, 1),
            "avg_days_to_complete": round(avg_days, 1),
            "critical_compliance_count": critical_compliance_count,
            "recent_completions": recent_completions,
        }

        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def compliance_overview(self, request, tenant_id=None):
        """
        Get compliance overview with trend analysis
        """
        actions = self.get_queryset()

        # Overall compliance
        total = actions.count()
        compliant = actions.filter(compliance_status="compliant").count()
        at_risk = actions.filter(compliance_status="at_risk").count()
        overdue = actions.filter(compliance_status="overdue").count()

        # Critical compliance items
        critical_total = actions.filter(is_critical_compliance=True).count()
        critical_overdue = actions.filter(
            is_critical_compliance=True, compliance_status="overdue"
        ).count()

        # Trend data (last 6 months)
        trends = []
        for i in range(6):
            month_start = (
                (timezone.now() - timedelta(days=30 * i)).replace(day=1).date()
            )
            month_actions = actions.filter(identified_date__month=month_start.month)

            trends.append(
                {
                    "month": month_start.strftime("%B %Y"),
                    "total": month_actions.count(),
                    "completed": month_actions.filter(status="completed").count(),
                    "overdue": month_actions.filter(
                        compliance_status="overdue"
                    ).count(),
                }
            )

        return Response(
            {
                "overall": {
                    "total": total,
                    "compliant": compliant,
                    "at_risk": at_risk,
                    "overdue": overdue,
                    "compliance_rate": round(
                        (compliant / total * 100) if total > 0 else 0, 1
                    ),
                },
                "critical": {
                    "total": critical_total,
                    "overdue": critical_overdue,
                    "compliance_rate": round(
                        (
                            ((critical_total - critical_overdue) / critical_total * 100)
                            if critical_total > 0
                            else 100
                        ),
                        1,
                    ),
                },
                "trends": trends[::-1],  # Reverse to show oldest first
            }
        )

    def _classify_action(self, action):
        """
        Classify an improvement action using AI
        """
        result = self._classify_text(
            action.description, action.title, action.root_cause or ""
        )

        # Update action with AI results
        action.ai_classified_category = result["category"]
        action.ai_classification_confidence = result["confidence"]
        action.ai_summary = result["summary"]
        action.ai_keywords = result["keywords"]
        action.ai_related_standards = result["related_standards"]
        action.ai_processed_at = timezone.now()
        action.save()

        return result

    def _classify_text(self, description, title="", root_cause=""):
        """
        AI classification engine (using rule-based approach for now)
        In production, integrate with OpenAI GPT-4 or similar
        """
        combined_text = f"{title} {description} {root_cause}".lower()

        # Category classification using keyword matching
        category_keywords = {
            "training_assessment": [
                "training",
                "assessment",
                "tas",
                "learning",
                "teaching",
                "delivery",
                "curriculum",
            ],
            "trainer_qualifications": [
                "trainer",
                "assessor",
                "qualification",
                "competency",
                "industry experience",
                "tae",
            ],
            "student_support": [
                "student",
                "learner",
                "support",
                "wellbeing",
                "accessibility",
                "disability",
            ],
            "facilities_equipment": [
                "facility",
                "equipment",
                "classroom",
                "workshop",
                "resources",
                "tools",
            ],
            "admin_records": [
                "records",
                "documentation",
                "administration",
                "enrolment",
                "usi",
                "avetmiss",
            ],
            "compliance_governance": [
                "compliance",
                "governance",
                "audit",
                "regulation",
                "asqa",
                "policy",
            ],
            "marketing_recruitment": [
                "marketing",
                "recruitment",
                "advertising",
                "promotion",
                "enrolment",
            ],
            "financial_management": [
                "financial",
                "budget",
                "fees",
                "refund",
                "payment",
                "invoice",
            ],
            "quality_assurance": [
                "quality",
                "validation",
                "moderation",
                "review",
                "improvement",
            ],
            "stakeholder_engagement": [
                "stakeholder",
                "employer",
                "industry",
                "partnership",
                "consultation",
            ],
        }

        category_scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > 0:
                category_scores[category] = score

        # Determine category
        if category_scores:
            classified_category = max(category_scores, key=category_scores.get)
            max_score = category_scores[classified_category]
            total_keywords = len(category_keywords[classified_category])
            confidence = min(max_score / total_keywords, 1.0)
        else:
            classified_category = "other"
            confidence = 0.3

        # Extract keywords (top 10 most relevant words)
        words = re.findall(r"\b\w{4,}\b", combined_text)  # Words with 4+ chars
        stop_words = {
            "with",
            "from",
            "that",
            "this",
            "have",
            "been",
            "will",
            "their",
            "about",
        }
        filtered_words = [w for w in words if w not in stop_words]

        # Count frequency
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1

        # Get top keywords
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keywords = [k[0] for k in keywords]

        # Identify ASQA standards
        standard_patterns = [
            r"\b(?:standard|std\.?)\s+(\d+(?:\.\d+)?)\b",
            r"\b(1\.\d+)\b",  # Standard 1.x
            r"\b(2\.\d+)\b",  # Standard 2.x
        ]

        related_standards = []
        for pattern in standard_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            related_standards.extend(matches)

        related_standards = list(set(related_standards))[:5]  # Unique, max 5

        # Generate summary (first 200 chars + keyword highlights)
        summary_base = description[:200] if len(description) > 200 else description
        if len(description) > 200:
            summary_base += "..."

        summary = f"{summary_base}\n\nKey areas: {', '.join(keywords[:5])}"
        if related_standards:
            summary += f"\nRelated ASQA Standards: {', '.join(related_standards)}"

        return {
            "category": classified_category,
            "confidence": round(confidence, 2),
            "summary": summary,
            "keywords": keywords,
            "related_standards": related_standards,
            "category_display": dict(
                ImprovementAction._meta.get_field("status").choices
            ).get(classified_category, classified_category.replace("_", " ").title()),
        }


class ActionTrackingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for action tracking updates
    """

    serializer_class = ActionTrackingSerializer

    def get_queryset(self):
        tenant_id = self.kwargs.get("tenant_id")
        action_id = self.request.query_params.get("action_id")

        queryset = ActionTracking.objects.filter(
            improvement_action__tenant_id=tenant_id
        ).select_related("improvement_action", "created_by")

        if action_id:
            queryset = queryset.filter(improvement_action_id=action_id)

        return queryset


class ImprovementReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for improvement reviews
    """

    serializer_class = ImprovementReviewSerializer

    def get_queryset(self):
        tenant_id = self.kwargs.get("tenant_id")
        return ImprovementReview.objects.filter(tenant_id=tenant_id).prefetch_related(
            "actions_reviewed", "attendees"
        )

    def perform_create(self, serializer):
        tenant_id = self.kwargs.get("tenant_id")
        serializer.save(tenant_id=tenant_id)

    @action(detail=True, methods=["post"])
    def calculate_stats(self, request, tenant_id=None, pk=None):
        """
        Calculate review statistics
        """
        review = self.get_object()
        review.calculate_statistics()

        return Response(
            ImprovementReviewSerializer(review, context={"request": request}).data
        )

    @action(detail=True, methods=["post"])
    def generate_ai_insights(self, request, tenant_id=None, pk=None):
        """
        Generate AI insights for a review
        """
        review = self.get_object()

        # Get actions for this review
        actions = review.actions_reviewed.all()

        # Generate AI summary
        total = actions.count()
        completed = actions.filter(status="completed").count()
        overdue = actions.filter(compliance_status="overdue").count()

        # Simple AI summary (in production, use GPT-4)
        summary = f"Review of {total} improvement actions from {review.review_period_start} to {review.review_period_end}. "
        summary += f"{completed} actions completed ({round(completed/total*100 if total > 0 else 0, 1)}% completion rate). "

        if overdue > 0:
            summary += f"{overdue} actions are currently overdue and require immediate attention. "

        # Identify trends
        trends = []

        # Category analysis
        category_counts = (
            actions.values("category__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        if category_counts:
            top_category = category_counts[0]
            trends.append(
                {
                    "type": "category",
                    "finding": f"Most actions ({top_category['count']}) are related to {top_category['category__name']}",
                }
            )

        # Priority analysis
        high_priority = actions.filter(priority__in=["critical", "high"]).count()
        if high_priority > total * 0.5:
            trends.append(
                {
                    "type": "priority",
                    "finding": f"High proportion of critical/high priority actions ({high_priority}/{total})",
                }
            )

        # Recommendations
        recommendations = []

        if overdue > 0:
            recommendations.append(
                {
                    "priority": "high",
                    "recommendation": f"Address {overdue} overdue actions immediately to maintain compliance",
                }
            )

        at_risk = actions.filter(compliance_status="at_risk").count()
        if at_risk > 0:
            recommendations.append(
                {
                    "priority": "medium",
                    "recommendation": f"Monitor {at_risk} at-risk actions to prevent them becoming overdue",
                }
            )

        # Update review
        review.ai_summary = summary
        review.ai_trends = trends
        review.ai_recommendations = recommendations
        review.save()

        return Response(
            {"summary": summary, "trends": trends, "recommendations": recommendations}
        )
