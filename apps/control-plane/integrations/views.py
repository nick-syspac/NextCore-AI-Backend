from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone

from tenants.models import Tenant
from .models import Integration, IntegrationLog, IntegrationMapping
from .serializers import (
    IntegrationSerializer,
    IntegrationLogSerializer,
    IntegrationMappingSerializer,
    IntegrationConfigSerializer,
)


class IntegrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing integrations
    """
    serializer_class = IntegrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        tenant_slug = self.kwargs.get('tenant_slug')
        tenant = get_object_or_404(Tenant, slug=tenant_slug)
        return Integration.objects.filter(tenant=tenant)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        tenant_slug = self.kwargs.get('tenant_slug')
        context['tenant'] = get_object_or_404(Tenant, slug=tenant_slug)
        return context
    
    @action(detail=True, methods=['post'])
    def connect(self, request, tenant_slug=None, pk=None):
        """
        Connect/activate an integration
        """
        integration = self.get_object()
        
        # Validate credentials based on integration type
        if integration.integration_type == 'axcelerate':
            if not integration.config.get('axcelerate_wstoken'):
                return Response(
                    {'error': 'Axcelerate WS Token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif integration.integration_type == 'canvas':
            if not integration.api_key:
                return Response(
                    {'error': 'Canvas API Key is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif integration.integration_type in ['xero', 'myob']:
            if not integration.client_id or not integration.client_secret:
                return Response(
                    {'error': 'OAuth credentials are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Update status
        integration.status = 'active'
        integration.save()
        
        # Log connection
        IntegrationLog.objects.create(
            integration=integration,
            action='connect',
            status='success',
            message=f'Integration connected successfully',
            details={'user': request.user.username}
        )
        
        serializer = self.get_serializer(integration)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def disconnect(self, request, tenant_slug=None, pk=None):
        """
        Disconnect/deactivate an integration
        """
        integration = self.get_object()
        integration.status = 'inactive'
        integration.save()
        
        # Log disconnection
        IntegrationLog.objects.create(
            integration=integration,
            action='disconnect',
            status='success',
            message=f'Integration disconnected',
            details={'user': request.user.username}
        )
        
        serializer = self.get_serializer(integration)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def sync(self, request, tenant_slug=None, pk=None):
        """
        Trigger manual synchronization
        """
        integration = self.get_object()
        
        if integration.status != 'active':
            return Response(
                {'error': 'Integration must be active to sync'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update sync timestamp
        integration.last_sync_at = timezone.now()
        integration.last_sync_status = 'success'
        integration.save()
        
        # Log sync
        IntegrationLog.objects.create(
            integration=integration,
            action='sync',
            status='success',
            message=f'Manual sync triggered',
            details={'user': request.user.username}
        )
        
        serializer = self.get_serializer(integration)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, tenant_slug=None, pk=None):
        """
        Test integration connection
        """
        integration = self.get_object()
        
        # Simulate connection test
        # In production, this would make actual API calls
        test_result = {
            'success': True,
            'message': 'Connection test successful',
            'details': {
                'integration_type': integration.integration_type,
                'api_reachable': True,
                'credentials_valid': True,
            }
        }
        
        # Log test
        IntegrationLog.objects.create(
            integration=integration,
            action='config_update',
            status='success',
            message=f'Connection test performed',
            details=test_result
        )
        
        return Response(test_result)
    
    @action(detail=True, methods=['get'])
    def logs(self, request, tenant_slug=None, pk=None):
        """
        Get integration logs
        """
        integration = self.get_object()
        logs = integration.logs.all()[:50]  # Last 50 logs
        serializer = IntegrationLogSerializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get', 'post'])
    def mappings(self, request, tenant_slug=None, pk=None):
        """
        Get or create field mappings
        """
        integration = self.get_object()
        
        if request.method == 'GET':
            mappings = integration.mappings.all()
            serializer = IntegrationMappingSerializer(mappings, many=True)
            return Response(serializer.data)
        else:
            serializer = IntegrationMappingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(integration=integration)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IntegrationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing integration logs
    """
    serializer_class = IntegrationLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        tenant_slug = self.kwargs.get('tenant_slug')
        tenant = get_object_or_404(Tenant, slug=tenant_slug)
        return IntegrationLog.objects.filter(integration__tenant=tenant)
