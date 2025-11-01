from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ASQAStandardViewSet,
    ASQAClauseViewSet,
    PolicyViewSet,
    ComparisonSessionViewSet,
)

router = DefaultRouter()
router.register(r"standards", ASQAStandardViewSet, basename="asqa-standard")
router.register(r"clauses", ASQAClauseViewSet, basename="asqa-clause")
router.register(r"policies", PolicyViewSet, basename="policy")
router.register(r"sessions", ComparisonSessionViewSet, basename="comparison-session")

urlpatterns = router.urls
