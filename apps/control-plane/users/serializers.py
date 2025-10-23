"""
Serializers for user registration and management.
"""
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import UserInvitation, EmailVerification


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(required=True)
    invitation_token = serializers.UUIDField(required=False, write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'invitation_token')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }
    
    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        """Create user and generate token."""
        validated_data.pop('password_confirm')
        invitation_token = validated_data.pop('invitation_token', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create auth token
        Token.objects.create(user=user)
        
        # Create email verification
        EmailVerification.objects.create(user=user)
        
        # Handle invitation if provided
        if invitation_token:
            try:
                invitation = UserInvitation.objects.get(token=invitation_token)
                if invitation.can_accept() and invitation.email == user.email:
                    from tenants.models import TenantUser
                    TenantUser.objects.create(
                        tenant=invitation.tenant,
                        user=user,
                        role=invitation.role
                    )
                    invitation.status = 'accepted'
                    invitation.accepted_at = timezone.now()
                    invitation.accepted_by = user
                    invitation.save()
            except UserInvitation.DoesNotExist:
                pass
        
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile viewing/editing."""
    email_verified = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'email_verified', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'username', 'date_joined', 'email_verified')
    
    def get_email_verified(self, obj):
        """Check if user's email is verified."""
        try:
            return obj.email_verification.verified
        except EmailVerification.DoesNotExist:
            return False


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(required=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        """Validate that new passwords match."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class UserInvitationSerializer(serializers.ModelSerializer):
    """Serializer for creating and viewing invitations."""
    invited_by_username = serializers.CharField(source='invited_by.username', read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    can_accept = serializers.SerializerMethodField()
    
    class Meta:
        model = UserInvitation
        fields = ('id', 'tenant', 'tenant_name', 'email', 'role', 'message', 'status', 
                  'token', 'invited_by_username', 'created_at', 'expires_at', 'can_accept')
        read_only_fields = ('id', 'token', 'status', 'invited_by_username', 'created_at', 'can_accept')
    
    def get_can_accept(self, obj):
        """Check if invitation can still be accepted."""
        return obj.can_accept()


class InvitationAcceptSerializer(serializers.Serializer):
    """Serializer for accepting an invitation."""
    token = serializers.UUIDField(required=True)

