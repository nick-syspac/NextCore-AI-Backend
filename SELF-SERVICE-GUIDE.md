# NextCore AI Cloud - Self-Service User Registration

## ✅ Completed Backend Features

### 1. User Registration with Email Verification
- **Public registration endpoint**: `/api/users/register/`
- Automatic email verification token generation
- Verification email sent on registration
- Email verification endpoint: `/api/users/verify-email/`
- Resend verification: `/api/users/resend-verification/`

### 2. Tenant Invitation System
- **Create invitations**: `/api/users/invitations/` (POST - Admin/Owner only)
- **List invitations**: `/api/users/invitations/` (GET)
- **Get invitation details**: `/api/users/invitations/{token}/` (GET - Public)
- **Accept invitation**: `/api/users/accept-invitation/` (POST - Authenticated)
- Invitations expire after 7 days
- Email notifications sent automatically
- Role-based access (owner, admin, member, viewer)

### 3. User Profile Management
- View/update profile: `/api/users/profile/`
- Change password: `/api/users/change-password/`
- List user's tenants: `/api/users/my-tenants/`

## API Endpoints Reference

### Public Endpoints (No Auth Required)
```bash
# Register new user
POST /api/users/register/
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "invitation_token": "uuid-here" # optional
}

# Verify email
POST /api/users/verify-email/
{
  "token": "verification-token-uuid"
}

# Get invitation details
GET /api/users/invitations/{token}/
```

### Authenticated Endpoints
```bash
# Create invitation (Admin/Owner only)
POST /api/users/invitations/
Authorization: Token YOUR_TOKEN
{
  "tenant": "tenant-uuid",
  "email": "newuser@example.com",
  "role": "member",
  "message": "Welcome to our team!"
}

# Accept invitation
POST /api/users/accept-invitation/
Authorization: Token YOUR_TOKEN
{
  "token": "invitation-token-uuid"
}

# Resend verification email
POST /api/users/resend-verification/
Authorization: Token YOUR_TOKEN
```

## Next.js Web Portal Setup

### Quick Start
```bash
cd apps/web-portal

# Install dependencies
npm install

# Set environment variables
cp .env.example .env.local
# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_SITE_URL=http://localhost:3000

# Run development server
npm run dev
```

Visit http://localhost:3000

### Available Pages
- `/` - Landing page
- `/register` - User registration
- `/login` - User login
- `/verify-email/[token]` - Email verification
- `/accept-invitation/[token]` - Accept tenant invitation
- `/dashboard` - User dashboard (shows tenants)
- `/dashboard/[tenantSlug]` - Tenant-specific dashboard

## Complete User Journey

### 1. New User Registration
1. User visits `/register`
2. Fills out registration form
3. Submits → Account created
4. Receives verification email
5. Clicks link → Email verified

### 2. Invitation Flow
1. Tenant admin sends invitation via `/dashboard/{tenant}/invite`
2. Invitee receives email with link
3. If no account:
   - Clicks link → Goes to registration
   - Registers with matching email
   - Account auto-joins tenant
4. If existing account:
   - Clicks link → Goes to acceptance page
   - Accepts → Joins tenant

### 3. Login and Access
1. User logs in at `/login`
2. Redirected to `/dashboard`
3. Sees list of tenants they belong to
4. Clicks tenant → Tenant dashboard
5. Can use tenant features based on role

## Email Configuration

For production, update `.env` or docker-compose.yml:

```bash
# Use SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@nextcollege.edu.au
FRONTEND_URL=https://app.yourcompany.com
```

For development, emails are printed to console (current default).

## Testing the Flow

### Test Registration
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Test Invitation Creation
```bash
# First, get your auth token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}'

# Create invitation (replace TENANT_UUID and TOKEN)
curl -X POST http://localhost:8000/api/users/invitations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "tenant": "TENANT_UUID",
    "email": "invitee@example.com",
    "role": "member",
    "message": "Join our team!"
  }'
```

## Next Steps

1. **Build Next.js Frontend** (files provided in next commits)
2. **Configure Email Provider** (Gmail, SendGrid, etc.)
3. **Style with Tailwind CSS**
4. **Add OAuth (Google, Microsoft)** for easier login
5. **Implement Password Reset** flow
6. **Add 2FA** for enhanced security

All backend infrastructure is ready to support these features!
