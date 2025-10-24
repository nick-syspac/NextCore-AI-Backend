from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TrainerQualificationViewSet, UnitOfCompetencyViewSet,
    TrainerAssignmentViewSet, CompetencyGapViewSet,
    QualificationMappingViewSet, ComplianceCheckViewSet
)

router = DefaultRouter()
router.register(r'qualifications', TrainerQualificationViewSet, basename='qualification')
router.register(r'units', UnitOfCompetencyViewSet, basename='unit')
router.register(r'assignments', TrainerAssignmentViewSet, basename='assignment')
router.register(r'gaps', CompetencyGapViewSet, basename='gap')
router.register(r'mappings', QualificationMappingViewSet, basename='mapping')
router.register(r'compliance-checks', ComplianceCheckViewSet, basename='compliance-check')

urlpatterns = [
    path('', include(router.urls)),
]
