# Supabase Integration - Deployment Checklist

## Pre-Deployment

### Environment Setup
- [ ] Create Supabase project for production at https://app.supabase.com
- [ ] Note down production credentials:
  - [ ] Project URL
  - [ ] Anon key
  - [ ] Service role key
  - [ ] JWT secret
- [ ] Set up email templates in Supabase
- [ ] Configure OAuth providers (if needed)
- [ ] Set up custom SMTP (optional)

### Database Preparation
- [ ] Backup production database
  ```bash
  pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > backup_$(date +%Y%m%d_%H%M%S).sql
  ```
- [ ] Test backup restoration
  ```bash
  # In test environment
  psql -h localhost -U postgres -d test_db < backup_YYYYMMDD_HHMMSS.sql
  ```

### Code Review
- [ ] Review all changes in this PR
- [ ] Check environment variable names match
- [ ] Verify no hardcoded secrets
- [ ] Ensure logging is appropriate for production
- [ ] Review error messages (no sensitive data exposed)

## Deployment Steps

### 1. Update Environment Variables
```bash
# Production .env or environment config
SUPABASE_URL=https://your-prod-project.supabase.co
SUPABASE_ANON_KEY=eyJ...prod...
SUPABASE_SERVICE_ROLE_KEY=eyJ...prod...
SUPABASE_JWT_SECRET=your-prod-jwt-secret
SUPABASE_JWT_ALGORITHM=HS256

# Ensure Django settings are production-ready
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-django-secret
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Deploy Code
- [ ] Merge PR to main/production branch
- [ ] Deploy to production environment
- [ ] Verify deployment successful
- [ ] Check application starts without errors

### 3. Run Database Migrations
```bash
# SSH into production server or use deployment tool
cd /path/to/app/apps/control-plane

# Dry run first
python manage.py migrate --plan

# Apply migrations
python manage.py migrate

# Verify
python manage.py showmigrations users tenants
```

Expected output:
```
users
 [X] 0001_initial
 [X] 0002_useraccount
 [X] 0003_userinvitation_accepted_by_account
 ...
tenants
 [X] 0001_initial
 [X] 0002_...
 [X] 0003_tenantuser_user_account_status
 ...
```

### 4. Migrate Existing Users
```bash
# Dry run first to verify
python manage.py migrate_users_to_supabase --dry-run

# Check output carefully
# Expected: Lists all users that will be migrated

# Run actual migration
python manage.py migrate_users_to_supabase

# Verify results
python manage.py shell
>>> from users.models import UserAccount
>>> print(f"UserAccounts created: {UserAccount.objects.count()}")
>>> print(f"With null supabase_user_id: {UserAccount.objects.filter(supabase_user_id__isnull=True).count()}")
>>> exit()
```

### 5. Verify Authentication
```bash
# Test bootstrap endpoint (use actual Supabase token)
curl -X POST https://your-domain.com/api/users/bootstrap-account/ \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"tenant_name": "Test Org"}'

# Expected: 201 Created with user/tenant/membership data
```

### 6. Monitor Logs
```bash
# Watch application logs
tail -f /var/log/django/django.log

# Watch for errors
grep -i error /var/log/django/django.log | tail -20

# Watch authentication attempts
grep -i "supabase" /var/log/django/django.log | tail -20
```

## User Communication

### Phase 1: Announcement (1 week before)
- [ ] Send email to all users announcing upgrade
- [ ] Explain benefits (better security, features)
- [ ] Provide timeline
- [ ] Link to FAQ/support

### Phase 2: Migration Day
- [ ] Deploy changes during low-traffic period
- [ ] Send email with password reset instructions
- [ ] Provide support contact
- [ ] Monitor user feedback

### Phase 3: Follow-up (1 week after)
- [ ] Send reminder to users who haven't reset password
- [ ] Collect feedback
- [ ] Address common issues
- [ ] Update documentation based on questions

### Email Templates

**Announcement Email:**
```
Subject: Important: Authentication System Upgrade on [DATE]

Hi [Name],

We're upgrading to a more secure authentication system on [DATE].

What this means for you:
✓ Better security
✓ Faster login
✓ More login options (Google, etc.)

What you need to do:
1. Check your email on [DATE] for password reset link
2. Set a new password
3. Log in as usual

Your data is safe and unchanged.

Questions? Reply to this email or visit [support link]

Thanks,
[Team]
```

**Migration Day Email:**
```
Subject: Action Required: Reset Your Password

Hi [Name],

Our authentication upgrade is complete!

Please reset your password:
👉 [Reset Password Link]

This takes 2 minutes:
1. Click the link above
2. Enter a new password
3. Log in with your email and new password

Need help? Contact [support email]

Thanks,
[Team]
```

## Post-Deployment Verification

### Immediate Checks (Within 1 hour)
- [ ] Application is accessible
- [ ] No critical errors in logs
- [ ] Test user can sign up via Supabase
- [ ] Test user can call bootstrap endpoint
- [ ] Test user can access tenant resources
- [ ] Existing users can reset password
- [ ] Admin panel is accessible

### First 24 Hours
- [ ] Monitor error rates
- [ ] Track authentication success/failure
- [ ] Monitor API response times
- [ ] Check database performance
- [ ] Review user support tickets
- [ ] Verify audit logs are working

### First Week
- [ ] Track password reset completion rate
- [ ] Monitor user feedback
- [ ] Check for common error patterns
- [ ] Verify all features working
- [ ] Review performance metrics
- [ ] Update documentation based on issues

## Monitoring Queries

```python
# In Django shell: python manage.py shell

