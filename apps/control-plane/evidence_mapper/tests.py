from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from .models import (
    EvidenceMapping,
    SubmissionEvidence,
    CriteriaTag,
    EvidenceAudit,
    EmbeddingSearch,
)
import json


class EvidenceMappingModelTest(TestCase):
    """Test EvidenceMapping model"""

    def test_create_evidence_mapping(self):
        """Test creating an evidence mapping"""
        mapping = EvidenceMapping.objects.create(
            name="Test Assessment Mapping",
            assessment_type="assignment",
            assessment_title="Python Programming Project",
            unit_code="CS101",
            total_criteria=5,
            total_submissions=20,
            created_by="test_user",
        )

        self.assertIsNotNone(mapping.mapping_number)
        self.assertTrue(mapping.mapping_number.startswith("EVM-"))
        self.assertEqual(mapping.status, "active")
        self.assertEqual(mapping.coverage_percentage, 0.0)

    def test_mapping_number_generation(self):
        """Test unique mapping number generation"""
        mapping1 = EvidenceMapping.objects.create(name="Mapping 1", created_by="user1")
        mapping2 = EvidenceMapping.objects.create(name="Mapping 2", created_by="user2")

        self.assertNotEqual(mapping1.mapping_number, mapping2.mapping_number)
        self.assertTrue(mapping1.mapping_number.startswith("EVM-"))
        self.assertTrue(mapping2.mapping_number.startswith("EVM-"))

    def test_calculate_coverage(self):
        """Test coverage calculation"""
        mapping = EvidenceMapping.objects.create(
            name="Coverage Test", total_criteria=10, created_by="test_user"
        )

        # Create submissions and tags
        submission1 = SubmissionEvidence.objects.create(
            mapping=mapping, student_id="S001", student_name="Test Student 1"
        )
        submission2 = SubmissionEvidence.objects.create(
            mapping=mapping, student_id="S002", student_name="Test Student 2"
        )

        # Tag 3 different criteria
        CriteriaTag.objects.create(
            evidence=submission1,
            criterion_id="CRIT-001",
            criterion_name="Criterion 1",
            tagged_text="Evidence for criterion 1",
            text_start_position=0,
            text_end_position=25,
            tagged_by="test_user",
        )
        CriteriaTag.objects.create(
            evidence=submission1,
            criterion_id="CRIT-002",
            criterion_name="Criterion 2",
            tagged_text="Evidence for criterion 2",
            text_start_position=0,
            text_end_position=25,
            tagged_by="test_user",
        )
        CriteriaTag.objects.create(
            evidence=submission2,
            criterion_id="CRIT-003",
            criterion_name="Criterion 3",
            tagged_text="Evidence for criterion 3",
            text_start_position=0,
            text_end_position=25,
            tagged_by="test_user",
        )

        # Calculate coverage
        coverage = mapping.calculate_coverage()

        # 3 criteria covered out of 10 = 30%
        self.assertEqual(coverage, 30.0)


