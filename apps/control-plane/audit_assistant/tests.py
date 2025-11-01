from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from .models import Evidence, ClauseEvidence, AuditReport, AuditReportClause
from policy_comparator.models import ASQAStandard, ASQAClause
from tenants.models import Tenant

User = get_user_model()


class EvidenceModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test RTO",
            slug="test-rto",
            contact_email="test@rto.com",
            contact_name="Test Contact",
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_evidence_creation(self):
        evidence = Evidence.objects.create(
            tenant=self.tenant,
            evidence_number="EV-001",
            title="Assessment Policy",
            evidence_type="policy",
            evidence_date=date.today(),
            uploaded_by=self.user,
        )
        self.assertEqual(str(evidence), "EV-001 - Assessment Policy")
        self.assertEqual(evidence.status, "uploaded")

    def test_evidence_ner_entities(self):
        evidence = Evidence.objects.create(
            tenant=self.tenant,
            evidence_number="EV-002",
            title="Training Records",
            evidence_type="record",
            evidence_date=date.today(),
            uploaded_by=self.user,
            ner_entities=[
                {"entity": "Standard 1", "type": "STANDARD", "start": 0, "end": 10},
                {"entity": "TAE40116", "type": "QUALIFICATION", "start": 20, "end": 28},
            ],
        )
        self.assertEqual(len(evidence.ner_entities), 2)
        self.assertEqual(evidence.ner_entities[0]["type"], "STANDARD")


class ClauseEvidenceModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test RTO",
            slug="test-rto",
            contact_email="test@rto.com",
            contact_name="Test Contact",
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.standard = ASQAStandard.objects.create(
            standard_number="1",
            title="Training and Assessment",
            standard_type="training_assessment",
        )

        self.clause = ASQAClause.objects.create(
            standard=self.standard,
            clause_number="1.1",
            title="Quality Training",
            clause_text="The RTO must provide quality training and assessment.",
            compliance_level="critical",
            keywords=["quality", "training", "assessment"],
        )

        self.evidence = Evidence.objects.create(
            tenant=self.tenant,
            evidence_number="EV-001",
            title="Assessment Policy",
            evidence_type="policy",
            evidence_date=date.today(),
            uploaded_by=self.user,
        )

    def test_clause_evidence_auto_ner(self):
        mapping = ClauseEvidence.objects.create(
            asqa_clause=self.clause,
            evidence=self.evidence,
            mapping_type="auto_ner",
            confidence_score=0.85,
            matched_keywords=["quality", "training"],
        )
        self.assertEqual(mapping.confidence_score, 0.85)
        self.assertIn("quality", mapping.matched_keywords)

    def test_clause_evidence_verification(self):
        mapping = ClauseEvidence.objects.create(
            asqa_clause=self.clause,
            evidence=self.evidence,
            mapping_type="auto_rule",
            confidence_score=0.90,
        )
        self.assertFalse(mapping.is_verified)

        mapping.is_verified = True
        mapping.verified_by = self.user
        mapping.save()
        self.assertTrue(mapping.is_verified)


class AuditReportModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test RTO",
            slug="test-rto",
            contact_email="test@rto.com",
            contact_name="Test Contact",
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.standard = ASQAStandard.objects.create(
            standard_number="1",
            title="Training and Assessment",
            standard_type="training_assessment",
        )

    def test_audit_report_creation(self):
        report = AuditReport.objects.create(
            tenant=self.tenant,
            report_number="AR-2024-001",
            title="Annual Compliance Audit",
            audit_period_start=date.today() - timedelta(days=365),
            audit_period_end=date.today(),
            created_by=self.user,
        )
        report.asqa_standards.add(self.standard)

        self.assertEqual(str(report), "AR-2024-001 - Annual Compliance Audit")
        self.assertEqual(report.status, "draft")
        self.assertEqual(report.asqa_standards.count(), 1)

    def test_calculate_metrics(self):
        # Create clauses
        clause1 = ASQAClause.objects.create(
            standard=self.standard,
            clause_number="1.1",
            title="Test Clause 1",
            compliance_level="critical",
        )
        clause2 = ASQAClause.objects.create(
            standard=self.standard,
            clause_number="1.2",
            title="Test Clause 2",
            compliance_level="essential",
        )

        # Create report
        report = AuditReport.objects.create(
            tenant=self.tenant,
            report_number="AR-2024-001",
            title="Test Audit",
            audit_period_start=date.today(),
            audit_period_end=date.today(),
            created_by=self.user,
        )
        report.asqa_standards.add(self.standard)

        # Calculate metrics
        report.calculate_metrics()

        self.assertEqual(report.total_clauses, 2)
        self.assertEqual(report.critical_clauses_count, 1)


class AuditReportClauseModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Test RTO",
            slug="test-rto",
            contact_email="test@rto.com",
            contact_name="Test Contact",
        )
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.standard = ASQAStandard.objects.create(
            standard_number="1",
            title="Training and Assessment",
            standard_type="training_assessment",
        )

        self.clause = ASQAClause.objects.create(
            standard=self.standard,
            clause_number="1.1",
            title="Quality Training",
            compliance_level="critical",
        )

        self.report = AuditReport.objects.create(
            tenant=self.tenant,
            report_number="AR-2024-001",
            title="Test Audit",
            audit_period_start=date.today(),
            audit_period_end=date.today(),
            created_by=self.user,
        )

    def test_report_clause_creation(self):
        entry = AuditReportClause.objects.create(
            audit_report=self.report,
            asqa_clause=self.clause,
            compliance_status="not_assessed",
        )
        self.assertEqual(str(entry), "AR-2024-001 - 1.1")
        self.assertEqual(entry.evidence_count, 0)

    def test_update_evidence_counts(self):
        evidence = Evidence.objects.create(
            tenant=self.tenant,
            evidence_number="EV-001",
            title="Test Evidence",
            evidence_type="policy",
            evidence_date=date.today(),
            uploaded_by=self.user,
            status="tagged",
        )

        ClauseEvidence.objects.create(
            asqa_clause=self.clause,
            evidence=evidence,
            mapping_type="auto_ner",
            confidence_score=0.85,
            is_verified=True,
        )

        entry = AuditReportClause.objects.create(
            audit_report=self.report, asqa_clause=self.clause
        )

        entry.update_evidence_counts()
        self.assertEqual(entry.evidence_count, 1)
        self.assertEqual(entry.verified_evidence_count, 1)
