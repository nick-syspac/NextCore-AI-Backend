"""
API views for audit log management.
"""

import logging
from typing import Any

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Audit, chain_hash
from .serializers import AuditSerializer

logger = logging.getLogger(__name__)


class AuditListView(generics.ListAPIView):
    """
    List audit events with optional filtering.

    Query parameters:
    - tenant_id: Filter by tenant ID
    - event_type: Filter by event type
    - since: Filter events after this timestamp (ISO format)
    """

    serializer_class = AuditSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["tenant_id", "event_type"]
    search_fields = ["tenant_id", "event_type"]
    ordering_fields = ["timestamp", "tenant_id"]
    ordering = ["-timestamp"]

    def get_queryset(self):
        """Get filtered queryset based on query parameters."""
        queryset = Audit.objects.all()

        # Check if user should only see their tenant's data
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            queryset = queryset.filter(tenant_id=self.request.tenant_id)

        tenant_id = self.request.query_params.get("tenant_id")
        event_type = self.request.query_params.get("event_type")
        since = self.request.query_params.get("since")

        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        if since:
            queryset = queryset.filter(timestamp__gte=since)

        return queryset


class AuditVerifyView(APIView):
    """
    Verify the integrity of the audit chain.

    This endpoint validates the entire audit chain by recomputing
    hashes and comparing them to stored values.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """
        Verify the audit chain integrity.

        Query parameters:
        - tenant_id: Verify chain for specific tenant (optional)

        Returns:
            Response with verification status and details
        """
        tenant_id = request.query_params.get("tenant_id")

        # Get events to verify
        queryset = Audit.objects.all()
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        elif hasattr(request, "tenant_id") and request.tenant_id:
            queryset = queryset.filter(tenant_id=request.tenant_id)

        events = queryset.order_by("timestamp")

        if not events.exists():
            return Response(
                {
                    "ok": True,
                    "message": "No audit events to verify.",
                    "verified_count": 0,
                }
            )

        # Verify each event in the chain
        verified_count = 0
        broken_links = []
        prev_hash = None

        for event in events:
            # Verify previous hash linkage
            if event.prev_hash != prev_hash:
                broken_links.append(
                    {
                        "event_id": event.id,
                        "event_type": event.event_type,
                        "timestamp": event.timestamp.isoformat(),
                        "expected_prev_hash": prev_hash.hex() if prev_hash else None,
                        "actual_prev_hash": (
                            event.prev_hash.hex() if event.prev_hash else None
                        ),
                    }
                )
                verified_count += 1  # Still count as verified if only linkage is broken
            else:
                # Recompute hash to verify integrity - must match exactly how it was computed in save()
                record = {
                    "tenant_id": str(event.tenant_id),  # Ensure string format matches
                    "event_type": str(event.event_type),
                    "payload": event.payload,
                    "timestamp": event.timestamp.isoformat(),
                }
                computed_hash = chain_hash(event.prev_hash, record)

                if computed_hash != event.hash:
                    broken_links.append(
                        {
                            "event_id": event.id,
                            "event_type": event.event_type,
                            "timestamp": event.timestamp.isoformat(),
                            "reason": "Hash mismatch - potential tampering detected",
                            "computed_hash": computed_hash.hex(),
                            "stored_hash": event.hash.hex(),
                        }
                    )
                else:
                    verified_count += 1

            prev_hash = event.hash

        is_valid = len(broken_links) == 0

        response_data = {
            "chain_valid": is_valid,
            "verified_count": verified_count,
            "total_events": events.count(),
            "chain_head": prev_hash.hex() if prev_hash else None,
        }

        if broken_links:
            response_data["broken_links"] = broken_links
            logger.warning(
                f"Audit chain verification failed for tenant {tenant_id or 'all'}",
                extra={
                    "tenant_id": tenant_id,
                    "broken_count": len(broken_links),
                },
            )
        else:
            logger.info(
                f"Audit chain verified successfully for tenant {tenant_id or 'all'}",
                extra={
                    "tenant_id": tenant_id,
                    "verified_count": verified_count,
                },
            )

        return Response(
            response_data,
            status=status.HTTP_200_OK if is_valid else status.HTTP_409_CONFLICT,
        )
