# Generated migration to add UserAccount model
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('supabase_user_id', models.UUIDField(db_index=True, help_text='Supabase Auth user ID (auth.users.id)', unique=True)),
                ('primary_email', models.EmailField(db_index=True, help_text='Primary email address from Supabase Auth', max_length=254, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=True, help_text='Whether the user account is active')),
                ('metadata', models.JSONField(blank=True, default=dict, help_text='Additional user metadata (preferences, settings, etc.)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('last_login_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_accounts',
            },
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(fields=['supabase_user_id'], name='user_accoun_supabase_8b5a9e_idx'),
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(fields=['primary_email'], name='user_accoun_primary_c7e3a1_idx'),
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(fields=['is_active'], name='user_accoun_is_acti_f9d2c4_idx'),
        ),
    ]
