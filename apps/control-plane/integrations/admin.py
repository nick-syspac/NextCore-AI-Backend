from django.contrib import admin
from .models import Integration, IntegrationLog, IntegrationMapping


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'tenant', 'integration_type', 'status', 'auto_sync_enabled', 'last_sync_at', 'created_at']
    list_filter = ['integration_type', 'status', 'auto_sync_enabled']
    search_fields = ['name', 'tenant__name', 'tenant__slug']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_sync_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'tenant', 'integration_type', 'name', 'description', 'status')
        }),
        ('Configuration', {
            'fields': ('config', 'api_base_url', 'api_key', 'webhook_url', 'webhook_secret')
        }),
        ('OAuth Credentials', {
            'fields': ('client_id', 'client_secret', 'access_token', 'refresh_token', 'token_expires_at'),
            'classes': ('collapse',)
        }),
        ('Sync Settings', {
            'fields': ('auto_sync_enabled', 'sync_interval_minutes', 'last_sync_at', 'last_sync_status', 'last_sync_error')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by')
        }),
    )


@admin.register(IntegrationLog)
class IntegrationLogAdmin(admin.ModelAdmin):
    list_display = ['integration', 'action', 'status', 'message', 'created_at']
    list_filter = ['action', 'status', 'created_at']
    search_fields = ['integration__name', 'message']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(IntegrationMapping)
class IntegrationMappingAdmin(admin.ModelAdmin):
    list_display = ['integration', 'source_entity', 'source_field', 'target_entity', 'target_field', 'is_bidirectional']
    list_filter = ['source_entity', 'target_entity', 'is_bidirectional']
    search_fields = ['integration__name', 'source_field', 'target_field']
    readonly_fields = ['id', 'created_at', 'updated_at']
