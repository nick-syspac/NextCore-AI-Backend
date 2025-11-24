"""
URL patterns for user management.
"""

from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileView,
    ChangePasswordView,
    UserInvitationListCreateView,
    user_tenants,
    verify_email,
    resend_verification_email,
    accept_invitation,
    get_invitation_details,
)
from .views_supabase import (
    bootstrap_account,
    user_tenants as supabase_user_tenants,
    user_profile as supabase_user_profile,
    update_profile,
)

urlpatterns = [
    # Legacy User registration and profile (Django User)
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("my-tenants/", user_tenants, name="user-tenants"),
    
    # Supabase User endpoints (new)
    path("bootstrap-account/", bootstrap_account, name="bootstrap-account"),
    path("supabase/profile/", supabase_user_profile, name="supabase-user-profile"),
    path("supabase/profile/update/", update_profile, name="supabase-update-profile"),
    path("supabase/tenants/", supabase_user_tenants, name="supabase-user-tenants"),
    
    # Email verification
    path("verify-email/", verify_email, name="verify-email"),
    path("resend-verification/", resend_verification_email, name="resend-verification"),
    
    # Invitations
    path(
        "invitations/", UserInvitationListCreateView.as_view(), name="invitation-list"
    ),
    path(
        "invitations/<uuid:token>/", get_invitation_details, name="invitation-details"
    ),
    path("accept-invitation/", accept_invitation, name="accept-invitation"),
]
