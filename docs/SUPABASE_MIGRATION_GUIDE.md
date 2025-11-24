# Supabase Integration - Migration Guide

## Overview

This guide walks through migrating your existing Django user authentication to Supabase authentication while maintaining all existing data and functionality.

## Pre-Migration Checklist

- [ ] **Backup your database**
  ```bash
  pg_dump -h localhost -U postgres -d rto > backup_$(date +%Y%m%d).sql
  ```

- [ ] **Set up Supabase project**
  - Create project at https://app.supabase.com
  - Note down Project URL, Keys, and JWT Secret
  - Configure email templates (optional)
  - Set up OAuth providers (optional)

- [ ] **Update environment variables**
  ```bash
  cp apps/control-plane/.env.supabase.example apps/control-plane/.env.local
  # Edit .env.local with your Supabase credentials
  ```

- [ ] **Install dependencies**
  ```bash
  cd apps/control-plane
  pip install -r requirements.txt
  ```

## Migration Steps

### Step 1: Create Database Migrations

```bash
cd apps/control-plane

# Create migrations for new models
python manage.py makemigrations users
python manage.py makemigrations tenants

# Review the migrations
ls users/migrations/
ls tenants/migrations/

# Apply migrations
python manage.py migrate
```

**Expected migrations:**
- `users/migrations/0002_useraccount_*.py` - Creates UserAccount model
- `users/migrations/0003_userinvitation_accepted_by_account.py` - Updates UserInvitation
- `tenants/migrations/0003_tenantuser_*.py` - Updates TenantUser model

### Step 2: Migrate Existing Users (Dry Run)

```bash
# Test migration without making changes
python manage.py migrate_users_to_supabase --dry-run
```

**Review the output:**
- How many users will be migrated?
- Are there any conflicts (duplicate emails)?
- Any users without email addresses?

### Step 3: Migrate Existing Users (Production)

```bash
# Perform actual migration
python manage.py migrate_users_to_supabase

# Verify results
python manage.py shell
>>> from users.models import UserAccount
>>> UserAccount.objects.count()  # Should match Django User count
>>> UserAccount.objects.filter(supabase_user_id__isnull=True).count()  # All should be NULL initially
```

### Step 4: Test Authentication

```bash
# Start development server
python manage.py runserver

# In another terminal, test the bootstrap endpoint
curl -X POST http://localhost:8000/api/users/bootstrap-account/ \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"tenant_name": "Test Org"}'
```

### Step 5: Update Frontend (See Frontend Guide)

The frontend needs to:
1. Integrate `@supabase/auth-helpers-nextjs`
2. Replace Django auth calls with Supabase
3. Call `/api/users/bootstrap-account/` after signup
4. Send Supabase JWT in Authorization header

### Step 6: Monitor and Validate

```bash
# Watch logs for errors
tail -f apps/control-plane/logs/django.log

# Check authentication attempts
python manage.py shell
>>> from users.models import UserAccount
>>> UserAccount.objects.filter(last_login_at__isnull=False).count()
```

## User Migration Process

### For Each Existing User

**Before Migration:**
```
Django User (auth_user)
├── username: john@example.com
├── email: john@example.com
├── password: django_hash_here
└── TenantUser memberships
```

**After Step 3 (migrate_users_to_supabase):**
```
Django User (auth_user)              UserAccount (user_accounts)
├── username: john@example.com  ←→   ├── primary_email: john@example.com
├── email: john@example.com          ├── supabase_user_id: NULL (not linked yet)
├── password: django_hash_here       ├── full_name: John Doe
└── TenantUser memberships      ←→   └── TenantUser memberships (updated)
```

**After User Resets Password & Logs In:**
```
Supabase (auth.users)                UserAccount (user_accounts)
├── id: uuid-abc-123            ←→   ├── supabase_user_id: uuid-abc-123
├── email: john@example.com          ├── primary_email: john@example.com
├── password: supabase_hash          ├── full_name: John Doe
└── (managed by Supabase)            └── TenantUser memberships
```

## User Communication

### Email Template

**Subject:** Important: Authentication System Update

**Body:**
```
Hi {name},

We've upgraded our authentication system to provide better security and features.

What you need to do:
1. Click this link to reset your password: {reset_link}
2. Set a new password
3. Log in with your email and new password

Your data and account settings remain unchanged.

Questions? Contact support@yourdomain.com

Thanks,
The Team
```

### Password Reset Link

Generate reset links in Supabase:
1. Go to Authentication > Users
2. Find user by email
3. Click "..." → "Send Password Recovery"

Or use the Supabase API:
```typescript
await supabase.auth.resetPasswordForEmail(
  'user@example.com',
  { redirectTo: 'https://yourapp.com/reset-password' }
)
```

## Rollback Plan

If you need to rollback:

### Step 1: Stop Using Supabase Auth
```python
# In settings.py, comment out SupabaseAuthentication
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "users.authentication.SupabaseAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}
```

### Step 2: Restore Database (if needed)
```bash
# Restore from backup
psql -h localhost -U postgres -d rto < backup_YYYYMMDD.sql
```

### Step 3: Revert Migrations (if needed)
```bash
# Revert to previous migration
python manage.py migrate users 0001_initial
python manage.py migrate tenants 0002_previous_migration
```

