from django.test import TestCase
from django.contrib.auth.models import User
from tenants.models import Tenant
from .models import (
    Assessment,
    AssessmentTask,
    AssessmentCriteria,
    AssessmentGenerationLog,
)


class AssessmentModelTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.tenant = Tenant.objects.create(
            slug="test-tenant",
            name="Test Tenant",
            contact_email="test@example.com",
            contact_name="Test User",
        )

    def test_create_assessment(self):
        """Test creating an assessment"""
        assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="BSBWHS332X",
            unit_title="Apply infection prevention and control procedures",
            training_package="CHC Community Services",
            assessment_type="knowledge",
            title="Test Assessment",
            status="draft",
            created_by=self.user,
        )

        self.assertEqual(assessment.unit_code, "BSBWHS332X")
        self.assertEqual(assessment.status, "draft")
        self.assertIsNotNone(assessment.assessment_number)
        self.assertTrue(assessment.assessment_number.startswith("ASM-"))

    def test_create_assessment_task(self):
        """Test creating an assessment task"""
        assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="TEST001",
            unit_title="Test Unit",
            assessment_type="knowledge",
            title="Test Assessment",
            status="draft",
            created_by=self.user,
        )

        task = AssessmentTask.objects.create(
            assessment=assessment,
            task_number="1",
            task_type="short_answer",
            question="What is the definition of infection control?",
            blooms_level="remember",
            blooms_verbs=["define", "describe"],
            ai_generated=True,
            display_order=1,
        )

        self.assertEqual(task.task_number, "1")
        self.assertEqual(task.blooms_level, "remember")
        self.assertEqual(len(task.blooms_verbs), 2)

    def test_blooms_distribution_calculation(self):
        """Test Bloom's taxonomy distribution calculation"""
        assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="TEST001",
            unit_title="Test Unit",
            assessment_type="knowledge",
            title="Test Assessment",
            status="draft",
            created_by=self.user,
        )

        # Create tasks with different Bloom's levels
        AssessmentTask.objects.create(
            assessment=assessment,
            task_number="1",
            task_type="short_answer",
            question="Define the term",
            blooms_level="remember",
            blooms_verbs=["define"],
            display_order=1,
        )

        AssessmentTask.objects.create(
            assessment=assessment,
            task_number="2",
            task_type="short_answer",
            question="Explain the concept",
            blooms_level="understand",
            blooms_verbs=["explain"],
            display_order=2,
        )

        AssessmentTask.objects.create(
            assessment=assessment,
            task_number="3",
            task_type="practical",
            question="Apply the procedure",
            blooms_level="apply",
            blooms_verbs=["apply"],
            display_order=3,
        )

        # Calculate distribution
        distribution = assessment.calculate_blooms_distribution()

        self.assertIsNotNone(distribution)
        self.assertIn("remember", distribution)
        self.assertIn("understand", distribution)
        self.assertIn("apply", distribution)

        # Each verb should be roughly 33.3% (1/3)
        self.assertAlmostEqual(distribution.get("remember", 0), 33.3, delta=1)
        self.assertAlmostEqual(distribution.get("understand", 0), 33.3, delta=1)
        self.assertAlmostEqual(distribution.get("apply", 0), 33.3, delta=1)

    def test_assessment_task_count(self):
        """Test getting task count"""
        assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="TEST001",
            unit_title="Test Unit",
            assessment_type="knowledge",
            title="Test Assessment",
            status="draft",
            created_by=self.user,
        )

        # Create multiple tasks
        for i in range(5):
            AssessmentTask.objects.create(
                assessment=assessment,
                task_number=str(i + 1),
                task_type="short_answer",
                question=f"Question {i + 1}",
                blooms_level="remember",
                blooms_verbs=["define"],
                display_order=i + 1,
            )

        self.assertEqual(assessment.get_task_count(), 5)

    def test_assessment_generation_log(self):
        """Test creating assessment generation log"""
        assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code="TEST001",
            unit_title="Test Unit",
            assessment_type="knowledge",
            title="Test Assessment",
            status="draft",
            created_by=self.user,
        )

        log = AssessmentGenerationLog.objects.create(
            assessment=assessment,
            action="generate_full",
            ai_model="GPT-4",
            prompt_used="Generate assessment for TEST001",
            tokens_used=1500,
            generation_time=2.5,
            success=True,
            performed_by=self.user,
        )

        self.assertEqual(log.action, "generate_full")
        self.assertTrue(log.success)
        self.assertEqual(log.tokens_used, 1500)
        self.assertEqual(log.generation_time, 2.5)
