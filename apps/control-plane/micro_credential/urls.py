from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MicroCredentialViewSet, 
    MicroCredentialVersionViewSet,
    MicroCredentialEnrollmentViewSet
)

router = DefaultRouter()
router.register(r'', MicroCredentialViewSet, basename='micro-credential')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:micro_credential_id>/versions/', 
         MicroCredentialVersionViewSet.as_view({'get': 'list'}), 
         name='micro-credential-versions'),
    path('enrollments/', 
         MicroCredentialEnrollmentViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='micro-credential-enrollments'),
]
