import uuid
from django.db import models
from django.utils import timezone
from tenants.models import Tenant


class Integration(models.Model):
    """
    Integration model for third-party service integrations.
    Supports: Axcelerate, Canvas, Xero, MYOB
    """

    INTEGRATION_TYPES = [
        # Existing integrations
        ("axcelerate", "Axcelerate"),
        ("canvas", "Canvas LMS"),
        ("xero", "Xero"),
        ("myob", "MYOB"),
        # SMS/RTO Systems
        ("readytech_jr", "ReadyTech JR Plus / Ready Student"),
        ("vettrak", "VETtrak (ReadyTech)"),
        ("eskilled", "eSkilled SMS+LMS"),
        # LMS/Assessment Systems
        ("cloudassess", "CloudAssess"),
        ("coursebox", "Coursebox AI-LMS"),
        ("moodle", "Moodle"),
        ("d2l_brightspace", "D2L Brightspace"),
        # Accounting Systems
        ("quickbooks", "QuickBooks Online"),
        ("sage_intacct", "Sage Intacct"),
        # Payment Gateways
        ("stripe", "Stripe (AU)"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("error", "Error"),
        ("pending", "Pending Setup"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="integrations"
    )
    integration_type = models.CharField(max_length=50, choices=INTEGRATION_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Configuration (stored as JSON)
    config = models.JSONField(
        default=dict, help_text="Integration-specific configuration"
    )

    # OAuth credentials (encrypted in production)
    client_id = models.CharField(max_length=500, blank=True)
    client_secret = models.CharField(max_length=500, blank=True)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)

    # API Configuration
    api_base_url = models.URLField(max_length=500, blank=True)
    api_key = models.CharField(max_length=500, blank=True)
    webhook_url = models.URLField(max_length=500, blank=True)
    webhook_secret = models.CharField(max_length=200, blank=True)

    # Sync settings
    auto_sync_enabled = models.BooleanField(default=False)
    sync_interval_minutes = models.IntegerField(default=60)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    last_sync_status = models.CharField(max_length=50, blank=True)
    last_sync_error = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        db_table = "integrations"
        ordering = ["-created_at"]
        unique_together = [["tenant", "integration_type"]]

    def __str__(self):
        return f"{self.get_integration_type_display()} - {self.tenant.name}"

    def is_token_expired(self):
        """Check if OAuth token is expired"""
        if not self.token_expires_at:
            return True
        return timezone.now() >= self.token_expires_at

    def needs_sync(self):
        """Check if integration needs synchronization"""
        if not self.auto_sync_enabled or not self.last_sync_at:
            return False

        next_sync = self.last_sync_at + timezone.timedelta(
            minutes=self.sync_interval_minutes
        )
        return timezone.now() >= next_sync


class IntegrationLog(models.Model):
    """
    Audit log for integration activities
    """

    ACTION_TYPES = [
        ("connect", "Connected"),
        ("disconnect", "Disconnected"),
        ("sync", "Synced"),
        ("error", "Error"),
        ("config_update", "Configuration Updated"),
        ("webhook", "Webhook Received"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    integration = models.ForeignKey(
        Integration, on_delete=models.CASCADE, related_name="logs"
    )
    action = models.CharField(max_length=50, choices=ACTION_TYPES)
    status = models.CharField(max_length=20)  # success, error, warning
    message = models.TextField()
    details = models.JSONField(default=dict)

    # Request/Response data
    request_data = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "integration_logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.integration} - {self.action} - {self.status}"


class IntegrationMapping(models.Model):
    """
    Field mappings between NextCore and external systems
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    integration = models.ForeignKey(
        Integration, on_delete=models.CASCADE, related_name="mappings"
    )

    # Source and target fields
    source_entity = models.CharField(
        max_length=100
    )  # e.g., 'user', 'course', 'invoice'
    source_field = models.CharField(max_length=100)
    target_entity = models.CharField(max_length=100)
    target_field = models.CharField(max_length=100)

    # Transformation rules
    transform_rule = models.TextField(
        blank=True, help_text="Python expression for data transformation"
    )
    is_bidirectional = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "integration_mappings"
        unique_together = [["integration", "source_entity", "source_field"]]

    def __str__(self):
        return f"{self.integration} - {self.source_entity}.{self.source_field} → {self.target_entity}.{self.target_field}"
