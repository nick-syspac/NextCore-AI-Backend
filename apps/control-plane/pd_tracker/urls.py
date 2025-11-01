from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PDActivityViewSet,
    TrainerProfileViewSet,
    PDSuggestionViewSet,
    ComplianceRuleViewSet,
    ComplianceCheckViewSet,
)

router = DefaultRouter()
router.register(r"activities", PDActivityViewSet, basename="pd_activity")
router.register(r"profiles", TrainerProfileViewSet, basename="trainer_profile")
router.register(r"suggestions", PDSuggestionViewSet, basename="pd_suggestion")
router.register(r"rules", ComplianceRuleViewSet, basename="compliance_rule")
router.register(r"checks", ComplianceCheckViewSet, basename="compliance_check")

urlpatterns = [
    path("", include(router.urls)),
]
