from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r"pathways", views.LearningPathwayViewSet, basename="pathway")
router.register(r"steps", views.LearningStepViewSet, basename="step")
router.register(r"progress", views.StudentProgressViewSet, basename="progress")
router.register(
    r"recommendations", views.PathwayRecommendationViewSet, basename="recommendation"
)
router.register(r"embeddings", views.ContentEmbeddingViewSet, basename="embedding")

urlpatterns = [
    path("", include(router.urls)),
]
