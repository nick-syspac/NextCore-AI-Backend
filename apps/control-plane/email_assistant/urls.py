from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentMessageViewSet, DraftReplyViewSet, MessageTemplateViewSet,
    ConversationThreadViewSet, ToneProfileViewSet, ReplyHistoryViewSet
)

router = DefaultRouter()
router.register(r'messages', StudentMessageViewSet, basename='student-message')
router.register(r'drafts', DraftReplyViewSet, basename='draft-reply')
router.register(r'templates', MessageTemplateViewSet, basename='message-template')
router.register(r'threads', ConversationThreadViewSet, basename='conversation-thread')
router.register(r'tone-profiles', ToneProfileViewSet, basename='tone-profile')
router.register(r'history', ReplyHistoryViewSet, basename='reply-history')

urlpatterns = [
    path('', include(router.urls)),
]
