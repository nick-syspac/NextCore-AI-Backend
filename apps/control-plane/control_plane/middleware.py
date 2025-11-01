"""
Custom middleware for tenant context and request processing.
"""

import logging
import threading
from typing import Callable

from django.http import HttpRequest, HttpResponse
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


class TenantContextMiddleware(MiddlewareMixin):
    """
    Middleware to extract and set tenant context from request headers.

    Expects X-Tenant-ID header in requests.
    """

    def process_request(self, request: HttpRequest) -> None:
        """Extract tenant ID from request header and set in thread-local storage."""
        tenant_id = request.headers.get("X-Tenant-ID")

        if tenant_id:
            set_current_tenant_id(tenant_id)
            request.tenant_id = tenant_id
            logger.debug(f"Tenant context set: {tenant_id}")
        else:
            set_current_tenant_id(None)
            request.tenant_id = None
            logger.debug("No tenant context in request")

    def process_response(
        self, request: HttpRequest, response: HttpResponse
    ) -> HttpResponse:
        """Clear tenant context after request is processed."""
        set_current_tenant_id(None)
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
