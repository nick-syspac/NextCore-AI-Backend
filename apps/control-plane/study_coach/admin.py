from django.contrib import admin
from .models import ChatSession, ChatMessage, KnowledgeDocument, CoachingInsight, CoachConfiguration


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_number', 'student_name', 'session_type', 'status', 
                    'message_count', 'satisfaction_rating', 'created_at']
    list_filter = ['status', 'session_type', 'created_at']
    search_fields = ['session_number', 'student_name', 'student_id', 'subject', 'topic']
    readonly_fields = ['session_number', 'created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['message_number', 'session', 'role', 'sentiment', 
                    'model_used', 'total_tokens', 'created_at']
    list_filter = ['role', 'sentiment', 'model_used', 'created_at']
    search_fields = ['message_number', 'content', 'session__session_number']
    readonly_fields = ['message_number', 'created_at']


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'title', 'document_type', 'subject', 
                    'retrieval_count', 'visibility', 'created_at']
    list_filter = ['document_type', 'visibility', 'subject', 'created_at']
    search_fields = ['document_number', 'title', 'subject', 'topic', 'content']
    readonly_fields = ['document_number', 'vector_id', 'retrieval_count', 
                       'average_relevance_score', 'last_retrieved_at', 
                       'created_at', 'updated_at']


@admin.register(CoachingInsight)
class CoachingInsightAdmin(admin.ModelAdmin):
    list_display = ['insight_number', 'student_id', 'time_period', 'total_sessions',
                    'average_satisfaction', 'sentiment_trend', 'created_at']
    list_filter = ['sentiment_trend', 'time_period', 'created_at']
    search_fields = ['insight_number', 'student_id']
    readonly_fields = ['insight_number', 'created_at', 'updated_at']


@admin.register(CoachConfiguration)
class CoachConfigurationAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'primary_model', 'coaching_style', 'vector_db_enabled',
                    'available_24_7', 'created_at']
    list_filter = ['coaching_style', 'vector_db_enabled', 'available_24_7']
    search_fields = ['tenant']
    readonly_fields = ['created_at', 'updated_at']
