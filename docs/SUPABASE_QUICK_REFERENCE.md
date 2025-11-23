# Supabase Authentication - Quick Reference

## Setup Checklist

### 1. Environment Variables
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_JWT_SECRET=your-jwt-secret
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

### 2. Install Dependencies
```bash
cd apps/control-plane
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations users tenants
python manage.py migrate
```

### 4. Migrate Existing Users (Optional)
```bash
python manage.py migrate_users_to_supabase --dry-run
python manage.py migrate_users_to_supabase
```

## API Endpoints

### Bootstrap New User Account
```
POST /api/users/bootstrap-account/
Authorization: Bearer <supabase-jwt>

{
  "tenant_name": "My Organization",
  "full_name": "John Doe"
}
```

### Get User Profile
```
GET /api/users/supabase/profile/
Authorization: Bearer <supabase-jwt>
```

### Update Profile
```
PATCH /api/users/supabase/profile/update/
Authorization: Bearer <supabase-jwt>

{
  "full_name": "John Smith",
  "metadata": {"theme": "dark"}
}
```

### List User's Tenants
```
GET /api/users/supabase/tenants/
Authorization: Bearer <supabase-jwt>
```

### Access Tenant Resources
```
GET /api/any-endpoint/
Authorization: Bearer <supabase-jwt>
X-Tenant-ID: <tenant-uuid>
```

## Common Patterns

### Check Authentication in Views
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_view(request):
    user_account = request.user_account
    tenant = request.tenant
    role = request.tenant_role
    
    # Your logic here
    return Response({"status": "ok"})
```

### Verify Tenant Access
```python
from rest_framework.exceptions import PermissionDenied

def my_view(request):
    if not hasattr(request, 'tenant'):
        raise PermissionDenied("Tenant context required")
    
    if request.tenant_role not in ['owner', 'admin']:
        raise PermissionDenied("Insufficient permissions")
```

### Query Tenant-Scoped Data
```python
def list_resources(request):
    # Filter by tenant
    resources = Resource.objects.filter(
        tenant=request.tenant
    )
    return Response(serializer.data)
```

## Database Models

### UserAccount
```python
UserAccount.objects.get(supabase_user_id=uuid)
UserAccount.objects.get(primary_email=email)
```

### TenantUser (Membership)
```python
TenantUser.objects.filter(
    user_account=user_account,
    status=TenantUser.Status.ACTIVE
)
```

### Check Tenant Membership
```python
membership = TenantUser.objects.filter(
    tenant_id=tenant_id,
    user_account=user_account,
    status=TenantUser.Status.ACTIVE
).first()

if not membership:
    raise PermissionDenied("Not a member of this tenant")
```

## Testing

### Test with Bearer Token
```bash
# Get token from Supabase (in your app)
export TOKEN="eyJ..."

# Test bootstrap
curl -X POST http://localhost:8000/api/users/bootstrap-account/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tenant_name": "Test Org"}'

# Test with tenant context
curl http://localhost:8000/api/some-endpoint/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-ID: tenant-uuid"
```

### Python Shell Testing
```python
python manage.py shell

from users.models import UserAccount
from tenants.models import TenantUser

# Find user
user = UserAccount.objects.get(primary_email='user@example.com')

# Check memberships
memberships = TenantUser.objects.filter(user_account=user)
for m in memberships:
    print(f"{m.tenant.name}: {m.role}")
```

## Troubleshooting

### JWT Errors
```python
# Check JWT secret is correct
import os
print(os.getenv('SUPABASE_JWT_SECRET'))

# Decode JWT manually
import jwt
token = "eyJ..."
secret = "your-secret"
payload = jwt.decode(token, secret, algorithms=['HS256'])
print(payload)
```

### User Not Authenticated
1. Check Authorization header format: `Bearer <token>`
2. Verify token hasn't expired
3. Check SUPABASE_JWT_SECRET matches your project
4. Look for errors in logs

### Tenant Access Denied
1. User must call bootstrap-account first
2. Check X-Tenant-ID header is set
3. Verify user has TenantUser membership
4. Check membership status is 'active'

## Logs

```bash
# View Django logs
tail -f apps/control-plane/logs/django.log

# Enable debug logging
export DJANGO_LOG_LEVEL=DEBUG
python manage.py runserver
```

## Management Commands

```bash
# Migrate users
python manage.py migrate_users_to_supabase --help

# Create superuser (for admin)
python manage.py createsuperuser

# Database shell
python manage.py dbshell
```

## Key Files

```
apps/control-plane/
├── users/
│   ├── models.py              # UserAccount model
│   ├── authentication.py      # SupabaseAuthentication
│   ├── views_supabase.py      # Bootstrap & profile endpoints
│   └── management/commands/
│       └── migrate_users_to_supabase.py
├── tenants/
│   └── models.py              # Tenant, TenantUser models
├── control_plane/
│   ├── settings.py            # Configuration
│   └── middleware.py          # TenantContextMiddleware
└── requirements.txt           # PyJWT dependency
```

## Security Best Practices

✅ **DO:**
- Verify JWT on every request
- Check tenant membership
- Use HTTPS in production
- Rotate JWT secrets periodically
- Log authentication failures
- Set short token expiry times

❌ **DON'T:**
- Store JWT secret in code
- Trust client-supplied tenant IDs without verification
- Skip authentication checks
- Use same secret across environments
- Log sensitive token data

## Production Considerations

1. **Set proper environment variables**
   ```bash
   DJANGO_DEBUG=False
   SECURE_SSL_REDIRECT=True
   SUPABASE_JWT_SECRET=<production-secret>
   ```

2. **Use environment-specific Supabase projects**
   - Dev: dev-project.supabase.co
   - Staging: staging-project.supabase.co
   - Production: prod-project.supabase.co

3. **Monitor authentication logs**
   - Failed login attempts
   - Invalid tokens
   - Unauthorized tenant access

4. **Set up alerts**
   - High rate of auth failures
   - Unusual tenant access patterns
   - Token verification errors

## Quick Links

- **Supabase Docs**: https://supabase.com/docs/guides/auth
- **JWT Docs**: https://pyjwt.readthedocs.io/
- **DRF Auth**: https://www.django-rest-framework.org/api-guide/authentication/
