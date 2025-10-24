from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvidenceViewSet, ClauseEvidenceViewSet, AuditReportViewSet

router = DefaultRouter()
router.register(r'evidence', EvidenceViewSet, basename='evidence')
router.register(r'clause-evidence', ClauseEvidenceViewSet, basename='clause-evidence')
router.register(r'audit-reports', AuditReportViewSet, basename='audit-reports')

urlpatterns = [
    path('', include(router.urls)),
]
