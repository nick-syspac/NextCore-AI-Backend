from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import (
    TrainerQualification, UnitOfCompetency, TrainerAssignment,
    CompetencyGap, QualificationMapping, ComplianceCheck
)


class TrainerQualificationModelTest(TestCase):
    def setUp(self):
        self.qualification = TrainerQualification.objects.create(
            tenant='test-tenant',
            trainer_id='trainer-001',
            trainer_name='John Doe',
            qualification_type='tae_cert_iv',
            qualification_code='TAE40116',
            qualification_name='Certificate IV in Training and Assessment',
            issuing_organization='Test RTO',
            date_obtained=timezone.now().date(),
            verification_status='verified',
            industry_experience_years=5,
            recent_industry_work=True
        )
    
    def test_qualification_creation(self):
        self.assertIsNotNone(self.qualification.qualification_id)
        self.assertTrue(self.qualification.qualification_id.startswith('QUAL-'))
    
    def test_qualification_str(self):
        expected = f'{self.qualification.trainer_name} - {self.qualification.qualification_name}'
        self.assertEqual(str(self.qualification), expected)
    
    def test_unique_together(self):
        # Should not allow duplicate (tenant, trainer_id, qualification_code)
        with self.assertRaises(Exception):
            TrainerQualification.objects.create(
                tenant='test-tenant',
                trainer_id='trainer-001',
                trainer_name='John Doe',
                qualification_type='tae_cert_iv',
                qualification_code='TAE40116',
                qualification_name='Certificate IV in Training and Assessment',
                issuing_organization='Test RTO',
                date_obtained=timezone.now().date()
            )


class UnitOfCompetencyModelTest(TestCase):
    def setUp(self):
        self.unit = UnitOfCompetency.objects.create(
            tenant='test-tenant',
            unit_code='ICTICT418',
            unit_name='Contribute to copyright, ethics and privacy in an ICT environment',
            unit_type='core',
            qualification_code='ICT40120',
            requires_tae=True,
            requires_industry_currency=True,
            required_industry_experience=2
        )
    
    def test_unit_creation(self):
        self.assertIsNotNone(self.unit.unit_id)
        self.assertTrue(self.unit.unit_id.startswith('UNIT-'))
    
    def test_unit_str(self):
        expected = f'{self.unit.unit_code} - {self.unit.unit_name}'
        self.assertEqual(str(self.unit), expected)


class TrainerAssignmentModelTest(TestCase):
    def setUp(self):
        self.unit = UnitOfCompetency.objects.create(
            tenant='test-tenant',
            unit_code='ICTICT418',
            unit_name='Contribute to copyright, ethics and privacy in an ICT environment',
            unit_type='core',
            qualification_code='ICT40120'
        )
        
        self.assignment = TrainerAssignment.objects.create(
            tenant='test-tenant',
            trainer_id='trainer-001',
            trainer_name='John Doe',
            unit=self.unit,
            meets_requirements=True,
            compliance_score=85.5
        )
    
    def test_assignment_creation(self):
        self.assertIsNotNone(self.assignment.assignment_id)
        self.assertTrue(self.assignment.assignment_id.startswith('ASSIGN-'))
    
    def test_assignment_relationship(self):
        self.assertEqual(self.assignment.unit, self.unit)
        self.assertIn(self.assignment, self.unit.assignments.all())


class CompetencyGapModelTest(TestCase):
    def setUp(self):
        self.unit = UnitOfCompetency.objects.create(
            tenant='test-tenant',
            unit_code='ICTICT418',
            unit_name='Test Unit',
            unit_type='core',
            qualification_code='ICT40120'
        )
        
        self.gap = CompetencyGap.objects.create(
            tenant='test-tenant',
            trainer_id='trainer-001',
            trainer_name='John Doe',
            unit=self.unit,
            gap_type='missing_qualification',
            gap_severity='critical',
            gap_description='Missing required ICT qualification',
            recommended_action='Complete ICT40120'
        )
    
    def test_gap_creation(self):
        self.assertIsNotNone(self.gap.gap_id)
        self.assertTrue(self.gap.gap_id.startswith('GAP-'))
    
    def test_gap_defaults(self):
        self.assertFalse(self.gap.is_resolved)


class QualificationMappingModelTest(TestCase):
    def setUp(self):
        self.mapping = QualificationMapping.objects.create(
            tenant='test-tenant',
            source_qualification_code='ICT40120',
            source_qualification_name='Certificate IV in Information Technology',
            match_strength=0.95,
            match_confidence=0.88
        )
    
    def test_mapping_creation(self):
        self.assertIsNotNone(self.mapping.mapping_id)
        self.assertTrue(self.mapping.mapping_id.startswith('MAP-'))


class ComplianceCheckModelTest(TestCase):
    def setUp(self):
        self.check = ComplianceCheck.objects.create(
            tenant='test-tenant',
            check_type='full_matrix',
            check_status='pending',
            total_assignments_checked=10,
            compliant_assignments=8,
            non_compliant_assignments=2,
            gaps_found=5,
            critical_gaps=1,
            high_gaps=2,
            overall_compliance_score=80.0
        )
    
    def test_check_creation(self):
        self.assertIsNotNone(self.check.check_id)
        self.assertTrue(self.check.check_id.startswith('CHECK-'))
    
    def test_compliance_calculation(self):
        self.assertEqual(self.check.compliant_assignments, 8)
        self.assertEqual(self.check.overall_compliance_score, 80.0)
