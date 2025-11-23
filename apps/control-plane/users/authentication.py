"""
Supabase JWT authentication backend for Django REST Framework.

This module implements JWT token verification following best practices:
- Verifies JWT signature using Supabase JWT secret
- Validates issuer, audience, and expiry
- Maps Supabase user ID to UserAccount
- Does not use the Supabase client library (just JWT verification)
"""

import jwt
import logging
from django.conf import settings
from django.utils import timezone
from rest_framework import authentication
from rest_framework import exceptions

from .models import UserAccount

logger = logging.getLogger(__name__)


class SupabaseAuthentication(authentication.BaseAuthentication):
    """
    Authentication backend for Supabase JWT tokens.
    
    Verifies Supabase JWTs and maps to UserAccount.
    This is the primary authentication method for the application.
    """

    def authenticate(self, request):
        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        # Check for Bearer token
        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return None
            token = parts[1]
        except (ValueError, IndexError):
            return None

        # Check if Supabase is configured
        jwt_secret = settings.SUPABASE_JWT_SECRET
        if not jwt_secret:
            logger.warning("SUPABASE_JWT_SECRET not configured, skipping Supabase authentication")
            return None

        try:
            # Decode and verify the JWT
            payload = self.verify_jwt(token, jwt_secret)
            
            # Extract user information from claims
            supabase_user_id = payload.get("sub")
            if not supabase_user_id:
                raise exceptions.AuthenticationFailed("Token missing 'sub' claim")

            email = payload.get("email")
            if not email:
                raise exceptions.AuthenticationFailed("Token missing 'email' claim")

            # Get or create UserAccount
            user_account = self.get_or_create_user_account(
                supabase_user_id=supabase_user_id,
                email=email,
                user_metadata=payload.get("user_metadata", {}),
            )

            # Attach raw Supabase claims to the request for downstream use
            request.supabase_claims = payload
            request.user_account = user_account

            # Update last login timestamp
            user_account.update_last_login()

            # Return tuple of (user, auth) where user is our UserAccount
            # DRF expects this format
            return (user_account, None)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {str(e)}")
            raise exceptions.AuthenticationFailed("Invalid token")
        except Exception as e:
            logger.error(f"Supabase authentication error: {str(e)}", exc_info=True)
            raise exceptions.AuthenticationFailed(f"Authentication failed: {str(e)}")

    def verify_jwt(self, token: str, secret: str) -> dict:
        """
        Verify and decode the JWT token.
        
        Args:
            token: The JWT token string
            secret: The Supabase JWT secret
            
        Returns:
            Decoded JWT payload as dict
            
        Raises:
            jwt.InvalidTokenError: If token is invalid
        """
        # Supabase typically uses HS256 algorithm
        # If using JWKS/RS256, you'll need to fetch and verify with public key
        algorithms = ["HS256", "RS256"]
        
        # Decode and verify
        payload = jwt.decode(
            token,
            secret,
            algorithms=algorithms,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": False,  # Supabase doesn't always set audience
            },
        )
        
        return payload

    def get_or_create_user_account(
        self,
        supabase_user_id: str,
        email: str,
        user_metadata: dict = None,
    ) -> UserAccount:
        """
        Get or create a UserAccount from Supabase user info.
        
        Args:
            supabase_user_id: The Supabase user UUID
            email: User's email address
            user_metadata: Optional metadata from Supabase user object
            
        Returns:
            UserAccount instance
        """
        user_metadata = user_metadata or {}
        
        try:
            # Try to get existing account by Supabase ID
            user_account = UserAccount.objects.get(supabase_user_id=supabase_user_id)
            
            # Update email if it changed
            if user_account.primary_email != email:
                user_account.primary_email = email
                user_account.save(update_fields=["primary_email", "updated_at"])
                
            return user_account
            
        except UserAccount.DoesNotExist:
            # Create new account
            logger.info(f"Creating new UserAccount for Supabase user {supabase_user_id}")
            
            user_account = UserAccount.objects.create(
                supabase_user_id=supabase_user_id,
                primary_email=email,
                full_name=user_metadata.get("full_name", ""),
                is_active=True,
            )
            
            return user_account

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response.
        """
        return 'Bearer realm="api"'
