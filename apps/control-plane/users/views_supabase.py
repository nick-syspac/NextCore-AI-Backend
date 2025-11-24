"""
Supabase-specific views for user onboarding and account management.
"""

import logging
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserAccount
from tenants.models import Tenant, TenantUser
from audit.models import Audit

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def bootstrap_account(request):
    """
    Bootstrap a new user account after Supabase signup.
    
    This endpoint is called by the frontend after a successful Supabase signup
    to create the corresponding UserAccount and default tenant.
    
    Expected payload:
    {
        "tenant_name": "My Organization",  # Optional, for first-time users
        "tenant_slug": "my-org",           # Optional
        "full_name": "John Doe"            # Optional
    }
    
    Returns:
    {
        "user": {...},
        "tenant": {...},
        "membership": {...}
    }
    """
    # user_account is set by SupabaseAuthentication
    if not hasattr(request, "user_account"):
        return Response(
            {"error": "User account not found. Please ensure you're authenticated with Supabase."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    user_account = request.user_account
    
    # Check if user already has tenants
    existing_memberships = TenantUser.objects.filter(
        user_account=user_account,
        status=TenantUser.Status.ACTIVE,
    )
    
    if existing_memberships.exists():
        # User already bootstrapped, return existing info
        membership = existing_memberships.first()
        return Response({
            "message": "Account already bootstrapped",
            "user": {
                "id": str(user_account.id),
                "supabase_user_id": str(user_account.supabase_user_id),
                "email": user_account.primary_email,
                "full_name": user_account.full_name,
            },
            "tenant": {
                "id": str(membership.tenant.id),
                "name": membership.tenant.name,
                "slug": membership.tenant.slug,
            },
            "membership": {
                "role": membership.role,
                "status": membership.status,
            },
        })
    
    # Get data from request
    tenant_name = request.data.get("tenant_name", f"{user_account.primary_email}'s Organization")
    tenant_slug = request.data.get("tenant_slug")
    full_name = request.data.get("full_name", "")
    
    # Update user full name if provided
    if full_name and not user_account.full_name:
        user_account.full_name = full_name
        user_account.save(update_fields=["full_name", "updated_at"])
    
    # Generate tenant slug if not provided
    if not tenant_slug:
        import re
        base_slug = re.sub(r'[^a-z0-9]+', '-', tenant_name.lower()).strip('-')
        tenant_slug = base_slug
        
        # Ensure uniqueness
        counter = 1
        while Tenant.objects.filter(slug=tenant_slug).exists():
            tenant_slug = f"{base_slug}-{counter}"
            counter += 1
    
    try:
        with transaction.atomic():
            # Create tenant
            tenant = Tenant.objects.create(
                name=tenant_name,
                slug=tenant_slug,
                contact_email=user_account.primary_email,
                contact_name=user_account.full_name or user_account.primary_email,
                status="active",
            )
            
            # Create tenant membership with owner role
            membership = TenantUser.objects.create(
                tenant=tenant,
                user_account=user_account,
                role=TenantUser.Role.OWNER,
                status=TenantUser.Status.ACTIVE,
            )
            
            # Create audit log
            try:
                Audit.objects.create(
                    tenant_id=str(tenant.id),
                    user_id=str(user_account.id),
                    action="account.bootstrap",
                    resource_type="user_account",
                    resource_id=str(user_account.id),
                    changes={
                        "tenant_created": {
                            "id": str(tenant.id),
                            "name": tenant.name,
                            "slug": tenant.slug,
                        },
                        "membership_created": {
                            "role": membership.role,
                            "status": membership.status,
                        },
                    },
                    ip_address=request.META.get("REMOTE_ADDR"),
                    user_agent=request.META.get("HTTP_USER_AGENT", ""),
                )
            except Exception as e:
                logger.warning(f"Failed to create audit log for bootstrap: {str(e)}")
            
            logger.info(
                f"Bootstrapped account for {user_account.primary_email}: "
                f"tenant={tenant.slug}, membership={membership.id}"
            )
            
            return Response(
                {
                    "message": "Account bootstrapped successfully",
                    "user": {
                        "id": str(user_account.id),
                        "supabase_user_id": str(user_account.supabase_user_id),
                        "email": user_account.primary_email,
                        "full_name": user_account.full_name,
                    },
                    "tenant": {
                        "id": str(tenant.id),
                        "name": tenant.name,
                        "slug": tenant.slug,
                        "status": tenant.status,
                    },
                    "membership": {
                        "id": str(membership.id),
                        "role": membership.role,
                        "status": membership.status,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
    
    except Exception as e:
        logger.error(f"Failed to bootstrap account: {str(e)}", exc_info=True)
        return Response(
            {"error": f"Failed to create account: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_tenants(request):
    """
    Get all tenants for the authenticated user.
    
    Returns a list of tenants with membership information.
    """
    if not hasattr(request, "user_account"):
        return Response(
            {"error": "User account not found"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    user_account = request.user_account
    
    # Get all active memberships
    memberships = TenantUser.objects.filter(
        user_account=user_account,
        status=TenantUser.Status.ACTIVE,
    ).select_related("tenant")
    
    tenants = []
    for membership in memberships:
        tenants.append({
            "tenant": {
                "id": str(membership.tenant.id),
                "name": membership.tenant.name,
                "slug": membership.tenant.slug,
                "status": membership.tenant.status,
            },
            "membership": {
                "id": str(membership.id),
                "role": membership.role,
                "status": membership.status,
                "created_at": membership.created_at.isoformat(),
            },
        })
    
    return Response({
        "tenants": tenants,
        "count": len(tenants),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get the authenticated user's profile.
    """
    if not hasattr(request, "user_account"):
        return Response(
            {"error": "User account not found"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    user_account = request.user_account
    
    return Response({
        "id": str(user_account.id),
        "supabase_user_id": str(user_account.supabase_user_id),
        "email": user_account.primary_email,
        "full_name": user_account.full_name,
        "is_active": user_account.is_active,
        "metadata": user_account.metadata,
        "created_at": user_account.created_at.isoformat(),
        "updated_at": user_account.updated_at.isoformat(),
        "last_login_at": user_account.last_login_at.isoformat() if user_account.last_login_at else None,
    })


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the authenticated user's profile.
    
    Allowed fields: full_name, metadata
    """
    if not hasattr(request, "user_account"):
        return Response(
            {"error": "User account not found"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    
    user_account = request.user_account
    
    # Update allowed fields
    if "full_name" in request.data:
        user_account.full_name = request.data["full_name"]
    
    if "metadata" in request.data:
        # Merge metadata instead of replacing
        user_account.metadata.update(request.data["metadata"])
    
    user_account.save()
    
    return Response({
        "id": str(user_account.id),
        "email": user_account.primary_email,
        "full_name": user_account.full_name,
        "metadata": user_account.metadata,
        "updated_at": user_account.updated_at.isoformat(),
    })
