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

urlpatterns = [
    # User registration and profile
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('my-tenants/', user_tenants, name='user-tenants'),
    
    # Email verification
    path('verify-email/', verify_email, name='verify-email'),
    path('resend-verification/', resend_verification_email, name='resend-verification'),
    
    # Invitations
    path('invitations/', UserInvitationListCreateView.as_view(), name='invitation-list'),
    path('invitations/<uuid:token>/', get_invitation_details, name='invitation-details'),
    path('accept-invitation/', accept_invitation, name='accept-invitation'),
]

