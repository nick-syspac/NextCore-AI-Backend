"""
Tenant models for multi-tenancy support.
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.utils import timezone

User = get_user_model()


class TenantStatus(models.TextChoices):
    """Status choices for tenants."""

    ACTIVE = "active", "Active"
    SUSPENDED = "suspended", "Suspended"
    PENDING = "pending", "Pending"
    DEACTIVATED = "deactivated", "Deactivated"


class SubscriptionTier(models.TextChoices):
    """Subscription tier choices."""

    FREE = "free", "Free"
    BASIC = "basic", "Basic"
    PROFESSIONAL = "professional", "Professional"
    ENTERPRISE = "enterprise", "Enterprise"


class BusinessStructure(models.TextChoices):
    """Business structure choices."""

    SOLE_TRADER = "sole_trader", "Sole Trader"
    PARTNERSHIP = "partnership", "Partnership"
    COMPANY = "company", "Company (Pty Ltd)"
    TRUST = "trust", "Trust"
    INCORPORATED_ASSOCIATION = "incorporated_association", "Incorporated Association"


class Tenant(models.Model):
    """
    Represents a tenant in the multi-tenant system.

    Each tenant represents a separate organization/customer with isolated data.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Organization name")
    slug = models.SlugField(
        max_length=255, unique=True, help_text="URL-safe identifier"
    )
    domain = models.CharField(
        max_length=255, blank=True, help_text="Custom domain (optional)"
    )

    status = models.CharField(
        max_length=20,
        choices=TenantStatus.choices,
        default=TenantStatus.PENDING,
    )

    subscription_tier = models.CharField(
        max_length=20,
        choices=SubscriptionTier.choices,
        default=SubscriptionTier.FREE,
    )

    # Contact Information
    contact_email = models.EmailField(validators=[EmailValidator()])
    contact_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=50, blank=True)

    # Legal Business Information
    registered_business_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="ASIC-registered business name"
    )
    trading_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Trading name (if different from registered name)"
    )
    abn = models.CharField(
        max_length=11,
        blank=True,
        help_text="Australian Business Number (11 digits)"
    )
    acn = models.CharField(
        max_length=9,
        blank=True,
        help_text="Australian Company Number (9 digits, required for companies)"
    )
    business_structure = models.CharField(
        max_length=30,
        choices=BusinessStructure.choices,
        blank=True,
        help_text="Legal structure of the business"
    )
    gst_registered = models.BooleanField(
        default=False,
        help_text="Is the business registered for GST?"
    )
    registered_address = models.TextField(
        blank=True,
        help_text="Registered business address"
    )
    postal_address = models.TextField(
        blank=True,
        help_text="Postal address (if different from registered address)"
    )

    # Billing
    billing_email = models.EmailField(blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    suspended_at = models.DateTimeField(null=True, blank=True)
    suspension_reason = models.TextField(blank=True)

    # Settings
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.slug})"

    def activate(self):
        """Activate the tenant."""
        self.status = TenantStatus.ACTIVE
        self.activated_at = timezone.now()
        self.save()

    def suspend(self, reason: str = ""):
        """Suspend the tenant."""
        self.status = TenantStatus.SUSPENDED
        self.suspended_at = timezone.now()
        self.suspension_reason = reason
        self.save()

    def restore(self):
        """Restore a suspended tenant."""
        if self.status == TenantStatus.SUSPENDED:
            self.status = TenantStatus.ACTIVE
            self.suspended_at = None
            self.suspension_reason = ""
            self.save()


