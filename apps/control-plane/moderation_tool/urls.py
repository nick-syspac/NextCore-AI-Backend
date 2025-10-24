from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ModerationSessionViewSet, AssessorDecisionViewSet,
    OutlierDetectionViewSet, BiasScoreViewSet, ModerationLogViewSet
)

router = DefaultRouter()
router.register(r'sessions', ModerationSessionViewSet, basename='moderationsession')
router.register(r'decisions', AssessorDecisionViewSet, basename='assessordecision')
router.register(r'outliers', OutlierDetectionViewSet, basename='outlierdetection')
router.register(r'bias-scores', BiasScoreViewSet, basename='biasscore')
router.register(r'logs', ModerationLogViewSet, basename='moderationlog')

urlpatterns = [
    path('', include(router.urls)),
]
