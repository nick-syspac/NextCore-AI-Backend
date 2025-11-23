"""
Custom middleware for tenant context and request processing.
"""

import logging
import threading
from typing import Callable

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

# Thread-local storage for tenant context
_thread_locals = threading.local()


def get_current_tenant_id() -> str | None:
    """Get the current tenant ID from thread-local storage."""
    return getattr(_thread_locals, "tenant_id", None)


def set_current_tenant_id(tenant_id: str | None) -> None:
    """Set the current tenant ID in thread-local storage."""
    _thread_locals.tenant_id = tenant_id


def get_current_tenant():
    """Get the current tenant object from thread-local storage."""
    return getattr(_thread_locals, "tenant", None)


def set_current_tenant(tenant) -> None:
    """Set the current tenant object in thread-local storage."""
    _thread_locals.tenant = tenant


class TenantContextMiddleware(MiddlewareMixin):
    """
    Middleware to extract and set tenant context from request headers.

    Expects X-Tenant-ID header in requests and verifies user has access to the tenant.
    """

    # Paths that don't require tenant context
    EXEMPT_PATHS = [
        "/api/auth/",
        "/api/users/register/",
        "/api/users/bootstrap-account/",
        "/api/admin/",
        "/api/docs/",
        "/api/schema/",
        "/health/",
    ]

    def process_request(self, request: HttpRequest) -> None:
        """Extract tenant ID from request header and set in thread-local storage."""
        # Check if path is exempt from tenant requirements
        if any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
            set_current_tenant_id(None)
            set_current_tenant(None)
            request.tenant_id = None
            request.tenant = None
            return None

        tenant_id = request.headers.get("X-Tenant-ID")

        if tenant_id:
            # Only validate tenant membership for authenticated requests with UserAccount
            if hasattr(request, "user_account"):
                from tenants.models import Tenant, TenantUser
                
                try:
                    # Get the tenant
                    tenant = Tenant.objects.get(id=tenant_id)
                    
                    # Verify user has access to this tenant
                    membership = TenantUser.objects.filter(
                        tenant=tenant,
                        user_account=request.user_account,
                        status=TenantUser.Status.ACTIVE,
                    ).first()
                    
                    if not membership:
                        logger.warning(
                            f"User {request.user_account.primary_email} attempted to access "
                            f"tenant {tenant_id} without membership"
                        )
                        # Don't set tenant context if no membership
                        set_current_tenant_id(None)
                        set_current_tenant(None)
                        request.tenant_id = None
                        request.tenant = None
                        request.tenant_membership = None
                        return None
                    
                    # Set tenant context
                    set_current_tenant_id(tenant_id)
                    set_current_tenant(tenant)
                    request.tenant_id = tenant_id
                    request.tenant = tenant
                    request.tenant_membership = membership
                    request.tenant_role = membership.role
                    
                    logger.debug(
                        f"Tenant context set: {tenant.name} ({tenant_id}) "
                        f"for user {request.user_account.primary_email} with role {membership.role}"
                    )
                    
                except Tenant.DoesNotExist:
                    logger.warning(f"Tenant {tenant_id} not found")
                    set_current_tenant_id(None)
                    set_current_tenant(None)
                    request.tenant_id = None
                    request.tenant = None
                except Exception as e:
                    logger.error(f"Error setting tenant context: {str(e)}", exc_info=True)
                    set_current_tenant_id(None)
                    set_current_tenant(None)
                    request.tenant_id = None
                    request.tenant = None
            else:
                # Unauthenticated or legacy auth - just set the ID
                set_current_tenant_id(tenant_id)
                request.tenant_id = tenant_id
                logger.debug(f"Tenant ID set without validation: {tenant_id}")
        else:
            set_current_tenant_id(None)
            set_current_tenant(None)
            request.tenant_id = None
            request.tenant = None
            logger.debug("No tenant context in request")

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """Clear tenant context after request is processed."""
        set_current_tenant_id(None)
        set_current_tenant(None)
        return response


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all incoming requests and responses.
    """

    def process_request(self, request: HttpRequest) -> None:
        """Log incoming request details."""
        logger.info(
            f"Request: {request.method} {request.path}",
            extra={
                "method": request.method,
                "path": request.path,
                "user": str(request.user) if hasattr(request, "user") else "anonymous",
                "tenant_id": getattr(request, "tenant_id", None),
            },
        )

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """Log response status."""
        logger.info(
            f"Response: {response.status_code} for {request.method} {request.path}",
            extra={
                "status_code": response.status_code,
                "method": request.method,
                "path": request.path,
            },
        )
        return response
