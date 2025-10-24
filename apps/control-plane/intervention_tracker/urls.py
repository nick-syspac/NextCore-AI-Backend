from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'interventions', views.InterventionViewSet, basename='intervention')
router.register(r'rules', views.InterventionRuleViewSet, basename='intervention-rule')
router.register(r'workflows', views.InterventionWorkflowViewSet, basename='intervention-workflow')
router.register(r'audit-logs', views.AuditLogViewSet, basename='audit-log')

urlpatterns = [
    path('', include(router.urls)),
]
