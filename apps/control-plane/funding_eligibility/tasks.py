"""
Celery tasks for funding eligibility system.
Handles external lookups, evaluation, and webhook delivery.
"""

from celery import shared_task
from django.utils import timezone
from django.db import transaction
import logging
import hmac
import hashlib
import json
import requests

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def enqueue_external_lookups(self, request_id: int):
    """
    Enqueue external lookups for an eligibility request.
    Determines which lookups are needed based on input data.
    """
    from .models_extended import EligibilityRequest, ExternalLookup
    from .services.connectors import ConnectorFactory

    try:
        request_obj = EligibilityRequest.objects.get(id=request_id)
        request_obj.status = "evaluating"
        request_obj.save()

        input_data = request_obj.input

        # Determine which lookups are needed
        lookups_needed = []

        # USI validation
        if input_data.get("usi"):
            lookups_needed.append(
                {
                    "provider": "usi",
                    "data": {
                        "usi": input_data["usi"],
                        "first_name": input_data.get("first_name"),
                        "family_name": input_data.get("family_name"),
                        "date_of_birth": input_data.get("date_of_birth"),
                    },
                }
            )

        # Postcode lookup
        if input_data.get("postcode"):
            lookups_needed.append(
                {"provider": "postcode", "data": {"postcode": input_data["postcode"]}}
            )

        # Concession card
        if input_data.get("concession_card"):
            lookups_needed.append(
                {
                    "provider": "concession",
                    "data": {
                        "card_number": input_data["concession_card"].get("number"),
                        "card_type": input_data["concession_card"].get("type"),
                        "holder_name": input_data.get("full_name"),
                    },
                }
            )

        # Visa check
        if input_data.get("passport_number"):
            lookups_needed.append(
                {
                    "provider": "visa",
                    "data": {
                        "passport_number": input_data["passport_number"],
                        "country_of_passport": input_data.get("country_of_passport"),
                        "date_of_birth": input_data.get("date_of_birth"),
                    },
                }
            )

        # Execute lookups
        for lookup_def in lookups_needed:
            perform_external_lookup.delay(
                request_id, lookup_def["provider"], lookup_def["data"]
            )

        logger.info(f"Enqueued {len(lookups_needed)} lookups for request {request_id}")

    except Exception as e:
        logger.error(f"Error enqueuing lookups for request {request_id}: {e}")
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def perform_external_lookup(self, request_id: int, provider: str, lookup_data: dict):
    """
    Perform a single external lookup.
    """
    from .models_extended import EligibilityRequest, ExternalLookup
    from .services.connectors import ConnectorFactory
    import asyncio

    try:
        request_obj = EligibilityRequest.objects.get(id=request_id)

        # Check if already cached
        existing = ExternalLookup.objects.filter(
            request=request_obj,
            provider=provider,
            status="success",
            cached_until__gt=timezone.now(),
        ).first()

        if existing:
            logger.info(f"Using cached {provider} lookup for request {request_id}")
            return

        # Create lookup record
        lookup = ExternalLookup.objects.create(
            request=request_obj,
            provider=provider,
            request_data=lookup_data,
            status="pending",
        )

        # Get connector
        connector_config = {
            "timeout": 30,
            "cache_ttl": 3600,
        }
        connector = ConnectorFactory.create(provider, connector_config)

        # Perform lookup (run async function in sync context)
        result = asyncio.run(connector.lookup(**lookup_data))

        # Update lookup record
        lookup.response_data = result.data
        lookup.status = "success" if result.success else "error"
        lookup.error_message = result.error or ""
        lookup.latency_ms = result.latency_ms
        lookup.cached_until = result.cache_until
        lookup.save()

        logger.info(
            f"Completed {provider} lookup for request {request_id}: {result.success}"
        )

    except Exception as e:
        logger.error(
            f"Error performing {provider} lookup for request {request_id}: {e}"
        )

        # Update lookup as error
        if "lookup" in locals():
            lookup.status = "error"
            lookup.error_message = str(e)
            lookup.save()

        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def evaluate_eligibility(self, request_id: int, ruleset_id: int = None):
    """
    Evaluate eligibility for a request.
    Called after all external lookups complete.
    """
    from .models_extended import EligibilityRequest, Ruleset, EligibilityDecision
    from .services.rules_engine import RulesEngine, EvaluationContext

    try:
        request_obj = EligibilityRequest.objects.get(id=request_id)

        # Check if all lookups complete
        pending_lookups = request_obj.external_lookups.filter(status="pending").count()
        if pending_lookups > 0:
            logger.info(
                f"Request {request_id} has {pending_lookups} pending lookups, retrying..."
            )
            raise self.retry(countdown=30)

        # Get ruleset
        if ruleset_id:
            ruleset = Ruleset.objects.get(id=ruleset_id, status="active")
        else:
            ruleset = Ruleset.objects.filter(
                jurisdiction_code=request_obj.jurisdiction_code, status="active"
            ).first()

        if not ruleset:
            raise ValueError(
                f"No active ruleset for jurisdiction {request_obj.jurisdiction_code}"
            )

        # Collect lookup results
        lookups = {}
        for lookup in request_obj.external_lookups.filter(status="success"):
            if lookup.provider not in lookups:
                lookups[lookup.provider] = {}
            lookups[lookup.provider].update(lookup.response_data)

        # Build context
        context = EvaluationContext(
            input_data=request_obj.input,
            lookups=lookups,
            reference_data={},  # TODO: Load reference tables
            jurisdiction_code=request_obj.jurisdiction_code,
            evaluation_date=timezone.now(),
        )

        # Get artifacts
        artifacts = []
        for artifact in ruleset.artifacts.all():
            artifacts.append(
                {
                    "type": artifact.type,
                    "name": artifact.name,
                    "blob": artifact.blob,
                }
            )

        # Evaluate
        engine = RulesEngine()
        result = engine.evaluate(artifacts, context, ruleset.version)

        # Create decision
        with transaction.atomic():
            decision = EligibilityDecision.objects.create(
                request=request_obj,
                ruleset=ruleset,
                outcome=result.outcome,
                reasons=result.reasons,
                clause_refs=result.clause_refs,
                decision_data=result.details,
                explanation=result.explanation,
                decided_by="system",
            )

            request_obj.status = "evaluated"
            request_obj.evaluated_at = timezone.now()
            request_obj.save()

        logger.info(f"Evaluated request {request_id}: {result.outcome}")

        # Trigger webhook
        deliver_webhook.delay(request_id, "decision.finalized")

        return decision.id

    except Exception as e:
        logger.error(f"Error evaluating request {request_id}: {e}")

        # Mark request as error
        try:
            request_obj = EligibilityRequest.objects.get(id=request_id)
            request_obj.status = "error"
            request_obj.save()
        except:
            pass

        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=5)
