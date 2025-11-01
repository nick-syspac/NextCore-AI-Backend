from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RubricViewSet, RubricCriterionViewSet, RubricLevelViewSet

router = DefaultRouter()
router.register(r"rubrics", RubricViewSet, basename="rubric")
router.register(r"criteria", RubricCriterionViewSet, basename="rubric-criterion")
router.register(r"levels", RubricLevelViewSet, basename="rubric-level")

app_name = "rubric_generator"

urlpatterns = [
    path("", include(router.urls)),
]
