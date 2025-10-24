from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeedbackTemplateViewSet,
    GeneratedFeedbackViewSet,
    FeedbackCriterionViewSet,
    FeedbackLogViewSet
)

router = DefaultRouter()
router.register('templates', FeedbackTemplateViewSet, basename='feedback-template')
router.register('generated', GeneratedFeedbackViewSet, basename='generated-feedback')
router.register('criteria', FeedbackCriterionViewSet, basename='feedback-criterion')
router.register('logs', FeedbackLogViewSet, basename='feedback-log')

urlpatterns = [
    path('', include(router.urls)),
]
