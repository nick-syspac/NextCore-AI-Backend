from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ImprovementCategoryViewSet, ImprovementActionViewSet,
    ActionTrackingViewSet, ImprovementReviewViewSet
)
from .views_cir import (
    ActionStepViewSet,
    CommentViewSet,
    AttachmentViewSet,
    VerificationViewSet,
    ClauseLinkViewSet,
    SLAPolicyViewSet,
    KPISnapshotViewSet,
    TaxonomyLabelViewSet,
    AIRunViewSet,
    ImprovementActionCIRViewSet,
)

# Main router for improvement actions and categories
router = DefaultRouter()
router.register(r'categories', ImprovementCategoryViewSet, basename='categories')
router.register(r'actions', ImprovementActionViewSet, basename='actions')
router.register(r'tracking', ActionTrackingViewSet, basename='tracking')
router.register(r'reviews', ImprovementReviewViewSet, basename='reviews')

# CIR-specific routers
router.register(r'steps', ActionStepViewSet, basename='steps')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'attachments', AttachmentViewSet, basename='attachments')
router.register(r'verifications', VerificationViewSet, basename='verifications')
router.register(r'clause-links', ClauseLinkViewSet, basename='clause-links')
router.register(r'sla-policies', SLAPolicyViewSet, basename='sla-policies')
router.register(r'kpi-snapshots', KPISnapshotViewSet, basename='kpi-snapshots')
router.register(r'taxonomy-labels', TaxonomyLabelViewSet, basename='taxonomy-labels')
router.register(r'ai-runs', AIRunViewSet, basename='ai-runs')

# Extended action endpoints with AI features
router.register(r'actions-cir', ImprovementActionCIRViewSet, basename='actions-cir')

urlpatterns = [
    path('', include(router.urls)),
]
