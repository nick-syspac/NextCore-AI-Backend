from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DiaryEntryViewSet,
    AudioRecordingViewSet,
    DailySummaryViewSet,
    EvidenceDocumentViewSet,
    TranscriptionJobViewSet,
)

router = DefaultRouter()
router.register(r"diary-entries", DiaryEntryViewSet, basename="diary-entry")
router.register(r"audio-recordings", AudioRecordingViewSet, basename="audio-recording")
router.register(r"daily-summaries", DailySummaryViewSet, basename="daily-summary")
router.register(
    r"evidence-documents", EvidenceDocumentViewSet, basename="evidence-document"
)
router.register(
    r"transcription-jobs", TranscriptionJobViewSet, basename="transcription-job"
)

urlpatterns = [
    path("", include(router.urls)),
]
