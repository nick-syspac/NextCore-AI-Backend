from rest_framework import serializers
from .models import Audit

class AuditSerializer(serializers.ModelSerializer):
    # Extract fields from payload
    event_type = serializers.SerializerMethodField()
    severity = serializers.SerializerMethodField()
    actor_type = serializers.SerializerMethodField()
    actor_id = serializers.SerializerMethodField()
    actor_username = serializers.SerializerMethodField()
    resource_type = serializers.SerializerMethodField()
    resource_id = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    ip_address = serializers.SerializerMethodField()
    user_agent = serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()
    
    class Meta:
        model = Audit
        fields = [
            'id', 'tenant_id', 'event_type', 'severity', 'actor_type', 
            'actor_id', 'actor_username', 'resource_type', 'resource_id',
            'action', 'status', 'ip_address', 'user_agent', 'metadata',
            'timestamp', 'hash', 'prev_hash', 'payload'
        ]
    
    def get_event_type(self, obj):
        return obj.event_type or obj.payload.get('event_type', 'unknown')
    
    def get_severity(self, obj):
        return obj.payload.get('severity', 'info')
    
    def get_actor_type(self, obj):
        return obj.payload.get('actor_type', 'system')
    
    def get_actor_id(self, obj):
        return obj.payload.get('actor_id', '')
    
    def get_actor_username(self, obj):
        return obj.payload.get('actor_username', 'unknown')
    
    def get_resource_type(self, obj):
        return obj.payload.get('resource_type', 'unknown')
    
    def get_resource_id(self, obj):
        return obj.payload.get('resource_id', '')
    
    def get_action(self, obj):
        return obj.payload.get('action', 'unknown_action')
    
    def get_status(self, obj):
        return obj.payload.get('status', 'unknown')
    
    def get_ip_address(self, obj):
        return obj.payload.get('ip_address', '0.0.0.0')
    
    def get_user_agent(self, obj):
        return obj.payload.get('user_agent', 'Unknown')
    
    def get_metadata(self, obj):
        # Return all payload data as metadata
        return obj.payload
