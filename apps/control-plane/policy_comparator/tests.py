from django.test import TestCase
from django.contrib.auth.models import User
from tenants.models import Tenant
from .models import (
    ASQAStandard,
    ASQAClause,
    Policy,
    ComparisonResult,
    ComparisonSession,
)


class ASQAStandardModelTest(TestCase):
    def setUp(self):
        self.standard = ASQAStandard.objects.create(
            standard_number="1.1",
            title="Training and assessment",
            description="Test standard",
            standard_type="training_assessment",
            full_text="Full standard text",
            version="2015",
        )

    def test_standard_creation(self):
        self.assertEqual(str(self.standard), "1.1 - Training and assessment (2015)")
        self.assertTrue(self.standard.is_active)


class ASQAClauseModelTest(TestCase):
    def setUp(self):
        self.standard = ASQAStandard.objects.create(
            standard_number="1.1",
            title="Training and assessment",
            standard_type="training_assessment",
            full_text="Full standard text",
        )
        self.clause = ASQAClause.objects.create(
            standard=self.standard,
            clause_number="1",
            title="Test clause",
            clause_text="Clause text",
            keywords=["training", "assessment", "compliance"],
            compliance_level="critical",
        )

    def test_clause_creation(self):
        self.assertEqual(self.clause.keywords, ["training", "assessment", "compliance"])
        self.assertEqual(self.clause.compliance_level, "critical")


class PolicyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test College",
            slug="test-college",
            domain="test.example.com",
            contact_email="test@example.com",
            contact_name="Test Contact",
        )
        self.policy = Policy.objects.create(
            tenant=self.tenant,
            policy_number="POL-001",
            title="Assessment Policy",
            policy_type="assessment",
            content="This is the policy content regarding assessment procedures.",
            created_by=self.user,
        )

    def test_policy_creation(self):
        self.assertEqual(str(self.policy), "POL-001 - Assessment Policy")
        self.assertEqual(self.policy.status, "draft")
        self.assertIsNone(self.policy.compliance_score)


class ComparisonResultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test College",
            slug="test-college",
            domain="test.example.com",
            contact_email="test@example.com",
            contact_name="Test Contact",
        )
        self.standard = ASQAStandard.objects.create(
            standard_number="1.1",
            title="Training and assessment",
            standard_type="training_assessment",
            full_text="Full standard text",
        )
        self.clause = ASQAClause.objects.create(
            standard=self.standard,
            clause_number="1",
            title="Test clause",
            clause_text="Clause text",
        )
        self.policy = Policy.objects.create(
            tenant=self.tenant,
            policy_number="POL-001",
            title="Assessment Policy",
            policy_type="assessment",
            content="Policy content",
            created_by=self.user,
        )

    def test_comparison_result_full_match(self):
        result = ComparisonResult.objects.create(
            policy=self.policy,
            asqa_clause=self.clause,
            similarity_score=0.85,
        )
        self.assertEqual(result.match_type, "full")
        self.assertTrue(result.is_compliant)

    def test_comparison_result_partial_match(self):
        result = ComparisonResult.objects.create(
            policy=self.policy,
            asqa_clause=self.clause,
            similarity_score=0.65,
        )
        self.assertEqual(result.match_type, "partial")
        self.assertTrue(result.requires_action)

    def test_comparison_result_no_match(self):
        result = ComparisonResult.objects.create(
            policy=self.policy,
            asqa_clause=self.clause,
            similarity_score=0.25,
        )
        self.assertEqual(result.match_type, "no_match")
        self.assertTrue(result.requires_action)


class ComparisonSessionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.tenant = Tenant.objects.create(
            name="Test College",
            slug="test-college",
            domain="test.example.com",
            contact_email="test@example.com",
            contact_name="Test Contact",
        )
        self.policy = Policy.objects.create(
            tenant=self.tenant,
            policy_number="POL-001",
            title="Assessment Policy",
            policy_type="assessment",
            content="Policy content",
            created_by=self.user,
        )
        self.session = ComparisonSession.objects.create(
            tenant=self.tenant,
            policy=self.policy,
            session_name="Test Session",
            total_clauses_checked=10,
            compliant_count=6,
            partial_match_count=3,
            gap_count=1,
            created_by=self.user,
        )

    def test_session_creation(self):
        self.assertEqual(self.session.status, "pending")
        self.assertEqual(self.session.total_clauses_checked, 10)

    def test_compliance_score_calculation(self):
        score = self.session.calculate_compliance_score()
        # (6*100 + 3*60 + 1*0) / 10 = 78
        self.assertEqual(score, 78.0)
