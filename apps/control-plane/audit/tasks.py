from celery import shared_task
from django.utils import timezone
from .models import Outbox
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_outbox():
    """
    Process pending outbox events and send them to the message broker.
    
    This task is scheduled to run periodically via Celery Beat.
    """
    events = Outbox.objects.filter(processed_at__isnull=True).order_by('created_at')
    processed_count = 0
    
    for event in events:
        try:
            # In a real implementation, you would send this to EventBridge/Kafka/SNS
            logger.info(
                f"Processing audit event: {event.audit_event.id}",
                extra={
                    "event_id": event.audit_event.id,
                    "event_type": event.audit_event.event_type,
                    "tenant_id": event.audit_event.tenant_id,
                }
            )
            
            # TODO: Implement actual message broker integration
            # Example: send_to_eventbridge(event.audit_event)
            # Example: kafka_producer.send('audit-events', event.audit_event.to_dict())
            
            event.processed_at = timezone.now()
            event.save()
            processed_count += 1
            
        except Exception as e:
            logger.error(
                f"Error processing outbox event {event.id}: {e}",
                extra={"event_id": event.id, "error": str(e)},
                exc_info=True
            )
    
    logger.info(f"Processed {processed_count} outbox events")
    return processed_count
