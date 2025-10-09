from celery import shared_task
from .models import Outbox
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_outbox():
    events = Outbox.objects.filter(processed_at__isnull=True).order_by('created_at')
    for event in events:
        try:
            # In a real implementation, you would send this to EventBridge/Kafka
            logger.info(f"Processing audit event: {event.audit_event.id}")
            
            # Simulate sending to a message broker
            print(f"Delivering event {event.audit_event.id} to message broker")
            
            event.processed_at = timezone.now()
            event.save()
        except Exception as e:
            logger.error(f"Error processing outbox event {event.id}: {e}")
