from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TASViewSet, TASTemplateViewSet, TASTemplateSectionViewSet

router = DefaultRouter()
router.register(r"templates", TASTemplateViewSet, basename="tas-template")
router.register(r"template-sections", TASTemplateSectionViewSet, basename="tas-template-section")
router.register(r"", TASViewSet, basename="tas")

urlpatterns = router.urls
