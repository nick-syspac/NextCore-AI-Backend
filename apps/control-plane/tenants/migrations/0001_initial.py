# Generated migration for tenants app
from django.db import migrations, models
import django.db.models.deletion
import uuid
import django.core.validators
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Organization name', max_length=255)),
                ('slug', models.SlugField(help_text='URL-safe identifier', max_length=255, unique=True)),
                ('domain', models.CharField(blank=True, help_text='Custom domain (optional)', max_length=255)),
                ('status', models.CharField(choices=[('active', 'Active'), ('suspended', 'Suspended'), ('pending', 'Pending'), ('deactivated', 'Deactivated')], default='pending', max_length=20)),
                ('subscription_tier', models.CharField(choices=[('free', 'Free'), ('basic', 'Basic'), ('professional', 'Professional'), ('enterprise', 'Enterprise')], default='free', max_length=20)),
                ('contact_email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('contact_name', models.CharField(max_length=255)),
                ('contact_phone', models.CharField(blank=True, max_length=50)),
                ('billing_email', models.EmailField(blank=True, max_length=254)),
                ('stripe_customer_id', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activated_at', models.DateTimeField(blank=True, null=True)),
                ('suspended_at', models.DateTimeField(blank=True, null=True)),
                ('suspension_reason', models.TextField(blank=True)),
                ('settings', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TenantUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('admin', 'Admin'), ('member', 'Member'), ('viewer', 'Viewer')], default='member', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='tenants.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['tenant', 'role'],
                'unique_together': {('tenant', 'user')},
            },
        ),
        migrations.CreateModel(
            name='TenantQuota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_calls_limit', models.IntegerField(default=10000, help_text='API calls per month')),
                ('api_calls_used', models.IntegerField(default=0)),
                ('ai_tokens_limit', models.IntegerField(default=100000, help_text='AI tokens per month')),
                ('ai_tokens_used', models.IntegerField(default=0)),
                ('storage_limit_gb', models.FloatField(default=10.0, help_text='Storage limit in GB')),
                ('storage_used_gb', models.FloatField(default=0.0)),
                ('max_users', models.IntegerField(default=5, help_text='Maximum number of users')),
                ('current_users', models.IntegerField(default=0)),
                ('quota_reset_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_reset_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tenant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quota', to='tenants.tenant')),
            ],
            options={
                'verbose_name_plural': 'Tenant quotas',
            },
        ),
        migrations.CreateModel(
            name='TenantAPIKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Key description', max_length=255)),
                ('key_prefix', models.CharField(editable=False, max_length=16)),
                ('key_hash', models.CharField(editable=False, max_length=128)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_used_at', models.DateTimeField(blank=True, null=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('scopes', models.JSONField(default=list, help_text='List of allowed scopes')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_keys', to='tenants.tenant')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='tenant',
            index=models.Index(fields=['slug'], name='tenants_ten_slug_idx'),
        ),
        migrations.AddIndex(
            model_name='tenant',
            index=models.Index(fields=['status'], name='tenants_ten_status_idx'),
        ),
    ]
