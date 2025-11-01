# Generated migration for TAS app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tenants", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TASTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                (
                    "template_type",
                    models.CharField(
                        choices=[
                            ("general", "General Template"),
                            ("trade", "Trade/Technical"),
                            ("business", "Business/Commerce"),
                            ("health", "Health/Community Services"),
                            ("creative", "Creative Industries"),
                            ("hospitality", "Hospitality/Tourism"),
                            ("technology", "Information Technology"),
                            ("education", "Education/Training"),
                        ],
                        default="general",
                        max_length=50,
                    ),
                ),
                (
                    "aqf_level",
                    models.CharField(
                        choices=[
                            ("certificate_i", "Certificate I"),
                            ("certificate_ii", "Certificate II"),
                            ("certificate_iii", "Certificate III"),
                            ("certificate_iv", "Certificate IV"),
                            ("diploma", "Diploma"),
                            ("advanced_diploma", "Advanced Diploma"),
                            ("graduate_certificate", "Graduate Certificate"),
                            ("graduate_diploma", "Graduate Diploma"),
                            ("bachelor", "Bachelor Degree"),
                            ("masters", "Masters Degree"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "structure",
                    models.JSONField(
                        default=dict,
                        help_text="Template structure with sections and GPT-4 prompts",
                    ),
                ),
                (
                    "default_sections",
                    models.JSONField(
                        default=list, help_text="List of default sections to include"
                    ),
                ),
                (
                    "gpt_prompts",
                    models.JSONField(
                        default=dict, help_text="GPT-4 prompts for each section"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "is_system_template",
                    models.BooleanField(
                        default=False, help_text="System templates cannot be deleted"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tas_templates_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "TAS Template",
                "verbose_name_plural": "TAS Templates",
                "db_table": "tas_templates",
                "ordering": ["aqf_level", "name"],
            },
        ),
        migrations.CreateModel(
            name="TAS",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=300)),
                (
                    "code",
                    models.CharField(
                        help_text="Qualification code (e.g., BSB50120)", max_length=50
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("qualification_name", models.CharField(max_length=300)),
                (
                    "aqf_level",
                    models.CharField(
                        choices=[
                            ("certificate_i", "Certificate I"),
                            ("certificate_ii", "Certificate II"),
                            ("certificate_iii", "Certificate III"),
                            ("certificate_iv", "Certificate IV"),
                            ("diploma", "Diploma"),
                            ("advanced_diploma", "Advanced Diploma"),
                            ("graduate_certificate", "Graduate Certificate"),
                            ("graduate_diploma", "Graduate Diploma"),
                            ("bachelor", "Bachelor Degree"),
                            ("masters", "Masters Degree"),
                        ],
                        max_length=50,
                    ),
                ),
                ("training_package", models.CharField(blank=True, max_length=100)),
                (
                    "sections",
                    models.JSONField(
                        default=list, help_text="Document sections with content"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("in_review", "In Review"),
                            ("approved", "Approved"),
                            ("published", "Published"),
                            ("archived", "Archived"),
                        ],
                        default="draft",
                        max_length=20,
                    ),
                ),
                ("version", models.IntegerField(default=1)),
                ("is_current_version", models.BooleanField(default=True)),
                ("gpt_generated", models.BooleanField(default=False)),
                ("gpt_generation_date", models.DateTimeField(blank=True, null=True)),
                (
                    "gpt_model_used",
                    models.CharField(
                        blank=True, help_text="GPT model version used", max_length=50
                    ),
                ),
                ("gpt_tokens_used", models.IntegerField(default=0)),
                (
                    "generation_time_seconds",
                    models.FloatField(default=0.0, help_text="Time taken to generate"),
                ),
                (
                    "content",
                    models.JSONField(
                        default=dict,
                        help_text="Full document content including all sections",
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        default=dict,
                        help_text="Additional metadata (units, assessments, etc.)",
                    ),
                ),
                (
                    "submitted_for_review_at",
                    models.DateTimeField(blank=True, null=True),
                ),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("approved_at", models.DateTimeField(blank=True, null=True)),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "approved_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tas_approved",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tas_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "reviewed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tas_reviewed",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "submitted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tas_submitted",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tas_documents",
                        to="tas.tastemplate",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tas_documents",
                        to="tenants.tenant",
                    ),
                ),
            ],
            options={
                "verbose_name": "TAS Document",
                "verbose_name_plural": "TAS Documents",
                "db_table": "tas_documents",
                "ordering": ["-created_at"],
                "unique_together": {("tenant", "code", "version")},
            },
        ),
        migrations.CreateModel(
            name="TASVersion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("version_number", models.IntegerField()),
                (
                    "change_summary",
                    models.TextField(help_text="Summary of changes in this version"),
                ),
                (
                    "changed_sections",
                    models.JSONField(
                        default=list, help_text="List of sections that were modified"
                    ),
                ),
                (
                    "content_diff",
                    models.JSONField(
                        default=dict, help_text="Detailed diff of changes"
                    ),
                ),
                (
                    "previous_content",
                    models.JSONField(
                        default=dict, help_text="Snapshot of previous version content"
                    ),
                ),
                (
                    "new_content",
                    models.JSONField(
                        default=dict, help_text="Snapshot of new version content"
                    ),
                ),
                ("was_regenerated", models.BooleanField(default=False)),
                ("regeneration_reason", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tas",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="version_history",
                        to="tas.tas",
                    ),
                ),
            ],
            options={
                "verbose_name": "TAS Version",
                "verbose_name_plural": "TAS Versions",
                "db_table": "tas_versions",
                "ordering": ["-version_number"],
                "unique_together": {("tas", "version_number")},
            },
        ),
        migrations.CreateModel(
            name="TASGenerationLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "requested_sections",
                    models.JSONField(
                        default=list, help_text="Sections requested for generation"
                    ),
                ),
                (
                    "input_data",
                    models.JSONField(
                        default=dict, help_text="Input data provided to GPT-4"
                    ),
                ),
                (
                    "gpt_prompts",
                    models.JSONField(default=dict, help_text="Prompts sent to GPT-4"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "generated_content",
                    models.JSONField(
                        default=dict, help_text="Content generated by GPT-4"
                    ),
                ),
                ("model_version", models.CharField(default="gpt-4", max_length=50)),
                ("tokens_prompt", models.IntegerField(default=0)),
                ("tokens_completion", models.IntegerField(default=0)),
                ("tokens_total", models.IntegerField(default=0)),
                ("generation_time_seconds", models.FloatField(default=0.0)),
                ("error_message", models.TextField(blank=True)),
                ("retry_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tas",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="generation_logs",
                        to="tas.tas",
                    ),
                ),
            ],
            options={
                "verbose_name": "TAS Generation Log",
                "verbose_name_plural": "TAS Generation Logs",
                "db_table": "tas_generation_logs",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="tas",
            index=models.Index(
                fields=["tenant", "status"], name="tas_documen_tenant__4ac7ea_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tas",
            index=models.Index(
                fields=["tenant", "code"], name="tas_documen_tenant__b9e5c8_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="tas",
            index=models.Index(
                fields=["created_at"], name="tas_documen_created_5f8b91_idx"
            ),
        ),
    ]
