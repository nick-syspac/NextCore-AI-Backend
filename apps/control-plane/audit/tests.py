"""
Tests for audit functionality.
"""
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Audit, Outbox, chain_hash

User = get_user_model()


class AuditModelTestCase(TestCase):
    """Test cases for Audit model."""

    def test_audit_creation(self):
        """Test creating an audit event."""
        audit = Audit.objects.create(
            tenant_id="test-tenant",
            event_type="user.created",
            payload={"user_id": "123", "email": "test@example.com"},
        )
        
        self.assertIsNotNone(audit.hash)
        self.assertIsNone(audit.prev_hash)
        self.assertEqual(audit.tenant_id, "test-tenant")

    def test_audit_chain(self):
        """Test audit chain integrity."""
        # Create first event
        audit1 = Audit.objects.create(
            tenant_id="test-tenant",
            event_type="user.created",
            payload={"user_id": "123"},
        )
        
        # Create second event
        audit2 = Audit.objects.create(
            tenant_id="test-tenant",
            event_type="user.updated",
            payload={"user_id": "123", "name": "John"},
        )
        
        # Verify chain
        self.assertEqual(audit2.prev_hash, audit1.hash)
        self.assertIsNone(audit1.prev_hash)

    def test_audit_hash_computation(self):
        """Test hash computation."""
        prev_hash = b"test"
        record = {
            "tenant_id": "test",
            "event_type": "test.event",
            "payload": {"key": "value"},
            "timestamp": "2024-01-01T00:00:00",
        }
        
        hash1 = chain_hash(prev_hash, record)
        hash2 = chain_hash(prev_hash, record)
        
        # Same input should produce same hash
        self.assertEqual(hash1, hash2)
        
        # Different input should produce different hash
        record["payload"]["key"] = "different"
        hash3 = chain_hash(prev_hash, record)
        self.assertNotEqual(hash1, hash3)


class AuditAPITestCase(APITestCase):
    """Test cases for Audit API endpoints."""

    def setUp(self):
        """Set up test user and authentication."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_list_audit_events(self):
        """Test listing audit events."""
        # Create test data
        Audit.objects.create(
            tenant_id="tenant1",
            event_type="user.created",
            payload={"user_id": "123"},
        )
        Audit.objects.create(
            tenant_id="tenant1",
            event_type="user.updated",
            payload={"user_id": "123"},
        )
        
        response = self.client.get("/api/audit/events/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  # At least 2 events

    def test_filter_by_tenant(self):
        """Test filtering audit events by tenant."""
        Audit.objects.create(
            tenant_id="tenant1",
            event_type="user.created",
            payload={"user_id": "123"},
        )
        Audit.objects.create(
            tenant_id="tenant2",
            event_type="user.created",
            payload={"user_id": "456"},
        )
        
        response = self.client.get("/api/audit/events/?tenant_id=tenant1")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # At least 1 event for tenant1
        # Verify all returned events are for tenant1
        for event in response.data:
            self.assertEqual(event["tenant_id"], "tenant1")

    def test_verify_chain(self):
        """Test chain verification endpoint."""
        # Create some events
        Audit.objects.create(
            tenant_id="tenant1",
            event_type="user.created",
            payload={"user_id": "123"},
        )
        Audit.objects.create(
            tenant_id="tenant1",
            event_type="user.updated",
            payload={"user_id": "123"},
        )
        
        response = self.client.get("/api/audit/verify/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["chain_valid"])
        self.assertEqual(response.data["verified_count"], 2)


class OutboxTestCase(TestCase):
    """Test cases for Outbox model."""

    def test_outbox_creation(self):
        """Test creating outbox entry."""
        audit = Audit.objects.create(
            tenant_id="test-tenant",
            event_type="user.created",
            payload={"user_id": "123"},
        )
        
        outbox = Outbox.objects.create(audit_event=audit)
        
        self.assertIsNone(outbox.processed_at)
        self.assertEqual(outbox.audit_event, audit)

    def test_outbox_processing(self):
        """Test marking outbox as processed."""
        audit = Audit.objects.create(
            tenant_id="test-tenant",
            event_type="user.created",
            payload={"user_id": "123"},
        )
        
        outbox = Outbox.objects.create(audit_event=audit)
        outbox.processed_at = timezone.now()
        outbox.save()
        
        self.assertIsNotNone(outbox.processed_at)

