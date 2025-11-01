from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthenticityCheckViewSet,
    SubmissionAnalysisViewSet,
    PlagiarismMatchViewSet,
    MetadataVerificationViewSet,
    AnomalyDetectionViewSet,
)

router = DefaultRouter()
router.register(r"checks", AuthenticityCheckViewSet, basename="authenticity-check")
router.register(r"analyses", SubmissionAnalysisViewSet, basename="submission-analysis")
router.register(
    r"plagiarism-matches", PlagiarismMatchViewSet, basename="plagiarism-match"
)
router.register(
    r"metadata-verifications",
    MetadataVerificationViewSet,
    basename="metadata-verification",
)
router.register(
    r"anomaly-detections", AnomalyDetectionViewSet, basename="anomaly-detection"
)

urlpatterns = [
    path("", include(router.urls)),
]
