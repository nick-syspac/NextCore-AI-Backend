from django.contrib import admin
from .models import UserInvitation, EmailVerification, UserProfile


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
    readonly_fields = ("token", "created_at", "accepted_at", "accepted_by")

    fieldsets = (
        ("Invitation Details", {"fields": ("tenant", "email", "role", "message")}),
        ("Status", {"fields": ("status", "token", "invited_by", "accepted_by")}),
        ("Dates", {"fields": ("created_at", "expires_at", "accepted_at")}),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "verified", "created_at", "verified_at")
    list_filter = ("verified", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("token", "created_at", "verified_at")
