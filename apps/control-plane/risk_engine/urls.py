from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RiskAssessmentViewSet,
    RiskFactorViewSet,
    StudentEngagementMetricViewSet,
    SentimentAnalysisViewSet,
    InterventionActionViewSet,
)

router = DefaultRouter()
router.register(r"risk-assessments", RiskAssessmentViewSet, basename="risk-assessment")
router.register(r"risk-factors", RiskFactorViewSet, basename="risk-factor")
router.register(
    r"engagement-metrics", StudentEngagementMetricViewSet, basename="engagement-metric"
)
router.register(
    r"sentiment-analyses", SentimentAnalysisViewSet, basename="sentiment-analysis"
)
router.register(r"interventions", InterventionActionViewSet, basename="intervention")

urlpatterns = [
    path("", include(router.urls)),
]
