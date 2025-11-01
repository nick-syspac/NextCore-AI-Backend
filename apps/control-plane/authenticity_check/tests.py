from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from assessment_builder.models import Assessment
from tenants.models import Tenant
from .models import (
    AuthenticityCheck,
    SubmissionAnalysis,
    PlagiarismMatch,
    MetadataVerification,
    AnomalyDetection,
)


class AuthenticityCheckModelTest(TestCase):
    """Test AuthenticityCheck model"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test Tenant", slug="test-tenant", contact_email="test@example.com"
        )
        self.assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="TEST001",
            unit_title="Test Unit",
            assessment_type="knowledge",
            title="Test Assessment",
            created_by=self.user,
        )

    def test_create_authenticity_check(self):
        """Test creating an authenticity check"""
        check = AuthenticityCheck.objects.create(
            assessment=self.assessment,
            name="Plagiarism Check",
            description="Check for plagiarism",
            created_by=self.user,
        )

        self.assertIsNotNone(check.check_number)
        self.assertTrue(check.check_number.startswith("AUTH-"))
        self.assertEqual(check.status, "pending")
        self.assertEqual(check.overall_integrity_score, 0.0)

    def test_auto_generate_check_number(self):
        """Test auto-generation of check number"""
        check1 = AuthenticityCheck.objects.create(
            assessment=self.assessment, name="Check 1", created_by=self.user
        )
        check2 = AuthenticityCheck.objects.create(
            assessment=self.assessment, name="Check 2", created_by=self.user
        )

        self.assertNotEqual(check1.check_number, check2.check_number)
        self.assertTrue(check1.check_number < check2.check_number)

    def test_calculate_overall_score(self):
        """Test calculation of overall integrity score"""
        check = AuthenticityCheck.objects.create(
            assessment=self.assessment, name="Score Test", created_by=self.user
        )

        analysis1 = SubmissionAnalysis.objects.create(
            authenticity_check=check,
            submission_id="SUB-001",
            student_id="ST001",
            student_name="Student 1",
            submission_content="Content 1",
            combined_integrity_score=80.0,
        )

        analysis2 = SubmissionAnalysis.objects.create(
            authenticity_check=check,
            submission_id="SUB-002",
            student_id="ST002",
            student_name="Student 2",
            submission_content="Content 2",
            combined_integrity_score=90.0,
        )

        score = check.calculate_overall_score()
        self.assertEqual(score, 85.0)
        self.assertEqual(check.overall_integrity_score, 85.0)


class SubmissionAnalysisModelTest(TestCase):
    """Test SubmissionAnalysis model"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test Tenant", slug="test-tenant", contact_email="test@example.com"
        )
        self.assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="TEST001",
            unit_title="Test Unit",
            assessment_type="knowledge",
            title="Test Assessment",
            created_by=self.user,
        )
        self.check = AuthenticityCheck.objects.create(
            assessment=self.assessment, name="Test Check", created_by=self.user
        )

    def test_create_submission_analysis(self):
        """Test creating a submission analysis"""
        analysis = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-001",
            student_id="ST001",
            student_name="Test Student",
            submission_content="Test content for analysis",
        )

        self.assertIsNotNone(analysis.analysis_number)
        self.assertTrue(analysis.analysis_number.startswith("ANA-"))
        self.assertIsNotNone(analysis.content_hash)
        self.assertEqual(analysis.word_count, 4)
        self.assertGreater(analysis.character_count, 0)

    def test_content_hash_generation(self):
        """Test automatic content hash generation"""
        content = "Specific content for hashing"
        analysis1 = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-001",
            submission_content=content,
        )

        analysis2 = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-002",
            submission_content=content,
        )

        self.assertEqual(analysis1.content_hash, analysis2.content_hash)

    def test_calculate_combined_score(self):
        """Test combined integrity score calculation"""
        analysis = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-001",
            submission_content="Test content",
            plagiarism_score=0.3,
            metadata_verification_score=90.0,
            anomaly_score=20.0,
        )

        score = analysis.calculate_combined_score()

        # Score should be reduced based on penalties
        self.assertLess(score, 100.0)
        self.assertEqual(analysis.combined_integrity_score, score)

        # Check status assignment
        if score >= 80:
            self.assertEqual(analysis.integrity_status, "pass")
        elif score >= 60:
            self.assertEqual(analysis.integrity_status, "warning")
        else:
            self.assertEqual(analysis.integrity_status, "fail")


