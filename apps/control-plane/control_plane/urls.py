from django.urls import path, include
from django.http import JsonResponse

def health(_):
    return JsonResponse({"status":"ok","service":"control-plane"})

urlpatterns = [
    path("health", health),
    path("api/", include("audit.urls")),
]
