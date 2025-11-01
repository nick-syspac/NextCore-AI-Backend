from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r"heatmaps", views.EngagementHeatmapViewSet, basename="heatmap")
router.register(r"attendance", views.AttendanceRecordViewSet, basename="attendance")
router.register(r"lms-activity", views.LMSActivityViewSet, basename="lms-activity")
router.register(r"sentiment", views.DiscussionSentimentViewSet, basename="sentiment")
router.register(r"alerts", views.EngagementAlertViewSet, basename="alert")

urlpatterns = [
    path("", include(router.urls)),
]
