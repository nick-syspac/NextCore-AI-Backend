import os
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from supabase import create_client, Client

class SupabaseAuthentication(authentication.BaseAuthentication):
    """
    Authentication backend for Supabase JWT tokens.
    """

    def authenticate(self, request):
        # Get the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        # Check for Bearer token
        try:
            prefix, token = auth_header.split()
            if prefix.lower() != "bearer":
                return None
        except ValueError:
            return None

        # Initialize Supabase client
        url: str = settings.SUPABASE_URL
        key: str = settings.SUPABASE_KEY
        
        if not url or not key:
            # If Supabase is not configured, skip this authentication method
            return None

        try:
            supabase: Client = create_client(url, key)
            
            # Verify the token using Supabase Auth
            user_response = supabase.auth.get_user(token)
            
            if not user_response or not user_response.user:
                raise exceptions.AuthenticationFailed("Invalid Supabase token")
                
            supabase_user = user_response.user
            email = supabase_user.email
            
            if not email:
                raise exceptions.AuthenticationFailed("Supabase user has no email")

            # Get or create the Django user
            # We use the email as the unique identifier
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create a new user if they don't exist
                # We'll set a random password since they'll use Supabase to login
                user = User.objects.create_user(
                    username=email,  # Use email as username
                    email=email,
                    password=None
                )
                user.set_unusable_password()
                user.save()

            return (user, None)

        except Exception as e:
            # If anything goes wrong with Supabase verification, fail authentication
            # You might want to log the specific error 'e' here
            raise exceptions.AuthenticationFailed(f"Supabase authentication failed: {str(e)}")
