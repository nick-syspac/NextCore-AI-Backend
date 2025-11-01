from django.test import TestCase
from django.utils import timezone
from .models import (
    TrainerProfile,
    VerificationScan,
    LinkedInActivity,
    GitHubActivity,
    CurrencyEvidence,
    EntityExtraction,
)


class TrainerProfileModelTest(TestCase):
    def setUp(self):
        self.profile = TrainerProfile.objects.create(
            tenant="test-tenant",
            trainer_id="trainer-001",
            trainer_name="John Smith",
            email="john.smith@example.com",
            linkedin_url="https://linkedin.com/in/johnsmith",
            github_url="https://github.com/johnsmith",
            primary_industry="Information Technology",
            specializations=["Python", "Machine Learning", "Cloud Computing"],
            years_experience=10,
            currency_status="not_verified",
        )

    def test_profile_creation(self):
        """Test profile is created with auto-generated number"""
        self.assertIsNotNone(self.profile.profile_number)
        self.assertTrue(self.profile.profile_number.startswith("PROFILE-"))
        self.assertEqual(self.profile.trainer_name, "John Smith")

    def test_unique_tenant_trainer(self):
        """Test unique constraint on tenant and trainer_id"""
        with self.assertRaises(Exception):
            TrainerProfile.objects.create(
                tenant="test-tenant", trainer_id="trainer-001", trainer_name="Duplicate"
            )


class VerificationScanModelTest(TestCase):
    def setUp(self):
        self.profile = TrainerProfile.objects.create(
            tenant="test-tenant",
            trainer_id="trainer-001",
            trainer_name="John Smith",
            primary_industry="Information Technology",
        )

        self.scan = VerificationScan.objects.create(
            trainer_profile=self.profile,
            scan_type="manual",
            sources_to_scan=["linkedin", "github"],
            scan_status="pending",
        )

    def test_scan_creation(self):
        """Test scan is created with auto-generated number"""
        self.assertIsNotNone(self.scan.scan_number)
        self.assertTrue(self.scan.scan_number.startswith("SCAN-"))
        self.assertEqual(self.scan.scan_type, "manual")

    def test_scan_relationship(self):
        """Test relationship between scan and profile"""
        self.assertEqual(self.scan.trainer_profile, self.profile)
        self.assertEqual(self.profile.scans.count(), 1)


class LinkedInActivityModelTest(TestCase):
    def setUp(self):
        profile = TrainerProfile.objects.create(
            tenant="test-tenant", trainer_id="trainer-001", trainer_name="John Smith"
        )

        scan = VerificationScan.objects.create(
            trainer_profile=profile, scan_type="manual"
        )

        self.activity = LinkedInActivity.objects.create(
            verification_scan=scan,
            activity_type="post",
            title="AI in Education",
            description="Discussion on machine learning applications",
            skills_mentioned=["Machine Learning", "Python"],
            technologies=["TensorFlow", "PyTorch"],
            relevance_score=0.92,
            is_industry_relevant=True,
        )

    def test_linkedin_activity_creation(self):
        """Test LinkedIn activity is created with auto-generated number"""
        self.assertIsNotNone(self.activity.activity_number)
        self.assertTrue(self.activity.activity_number.startswith("LI-"))
        self.assertEqual(self.activity.activity_type, "post")


class GitHubActivityModelTest(TestCase):
    def setUp(self):
        profile = TrainerProfile.objects.create(
            tenant="test-tenant", trainer_id="trainer-001", trainer_name="John Smith"
        )

        scan = VerificationScan.objects.create(
            trainer_profile=profile, scan_type="manual"
        )

        self.activity = GitHubActivity.objects.create(
            verification_scan=scan,
            activity_type="repository",
            repository_name="ai-learning-platform",
            description="AI-powered learning platform",
            language="Python",
            languages_used=["Python", "JavaScript"],
            technologies=["React", "TensorFlow"],
            stars=45,
            relevance_score=0.95,
            is_industry_relevant=True,
        )

    def test_github_activity_creation(self):
        """Test GitHub activity is created with auto-generated number"""
        self.assertIsNotNone(self.activity.activity_number)
        self.assertTrue(self.activity.activity_number.startswith("GH-"))
        self.assertEqual(self.activity.repository_name, "ai-learning-platform")


class CurrencyEvidenceModelTest(TestCase):
    def setUp(self):
        profile = TrainerProfile.objects.create(
            tenant="test-tenant", trainer_id="trainer-001", trainer_name="John Smith"
        )

        scan = VerificationScan.objects.create(
            trainer_profile=profile, scan_type="manual", currency_score=85.0
        )

        self.evidence = CurrencyEvidence.objects.create(
            trainer_profile=profile,
            verification_scan=scan,
            evidence_type="combined_report",
            title="Industry Currency Report",
            content="Report content...",
            currency_score=85.0,
            file_format="markdown",
        )

    def test_evidence_creation(self):
        """Test evidence is created with auto-generated number"""
        self.assertIsNotNone(self.evidence.evidence_number)
        self.assertTrue(self.evidence.evidence_number.startswith("EVIDENCE-"))
        self.assertEqual(self.evidence.evidence_type, "combined_report")


class EntityExtractionModelTest(TestCase):
    def setUp(self):
        profile = TrainerProfile.objects.create(
            tenant="test-tenant", trainer_id="trainer-001", trainer_name="John Smith"
        )

        scan = VerificationScan.objects.create(
            trainer_profile=profile, scan_type="manual"
        )

        self.extraction = EntityExtraction.objects.create(
            verification_scan=scan,
            source_type="linkedin",
            source_text="Sample text with entities",
            entities={"TECH": ["Python", "React"], "SKILL": ["Machine Learning"]},
            entity_count=3,
            extraction_confidence=0.89,
        )

    def test_extraction_creation(self):
        """Test extraction is created with auto-generated number"""
        self.assertIsNotNone(self.extraction.extraction_number)
        self.assertTrue(self.extraction.extraction_number.startswith("EXTRACT-"))
        self.assertEqual(self.extraction.entity_count, 3)
