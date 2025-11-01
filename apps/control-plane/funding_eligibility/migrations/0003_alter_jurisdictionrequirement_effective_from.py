# Generated migration to fix effective_from default
from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('funding_eligibility', '0002_eligibilityrequest_evidenceattachment_externallookup_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jurisdictionrequirement',
            name='effective_from',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