class SubmissionEvidenceModelTest(TestCase):
    """Test SubmissionEvidence model"""

    def test_create_submission_evidence(self):
        """Test creating submission evidence"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )

        submission = SubmissionEvidence.objects.create(
            mapping=mapping,
            student_id="S001",
            student_name="John Doe",
            submission_type="pdf",
        )

        self.assertIsNotNone(submission.evidence_number)
        self.assertTrue(submission.evidence_number.startswith("EVD-"))
        self.assertEqual(submission.extraction_status, "pending")
        self.assertEqual(submission.total_tags, 0)

    def test_evidence_number_generation(self):
        """Test unique evidence number generation"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )

        submission1 = SubmissionEvidence.objects.create(
            mapping=mapping, student_id="S001"
        )
        submission2 = SubmissionEvidence.objects.create(
            mapping=mapping, student_id="S002"
        )

        self.assertNotEqual(submission1.evidence_number, submission2.evidence_number)
        self.assertTrue(submission1.evidence_number.startswith("EVD-"))
        self.assertTrue(submission2.evidence_number.startswith("EVD-"))

    def test_text_extraction(self):
        """Test text extraction fields"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )

        submission = SubmissionEvidence.objects.create(
            mapping=mapping,
            student_id="S001",
            extracted_text="This is extracted text from the submission.",
            extraction_status="completed",
            extraction_method="mock_ocr",
            extracted_at=timezone.now(),
        )

        self.assertEqual(
            submission.text_length, len("This is extracted text from the submission.")
        )
        self.assertEqual(submission.extraction_status, "completed")
        self.assertIsNotNone(submission.extracted_at)


class CriteriaTagModelTest(TestCase):
    """Test CriteriaTag model"""

    def test_create_criteria_tag(self):
        """Test creating a criteria tag"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )
        submission = SubmissionEvidence.objects.create(
            mapping=mapping, student_id="S001"
        )

        tag = CriteriaTag.objects.create(
            evidence=submission,
            criterion_id="CRIT-001",
            criterion_name="Test Criterion",
            tagged_text="This is the tagged evidence",
            text_start_position=0,
            text_end_position=26,
            tag_type="direct",
            confidence_level="high",
            tagged_by="test_user",
        )

        self.assertIsNotNone(tag.tag_number)
        self.assertTrue(tag.tag_number.startswith("TAG-"))
        self.assertFalse(tag.is_validated)

    def test_tag_number_generation(self):
        """Test unique tag number generation"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )
        submission = SubmissionEvidence.objects.create(
            mapping=mapping, student_id="S001"
        )

        tag1 = CriteriaTag.objects.create(
            evidence=submission,
            criterion_id="CRIT-001",
            tagged_text="Evidence 1",
            text_start_position=0,
            text_end_position=10,
            tagged_by="user1",
        )
        tag2 = CriteriaTag.objects.create(
            evidence=submission,
            criterion_id="CRIT-002",
            tagged_text="Evidence 2",
            text_start_position=0,
            text_end_position=10,
            tagged_by="user2",
        )

        self.assertNotEqual(tag1.tag_number, tag2.tag_number)
        self.assertTrue(tag1.tag_number.startswith("TAG-"))
        self.assertTrue(tag2.tag_number.startswith("TAG-"))

    def test_get_tagged_length(self):
        """Test tagged text length calculation"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )
        submission = SubmissionEvidence.objects.create(
            mapping=mapping, student_id="S001"
        )

        tag = CriteriaTag.objects.create(
            evidence=submission,
            criterion_id="CRIT-001",
            tagged_text="This is a test",
            text_start_position=0,
            text_end_position=14,
            tagged_by="test_user",
        )

        self.assertEqual(tag.get_tagged_length(), 14)


class EvidenceAuditModelTest(TestCase):
    """Test EvidenceAudit model"""

    def test_create_audit_log(self):
        """Test creating an audit log entry"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )

        audit = EvidenceAudit.objects.create(
            mapping=mapping,
            action="mapping_created",
            description="Created new evidence mapping",
            performed_by="test_user",
            ip_address="127.0.0.1",
            processing_time_ms=150,
        )

        self.assertEqual(audit.action, "mapping_created")
        self.assertIsNotNone(audit.timestamp)
        self.assertEqual(audit.ip_address, "127.0.0.1")

    def test_audit_action_choices(self):
        """Test different audit action types"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )

        actions = [
            "mapping_created",
            "submission_added",
            "text_extracted",
            "embedding_generated",
            "evidence_tagged",
            "tag_validated",
        ]

        for action in actions:
            audit = EvidenceAudit.objects.create(
                mapping=mapping, action=action, performed_by="test_user"
            )
            self.assertEqual(audit.action, action)


class EmbeddingSearchModelTest(TestCase):
    """Test EmbeddingSearch model"""

    def test_create_embedding_search(self):
        """Test creating an embedding search log"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )

        search = EmbeddingSearch.objects.create(
            mapping=mapping,
            query_text="test query",
            search_type="similarity",
            results_count=5,
            search_time_ms=250,
            performed_by="test_user",
        )

        self.assertIsNotNone(search.search_number)
        self.assertTrue(search.search_number.startswith("SRCH-"))
        self.assertEqual(search.results_count, 5)

    def test_search_number_generation(self):
        """Test unique search number generation"""
        mapping = EvidenceMapping.objects.create(
            name="Test Mapping", created_by="test_user"
        )

        search1 = EmbeddingSearch.objects.create(
            mapping=mapping, query_text="query 1", performed_by="user1"
        )
        search2 = EmbeddingSearch.objects.create(
            mapping=mapping, query_text="query 2", performed_by="user2"
        )

        self.assertNotEqual(search1.search_number, search2.search_number)
        self.assertTrue(search1.search_number.startswith("SRCH-"))
        self.assertTrue(search2.search_number.startswith("SRCH-"))
