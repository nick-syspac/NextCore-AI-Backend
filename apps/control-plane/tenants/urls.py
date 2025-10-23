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
]
