from django.test import TestCase
from django.contrib.auth import get_user_model
from tenants.models import Tenant
from .models import Integration, IntegrationLog, IntegrationMapping

User = get_user_model()


class IntegrationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.tenant = Tenant.objects.create(
            name='Test Org',
            slug='test-org',
            tier='professional'
        )
    
    def test_create_integration(self):
        integration = Integration.objects.create(
            tenant=self.tenant,
            integration_type='canvas',
            name='Canvas LMS Integration',
            description='Integration with Canvas LMS',
            status='pending',
            created_by='testuser'
        )
        
        self.assertEqual(integration.tenant, self.tenant)
        self.assertEqual(integration.integration_type, 'canvas')
        self.assertEqual(integration.status, 'pending')
    
    def test_unique_integration_per_type(self):
        Integration.objects.create(
            tenant=self.tenant,
            integration_type='canvas',
            name='Canvas Integration 1',
            created_by='testuser'
        )
        
        # Attempting to create another Canvas integration for same tenant should fail
        with self.assertRaises(Exception):
            Integration.objects.create(
                tenant=self.tenant,
                integration_type='canvas',
                name='Canvas Integration 2',
                created_by='testuser'
            )
    
    def test_integration_log(self):
        integration = Integration.objects.create(
            tenant=self.tenant,
            integration_type='xero',
            name='Xero Integration',
            created_by='testuser'
        )
        
        log = IntegrationLog.objects.create(
            integration=integration,
            action='connect',
            status='success',
            message='Connected successfully'
        )
        
        self.assertEqual(log.integration, integration)
        self.assertEqual(log.action, 'connect')
        self.assertEqual(log.status, 'success')
    
    def test_integration_mapping(self):
        integration = Integration.objects.create(
            tenant=self.tenant,
            integration_type='axcelerate',
            name='Axcelerate Integration',
            created_by='testuser'
        )
        
        mapping = IntegrationMapping.objects.create(
            integration=integration,
            source_entity='user',
            source_field='email',
            target_entity='contact',
            target_field='email_address',
            is_bidirectional=True
        )
        
        self.assertEqual(mapping.integration, integration)
        self.assertEqual(mapping.source_entity, 'user')
        self.assertTrue(mapping.is_bidirectional)
