"""
API views for tenant management.
"""
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Tenant, TenantUser, TenantQuota, TenantAPIKey
from .serializers import (
    TenantSerializer,
    TenantCreateSerializer,
    TenantUserSerializer,
    TenantQuotaSerializer,
    TenantAPIKeySerializer,
)

logger = logging.getLogger(__name__)


class TenantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tenants.
    
    Provides CRUD operations and additional actions for tenant lifecycle management.
    """
    queryset = Tenant.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"
    
    def get_serializer_class(self):
        if self.action == "create":
            return TenantCreateSerializer
        return TenantSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        user = self.request.user
        
        # Superusers can see all tenants
        if user.is_superuser:
            return Tenant.objects.all()
        
        # Regular users only see their tenants
        return Tenant.objects.filter(users__user=user).distinct()
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def activate(self, request, slug=None):
        """Activate a tenant."""
        tenant = self.get_object()
        tenant.activate()
        
        logger.info(f"Tenant activated: {tenant.slug}", extra={"tenant_id": str(tenant.id)})
        
        serializer = self.get_serializer(tenant)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def suspend(self, request, slug=None):
        """Suspend a tenant."""
        tenant = self.get_object()
        reason = request.data.get("reason", "")
        
        tenant.suspend(reason=reason)
        
        logger.warning(
            f"Tenant suspended: {tenant.slug}",
            extra={"tenant_id": str(tenant.id), "reason": reason}
        )
        
        serializer = self.get_serializer(tenant)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def restore(self, request, slug=None):
        """Restore a suspended tenant."""
        tenant = self.get_object()
        tenant.restore()
        
        logger.info(f"Tenant restored: {tenant.slug}", extra={"tenant_id": str(tenant.id)})
        
        serializer = self.get_serializer(tenant)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"])
    def quota(self, request, slug=None):
        """Get quota information for a tenant."""
        tenant = self.get_object()
        quota, created = TenantQuota.objects.get_or_create(tenant=tenant)
        
        serializer = TenantQuotaSerializer(quota)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def reset_quota(self, request, slug=None):
        """Reset monthly quotas for a tenant."""
        tenant = self.get_object()
        quota = tenant.quota
        quota.reset_monthly_quotas()
        
        logger.info(f"Quota reset for tenant: {tenant.slug}", extra={"tenant_id": str(tenant.id)})
        
        serializer = TenantQuotaSerializer(quota)
        return Response(serializer.data)


class TenantUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tenant user relationships.
    """
    queryset = TenantUser.objects.all()
    serializer_class = TenantUserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        user = self.request.user
        
        if user.is_superuser:
            return TenantUser.objects.all()
        
        # Users can only see memberships for their tenants
        return TenantUser.objects.filter(tenant__users__user=user)


class TenantAPIKeyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tenant API keys.
    """
    queryset = TenantAPIKey.objects.all()
    serializer_class = TenantAPIKeySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        user = self.request.user
        
        if user.is_superuser:
            return TenantAPIKey.objects.all()
        
        # Users can only see API keys for their tenants
        return TenantAPIKey.objects.filter(tenant__users__user=user)
    
    @action(detail=True, methods=["post"])
    def revoke(self, request, pk=None):
        """Revoke an API key."""
        api_key = self.get_object()
        api_key.is_active = False
        api_key.save()
        
        logger.info(
            f"API key revoked: {api_key.name}",
            extra={"api_key_id": str(api_key.id), "tenant_id": str(api_key.tenant.id)}
        )
        
        serializer = self.get_serializer(api_key)
        return Response(serializer.data)