def deliver_webhook(self, request_id: int, event_type: str):
    """
    Deliver webhook for an eligibility event.
    """
    from .models_extended import EligibilityRequest, WebhookEndpoint

    try:
        request_obj = EligibilityRequest.objects.get(id=request_id)

        # Find active webhooks for this event
        webhooks = WebhookEndpoint.objects.filter(
            tenant=request_obj.tenant, active=True, events__contains=[event_type]
        )

        for webhook in webhooks:
            # Queue delivery
            deliver_webhook_to_endpoint.delay(
                webhook.id,
                {
                    "event_type": event_type,
                    "request_id": request_id,
                    "person_id": request_obj.person_id,
                    "course_id": request_obj.course_id,
                    "jurisdiction": request_obj.jurisdiction_code,
                    "timestamp": timezone.now().isoformat(),
                },
            )

        logger.info(
            f"Queued webhook delivery for request {request_id}, event {event_type}"
        )

    except Exception as e:
        logger.error(f"Error delivering webhook for request {request_id}: {e}")
        raise self.retry(exc=e, countdown=120)


@shared_task(bind=True, max_retries=5)
def deliver_webhook_to_endpoint(self, endpoint_id: int, payload: dict):
    """
    Deliver webhook to specific endpoint.
    """
    from .models_extended import WebhookEndpoint, WebhookDelivery

    try:
        endpoint = WebhookEndpoint.objects.get(id=endpoint_id)

        # Create or get delivery record
        delivery, created = WebhookDelivery.objects.get_or_create(
            endpoint=endpoint,
            event_type=payload["event_type"],
            payload=payload,
            defaults={"attempt_count": 0},
        )

        if not created:
            delivery.attempt_count += 1
            delivery.save()

        # Generate HMAC signature
        payload_json = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            endpoint.secret.encode(), payload_json.encode(), hashlib.sha256
        ).hexdigest()

        # Send webhook
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
            "X-Webhook-Event": payload["event_type"],
        }

        response = requests.post(
            endpoint.url, json=payload, headers=headers, timeout=30
        )

        # Update delivery
        delivery.status_code = response.status_code
        delivery.response_body = response.text[:1000]  # Truncate

        if response.status_code >= 200 and response.status_code < 300:
            delivery.delivered_at = timezone.now()
            logger.info(f"Webhook delivered to {endpoint.name}: {response.status_code}")
        else:
            logger.warning(
                f"Webhook delivery failed to {endpoint.name}: {response.status_code}"
            )

            # Retry with exponential backoff
            if delivery.attempt_count < 5:
                raise self.retry(countdown=2**delivery.attempt_count * 60)

        delivery.save()

    except requests.RequestException as e:
        logger.error(f"Webhook delivery error to endpoint {endpoint_id}: {e}")

        if "delivery" in locals():
            delivery.error_message = str(e)
            delivery.save()

        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=2 ** (self.request.retries + 1) * 60)

    except Exception as e:
        logger.error(
            f"Unexpected error delivering webhook to endpoint {endpoint_id}: {e}"
        )
        raise


@shared_task
def cleanup_expired_lookups():
    """
    Cleanup expired external lookup cache entries.
    Run daily via Celery beat.
    """
    from .models_extended import ExternalLookup

    try:
        deleted = ExternalLookup.objects.filter(
            cached_until__lt=timezone.now()
        ).delete()

        logger.info(f"Cleaned up {deleted[0]} expired lookup cache entries")

    except Exception as e:
        logger.error(f"Error cleaning up expired lookups: {e}")


@shared_task
def compute_eligibility_metrics():
    """
    Compute eligibility metrics for dashboards.
    Run hourly via Celery beat.
    """
    from .models_extended import EligibilityRequest, EligibilityDecision
    from django.db.models import Count, Q
    from datetime import timedelta

    try:
        # Last 30 days
        since = timezone.now() - timedelta(days=30)

        # Count by outcome
        outcomes = (
            EligibilityDecision.objects.filter(decided_at__gte=since)
            .values("outcome")
            .annotate(count=Count("id"))
        )

        # Count by jurisdiction
        by_jurisdiction = (
            EligibilityRequest.objects.filter(requested_at__gte=since)
            .values("jurisdiction_code")
            .annotate(count=Count("id"))
        )

        # Average processing time
        # TODO: Calculate average time from request to decision

        metrics = {
            "outcomes": list(outcomes),
            "by_jurisdiction": list(by_jurisdiction),
            "computed_at": timezone.now().isoformat(),
        }

        logger.info(f"Computed eligibility metrics: {metrics}")

        # TODO: Store metrics in cache or database

        return metrics

    except Exception as e:
        logger.error(f"Error computing eligibility metrics: {e}")
