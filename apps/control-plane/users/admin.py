from django.contrib import admin
from .models import UserInvitation, EmailVerification, UserProfile, UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = (
        "primary_email",
        "full_name",
        "is_active",
        "supabase_user_id",
        "created_at",
        "last_login_at",
    )
    list_filter = ("is_active", "created_at", "last_login_at")
    search_fields = ("primary_email", "full_name", "supabase_user_id")
    readonly_fields = ("id", "supabase_user_id", "created_at", "updated_at", "last_login_at")
    
    fieldsets = (
        ("Identity", {
            "fields": ("id", "supabase_user_id", "primary_email")
        }),
        ("Profile", {
            "fields": ("full_name", "is_active", "metadata")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "last_login_at")
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "supabase_user_id", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "supabase_user_id")
    readonly_fields = ("created_at", "updated_at")


@admin.register(UserInvitation)
class UserInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "tenant",
        "role",
        "status",
        "invited_by",
        "created_at",
        "expires_at",
    )
    list_filter = ("status", "role", "created_at")
    search_fields = ("email", "tenant__name")
    readonly_fields = ("token", "created_at", "accepted_at", "accepted_by", "accepted_by_account")

    fieldsets = (
        ("Invitation Details", {"fields": ("tenant", "email", "role", "message")}),
        ("Status", {"fields": ("status", "token", "invited_by")}),
        ("Acceptance", {"fields": ("accepted_by_account", "accepted_by")}),
        ("Dates", {"fields": ("created_at", "expires_at", "accepted_at")}),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "verified", "created_at", "verified_at")
    list_filter = ("verified", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("token", "created_at", "verified_at")