## Troubleshooting

### Issue: Migration Creates Duplicate UserAccounts

**Cause:** Running migration multiple times

**Solution:**
```python
python manage.py shell
>>> from users.models import UserAccount
>>> # Find duplicates
>>> from django.db.models import Count
>>> duplicates = UserAccount.objects.values('primary_email').annotate(
...     count=Count('id')
... ).filter(count__gt=1)
>>> # Delete duplicates (keep first)
>>> for dup in duplicates:
...     accounts = UserAccount.objects.filter(primary_email=dup['primary_email'])
...     accounts.exclude(id=accounts.first().id).delete()
```

### Issue: TenantUser References Missing

**Cause:** TenantUser not updated with user_account

**Solution:**
```python
python manage.py shell
>>> from tenants.models import TenantUser
>>> from users.models import UserAccount
>>> # Update memberships
>>> for membership in TenantUser.objects.filter(user_account__isnull=True):
...     try:
...         account = UserAccount.objects.get(primary_email=membership.user.email)
...         membership.user_account = account
...         membership.save()
...     except UserAccount.DoesNotExist:
...         print(f"No account for {membership.user.email}")
```

### Issue: Users Can't Log In

**Symptoms:** "Invalid token" or "User not found"

**Check:**
1. JWT Secret matches Supabase project
2. User has called bootstrap endpoint
3. Token hasn't expired
4. User exists in Supabase auth.users

**Debug:**
```python
python manage.py shell
>>> import jwt
>>> token = "eyJ..."  # User's token
>>> secret = "your-jwt-secret"
>>> payload = jwt.decode(token, secret, algorithms=['HS256'])
>>> print(payload)
>>> 
>>> # Check if UserAccount exists
>>> from users.models import UserAccount
>>> UserAccount.objects.filter(supabase_user_id=payload['sub'])
```

## Performance Considerations

### Before Migration
- Typical auth: ~5ms (Django session/token lookup)

### After Migration
- JWT verification: ~2ms (no DB query, in-memory)
- UserAccount lookup: ~3ms (indexed query)
- Tenant validation: ~5ms (indexed query)
- **Total: ~10ms** (minimal overhead)

### Optimization Tips
1. Enable database query caching
2. Use Redis for session storage
3. Add connection pooling
4. Monitor slow queries

## Monitoring

### Key Metrics to Track

1. **Authentication Success Rate**
   ```python
   successful_auths = Audit.objects.filter(
       action='auth.success',
       created_at__gte=timezone.now() - timedelta(days=1)
   ).count()
   ```

2. **Failed Authentication Attempts**
   ```python
   failed_auths = Audit.objects.filter(
       action='auth.failed',
       created_at__gte=timezone.now() - timedelta(hours=1)
   ).count()
   ```

3. **Bootstrap Completions**
   ```python
   bootstraps = UserAccount.objects.filter(
       created_at__gte=timezone.now() - timedelta(days=7)
   ).count()
   ```

4. **Active Sessions**
   ```python
   recent_logins = UserAccount.objects.filter(
       last_login_at__gte=timezone.now() - timedelta(minutes=30)
   ).count()
   ```

## Testing Checklist

- [ ] **New user signup**
  - Sign up via Supabase
  - Bootstrap account via API
  - Verify tenant created
  - Verify membership created

- [ ] **Existing user login**
  - Reset password via Supabase
  - Log in with new password
  - Verify UserAccount linked
  - Verify tenant access preserved

- [ ] **Multi-tenant access**
  - User with multiple tenants
  - Switch between tenants
  - Verify data isolation

- [ ] **Permission checks**
  - Owner can manage tenant
  - Admin can modify settings
  - Member has limited access
  - Viewer is read-only

- [ ] **API endpoints**
  - All authenticated endpoints work
  - Tenant-scoped queries work
  - Permission decorators work

## Post-Migration

### Week 1
- Monitor error logs daily
- Track authentication metrics
- Respond to user issues quickly
- Keep rollback plan ready

### Week 2-4
- Verify all users have migrated
- Send reminder emails to inactive users
- Archive old Django authentication
- Update documentation

### After 30 Days
- Remove legacy Django auth code (optional)
- Archive old password reset emails
- Update user documentation
- Celebrate! 🎉

## Support Resources

- **Supabase Documentation**: https://supabase.com/docs
- **Django Rest Framework**: https://www.django-rest-framework.org/
- **PyJWT Documentation**: https://pyjwt.readthedocs.io/
- **Internal Docs**: 
  - `/docs/SUPABASE_BACKEND_IMPLEMENTATION.md`
  - `/docs/SUPABASE_QUICK_REFERENCE.md`

## Getting Help

If you encounter issues:

1. **Check logs**
   ```bash
   tail -f apps/control-plane/logs/django.log
   ```

2. **Enable debug mode**
   ```python
   # settings.py
   DEBUG = True
   LOGGING['loggers']['users']['level'] = 'DEBUG'
   ```

3. **Test manually**
   ```bash
   python manage.py shell
   # Interactive debugging
   ```

4. **Review documentation**
   - This guide
   - Supabase docs
   - Django docs

5. **Contact support**
   - Email: support@yourdomain.com
   - Slack: #engineering
