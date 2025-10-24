from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TrainerProfileViewSet,
    VerificationScanViewSet,
    LinkedInActivityViewSet,
    GitHubActivityViewSet,
    CurrencyEvidenceViewSet,
    EntityExtractionViewSet
)

router = DefaultRouter()
router.register(r'profiles', TrainerProfileViewSet, basename='trainer-profile')
router.register(r'scans', VerificationScanViewSet, basename='verification-scan')
router.register(r'linkedin-activities', LinkedInActivityViewSet, basename='linkedin-activity')
router.register(r'github-activities', GitHubActivityViewSet, basename='github-activity')
router.register(r'evidence', CurrencyEvidenceViewSet, basename='currency-evidence')
router.register(r'entity-extractions', EntityExtractionViewSet, basename='entity-extraction')

urlpatterns = [
    path('', include(router.urls)),
]