class TenantUser(models.Model):
    """
    Maps users to tenants with role-based access (TenantMembership).

    A user can belong to multiple tenants with different roles.
    Supports both legacy Django User and new UserAccount models.
    """

    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"
        VIEWER = "viewer", "Viewer"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INVITED = "invited", "Invited"
        PENDING = "pending", "Pending"
        SUSPENDED = "suspended", "Suspended"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users")
    
    # Support both legacy Django User and new UserAccount
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="tenant_memberships",
        null=True,
        blank=True,
    )
    user_account = models.ForeignKey(
        'users.UserAccount',
        on_delete=models.CASCADE,
        related_name="tenant_memberships",
        null=True,
        blank=True,
    )
    
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["tenant", "user"], ["tenant", "user_account"]]
        ordering = ["tenant", "role"]
        indexes = [
            models.Index(fields=["tenant", "status"]),
            models.Index(fields=["user_account", "status"]),
        ]

    def __str__(self):
        if self.user_account:
            return f"{self.user_account.primary_email} - {self.tenant.name} ({self.role})"
        elif self.user:
            return f"{self.user.username} - {self.tenant.name} ({self.role})"
        return f"TenantUser {self.id}"

    def get_email(self):
        """Get the email for this membership."""
        if self.user_account:
            return self.user_account.primary_email
        elif self.user:
            return self.user.email
        return None


class TenantQuota(models.Model):
    """
    Tracks usage quotas and limits for tenants.
    """

    tenant = models.OneToOneField(
        Tenant, on_delete=models.CASCADE, related_name="quota"
    )

    # API Quotas
    api_calls_limit = models.IntegerField(
        default=10000, help_text="API calls per month"
    )
    api_calls_used = models.IntegerField(default=0)

    # AI Gateway Quotas
    ai_tokens_limit = models.IntegerField(
        default=100000, help_text="AI tokens per month"
    )
    ai_tokens_used = models.IntegerField(default=0)

    # Storage Quotas
    storage_limit_gb = models.FloatField(default=10.0, help_text="Storage limit in GB")
    storage_used_gb = models.FloatField(default=0.0)

    # User Quotas
    max_users = models.IntegerField(default=5, help_text="Maximum number of users")
    current_users = models.IntegerField(default=0)

    # Reset tracking
    quota_reset_at = models.DateTimeField(default=timezone.now)
    last_reset_at = models.DateTimeField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Tenant quotas"

    def __str__(self):
        return f"Quota for {self.tenant.name}"

    def reset_monthly_quotas(self):
        """Reset monthly usage counters."""
        self.api_calls_used = 0
        self.ai_tokens_used = 0
        self.last_reset_at = timezone.now()
        self.quota_reset_at = timezone.now() + timezone.timedelta(days=30)
        self.save()

    def check_api_quota(self) -> bool:
        """Check if tenant has available API quota."""
        return self.api_calls_used < self.api_calls_limit

    def check_ai_token_quota(self, tokens: int = 0) -> bool:
        """Check if tenant has available AI token quota."""
        return (self.ai_tokens_used + tokens) < self.ai_tokens_limit

    def increment_api_calls(self, count: int = 1):
        """Increment API call usage."""
        self.api_calls_used += count
        self.save(update_fields=["api_calls_used", "updated_at"])

    def increment_ai_tokens(self, count: int):
        """Increment AI token usage."""
        self.ai_tokens_used += count
        self.save(update_fields=["ai_tokens_used", "updated_at"])


class TenantAPIKey(models.Model):
    """
    API keys for tenant authentication.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="api_keys"
    )
    name = models.CharField(max_length=255, help_text="Key description")
    description = models.TextField(
        blank=True, help_text="Optional description of key usage"
    )
    key_prefix = models.CharField(max_length=16, editable=False)
    key_hash = models.CharField(max_length=128, editable=False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    # Permissions
    scopes = models.JSONField(default=list, help_text="List of allowed scopes")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tenant.name} - {self.name}"

    def is_expired(self) -> bool:
        """Check if the API key has expired."""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at

    def is_valid(self) -> bool:
        """Check if the API key is valid for use."""
        return self.is_active and not self.is_expired()

    @staticmethod
    def generate_key():
        """Generate a new API key."""
        import secrets

        return f"nc_{secrets.token_urlsafe(32)}"

    @staticmethod
    def hash_key(key: str) -> str:
        """Hash an API key for storage."""
        import hashlib

        return hashlib.sha256(key.encode()).hexdigest()

    def save(self, *args, **kwargs):
        """Override save to generate key_prefix and key_hash if needed."""
        # This is handled in the serializer's create method instead
        super().save(*args, **kwargs)
