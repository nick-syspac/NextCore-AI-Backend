from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from tenants.models import Tenant
from .models import JurisdictionRequirement, EligibilityRule, EligibilityCheck


class JurisdictionRequirementTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.tenant = Tenant.objects.create(name='Test Tenant', slug='test-tenant')
        
        self.requirement = JurisdictionRequirement.objects.create(
            tenant=self.tenant,
            jurisdiction='nsw',
            name='Smart and Skilled NSW',
            code='SS-NSW',
            requires_australian_citizen=True,
            requires_jurisdiction_resident=True,
            min_jurisdiction_residency_months=6,
            min_age=15,
            max_age=64,
            funding_percentage=90.00,
            student_contribution=500.00,
            is_active=True,
            created_by=self.user
        )
    
    def test_requirement_creation(self):
        self.assertEqual(str(self.requirement), 'New South Wales - Smart and Skilled NSW')
        self.assertTrue(self.requirement.is_currently_effective())
    
    def test_requirement_expiry(self):
        self.requirement.effective_to = date.today() - timedelta(days=1)
        self.requirement.save()
        self.assertFalse(self.requirement.is_currently_effective())


class EligibilityRuleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.tenant = Tenant.objects.create(name='Test Tenant', slug='test-tenant')
        
        self.rule = EligibilityRule.objects.create(
            tenant=self.tenant,
            rule_type='age',
            name='Minimum Age 15',
            description='Student must be at least 15 years old',
            field_name='age',
            operator='greater_equal',
            expected_value='15',
            is_mandatory=True,
            error_message='Student must be at least 15 years old',
            created_by=self.user
        )
    
    def test_rule_evaluation_pass(self):
        student_data = {'age': 18}
        passed, message = self.rule.evaluate(student_data)
        self.assertTrue(passed)
    
    def test_rule_evaluation_fail(self):
        student_data = {'age': 14}
        passed, message = self.rule.evaluate(student_data)
        self.assertFalse(passed)
        self.assertEqual(message, 'Student must be at least 15 years old')
    
    def test_rule_evaluation_missing_field(self):
        student_data = {}
        passed, message = self.rule.evaluate(student_data)
        self.assertFalse(passed)
        self.assertIn('Missing required field', message)


class EligibilityCheckTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.tenant = Tenant.objects.create(name='Test Tenant', slug='test-tenant')
        
        self.check = EligibilityCheck.objects.create(
            tenant=self.tenant,
            student_first_name='John',
            student_last_name='Doe',
            student_dob=date(2000, 1, 1),
            student_email='john.doe@example.com',
            course_code='ICT50120',
            course_name='Diploma of Information Technology',
            aqf_level=5,
            intended_start_date=date.today() + timedelta(days=30),
            jurisdiction='nsw',
            student_data={'citizenship_status': 'citizen'},
            checked_by=self.user
        )
    
    def test_check_number_generation(self):
        self.assertTrue(self.check.check_number.startswith('EC-'))
    
    def test_age_calculation(self):
        age = self.check.calculate_age()
        expected_age = date.today().year - 2000
        self.assertEqual(age, expected_age)
    
    def test_eligibility_summary(self):
        self.check.is_eligible = True
        summary = self.check.get_eligibility_summary()
        self.assertIn('Eligible', summary)
