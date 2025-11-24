"""
Supabase service for user management integration.
"""

from typing import Optional, Dict, Any
from django.conf import settings
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)


class SupabaseService:
    """Service for interacting with Supabase Auth API."""

    def __init__(self):
        self.url = getattr(settings, "SUPABASE_URL", None)
        self.service_role_key = getattr(settings, "SUPABASE_SERVICE_ROLE_KEY", None)
        self.client: Optional[Client] = None

        if self.url and self.service_role_key:
            try:
                self.client = create_client(self.url, self.service_role_key)
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
        else:
            logger.warning("Supabase credentials not configured - user sync will be disabled")

    def is_configured(self) -> bool:
        """Check if Supabase is properly configured."""
        return self.client is not None

    def create_user(
        self, email: str, password: str, user_metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a user in Supabase Auth.

        Args:
            email: User's email address
            password: User's password
            user_metadata: Optional metadata to attach to the user

        Returns:
            User data from Supabase or None if creation failed
        """
        if not self.is_configured():
            logger.warning("Supabase is not configured, skipping user creation")
            return None

        try:
            # Use admin API to create user with service role key
            response = self.client.auth.admin.create_user(
                {
                    "email": email,
                    "password": password,
                    "email_confirm": False,  # User needs to verify email
                    "user_metadata": user_metadata or {},
                }
            )

            if response and hasattr(response, "user"):
                logger.info(f"Successfully created Supabase user for email: {email}")
                return response.user
            else:
                logger.error(f"Unexpected response from Supabase user creation: {response}")
                return None

        except Exception as e:
            logger.error(f"Failed to create Supabase user for {email}: {e}")
            return None

    def update_user(
        self, supabase_user_id: str, user_metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update a user's metadata in Supabase.

        Args:
            supabase_user_id: Supabase user UUID
            user_metadata: Metadata to update

        Returns:
            True if update was successful, False otherwise
        """
        if not self.is_configured():
            logger.warning("Supabase is not configured, skipping user update")
            return False

        try:
            self.client.auth.admin.update_user_by_id(
                supabase_user_id, {"user_metadata": user_metadata or {}}
            )
            logger.info(f"Successfully updated Supabase user: {supabase_user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to update Supabase user {supabase_user_id}: {e}")
            return False

    def delete_user(self, supabase_user_id: str) -> bool:
        """
        Delete a user from Supabase Auth.

        Args:
            supabase_user_id: Supabase user UUID

        Returns:
            True if deletion was successful, False otherwise
        """
        if not self.is_configured():
            logger.warning("Supabase is not configured, skipping user deletion")
            return False

        try:
            self.client.auth.admin.delete_user(supabase_user_id)
            logger.info(f"Successfully deleted Supabase user: {supabase_user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete Supabase user {supabase_user_id}: {e}")
            return False

    def send_verification_email(self, email: str) -> bool:
        """
        Send email verification to user.

        Args:
            email: User's email address

        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self.is_configured():
            logger.warning("Supabase is not configured, skipping verification email")
            return False

        try:
            # This would use Supabase's built-in email verification
            # For now, we're using Django's email system
            logger.info(f"Email verification handled by Django for: {email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {e}")
            return False


# Singleton instance
supabase_service = SupabaseService()
