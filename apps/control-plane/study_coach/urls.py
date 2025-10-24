from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sessions', views.ChatSessionViewSet, basename='chat-session')
router.register(r'messages', views.ChatMessageViewSet, basename='chat-message')
router.register(r'documents', views.KnowledgeDocumentViewSet, basename='knowledge-document')
router.register(r'insights', views.CoachingInsightViewSet, basename='coaching-insight')
router.register(r'config', views.CoachConfigurationViewSet, basename='coach-config')

urlpatterns = [
    path('', include(router.urls)),
]
