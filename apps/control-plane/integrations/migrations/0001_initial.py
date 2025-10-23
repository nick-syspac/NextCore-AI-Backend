# Generated migration for integrations app

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Integration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('integration_type', models.CharField(choices=[('axcelerate', 'Axcelerate'), ('canvas', 'Canvas LMS'), ('xero', 'Xero'), ('myob', 'MYOB')], max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('error', 'Error'), ('pending', 'Pending Setup')], default='pending', max_length=20)),
                ('config', models.JSONField(default=dict, help_text='Integration-specific configuration')),
                ('client_id', models.CharField(blank=True, max_length=500)),
                ('client_secret', models.CharField(blank=True, max_length=500)),
                ('access_token', models.TextField(blank=True)),
                ('refresh_token', models.TextField(blank=True)),
                ('token_expires_at', models.DateTimeField(blank=True, null=True)),
                ('api_base_url', models.URLField(blank=True, max_length=500)),
                ('api_key', models.CharField(blank=True, max_length=500)),
                ('webhook_url', models.URLField(blank=True, max_length=500)),
                ('webhook_secret', models.CharField(blank=True, max_length=200)),
                ('auto_sync_enabled', models.BooleanField(default=False)),
                ('sync_interval_minutes', models.IntegerField(default=60)),
                ('last_sync_at', models.DateTimeField(blank=True, null=True)),
                ('last_sync_status', models.CharField(blank=True, max_length=50)),
                ('last_sync_error', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(max_length=100)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='integrations', to='tenants.tenant')),
            ],
            options={
                'db_table': 'integrations',
                'ordering': ['-created_at'],
                'unique_together': {('tenant', 'integration_type')},
            },
        ),
        migrations.CreateModel(
            name='IntegrationLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[('connect', 'Connected'), ('disconnect', 'Disconnected'), ('sync', 'Synced'), ('error', 'Error'), ('config_update', 'Configuration Updated'), ('webhook', 'Webhook Received')], max_length=50)),
                ('status', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('details', models.JSONField(default=dict)),
                ('request_data', models.JSONField(blank=True, null=True)),
                ('response_data', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('integration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='integrations.integration')),
            ],
            options={
                'db_table': 'integration_logs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='IntegrationMapping',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source_entity', models.CharField(max_length=100)),
                ('source_field', models.CharField(max_length=100)),
                ('target_entity', models.CharField(max_length=100)),
                ('target_field', models.CharField(max_length=100)),
                ('transform_rule', models.TextField(blank=True, help_text='Python expression for data transformation')),
                ('is_bidirectional', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('integration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='integrations.integration')),
            ],
            options={
                'db_table': 'integration_mappings',
                'unique_together': {('integration', 'source_entity', 'source_field')},
            },
        ),
    ]
