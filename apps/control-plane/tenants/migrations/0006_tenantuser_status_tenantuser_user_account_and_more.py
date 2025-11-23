# Generated migration to add user_account field and status to TenantUser
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile'),
        ('tenants', '0005_tenant_gst_registered'),
    ]

    operations = [
        # Add status field
        migrations.AddField(
            model_name='tenantuser',
            name='status',
            field=models.CharField(
                choices=[
                    ('active', 'Active'),
                    ('invited', 'Invited'),
                    ('pending', 'Pending'),
                    ('suspended', 'Suspended'),
                ],
                default='active',
                max_length=20,
            ),
        ),
        # Add user_account field
        migrations.AddField(
            model_name='tenantuser',
            name='user_account',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='tenant_memberships',
                to='users.useraccount',
            ),
        ),
        # Make user field nullable
        migrations.AlterField(
            model_name='tenantuser',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='tenant_memberships',
                to='auth.user',
            ),
        ),
        # Update unique_together to include user_account
        migrations.AlterUniqueTogether(
            name='tenantuser',
            unique_together={('tenant', 'user'), ('tenant', 'user_account')},
        ),
        # Add indexes
        migrations.AddIndex(
            model_name='tenantuser',
            index=models.Index(fields=['tenant', 'status'], name='tenants_ten_tenant__5d7e9c_idx'),
        ),
        migrations.AddIndex(
            model_name='tenantuser',
            index=models.Index(fields=['user_account', 'status'], name='tenants_ten_user_ac_8f3a2d_idx'),
        ),
    ]
