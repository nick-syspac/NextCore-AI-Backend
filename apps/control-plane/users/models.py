"""
Models for user invitations and email verification.
"""

import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tenants.models import Tenant


class UserInvitation(models.Model):
    """Model for tenant user invitations."""

    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
        ("viewer", "Viewer"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    invited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_invitations"
    )

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_invitations",
    )

    message = models.TextField(
        blank=True, help_text="Optional message to include in invitation email"
    )

    class Meta:
        db_table = "user_invitations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email", "status"]),
            models.Index(fields=["token"]),
        ]

    def __str__(self):
        return f"{self.email} invited to {self.tenant.name} as {self.role}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Default expiration: 7 days
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def is_expired(self):
        """Check if invitation has expired."""
        return timezone.now() > self.expires_at

    def can_accept(self):
        """Check if invitation can be accepted."""
        return self.status == "pending" and not self.is_expired()


class EmailVerification(models.Model):
    """Model for email verification tokens."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="email_verification"
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "email_verifications"

    def __str__(self):
        return f"Email verification for {self.user.username}"

    def is_expired(self):
        """Check if verification token has expired (24 hours)."""
        return timezone.now() > self.created_at + timedelta(hours=24)
