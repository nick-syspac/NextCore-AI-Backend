import hashlib
import json
from django.db import models

def chain_hash(prev_hash: bytes|None, record: dict) -> bytes:
    m = hashlib.sha256()
    if prev_hash: m.update(prev_hash)
    m.update(json.dumps(record, sort_keys=True).encode())
    return m.digest()

class Audit(models.Model):
    tenant_id = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    payload = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    prev_hash = models.BinaryField(null=True, blank=True)
    hash = models.BinaryField()

    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        last_event = Audit.objects.filter(tenant_id=self.tenant_id).last()
        prev_hash = last_event.hash if last_event else None
        self.prev_hash = prev_hash
        record = {
            "tenant_id": self.tenant_id,
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
        }
        self.hash = chain_hash(prev_hash, record)
        super().save(*args, **kwargs)

class Outbox(models.Model):
    audit_event = models.ForeignKey(Audit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']