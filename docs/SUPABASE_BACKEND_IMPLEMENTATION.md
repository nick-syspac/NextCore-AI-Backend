# Supabase Authentication Integration - Backend Implementation

## Overview

This backend implementation follows best practices for integrating Supabase Auth into a Django/DRF multi-tenant application. Supabase is the **source of truth for authentication** (passwords, OAuth, magic links), while Django/Postgres remains the **source of truth for business data** (tenants, roles, profiles, etc.).

## Architecture

### High-Level Flow

1. **User signs up/logs in** → Supabase Auth (frontend calls Supabase directly)
2. **Supabase issues JWT** → Frontend receives access + refresh tokens
3. **API requests** → Frontend sends `Authorization: Bearer <token>` to Django
4. **Django verifies JWT** → Maps Supabase user ID to `UserAccount`
5. **Tenant resolution** → Middleware validates tenant membership
6. **Request proceeds** → With authenticated user and tenant context

### What's Where

**Supabase (Auth + Postgres):**
- `auth.users` → Core identity (email, password, OAuth)
- Issues JWTs signed with shared secret

**Django (App DB):**
- `user_accounts` → Application user identity (linked by Supabase user ID)
- `tenants` → Organization data
- `tenant_users` → User ↔ Tenant membership with roles
- All business/domain data

## Implementation Details

### 1. Models

#### UserAccount (`users/models.py`)
Main user identity in the application, keyed by Supabase user ID.

```python
class UserAccount(models.Model):
    id = models.UUIDField(primary_key=True)
    supabase_user_id = models.UUIDField(unique=True)  # Links to auth.users.id
    primary_email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict)
    last_login_at = models.DateTimeField(null=True)
```

#### TenantUser / TenantMembership (`tenants/models.py`)
Maps users to tenants with role-based access.

```python
class TenantUser(models.Model):
    tenant = models.ForeignKey(Tenant)
    user_account = models.ForeignKey('users.UserAccount')
    role = models.CharField(choices=Role.choices)  # owner/admin/member/viewer
    status = models.CharField(choices=Status.choices)  # active/invited/pending
```

### 2. Authentication Backend

#### SupabaseAuthentication (`users/authentication.py`)

Implements JWT verification following best practices:

1. **Extracts Bearer token** from Authorization header
2. **Verifies JWT signature** using `SUPABASE_JWT_SECRET`
3. **Validates claims** (issuer, expiry, etc.)
4. **Maps Supabase user ID** to `UserAccount`
5. **Auto-provisions** new accounts on first login
6. **Updates last login** timestamp

**Key Features:**
- No Supabase client library dependency (pure JWT verification)
- Proper error handling and logging
- Thread-safe
- Performance optimized

### 3. Tenant Middleware

#### TenantContextMiddleware (`control_plane/middleware.py`)

Enhanced to support Supabase authentication:

1. **Reads X-Tenant-ID header**
2. **Validates tenant exists**
3. **Checks user membership** via `TenantUser`
4. **Verifies active status**
5. **Attaches tenant context** to request
6. **Sets role information**

**Request attributes set:**
- `request.user_account` → UserAccount instance
- `request.tenant` → Tenant instance
- `request.tenant_membership` → TenantUser instance
- `request.tenant_role` → Role string
- `request.supabase_claims` → Raw JWT payload

### 4. Bootstrap Endpoint

#### `/api/users/bootstrap-account/` (`users/views_supabase.py`)

Called by frontend after successful Supabase signup to:

1. **Verify authentication** (user_account exists)
2. **Check if already bootstrapped**
3. **Create default tenant** (if first-time user)
4. **Create owner membership**
5. **Log audit event**

**Request:**
```json
{
  "tenant_name": "My Organization",
  "tenant_slug": "my-org",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "tenant": {
    "id": "uuid",
    "name": "My Organization",
    "slug": "my-org"
  },
  "membership": {
    "role": "owner",
    "status": "active"
  }
}
```

### 5. Additional Endpoints

#### GET `/api/users/supabase/profile/`
Get authenticated user's profile.

#### PATCH `/api/users/supabase/profile/update/`
Update user profile (full_name, metadata).

#### GET `/api/users/supabase/tenants/`
List all tenants user has access to with membership details.

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# JWT Secret (from Supabase Project Settings > API > JWT Settings)
SUPABASE_JWT_SECRET=your-jwt-secret-here

# JWT Algorithm (usually HS256)
SUPABASE_JWT_ALGORITHM=HS256
```

### Settings (`control_plane/settings.py`)

Authentication is configured to prioritize Supabase:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "users.authentication.SupabaseAuthentication",  # Primary
        "rest_framework.authentication.TokenAuthentication",  # Legacy
        "rest_framework.authentication.SessionAuthentication",  # Admin
    ],
}
```

## Database Migrations

### Create Migrations

```bash
cd apps/control-plane
python manage.py makemigrations users
python manage.py makemigrations tenants
```

### Apply Migrations

```bash
python manage.py migrate
```

