from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssessmentViewSet, AssessmentTaskViewSet, AssessmentCriteriaViewSet

router = DefaultRouter()
router.register(r"assessments", AssessmentViewSet, basename="assessment")
router.register(r"tasks", AssessmentTaskViewSet, basename="assessment-task")
router.register(r"criteria", AssessmentCriteriaViewSet, basename="assessment-criteria")

app_name = "assessment_builder"

urlpatterns = [
    path("", include(router.urls)),
]