# 1. Check UserAccount creation rate
from users.models import UserAccount
from django.utils import timezone
from datetime import timedelta

recent = UserAccount.objects.filter(
    created_at__gte=timezone.now() - timedelta(days=1)
).count()
print(f"New UserAccounts in last 24h: {recent}")

# 2. Check authentication activity
active_users = UserAccount.objects.filter(
    last_login_at__gte=timezone.now() - timedelta(hours=1)
).count()
print(f"Active users in last hour: {active_users}")

# 3. Check users who haven't linked Supabase ID
unlinked = UserAccount.objects.filter(
    supabase_user_id__isnull=True
).count()
print(f"Users not yet linked to Supabase: {unlinked}")

# 4. Check tenant memberships
from tenants.models import TenantUser
memberships = TenantUser.objects.filter(
    user_account__isnull=False
).count()
print(f"Tenant memberships using UserAccount: {memberships}")

# 5. Check for errors in audit log
from audit.models import Audit
errors = Audit.objects.filter(
    action__contains='auth',
    created_at__gte=timezone.now() - timedelta(hours=1)
).count()
print(f"Auth-related audit entries in last hour: {errors}")
```

## Rollback Procedure

### If Critical Issues Occur

**Step 1: Disable Supabase Authentication**
```python
# In settings.py or via environment variable
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "users.authentication.SupabaseAuthentication",  # Disabled
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}
```

**Step 2: Redeploy Previous Version**
```bash
git checkout previous-stable-tag
# Deploy previous version
```

**Step 3: Restore Database (if needed)**
```bash
# Stop application
sudo systemctl stop django

# Restore backup
psql -h $DB_HOST -U $DB_USER -d $DB_NAME < backup_YYYYMMDD_HHMMSS.sql

# Start application
sudo systemctl start django
```

**Step 4: Notify Users**
```
Subject: Service Update

Hi,

We've temporarily reverted to our previous authentication system while we resolve a technical issue.

Your account and data are safe. You can log in with your existing credentials.

We'll send an update within [timeframe].

Thanks for your patience,
[Team]
```

## Success Criteria

### Day 1
- [ ] Zero critical errors
- [ ] < 1% authentication failure rate
- [ ] API response time < 200ms average
- [ ] At least 50% of active users successfully logged in

### Week 1
- [ ] > 80% of users have reset password
- [ ] < 5 support tickets related to auth
- [ ] No performance degradation
- [ ] All features working as expected

### Month 1
- [ ] > 95% of users migrated
- [ ] Zero security incidents
- [ ] Improved authentication metrics
- [ ] Positive user feedback

## Troubleshooting Common Issues

### Issue: "Invalid token" errors
**Check:**
- SUPABASE_JWT_SECRET matches production project
- Token hasn't expired (1 hour default)
- User is using latest token (not cached)

### Issue: "User not found" errors
**Check:**
- User called bootstrap endpoint
- UserAccount was created
- supabase_user_id is set

### Issue: "Tenant access denied" errors
**Check:**
- X-Tenant-ID header is sent
- User has TenantUser membership
- Membership status is 'active'

### Issue: Slow authentication
**Check:**
- Database connection pool size
- Query performance (check indexes)
- Redis cache working
- Network latency

## Support Resources

### Documentation
- Implementation guide: `/docs/SUPABASE_BACKEND_IMPLEMENTATION.md`
- Quick reference: `/docs/SUPABASE_QUICK_REFERENCE.md`
- Migration guide: `/docs/SUPABASE_MIGRATION_GUIDE.md`

### External Resources
- Supabase Docs: https://supabase.com/docs
- Django Rest Framework: https://www.django-rest-framework.org/
- PyJWT: https://pyjwt.readthedocs.io/

### Internal Contacts
- Backend Lead: [email]
- DevOps: [email]
- Support: [email]
- On-call: [phone/pager]

## Final Checklist Before Going Live

- [ ] All tests passing
- [ ] Database backup completed
- [ ] Environment variables set correctly
- [ ] Migrations applied successfully
- [ ] Users migrated
- [ ] Test accounts working
- [ ] Monitoring configured
- [ ] Logs accessible
- [ ] Support team briefed
- [ ] Rollback plan documented
- [ ] User communication prepared
- [ ] Off-hours deployment scheduled
- [ ] Team available for support

## Post-Go-Live

- [ ] Monitor for 1 hour continuously
- [ ] Send user communication
- [ ] Update status page
- [ ] Document any issues encountered
- [ ] Create post-mortem document
- [ ] Celebrate success! 🎉

---

**Remember:**
- Deploy during low-traffic hours
- Have rollback plan ready
- Monitor closely for first 24 hours
- Communicate proactively with users
- Document everything
