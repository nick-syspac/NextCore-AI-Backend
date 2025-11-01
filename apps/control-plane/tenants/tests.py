"""
Tests for tenant management functionality.
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Tenant, TenantUser, TenantQuota, TenantStatus

User = get_user_model()


class TenantModelTestCase(TestCase):
    """Test cases for Tenant model."""

    def test_tenant_creation(self):
        """Test creating a tenant."""
        tenant = Tenant.objects.create(
            name="Test Organization",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        
        self.assertEqual(tenant.status, TenantStatus.PENDING)
        self.assertEqual(tenant.name, "Test Organization")

    def test_tenant_activation(self):
        """Test activating a tenant."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        
        tenant.activate()
        
        self.assertEqual(tenant.status, TenantStatus.ACTIVE)
        self.assertIsNotNone(tenant.activated_at)

    def test_tenant_suspension(self):
        """Test suspending a tenant."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        tenant.activate()
        
        tenant.suspend(reason="Payment overdue")
        
        self.assertEqual(tenant.status, TenantStatus.SUSPENDED)
        self.assertIsNotNone(tenant.suspended_at)
        self.assertEqual(tenant.suspension_reason, "Payment overdue")

    def test_tenant_restore(self):
        """Test restoring a suspended tenant."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        tenant.activate()
        tenant.suspend(reason="Test")
        
        tenant.restore()
        
        self.assertEqual(tenant.status, TenantStatus.ACTIVE)
        self.assertIsNone(tenant.suspended_at)
        self.assertEqual(tenant.suspension_reason, "")


class TenantQuotaTestCase(TestCase):
    """Test cases for TenantQuota model."""

    def test_quota_creation(self):
        """Test creating quota for tenant."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        
        quota = TenantQuota.objects.create(tenant=tenant)
        
        self.assertEqual(quota.api_calls_used, 0)
        self.assertEqual(quota.ai_tokens_used, 0)

    def test_quota_check(self):
        """Test quota checking."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        
        quota = TenantQuota.objects.create(
            tenant=tenant,
            api_calls_limit=100,
            api_calls_used=50,
        )
        
        self.assertTrue(quota.check_api_quota())
        
        quota.api_calls_used = 100
        quota.save()
        
        self.assertFalse(quota.check_api_quota())

    def test_quota_increment(self):
        """Test incrementing quota usage."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        
        quota = TenantQuota.objects.create(tenant=tenant)
        
        quota.increment_api_calls(5)
        quota.refresh_from_db()
        
        self.assertEqual(quota.api_calls_used, 5)

    def test_quota_reset(self):
        """Test resetting monthly quotas."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        
        quota = TenantQuota.objects.create(
            tenant=tenant,
            api_calls_used=100,
            ai_tokens_used=1000,
        )
        
        quota.reset_monthly_quotas()
        
        self.assertEqual(quota.api_calls_used, 0)
        self.assertEqual(quota.ai_tokens_used, 0)
        self.assertIsNotNone(quota.last_reset_at)


class TenantAPITestCase(APITestCase):
    """Test cases for Tenant API endpoints."""

    def setUp(self):
        """Set up test user and authentication."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="admin@example.com",
        )

    def test_create_tenant(self):
        """Test creating a tenant via API."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            "name": "New Organization",
            "slug": "new-org",
            "contact_email": "contact@neworg.com",
            "contact_name": "John Doe",
        }
        
        response = self.client.post("/api/tenants/", data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Organization")

    def test_list_tenants_as_user(self):
        """Test listing tenants as regular user."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        
        # Associate user with tenant
        TenantUser.objects.create(
            tenant=tenant,
            user=self.user,
            role=TenantUser.Role.MEMBER,
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/tenants/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Handle both paginated and non-paginated responses
        data = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        # User should see at least their tenant
        self.assertGreaterEqual(len(data), 1)
        # Verify the user's tenant is in the results
        tenant_slugs = [t['slug'] for t in data]
        self.assertIn('test-org', tenant_slugs)

    def test_activate_tenant(self):
        """Test activating a tenant via API."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f"/api/tenants/{tenant.slug}/activate/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        tenant.refresh_from_db()
        self.assertEqual(tenant.status, TenantStatus.ACTIVE)

    def test_get_quota(self):
        """Test getting quota information."""
        tenant = Tenant.objects.create(
            name="Test Org",
            slug="test-org",
            contact_email="test@example.com",
            contact_name="Test User",
        )
        TenantQuota.objects.create(tenant=tenant)
        
        TenantUser.objects.create(
            tenant=tenant,
            user=self.user,
            role=TenantUser.Role.ADMIN,
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/tenants/{tenant.slug}/quota/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("api_calls_limit", response.data)
