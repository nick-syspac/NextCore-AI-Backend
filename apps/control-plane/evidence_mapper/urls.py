from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EvidenceMappingViewSet,
    SubmissionEvidenceViewSet,
    CriteriaTagViewSet,
    EvidenceAuditViewSet,
    EmbeddingSearchViewSet,
)

router = DefaultRouter()
router.register(r"mappings", EvidenceMappingViewSet, basename="evidencemapping")
router.register(
    r"submissions", SubmissionEvidenceViewSet, basename="submissionevidence"
)
router.register(r"tags", CriteriaTagViewSet, basename="criteriatag")
router.register(r"audit", EvidenceAuditViewSet, basename="evidenceaudit")
router.register(r"searches", EmbeddingSearchViewSet, basename="embeddingsearch")

urlpatterns = [
    path("", include(router.urls)),
]
