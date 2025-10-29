from rest_framework import routers
from .views import JurisdictionRequirementViewSet, EligibilityRuleViewSet, EligibilityCheckViewSet
from .views_extended import (
    JurisdictionViewSet,
    RulesetViewSet,
    ReferenceTableViewSet,
    EligibilityRequestViewSet,
    DecisionOverrideViewSet,
    EvidenceAttachmentViewSet,
    WebhookEndpointViewSet,
)

router = routers.DefaultRouter()

# Legacy endpoints (original implementation)
router.register(r'jurisdictions-legacy', JurisdictionRequirementViewSet, basename='jurisdiction-legacy')
router.register(r'rules-legacy', EligibilityRuleViewSet, basename='rule-legacy')
router.register(r'checks-legacy', EligibilityCheckViewSet, basename='check-legacy')

# Extended endpoints (new implementation with rules engine)
router.register(r'jurisdictions', JurisdictionViewSet, basename='jurisdiction')
router.register(r'rulesets', RulesetViewSet, basename='ruleset')
router.register(r'reference-tables', ReferenceTableViewSet, basename='reference-table')
router.register(r'requests', EligibilityRequestViewSet, basename='request')
router.register(r'overrides', DecisionOverrideViewSet, basename='override')
router.register(r'attachments', EvidenceAttachmentViewSet, basename='attachment')
router.register(r'webhooks', WebhookEndpointViewSet, basename='webhook')

urlpatterns = router.urls
