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


class Tenant(models.Model):
    """
    Represents a tenant in the multi-tenant system.
    
    Each tenant represents a separate organization/customer with isolated data.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Organization name")
    slug = models.SlugField(max_length=255, unique=True, help_text="URL-safe identifier")
    domain = models.CharField(max_length=255, blank=True, help_text="Custom domain (optional)")
    
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
    Maps users to tenants with role-based access.
    
    A user can belong to multiple tenants with different roles.
    """
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"
        VIEWER = "viewer", "Viewer"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tenant_memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [["tenant", "user"]]
        ordering = ["tenant", "role"]

    def __str__(self):
        return f"{self.user.username} - {self.tenant.name} ({self.role})"


class TenantQuota(models.Model):
    """
    Tracks usage quotas and limits for tenants.
    """
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name="quota")
    
    # API Quotas
    api_calls_limit = models.IntegerField(default=10000, help_text="API calls per month")
    api_calls_used = models.IntegerField(default=0)
    
    # AI Gateway Quotas
    ai_tokens_limit = models.IntegerField(default=100000, help_text="AI tokens per month")
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
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="api_keys")
    name = models.CharField(max_length=255, help_text="Key description")
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
