from django.urls import path
from django.http import JsonResponse

def health(_):
    return JsonResponse({"status":"ok","service":"control-plane"})

urlpatterns = [
    path("health", health),
]
