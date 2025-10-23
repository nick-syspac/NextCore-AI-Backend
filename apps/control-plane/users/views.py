"""
Views for user registration and management.
"""
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from tenants.models import TenantUser
from .models import UserInvitation, EmailVerification
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    UserInvitationSerializer,
    InvitationAcceptSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """
    Public endpoint for user registration.
    No authentication required.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get the token
        token = Token.objects.get(user=user)
        
        # Send verification email
        try:
            verification = EmailVerification.objects.get(user=user)
            self.send_verification_email(user, verification)
        except Exception as e:
            # Log error but don't fail registration
            print(f"Failed to send verification email: {e}")
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email_verified': False,
            },
            'token': token.key,
            'message': 'User created successfully. Please check your email to verify your account.'
        }, status=status.HTTP_201_CREATED)
    
    def send_verification_email(self, user, verification):
        """Send email verification link."""
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{verification.token}"
        
        send_mail(
            subject='Verify your email - NextCore AI Cloud',
            message=f'Hi {user.first_name or user.username},\n\n'
                    f'Please verify your email by clicking this link:\n{verification_url}\n\n'
                    f'This link will expire in 24 hours.\n\n'
                    f'If you didn\'t create this account, please ignore this email.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View and update user profile.
    Requires authentication.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """
    Change user password.
    Requires authentication.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password updated successfully.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """Verify user email with token."""
    token = request.data.get('token')
    
    if not token:
        return Response(
            {'error': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        verification = EmailVerification.objects.get(token=token)
        
        if verification.verified:
            return Response({'message': 'Email already verified'})
        
        if verification.is_expired():
            return Response(
                {'error': 'Verification link has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        verification.verified = True
        verification.verified_at = timezone.now()
        verification.save()
        
        return Response({'message': 'Email verified successfully'})
    
    except EmailVerification.DoesNotExist:
        return Response(
            {'error': 'Invalid verification token'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resend_verification_email(request):
    """Resend verification email."""
    user = request.user
    
    try:
        verification = EmailVerification.objects.get(user=user)
        
        if verification.verified:
            return Response({'message': 'Email already verified'})
        
        # Create new token if expired
        if verification.is_expired():
            verification.token = EmailVerification._meta.get_field('token').default()
            verification.created_at = timezone.now()
            verification.save()
        
        # Send email
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{verification.token}"
        send_mail(
            subject='Verify your email - NextCore AI Cloud',
            message=f'Hi {user.first_name or user.username},\n\n'
                    f'Please verify your email by clicking this link:\n{verification_url}\n\n'
                    f'This link will expire in 24 hours.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return Response({'message': 'Verification email sent'})
    
    except EmailVerification.DoesNotExist:
        return Response(
            {'error': 'Verification record not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class UserInvitationListCreateView(generics.ListCreateAPIView):
    """
    List and create invitations.
    Only tenant admins/owners can create invitations.
    """
    serializer_class = UserInvitationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter invitations based on user's tenant permissions."""
        user = self.request.user
        # Get tenants where user is admin or owner
        tenant_users = TenantUser.objects.filter(
            user=user,
            role__in=['owner', 'admin']
        ).values_list('tenant_id', flat=True)
        
        return UserInvitation.objects.filter(tenant_id__in=tenant_users)
    
    def perform_create(self, serializer):
        """Create invitation and send email."""
        # Check if user has permission for this tenant
        tenant = serializer.validated_data['tenant']
        try:
            tenant_user = TenantUser.objects.get(user=self.request.user, tenant=tenant)
            if tenant_user.role not in ['owner', 'admin']:
                raise permissions.PermissionDenied("Only tenant admins can send invitations")
        except TenantUser.DoesNotExist:
            raise permissions.PermissionDenied("You don't have access to this tenant")
        
        invitation = serializer.save(invited_by=self.request.user)
        
        # Send invitation email
        self.send_invitation_email(invitation)
    
    def send_invitation_email(self, invitation):
        """Send invitation email."""
        invitation_url = f"{settings.FRONTEND_URL}/accept-invitation/{invitation.token}"
        
        send_mail(
            subject=f'Invitation to join {invitation.tenant.name} - NextCore AI Cloud',
            message=f'Hi,\n\n'
                    f'{invitation.invited_by.get_full_name() or invitation.invited_by.username} '
                    f'has invited you to join {invitation.tenant.name} as a {invitation.role}.\n\n'
                    f'{invitation.message}\n\n'
                    f'Click here to accept the invitation:\n{invitation_url}\n\n'
                    f'This invitation will expire on {invitation.expires_at.strftime("%Y-%m-%d %H:%M")}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.email],
            fail_silently=False,
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invitation(request):
    """Accept a tenant invitation."""
    serializer = InvitationAcceptSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    token = serializer.validated_data['token']
    user = request.user
    
    try:
        invitation = UserInvitation.objects.get(token=token)
        
        # Validate invitation can be accepted
        if not invitation.can_accept():
            if invitation.is_expired():
                return Response(
                    {'error': 'Invitation has expired'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': f'Invitation cannot be accepted (status: {invitation.status})'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check email matches
        if invitation.email != user.email:
            return Response(
                {'error': 'Invitation email does not match your account'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already a member
        if TenantUser.objects.filter(tenant=invitation.tenant, user=user).exists():
            return Response(
                {'error': 'You are already a member of this tenant'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create tenant user
        TenantUser.objects.create(
            tenant=invitation.tenant,
            user=user,
            role=invitation.role
        )
        
        # Update invitation
        invitation.status = 'accepted'
        invitation.accepted_at = timezone.now()
        invitation.accepted_by = user
        invitation.save()
        
        return Response({
            'message': f'Successfully joined {invitation.tenant.name}',
            'tenant': {
                'id': str(invitation.tenant.id),
                'name': invitation.tenant.name,
                'slug': invitation.tenant.slug,
                'role': invitation.role
            }
        })
    
    except UserInvitation.DoesNotExist:
        return Response(
            {'error': 'Invalid invitation token'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_invitation_details(request, token):
    """Get invitation details (public endpoint for preview before accepting)."""
    try:
        invitation = UserInvitation.objects.get(token=token)
        
        return Response({
            'tenant_name': invitation.tenant.name,
            'role': invitation.role,
            'invited_by': invitation.invited_by.get_full_name() or invitation.invited_by.username,
            'message': invitation.message,
            'expires_at': invitation.expires_at,
            'can_accept': invitation.can_accept(),
            'status': invitation.status
        })
    
    except UserInvitation.DoesNotExist:
        return Response(
            {'error': 'Invitation not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_tenants(request):
    """
    List all tenants the authenticated user belongs to.
    """
    tenant_users = TenantUser.objects.filter(user=request.user).select_related('tenant')
    
    tenants = []
    for tu in tenant_users:
        tenants.append({
            'tenant_id': str(tu.tenant.id),
            'tenant_name': tu.tenant.name,
            'tenant_slug': tu.tenant.slug,
            'role': tu.role,
            'joined_at': tu.created_at,
        })
    
    return Response({'tenants': tenants})


