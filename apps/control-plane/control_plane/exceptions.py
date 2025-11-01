"""
Custom exception handlers for the application.
"""

import logging
from typing import Any

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


class TenantRequiredError(exceptions.APIException):
    """Raised when a tenant context is required but not provided."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Tenant context is required for this operation."
    default_code = "tenant_required"


class TenantNotFoundError(exceptions.APIException):
    """Raised when a tenant is not found."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Tenant not found."
    default_code = "tenant_not_found"


class TenantSuspendedError(exceptions.APIException):
    """Raised when attempting to access a suspended tenant."""

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Tenant is suspended."
    default_code = "tenant_suspended"


class QuotaExceededError(exceptions.APIException):
    """Raised when a tenant exceeds their quota."""

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = "Quota exceeded."
    default_code = "quota_exceeded"


def custom_exception_handler(
    exc: Exception, context: dict[str, Any]
) -> Response | None:
    """
    Custom exception handler that provides consistent error responses.

    Args:
        exc: The exception that was raised
        context: Context information about the request

    Returns:
        Response object with error details
    """
    # Call REST framework's default exception handler first
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Standardize error response format
        error_data = {
            "error": {
                "code": getattr(exc, "default_code", "error"),
                "message": str(exc),
                "details": (
                    response.data
                    if isinstance(response.data, dict)
                    else {"detail": response.data}
                ),
            }
        }
        response.data = error_data

        # Log the error
        logger.error(
            f"API Exception: {exc.__class__.__name__}",
            extra={
                "exception": str(exc),
                "status_code": response.status_code,
                "path": context.get("request").path if context.get("request") else None,
            },
            exc_info=True,
        )

        return response

    # Handle Django exceptions
    if isinstance(exc, Http404):
        error_data = {
            "error": {
                "code": "not_found",
                "message": "Resource not found.",
                "details": {},
            }
        }
        return Response(error_data, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, PermissionDenied):
        error_data = {
            "error": {
                "code": "permission_denied",
                "message": "You do not have permission to perform this action.",
                "details": {},
            }
        }
        return Response(error_data, status=status.HTTP_403_FORBIDDEN)

    # Handle unexpected exceptions
    logger.exception(
        f"Unhandled exception: {exc.__class__.__name__}",
        extra={
            "exception": str(exc),
            "path": context.get("request").path if context.get("request") else None,
        },
    )

    error_data = {
        "error": {
            "code": "internal_error",
            "message": "An unexpected error occurred.",
            "details": {},
        }
    }
    return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