## User Migration

### Migrate Existing Users

For existing Django users, use the management command:

```bash
# Dry run (preview changes)
python manage.py migrate_users_to_supabase --dry-run

# Migrate all users
python manage.py migrate_users_to_supabase

# Migrate specific user
python manage.py migrate_users_to_supabase --email=user@example.com
```

**What it does:**
1. Creates `UserAccount` for each Django `User`
2. Links tenant memberships to new `UserAccount`
3. Leaves `supabase_user_id` as NULL (linked on first login)

**After migration:**
- Users must reset their password via Supabase
- On first Supabase login, the `supabase_user_id` is linked

## API Usage Examples

### Authentication Flow

#### 1. User Signs Up (Frontend → Supabase)

```typescript
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
  options: {
    data: {
      full_name: 'John Doe',
    },
  },
});
```

#### 2. Bootstrap Account (Frontend → Django)

```typescript
const session = (await supabase.auth.getSession()).data.session;

const response = await fetch('/api/users/bootstrap-account/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${session.access_token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    tenant_name: 'My Company',
    full_name: 'John Doe',
  }),
});
```

#### 3. Subsequent API Calls

```typescript
const session = (await supabase.auth.getSession()).data.session;

const response = await fetch('/api/some-endpoint/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${session.access_token}`,
    'X-Tenant-ID': tenantId,
  },
});
```

### Multi-Tenant Access

```typescript
// Get user's tenants
const tenants = await fetch('/api/users/supabase/tenants/', {
  headers: {
    'Authorization': `Bearer ${session.access_token}`,
  },
});

// Switch tenant context
const data = await fetch('/api/some-resource/', {
  headers: {
    'Authorization': `Bearer ${session.access_token}`,
    'X-Tenant-ID': selectedTenantId,
  },
});
```

## Security Considerations

### JWT Verification
- ✅ Verifies signature with shared secret
- ✅ Checks expiration
- ✅ Validates claims structure
- ✅ Logs verification failures

### Tenant Isolation
- ✅ Validates tenant membership on every request
- ✅ Checks active status
- ✅ Verifies role permissions
- ✅ Prevents cross-tenant data access

### Token Management
- ✅ Short-lived access tokens (1 hour default)
- ✅ Refresh tokens handled by frontend
- ✅ No server-side session storage
- ✅ Stateless authentication

## Backward Compatibility

The implementation maintains backward compatibility:

1. **Legacy Django User** still works with Token/Session auth
2. **UserProfile model** preserved for existing references
3. **TenantUser** supports both `user` and `user_account` fields
4. **Gradual migration** - old and new systems coexist

## Troubleshooting

### JWT Verification Fails

**Check:**
1. `SUPABASE_JWT_SECRET` is correct (from Supabase settings)
2. Token hasn't expired
3. Token is from the correct Supabase project
4. Algorithm matches (HS256 vs RS256)

**Debug:**
```python
# Add to authentication.py
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
```

### User Not Found

**Possible causes:**
1. First-time user hasn't called bootstrap endpoint
2. Supabase user ID not linked to UserAccount
3. User was deleted from Django but not Supabase

**Fix:**
```bash
# Re-run bootstrap for user
curl -X POST /api/users/bootstrap-account/ \
  -H "Authorization: Bearer $TOKEN"
```

### Tenant Access Denied

**Check:**
1. User has active TenantUser membership
2. Correct X-Tenant-ID header sent
3. Tenant status is "active"
4. Membership status is "active"

## Testing

### Unit Tests

```python
# Test authentication
from users.authentication import SupabaseAuthentication
from rest_framework.test import APIRequestFactory

def test_supabase_auth():
    factory = APIRequestFactory()
    request = factory.get('/', HTTP_AUTHORIZATION='Bearer valid-token')
    auth = SupabaseAuthentication()
    user_account, _ = auth.authenticate(request)
    assert user_account is not None
```

### Integration Tests

```python
# Test bootstrap flow
def test_bootstrap_account():
    # Authenticate with Supabase
    response = client.post('/api/users/bootstrap-account/', {
        'tenant_name': 'Test Org',
    }, headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 201
    assert 'tenant' in response.json()
```

## Performance Considerations

1. **JWT Verification** - Cached in memory, no DB queries
2. **UserAccount Lookup** - Indexed by supabase_user_id
3. **Tenant Membership** - Indexed by tenant + user_account
4. **Last Login Update** - Async via update_fields to minimize overhead

## Next Steps

### Frontend Integration
See the main design document for Next.js frontend integration using `@supabase/auth-helpers-nextjs`.

### Advanced Features
- [ ] Role-based permissions decorators
- [ ] Tenant-scoped querysets
- [ ] Invitation acceptance flow with Supabase
- [ ] SSO integration via Supabase
- [ ] Audit logging for all auth events

## Support

For issues or questions:
1. Check logs: `apps/control-plane/logs/django.log`
2. Enable debug logging in settings
3. Review Supabase project settings
4. Check database migrations applied correctly
