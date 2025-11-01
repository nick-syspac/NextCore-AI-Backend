from django.contrib import admin
from .models import UserInvitation, EmailVerification


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
