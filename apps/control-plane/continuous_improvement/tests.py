from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from .models import ImprovementCategory, ImprovementAction, ActionTracking, ImprovementReview
from tenants.models import Tenant

User = get_user_model()


class ImprovementCategoryTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test RTO", slug="test-rto")
        self.user = User.objects.create_user(username="testuser", password="testpass")
    
    def test_category_creation(self):
        category = ImprovementCategory.objects.create(
            tenant=self.tenant,
            name="Training Quality",
            category_type="training_assessment",
            related_standards=["1.1", "1.8"],
            created_by=self.user
        )
        self.assertEqual(str(category), "Training Quality (Training & Assessment)")
        self.assertTrue(category.is_active)


class ImprovementActionTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test RTO", slug="test-rto")
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = ImprovementCategory.objects.create(
            tenant=self.tenant,
            name="Training Quality",
            category_type="training_assessment",
            created_by=self.user
        )
    
    def test_action_creation(self):
        action = ImprovementAction.objects.create(
            tenant=self.tenant,
            action_number="CI-2024-001",
            title="Improve assessment validation process",
            description="Implement regular validation meetings",
            category=self.category,
            priority="high",
            source="audit",
            target_completion_date=date.today() + timedelta(days=30),
            responsible_person=self.user,
            created_by=self.user
        )
        self.assertEqual(str(action), "CI-2024-001 - Improve assessment validation process")
        self.assertEqual(action.status, "identified")
        self.assertEqual(action.compliance_status, "compliant")
    
    def test_overdue_detection(self):
        action = ImprovementAction.objects.create(
            tenant=self.tenant,
            action_number="CI-2024-002",
            title="Test Overdue",
            description="Test",
            priority="medium",
            source="audit",
            target_completion_date=date.today() - timedelta(days=5),
            created_by=self.user
        )
        self.assertTrue(action.is_overdue)
        self.assertEqual(action.compliance_status, "overdue")
    
    def test_at_risk_detection(self):
        action = ImprovementAction.objects.create(
            tenant=self.tenant,
            action_number="CI-2024-003",
            title="Test At Risk",
            description="Test",
            priority="medium",
            source="audit",
            target_completion_date=date.today() + timedelta(days=5),
            created_by=self.user
        )
        self.assertEqual(action.compliance_status, "at_risk")
    
    def test_progress_percentage(self):
        action = ImprovementAction.objects.create(
            tenant=self.tenant,
            action_number="CI-2024-004",
            title="Test Progress",
            description="Test",
            priority="medium",
            source="audit",
            status="in_progress",
            created_by=self.user
        )
        self.assertEqual(action.progress_percentage, 50)


class ActionTrackingTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test RTO", slug="test-rto")
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.action = ImprovementAction.objects.create(
            tenant=self.tenant,
            action_number="CI-2024-001",
            title="Test Action",
            description="Test",
            priority="medium",
            source="audit",
            created_by=self.user
        )
    
    def test_tracking_creation(self):
        tracking = ActionTracking.objects.create(
            improvement_action=self.action,
            update_type="progress",
            update_text="Started implementation",
            progress_percentage=25,
            created_by=self.user
        )
        self.assertEqual(tracking.progress_percentage, 25)
        self.assertFalse(tracking.is_blocker)
    
    def test_blocker_tracking(self):
        tracking = ActionTracking.objects.create(
            improvement_action=self.action,
            update_type="issue",
            update_text="Resource unavailable",
            is_blocker=True,
            created_by=self.user
        )
        self.assertTrue(tracking.is_blocker)
        self.assertFalse(tracking.blocker_resolved)


class ImprovementReviewTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test RTO", slug="test-rto")
        self.user = User.objects.create_user(username="testuser", password="testpass")
    
    def test_review_creation(self):
        review = ImprovementReview.objects.create(
            tenant=self.tenant,
            review_number="REV-2024-Q1",
            title="Q1 2024 Review",
            review_type="quarterly",
            review_date=date.today(),
            review_period_start=date.today() - timedelta(days=90),
            review_period_end=date.today(),
            reviewed_by=self.user
        )
        self.assertEqual(str(review), "REV-2024-Q1 - Q1 2024 Review")
    
    def test_calculate_statistics(self):
        review = ImprovementReview.objects.create(
            tenant=self.tenant,
            review_number="REV-2024-Q1",
            title="Q1 2024 Review",
            review_type="quarterly",
            review_date=date.today(),
            review_period_start=date.today() - timedelta(days=90),
            review_period_end=date.today(),
            reviewed_by=self.user
        )
        
        # Create actions
        action1 = ImprovementAction.objects.create(
            tenant=self.tenant,
            action_number="CI-2024-001",
            title="Action 1",
            description="Test",
            priority="high",
            source="audit",
            status="completed",
            created_by=self.user
        )
        
        action2 = ImprovementAction.objects.create(
            tenant=self.tenant,
            action_number="CI-2024-002",
            title="Action 2",
            description="Test",
            priority="medium",
            source="audit",
            status="in_progress",
            compliance_status="overdue",
            created_by=self.user
        )
        
        review.actions_reviewed.add(action1, action2)
        review.calculate_statistics()
        
        self.assertEqual(review.total_actions_reviewed, 2)
        self.assertEqual(review.actions_completed, 1)
        self.assertEqual(review.actions_overdue, 1)
