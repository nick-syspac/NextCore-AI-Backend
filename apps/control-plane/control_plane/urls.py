"""
URL configuration for control plane application.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.authtoken.views import obtain_auth_token


def health(_):
    """Health check endpoint."""
    return JsonResponse({"status": "ok", "service": "control-plane"})


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # Health check
    path("health", health),
    
    # Authentication
    path("api/auth/token/", obtain_auth_token, name="api-token-auth"),
    
    # API endpoints
    path("api/audit/", include("audit.urls")),
    path("api/", include("tenants.urls")),
]
