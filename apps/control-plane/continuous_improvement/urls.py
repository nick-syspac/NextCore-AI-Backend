from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ImprovementCategoryViewSet, ImprovementActionViewSet,
    ActionTrackingViewSet, ImprovementReviewViewSet
)

router = DefaultRouter()
router.register(r'categories', ImprovementCategoryViewSet, basename='categories')
router.register(r'actions', ImprovementActionViewSet, basename='actions')
router.register(r'tracking', ActionTrackingViewSet, basename='tracking')
router.register(r'reviews', ImprovementReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
]
