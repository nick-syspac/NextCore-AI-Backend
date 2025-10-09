from functools import wraps
from .models import Audit, Outbox

def audited(event_type, payload_builder):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            payload = payload_builder(result)
            tenant_id = payload.get("tenant_id") # Assumes payload_builder includes tenant_id
            
            audit_event = Audit.objects.create(
                tenant_id=tenant_id,
                event_type=event_type,
                payload=payload
            )
            Outbox.objects.create(audit_event=audit_event)
            
            return result
        return wrapper
    return decorator
