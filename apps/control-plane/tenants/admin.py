"""
Admin configuration for tenant models.
"""

from django.contrib import admin
from .models import Tenant, TenantUser, TenantQuota, TenantAPIKey


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "status", "subscription_tier", "created_at"]
    list_filter = ["status", "subscription_tier", "created_at"]
    search_fields = ["name", "slug", "contact_email"]
    readonly_fields = ["id", "created_at", "updated_at", "activated_at", "suspended_at"]
    fieldsets = [
        (
            "Basic Information",
            {"fields": ["id", "name", "slug", "domain", "status", "subscription_tier"]},
        ),
        (
            "Contact Information",
            {"fields": ["contact_name", "contact_email", "contact_phone"]},
        ),
        (
            "Legal Business Information",
            {
                "fields": [
                    "registered_business_name",
                    "trading_name",
                    "abn",
                    "acn",
                    "business_structure",
                    "gst_registered",
                    "registered_address",
                    "postal_address",
                ]
            },
        ),
        ("Billing", {"fields": ["billing_email", "stripe_customer_id"]}),
        (
            "Metadata",
            {
                "fields": [
                    "created_at",
                    "updated_at",
                    "activated_at",
                    "suspended_at",
                    "suspension_reason",
                ]
            },
        ),
        ("Settings", {"fields": ["settings"], "classes": ["collapse"]}),
    ]


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ["user", "tenant", "role", "created_at"]
    list_filter = ["role", "created_at"]
    search_fields = ["user__username", "user__email", "tenant__name"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(TenantQuota)
class TenantQuotaAdmin(admin.ModelAdmin):
    list_display = [
        "tenant",
        "api_calls_used",
        "api_calls_limit",
        "ai_tokens_used",
        "ai_tokens_limit",
    ]
    search_fields = ["tenant__name"]
    readonly_fields = ["updated_at", "last_reset_at"]


@admin.register(TenantAPIKey)
class TenantAPIKeyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "tenant",
        "key_prefix",
        "is_active",
        "created_at",
        "expires_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "tenant__name", "key_prefix"]
    readonly_fields = ["id", "key_prefix", "key_hash", "created_at", "last_used_at"]
