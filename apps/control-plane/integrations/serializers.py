from rest_framework import serializers
from .models import Integration, IntegrationLog, IntegrationMapping


class IntegrationSerializer(serializers.ModelSerializer):
    integration_type_display = serializers.CharField(source='get_integration_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_token_expired = serializers.BooleanField(read_only=True)
    needs_sync = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Integration
        fields = [
            'id', 'tenant', 'integration_type', 'integration_type_display',
            'name', 'description', 'status', 'status_display',
            'config', 'client_id', 'api_base_url', 'api_key',
            'webhook_url', 'webhook_secret',
            'auto_sync_enabled', 'sync_interval_minutes',
            'last_sync_at', 'last_sync_status', 'last_sync_error',
            'is_token_expired', 'needs_sync',
            'created_at', 'updated_at', 'created_by',
        ]
        read_only_fields = ['id', 'tenant', 'created_at', 'updated_at', 'last_sync_at']
        extra_kwargs = {
            'client_secret': {'write_only': True},
            'access_token': {'write_only': True},
            'refresh_token': {'write_only': True},
        }
    
    def create(self, validated_data):
        # Set tenant from context
        validated_data['tenant'] = self.context['tenant']
        validated_data['created_by'] = self.context['request'].user.username
        return super().create(validated_data)


class IntegrationLogSerializer(serializers.ModelSerializer):
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = IntegrationLog
        fields = [
            'id', 'integration', 'action', 'action_display',
            'status', 'message', 'details',
            'request_data', 'response_data', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class IntegrationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationMapping
        fields = [
            'id', 'integration', 'source_entity', 'source_field',
            'target_entity', 'target_field', 'transform_rule',
            'is_bidirectional', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class IntegrationConfigSerializer(serializers.Serializer):
    """
    Serializer for integration-specific configuration
    """
    # Axcelerate
    axcelerate_subdomain = serializers.CharField(required=False, allow_blank=True)
    axcelerate_wstoken = serializers.CharField(required=False, allow_blank=True)
    
    # Canvas
    canvas_domain = serializers.CharField(required=False, allow_blank=True)
    canvas_account_id = serializers.CharField(required=False, allow_blank=True)
    
    # Xero
    xero_tenant_id = serializers.CharField(required=False, allow_blank=True)
    xero_organization_name = serializers.CharField(required=False, allow_blank=True)
    
    # MYOB
    myob_company_file_id = serializers.CharField(required=False, allow_blank=True)
    myob_company_name = serializers.CharField(required=False, allow_blank=True)
    
    # Common settings
    sync_users = serializers.BooleanField(required=False, default=False)
    sync_courses = serializers.BooleanField(required=False, default=False)
    sync_enrollments = serializers.BooleanField(required=False, default=False)
    sync_invoices = serializers.BooleanField(required=False, default=False)
