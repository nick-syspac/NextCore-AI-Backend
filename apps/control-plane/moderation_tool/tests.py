from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from .models import (
    ModerationSession,
    AssessorDecision,
    OutlierDetection,
    BiasScore,
    ModerationLog,
)


class ModerationSessionModelTests(TestCase):
    def test_session_creation(self):
        """Test that ModerationSession is created with correct attributes"""
        session = ModerationSession.objects.create(
            name="Test Moderation Session",
            description="Testing moderation",
            assessment_type="exam",
            assessment_title="Final Exam 2025",
            total_submissions=50,
            assessors_count=3,
        )

        self.assertIsNotNone(session.session_number)
        self.assertTrue(session.session_number.startswith("MOD-"))
        self.assertEqual(session.outlier_threshold, 2.0)
        self.assertEqual(session.bias_sensitivity, 5)
        self.assertEqual(session.status, "active")

    def test_fairness_score_calculation(self):
        """Test fairness score calculation"""
        session = ModerationSession.objects.create(
            name="Fairness Test",
            assessment_title="Test",
            decisions_compared=100,
            outliers_detected=5,
            bias_flags_raised=3,
            average_agreement_rate=0.85,
        )

        fairness_score = session.get_fairness_score()
        self.assertGreater(fairness_score, 0)
        self.assertLessEqual(fairness_score, 100)


class AssessorDecisionModelTests(TestCase):
    def setUp(self):
        self.session = ModerationSession.objects.create(
            name="Test Session", assessment_title="Test Assessment"
        )

    def test_decision_creation(self):
        """Test that AssessorDecision is created correctly"""
        decision = AssessorDecision.objects.create(
            session=self.session,
            student_id="S12345",
            student_name="Test Student",
            submission_id="SUB001",
            assessor_id="A001",
            assessor_name="Dr. Smith",
            score=85,
            max_score=100,
            grade="D",
            marked_at=timezone.now(),
        )

        self.assertIsNotNone(decision.decision_number)
        self.assertTrue(decision.decision_number.startswith("DEC-"))
        self.assertFalse(decision.is_outlier)
        self.assertFalse(decision.has_bias_flag)

    def test_percentage_score_calculation(self):
        """Test percentage score calculation"""
        decision = AssessorDecision.objects.create(
            session=self.session,
            student_id="S12345",
            assessor_id="A001",
            assessor_name="Dr. Smith",
            score=75,
            max_score=100,
            grade="C",
            marked_at=timezone.now(),
        )

        self.assertEqual(decision.get_percentage_score(), 75.0)


class OutlierDetectionTests(TestCase):
    def setUp(self):
        self.session = ModerationSession.objects.create(
            name="Test Session", assessment_title="Test"
        )
        self.decision = AssessorDecision.objects.create(
            session=self.session,
            student_id="S12345",
            assessor_id="A001",
            assessor_name="Dr. Smith",
            score=95,
            max_score=100,
            grade="HD",
            marked_at=timezone.now(),
        )

    def test_outlier_creation(self):
        """Test that OutlierDetection is created correctly"""
        outlier = OutlierDetection.objects.create(
            session=self.session,
            decision=self.decision,
            outlier_type="high_scorer",
            severity="high",
            z_score=2.5,
            deviation_percentage=25.0,
            expected_score=70.0,
            actual_score=95.0,
            cohort_mean=70.0,
            cohort_std_dev=10.0,
            assessor_mean=88.0,
            explanation="Significantly higher than expected",
            confidence_score=0.85,
        )

        self.assertIsNotNone(outlier.outlier_number)
        self.assertTrue(outlier.outlier_number.startswith("OUT-"))
        self.assertFalse(outlier.is_resolved)
        self.assertEqual(outlier.severity, "high")


class BiasScoreTests(TestCase):
    def setUp(self):
        self.session = ModerationSession.objects.create(
            name="Test Session", assessment_title="Test"
        )

    def test_bias_creation(self):
        """Test that BiasScore is created correctly"""
        bias = BiasScore.objects.create(
            session=self.session,
            assessor_id="A001",
            assessor_name="Dr. Smith",
            bias_type="leniency",
            bias_score=0.65,
            sample_size=30,
            mean_difference=8.5,
            std_dev_ratio=0.9,
            evidence={"pattern": "Consistently high scores"},
            affected_students=["S001", "S002", "S003"],
            recommendation="Review marking criteria",
            severity_level=7,
        )

        self.assertIsNotNone(bias.bias_number)
        self.assertTrue(bias.bias_number.startswith("BIAS-"))
        self.assertFalse(bias.is_validated)
        self.assertEqual(bias.get_severity_label(), "Significant")

    def test_severity_labels(self):
        """Test severity label generation"""
        # Test minor
        bias1 = BiasScore.objects.create(
            session=self.session,
            assessor_id="A001",
            assessor_name="Test",
            bias_type="leniency",
            bias_score=0.2,
            sample_size=10,
            mean_difference=2.0,
            std_dev_ratio=1.0,
            recommendation="Monitor",
            severity_level=2,
        )
        self.assertEqual(bias1.get_severity_label(), "Minor")

        # Test critical
        bias2 = BiasScore.objects.create(
            session=self.session,
            assessor_id="A002",
            assessor_name="Test2",
            bias_type="severity",
            bias_score=0.9,
            sample_size=20,
            mean_difference=-15.0,
            std_dev_ratio=0.5,
            recommendation="Immediate review",
            severity_level=10,
        )
        self.assertEqual(bias2.get_severity_label(), "Critical")


class ModerationLogTests(TestCase):
    def setUp(self):
        self.session = ModerationSession.objects.create(
            name="Test Session", assessment_title="Test"
        )

    def test_log_creation(self):
        """Test that ModerationLog is created correctly"""
        log = ModerationLog.objects.create(
            session=self.session,
            action="comparison_run",
            description="Compared decisions for student S123",
            decisions_processed=5,
            outliers_found=1,
            bias_flags=0,
            processing_time_ms=150,
            performed_by="admin",
        )

        self.assertEqual(log.action, "comparison_run")
        self.assertEqual(log.decisions_processed, 5)
        self.assertIsNotNone(log.timestamp)
