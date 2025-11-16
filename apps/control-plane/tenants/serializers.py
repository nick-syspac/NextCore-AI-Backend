"""
Serializers for tenant management.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tenant, TenantUser, TenantQuota, TenantAPIKey

User = get_user_model()


class TenantQuotaSerializer(serializers.ModelSerializer):
    """Serializer for tenant quota information."""

    api_calls_percentage = serializers.SerializerMethodField()
    ai_tokens_percentage = serializers.SerializerMethodField()
    storage_percentage = serializers.SerializerMethodField()

    class Meta:
        model = TenantQuota
        fields = [
            "api_calls_limit",
            "api_calls_used",
            "api_calls_percentage",
            "ai_tokens_limit",
            "ai_tokens_used",
            "ai_tokens_percentage",
            "storage_limit_gb",
            "storage_used_gb",
            "storage_percentage",
            "max_users",
            "current_users",
            "quota_reset_at",
            "last_reset_at",
        ]
        read_only_fields = [
            "api_calls_used",
            "ai_tokens_used",
            "storage_used_gb",
            "current_users",
            "last_reset_at",
        ]

    def get_api_calls_percentage(self, obj):
        if obj.api_calls_limit == 0:
            return 0
        return round((obj.api_calls_used / obj.api_calls_limit) * 100, 2)

    def get_ai_tokens_percentage(self, obj):
        if obj.ai_tokens_limit == 0:
            return 0
        return round((obj.ai_tokens_used / obj.ai_tokens_limit) * 100, 2)

    def get_storage_percentage(self, obj):
        if obj.storage_limit_gb == 0:
            return 0
        return round((obj.storage_used_gb / obj.storage_limit_gb) * 100, 2)


class TenantSerializer(serializers.ModelSerializer):
    """Serializer for tenant information."""

    quota = TenantQuotaSerializer(read_only=True)
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = [
            "id",
            "name",
            "slug",
            "domain",
            "status",
            "subscription_tier",
            "contact_email",
            "contact_name",
            "contact_phone",
            "registered_business_name",
            "trading_name",
            "abn",
            "acn",
            "business_structure",
            "registered_address",
            "postal_address",
            "billing_email",
            "created_at",
            "updated_at",
            "activated_at",
            "suspended_at",
            "suspension_reason",
            "settings",
            "quota",
            "user_count",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "activated_at",
            "suspended_at",
        ]

    def get_user_count(self, obj):
        return obj.users.count()


class TenantCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new tenant."""

    class Meta:
        model = Tenant
        fields = [
            "name",
            "slug",
            "domain",
            "subscription_tier",
            "contact_email",
            "contact_name",
            "contact_phone",
            "registered_business_name",
            "trading_name",
            "abn",
            "acn",
            "business_structure",
            "gst_registered",
            "registered_address",
            "postal_address",
            "billing_email",
        ]

    def create(self, validated_data):
        # Create tenant
        tenant = Tenant.objects.create(**validated_data)

        # Create default quota
        TenantQuota.objects.create(tenant=tenant)

        return tenant


class TenantUserSerializer(serializers.ModelSerializer):
    """Serializer for tenant user relationships."""

    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)

    class Meta:
        model = TenantUser
        fields = [
            "id",
            "tenant",
            "tenant_name",
            "user",
            "user_email",
            "user_username",
            "role",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TenantAPIKeySerializer(serializers.ModelSerializer):
    """Serializer for API keys."""

    tenant = serializers.PrimaryKeyRelatedField(
        queryset=Tenant.objects.all(), write_only=True
    )
    key = serializers.CharField(
        read_only=True, help_text="Full API key (only returned on creation)"
    )

    class Meta:
        model = TenantAPIKey
        fields = [
            "id",
            "tenant",
            "name",
            "description",
            "key",
            "key_prefix",
            "is_active",
            "created_at",
            "last_used_at",
            "expires_at",
            "scopes",
        ]
        read_only_fields = [
            "id",
            "key",
            "key_prefix",
            "created_at",
            "last_used_at",
        ]

    def create(self, validated_data):
        """Create a new API key with generated key."""
        # Generate the actual API key
        api_key = TenantAPIKey.generate_key()

        # Extract the prefix (first 8 characters after "nc_")
        key_prefix = api_key[:11]  # "nc_" + first 8 chars

        # Hash the key for storage
        key_hash = TenantAPIKey.hash_key(api_key)

        # Create the API key object
        api_key_obj = TenantAPIKey.objects.create(
            **validated_data, key_prefix=key_prefix, key_hash=key_hash
        )

        # Attach the plain key to the instance (not saved to DB)
        # This allows us to return it once
        api_key_obj._plain_key = api_key

        return api_key_obj

    def to_representation(self, instance):
        """Include the plain key only when it's available (on creation)."""
        representation = super().to_representation(instance)

        # If the instance has a _plain_key attribute, include it
        if hasattr(instance, "_plain_key"):
            representation["key"] = instance._plain_key
        else:
            # Remove the key field from response if not creating
            representation.pop("key", None)

        return representation
