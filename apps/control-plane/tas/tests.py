from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from tenants.models import Tenant
from .models import TAS, TASTemplate, TASVersion, TASGenerationLog


class TASTemplateModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.template = TASTemplate.objects.create(
            name="Certificate III Template",
            description="Standard template for Certificate III",
            template_type="general",
            aqf_level="certificate_iii",
            created_by=self.user,
        )

    def test_template_creation(self):
        self.assertEqual(
            str(self.template), "Certificate III Template (Certificate III)"
        )
        self.assertTrue(self.template.is_active)
        self.assertFalse(self.template.is_system_template)


class TASModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test College",
            slug="test-college",
            domain="test.example.com",
            contact_email="test@example.com",
            contact_name="Test Contact",
        )
        self.tas = TAS.objects.create(
            tenant=self.tenant,
            title="BSB50120 - Diploma of Business",
            code="BSB50120",
            qualification_name="Diploma of Business",
            aqf_level="diploma",
            created_by=self.user,
            gpt_generated=True,
            generation_time_seconds=45.5,
        )

    def test_tas_creation(self):
        self.assertEqual(
            str(self.tas), "BSB50120 - BSB50120 - Diploma of Business (v1)"
        )
        self.assertEqual(self.tas.version, 1)
        self.assertTrue(self.tas.is_current_version)

    def test_version_increment(self):
        # Create a second TAS with same code
        tas2 = TAS.objects.create(
            tenant=self.tenant,
            title="BSB50120 - Diploma of Business",
            code="BSB50120",
            qualification_name="Diploma of Business",
            aqf_level="diploma",
            created_by=self.user,
        )
        self.assertEqual(tas2.version, 2)

    def test_unique_constraint(self):
        # The save() method auto-increments version to prevent duplicates
        # Test that this works correctly
        tas2 = TAS.objects.create(
            tenant=self.tenant,
            title="BSB50120 - Diploma of Business Updated",
            code="BSB50120",
            qualification_name="Diploma of Business",
            aqf_level="diploma",
            version=1,  # Try to use same version
            created_by=self.user,
        )
        # Version should have been auto-incremented to 2
        self.assertEqual(tas2.version, 2)

    def test_time_saved_calculation(self):
        time_saved = self.tas.get_time_saved()
        self.assertIsNotNone(time_saved)
        self.assertEqual(time_saved["percentage_saved"], 90)
        self.assertGreater(time_saved["saved_hours"], 0)

    def test_create_new_version(self):
        new_version = self.tas.create_new_version(self.user)
        self.assertEqual(new_version.version, 2)
        self.assertTrue(new_version.is_current_version)

        # Check old version is no longer current
        self.tas.refresh_from_db()
        self.assertFalse(self.tas.is_current_version)


class TASVersionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test College",
            slug="test-college",
            domain="test.example.com",
            contact_email="test@example.com",
            contact_name="Test Contact",
        )
        self.tas = TAS.objects.create(
            tenant=self.tenant,
            title="BSB50120 - Diploma of Business",
            code="BSB50120",
            qualification_name="Diploma of Business",
            aqf_level="diploma",
            created_by=self.user,
        )
        self.version = TASVersion.objects.create(
            tas=self.tas,
            version_number=1,
            change_summary="Initial version",
            created_by=self.user,
        )

    def test_version_creation(self):
        self.assertEqual(str(self.version), "BSB50120 - Version 1")


class TASGenerationLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test College",
            slug="test-college",
            domain="test.example.com",
            contact_email="test@example.com",
            contact_name="Test Contact",
        )
        self.tas = TAS.objects.create(
            tenant=self.tenant,
            title="BSB50120 - Diploma of Business",
            code="BSB50120",
            qualification_name="Diploma of Business",
            aqf_level="diploma",
            created_by=self.user,
        )
        self.log = TASGenerationLog.objects.create(
            tas=self.tas,
            status="completed",
            model_version="gpt-4",
            tokens_total=5000,
            generation_time_seconds=30.5,
            created_by=self.user,
        )

    def test_log_creation(self):
        self.assertEqual(self.log.status, "completed")
        self.assertEqual(self.log.tokens_total, 5000)
