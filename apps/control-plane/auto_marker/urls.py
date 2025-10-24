from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AutoMarkerViewSet,
    MarkedResponseViewSet,
    MarkingCriterionViewSet,
    MarkingLogViewSet
)

router = DefaultRouter()
router.register('markers', AutoMarkerViewSet, basename='auto-marker')
router.register('responses', MarkedResponseViewSet, basename='marked-response')
router.register('criteria', MarkingCriterionViewSet, basename='marking-criterion')
router.register('logs', MarkingLogViewSet, basename='marking-log')

urlpatterns = [
    path('', include(router.urls)),
]
