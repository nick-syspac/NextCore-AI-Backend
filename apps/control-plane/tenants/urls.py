"""
URL configuration for tenant management.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TenantViewSet, TenantUserViewSet, TenantAPIKeyViewSet

router = DefaultRouter()
router.register(r"tenants", TenantViewSet, basename="tenant")
router.register(r"tenant-users", TenantUserViewSet, basename="tenant-user")
router.register(r"api-keys", TenantAPIKeyViewSet, basename="api-key")

urlpatterns = [
    path("", include(router.urls)),
    path("tenants/<str:tenant_slug>/integrations/", include("integrations.urls")),
    path("tenants/<str:tenant_slug>/tas/", include("tas.urls")),
    path("tenants/<str:tenant_slug>/policy-comparator/", include("policy_comparator.urls")),
    path("tenants/<str:tenant_slug>/audit-assistant/", include("audit_assistant.urls")),
    path("tenants/<str:tenant_slug>/continuous-improvement/", include("continuous_improvement.urls")),
    path("tenants/<str:tenant_slug>/funding-eligibility/", include("funding_eligibility.urls")),
    path("tenants/<str:tenant_slug>/assessment-builder/", include("assessment_builder.urls")),
    path("tenants/<str:tenant_slug>/rubric-generator/", include("rubric_generator.urls")),
    path("tenants/<str:tenant_slug>/auto-marker/", include("auto_marker.urls")),
    path("tenants/<str:tenant_slug>/feedback-assistant/", include("feedback_assistant.urls")),
    path("tenants/<str:tenant_slug>/moderation-tool/", include("moderation_tool.urls")),
    path("tenants/<str:tenant_slug>/evidence-mapper/", include("evidence_mapper.urls")),
    path("tenants/<str:tenant_slug>/authenticity-check/", include("authenticity_check.urls")),
    path("tenants/<str:tenant_slug>/risk-engine/", include("risk_engine.urls")),
    path("tenants/<str:tenant_slug>/adaptive-pathway/", include("adaptive_pathway.urls")),
    path("tenants/<str:tenant_slug>/engagement-heatmap/", include("engagement_heatmap.urls")),
    path("tenants/<str:tenant_slug>/study-coach/", include("study_coach.urls")),
]