class PlagiarismMatchModelTest(TestCase):
    """Test PlagiarismMatch model"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test Tenant", slug="test-tenant", contact_email="test@example.com"
        )
        self.assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="TEST001",
            unit_title="Test Unit",
            assessment_type="knowledge",
            title="Test Assessment",
            created_by=self.user,
        )
        self.check = AuthenticityCheck.objects.create(
            assessment=self.assessment, name="Test Check", created_by=self.user
        )

        self.analysis1 = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-001",
            submission_content="Content 1",
        )
        self.analysis2 = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-002",
            submission_content="Content 2",
        )

    def test_create_plagiarism_match(self):
        """Test creating a plagiarism match"""
        match = PlagiarismMatch.objects.create(
            source_analysis=self.analysis1,
            matched_analysis=self.analysis2,
            similarity_score=0.85,
            matched_words_count=150,
            matched_percentage=85.0,
        )

        self.assertIsNotNone(match.match_number)
        self.assertTrue(match.match_number.startswith("PLG-"))
        self.assertEqual(match.match_type, "embedding")

    def test_severity_assignment(self):
        """Test automatic severity assignment based on similarity"""
        # Critical severity (>= 0.9)
        match_critical = PlagiarismMatch.objects.create(
            source_analysis=self.analysis1,
            matched_analysis=self.analysis2,
            similarity_score=0.92,
            matched_words_count=200,
        )
        self.assertEqual(match_critical.severity, "critical")

        analysis3 = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-003",
            submission_content="Content 3",
        )

        # High severity (>= 0.75)
        match_high = PlagiarismMatch.objects.create(
            source_analysis=self.analysis1,
            matched_analysis=analysis3,
            similarity_score=0.80,
            matched_words_count=180,
        )
        self.assertEqual(match_high.severity, "high")


class MetadataVerificationModelTest(TestCase):
    """Test MetadataVerification model"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test Tenant", slug="test-tenant", contact_email="test@example.com"
        )
        self.assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="TEST001",
            unit_title="Test Unit",
            assessment_type="knowledge",
            title="Test Assessment",
            created_by=self.user,
        )
        self.check = AuthenticityCheck.objects.create(
            assessment=self.assessment, name="Test Check", created_by=self.user
        )
        self.analysis = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-001",
            submission_content="Test content",
        )

    def test_create_metadata_verification(self):
        """Test creating a metadata verification"""
        verification = MetadataVerification.objects.create(
            submission_analysis=self.analysis,
            file_metadata={"file_type": "text/plain"},
            creation_timestamp=timezone.now(),
            author_matches_student=True,
        )

        self.assertIsNotNone(verification.verification_number)
        self.assertTrue(verification.verification_number.startswith("VER-"))
        self.assertEqual(verification.verification_status, "verified")
        self.assertEqual(verification.verification_score, 100.0)

    def test_verification_status_with_anomalies(self):
        """Test verification status changes with anomalies"""
        # No anomalies - should be verified
        verification1 = MetadataVerification.objects.create(
            submission_analysis=self.analysis, anomalies_detected=[]
        )
        self.assertEqual(verification1.verification_status, "verified")
        self.assertEqual(verification1.verification_score, 100.0)

        analysis2 = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-002",
            submission_content="Content 2",
        )

        # 1 anomaly - should be suspicious
        verification2 = MetadataVerification.objects.create(
            submission_analysis=analysis2, anomalies_detected=["Timestamp issue"]
        )
        self.assertEqual(verification2.verification_status, "suspicious")

        analysis3 = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-003",
            submission_content="Content 3",
        )

        # 3+ anomalies - should be failed
        verification3 = MetadataVerification.objects.create(
            submission_analysis=analysis3,
            anomalies_detected=["Issue 1", "Issue 2", "Issue 3"],
        )
        self.assertEqual(verification3.verification_status, "failed")


class AnomalyDetectionModelTest(TestCase):
    """Test AnomalyDetection model"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test Tenant", slug="test-tenant", contact_email="test@example.com"
        )
        self.assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="TEST001",
            unit_title="Test Unit",
            assessment_type="knowledge",
            title="Test Assessment",
            created_by=self.user,
        )
        self.check = AuthenticityCheck.objects.create(
            assessment=self.assessment, name="Test Check", created_by=self.user
        )
        self.analysis = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-001",
            submission_content="Test content",
        )

    def test_create_anomaly_detection(self):
        """Test creating an anomaly detection"""
        anomaly = AnomalyDetection.objects.create(
            submission_analysis=self.analysis,
            anomaly_type="typing_speed",
            severity="high",
            description="Unusual typing speed detected",
            confidence_score=0.85,
            anomaly_data={"typing_speed_wpm": 200},
        )

        self.assertIsNotNone(anomaly.anomaly_number)
        self.assertTrue(anomaly.anomaly_number.startswith("ANM-"))
        self.assertGreater(anomaly.impact_score, 0.0)

    def test_impact_score_calculation(self):
        """Test impact score calculation based on severity and confidence"""
        anomaly_critical = AnomalyDetection.objects.create(
            submission_analysis=self.analysis,
            anomaly_type="paste_events",
            severity="critical",
            description="Critical anomaly",
            confidence_score=1.0,
        )
        self.assertEqual(anomaly_critical.impact_score, 100.0)

        analysis2 = SubmissionAnalysis.objects.create(
            authenticity_check=self.check,
            submission_id="SUB-002",
            submission_content="Content 2",
        )

        anomaly_low = AnomalyDetection.objects.create(
            submission_analysis=analysis2,
            anomaly_type="time_gaps",
            severity="low",
            description="Low severity anomaly",
            confidence_score=0.5,
        )
        self.assertEqual(anomaly_low.impact_score, 12.5)
