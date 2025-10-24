from django.test import TestCase
from django.contrib.auth.models import User
from tenants.models import Tenant
from assessment_builder.models import Assessment
from .models import Rubric, RubricCriterion, RubricLevel, RubricGenerationLog


class RubricModelTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.tenant = Tenant.objects.create(
            slug='test-tenant',
            name='Test Tenant',
            contact_email='test@example.com',
            contact_name='Test User'
        )
        self.assessment = Assessment.objects.create(
            tenant=self.tenant,
            unit_code='TEST001',
            unit_title='Test Unit',
            assessment_type='knowledge',
            title='Test Assessment',
            status='approved',
            created_by=self.user
        )
    
    def test_create_rubric(self):
        """Test creating a rubric"""
        rubric = Rubric.objects.create(
            tenant=self.tenant,
            title='Test Rubric',
            rubric_type='analytic',
            assessment=self.assessment,
            total_points=100,
            passing_score=50,
            status='draft',
            created_by=self.user
        )
        
        self.assertEqual(rubric.title, 'Test Rubric')
        self.assertEqual(rubric.rubric_type, 'analytic')
        self.assertIsNotNone(rubric.rubric_number)
        self.assertTrue(rubric.rubric_number.startswith('RUB-'))
    
    def test_create_rubric_criterion(self):
        """Test creating a rubric criterion"""
        rubric = Rubric.objects.create(
            tenant=self.tenant,
            title='Test Rubric',
            rubric_type='analytic',
            assessment=self.assessment,
            total_points=100,
            status='draft',
            created_by=self.user
        )
        
        criterion = RubricCriterion.objects.create(
            rubric=rubric,
            criterion_number='1',
            title='Knowledge and Understanding',
            description='Demonstrates knowledge of key concepts',
            weight=1,
            max_points=25,
            blooms_level='understand',
            taxonomy_tags=['Bloom\'s: Understand', 'Knowledge'],
            display_order=1
        )
        
        self.assertEqual(criterion.title, 'Knowledge and Understanding')
        self.assertEqual(criterion.blooms_level, 'understand')
        self.assertEqual(len(criterion.taxonomy_tags), 2)
    
    def test_create_rubric_level(self):
        """Test creating a rubric performance level"""
        rubric = Rubric.objects.create(
            tenant=self.tenant,
            title='Test Rubric',
            rubric_type='analytic',
            assessment=self.assessment,
            total_points=100,
            status='draft',
            created_by=self.user
        )
        
        criterion = RubricCriterion.objects.create(
            rubric=rubric,
            criterion_number='1',
            title='Test Criterion',
            max_points=25,
            display_order=1
        )
        
        level = RubricLevel.objects.create(
            criterion=criterion,
            level_name='Exemplary',
            level_type='exemplary',
            points=25,
            description='Outstanding performance',
            indicators=['Comprehensive', 'Detailed', 'Innovative'],
            display_order=1
        )
        
        self.assertEqual(level.level_name, 'Exemplary')
        self.assertEqual(level.points, 25)
        self.assertEqual(len(level.indicators), 3)
    
    def test_criterion_count(self):
        """Test getting criterion count"""
        rubric = Rubric.objects.create(
            tenant=self.tenant,
            title='Test Rubric',
            rubric_type='analytic',
            assessment=self.assessment,
            total_points=100,
            status='draft',
            created_by=self.user
        )
        
        # Create multiple criteria
        for i in range(5):
            RubricCriterion.objects.create(
                rubric=rubric,
                criterion_number=str(i + 1),
                title=f'Criterion {i + 1}',
                max_points=20,
                display_order=i + 1
            )
        
        self.assertEqual(rubric.get_criterion_count(), 5)
    
    def test_rubric_generation_log(self):
        """Test creating rubric generation log"""
        rubric = Rubric.objects.create(
            tenant=self.tenant,
            title='Test Rubric',
            rubric_type='analytic',
            assessment=self.assessment,
            total_points=100,
            status='draft',
            created_by=self.user
        )
        
        log = RubricGenerationLog.objects.create(
            rubric=rubric,
            action='generate_full',
            ai_model='GPT-4',
            nlp_model='spaCy',
            prompt_used='Generate rubric for TEST001',
            tokens_used=2000,
            generation_time=3.5,
            success=True,
            performed_by=self.user
        )
        
        self.assertEqual(log.action, 'generate_full')
        self.assertTrue(log.success)
        self.assertEqual(log.tokens_used, 2000)
