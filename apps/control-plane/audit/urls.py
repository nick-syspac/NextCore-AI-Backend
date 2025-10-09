from django.urls import path
from .views import AuditListView, AuditVerifyView

urlpatterns = [
    path('audit', AuditListView.as_view(), name='audit-list'),
    path('audit/verify/latest', AuditVerifyView.as_view(), name='audit-verify'),
]
