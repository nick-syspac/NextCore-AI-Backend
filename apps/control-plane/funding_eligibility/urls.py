from rest_framework import routers
from .views import JurisdictionRequirementViewSet, EligibilityRuleViewSet, EligibilityCheckViewSet

router = routers.DefaultRouter()
router.register(r'jurisdictions', JurisdictionRequirementViewSet, basename='jurisdiction')
router.register(r'rules', EligibilityRuleViewSet, basename='rule')
router.register(r'checks', EligibilityCheckViewSet, basename='check')

urlpatterns = router.urls
