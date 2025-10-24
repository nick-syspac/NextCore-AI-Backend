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


def api_root(request):
    """API root endpoint with available endpoints."""
    return JsonResponse({
        "service": "NextCore AI Cloud - Control Plane",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": f"{request.scheme}://{request.get_host()}/health",
            "admin": f"{request.scheme}://{request.get_host()}/admin/",
            "api": {
                "authentication": f"{request.scheme}://{request.get_host()}/api/auth/token/",
                "tenants": f"{request.scheme}://{request.get_host()}/api/tenants/",
                "tenant_users": f"{request.scheme}://{request.get_host()}/api/tenant-users/",
                "api_keys": f"{request.scheme}://{request.get_host()}/api/api-keys/",
                "audit_events": f"{request.scheme}://{request.get_host()}/api/audit/events/",
                "audit_verify": f"{request.scheme}://{request.get_host()}/api/audit/verify/",
                "integrations": f"{request.scheme}://{request.get_host()}/api/tenants/{{tenant_slug}}/integrations/",
                "tas": f"{request.scheme}://{request.get_host()}/api/tenants/{{tenant_slug}}/tas/",
            },
        },
        "documentation": "See API_DOCUMENTATION.md for complete API reference",
    })


urlpatterns = [
    # Root
    path("", api_root, name="api-root"),
    
    # Admin
    path("admin/", admin.site.urls),
    
    # Health check
    path("health", health),
    
    # Authentication
    path("api/auth/token/", obtain_auth_token, name="api-token-auth"),
    
    # API endpoints
    path("api/users/", include("users.urls")),
    path("api/audit/", include("audit.urls")),
    path("api/", include("tenants.urls")),
    path("api/trainer-diary/", include("trainer_diary.urls")),
    path("api/industry-currency/", include("industry_currency.urls")),
]
