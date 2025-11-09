"""
Management command to populate database with realistic test data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from tenants.models import Tenant, TenantUser, TenantAPIKey
from tas.models import TAS, TASTemplate, TASConversionSession
from policy_comparator.models import (
    Policy, ASQAStandard, ASQAClause, 
    ComparisonResult, ComparisonSession,
    PolicyConversionSession
)


class Command(BaseCommand):
    help = 'Populate database with realistic test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing test data...')
            self.clear_data()

        self.stdout.write('Creating test data...')
        
        # Create users
        users = self.create_users()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(users)} users'))
        
        # Create tenants
        tenants = self.create_tenants(users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(tenants)} tenants'))
        
        # Create TAS templates
        templates = self.create_tas_templates(users[0])
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(templates)} TAS templates'))
        
        # Create TAS documents
        tas_docs = self.create_tas_documents(tenants, users, templates)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(tas_docs)} TAS documents'))
        
        # Create TAS conversion sessions
        conversions = self.create_tas_conversions(tas_docs, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(conversions)} TAS conversion sessions'))
        
        # Create policies
        policies = self.create_policies(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(policies)} policies'))
        
        # Create policy conversion sessions
        policy_conversions = self.create_policy_conversions(policies, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(policy_conversions)} policy conversion sessions'))
        
        # Create comparison sessions
        comparison_sessions = self.create_comparison_sessions(policies, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(comparison_sessions)} comparison sessions'))
        
        # Create API keys
        api_keys = self.create_api_keys(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(api_keys)} API keys'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ Test data population complete!'))
        self.stdout.write('\nTest Credentials:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Manager: manager / manager123')
        self.stdout.write('  Trainer: trainer / trainer123')

    def clear_data(self):
        """Clear existing test data"""
        from django.db import connection
        from django.db.utils import ProgrammingError
        
        # Delete in order to avoid foreign key constraints
        try:
            TASConversionSession.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            PolicyConversionSession.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            ComparisonSession.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            ComparisonResult.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            TAS.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            Policy.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            TASTemplate.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            TenantAPIKey.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            TenantUser.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            Tenant.objects.filter(slug__in=['demo-rto', 'sydney-skills', 'melbourne-training']).delete()
        except ProgrammingError:
            pass
        
        try:
            User.objects.filter(username__in=['admin', 'manager', 'trainer', 'assessor']).delete()
        except ProgrammingError:
            pass

    def create_users(self):
        """Create test users"""
        users = []
        
        # Admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
        users.append(admin)
        
        # Manager user
        manager, created = User.objects.get_or_create(
            username='manager',
            defaults={
                'email': 'manager@example.com',
                'first_name': 'Sarah',
                'last_name': 'Manager',
                'is_staff': True,
            }
        )
        if created:
            manager.set_password('manager123')
            manager.save()
        users.append(manager)
        
        # Trainer user
        trainer, created = User.objects.get_or_create(
            username='trainer',
            defaults={
                'email': 'trainer@example.com',
                'first_name': 'John',
                'last_name': 'Trainer',
            }
        )
        if created:
            trainer.set_password('trainer123')
            trainer.save()
        users.append(trainer)
        
        # Assessor user
        assessor, created = User.objects.get_or_create(
            username='assessor',
            defaults={
                'email': 'assessor@example.com',
                'first_name': 'Jane',
                'last_name': 'Assessor',
            }
        )
        if created:
            assessor.set_password('assessor123')
            assessor.save()
        users.append(assessor)
        
        return users

    def create_tenants(self, users):
        """Create test tenants"""
        tenants = []
        
        from tenants.models import SubscriptionTier, TenantStatus
        
        tenant_data = [
            {
                'name': 'Demo RTO',
                'slug': 'demo-rto',
                'contact_email': 'admin@demorto.edu.au',
                'contact_name': 'Demo Admin',
                'contact_phone': '+61 2 9999 0001',
                'status': TenantStatus.ACTIVE,
                'subscription_tier': SubscriptionTier.PROFESSIONAL,
                'settings': {
                    'industry': 'Multi-sector Training',
                    'abn': '12 345 678 901',
                }
            },
            {
                'name': 'Sydney Skills Institute',
                'slug': 'sydney-skills',
                'contact_email': 'info@sydneyskills.edu.au',
                'contact_name': 'Sydney Admin',
                'contact_phone': '+61 2 9999 0002',
                'status': TenantStatus.ACTIVE,
                'subscription_tier': SubscriptionTier.PROFESSIONAL,
                'settings': {
                    'industry': 'Business & IT Training',
                    'abn': '98 765 432 109',
                }
            },
            {
                'name': 'Melbourne Training College',
                'slug': 'melbourne-training',
                'contact_email': 'contact@melbournetraining.edu.au',
                'contact_name': 'Melbourne Admin',
                'contact_phone': '+61 3 9999 0003',
                'status': TenantStatus.ACTIVE,
                'subscription_tier': SubscriptionTier.ENTERPRISE,
                'settings': {
                    'industry': 'Hospitality & Tourism',
                    'abn': '55 444 333 222',
                }
            },
        ]
        
        for data in tenant_data:
            slug = data.pop('slug')
            tenant, created = Tenant.objects.get_or_create(
                slug=slug,
                defaults=data
            )
            tenants.append(tenant)
            
            # Create tenant users
            for i, user in enumerate(users):
                role = 'admin' if i == 0 else ('manager' if i == 1 else 'trainer')
                TenantUser.objects.get_or_create(
                    tenant=tenant,
                    user=user,
                    defaults={'role': role}
                )
        
        return tenants

    def create_tas_templates(self, user):
        """Create TAS templates"""
        templates = []
        
        template_data = [
            {
                'name': 'Certificate III - Trade Template',
                'aqf_level': 'certificate_iii',
                'template_type': 'trade',
                'description': 'Standard template for Certificate III trade qualifications',
                'default_sections': [
                    'Overview',
                    'Qualification Details',
                    'Training Delivery',
                    'Assessment Strategy',
                    'Resources',
                    'Staff Requirements'
                ],
                'gpt_prompts': {
                    'overview': 'Generate an overview for a Certificate III trade qualification...',
                    'assessment': 'Create assessment strategy aligned with QA1.2...'
                }
            },
            {
                'name': 'Certificate IV - Business Template',
                'aqf_level': 'certificate_iv',
                'template_type': 'business',
                'description': 'Template for Certificate IV business qualifications',
                'default_sections': [
                    'Overview',
                    'Qualification Details',
                    'Training Approach',
                    'Assessment Methods',
                    'Resources & Facilities',
                    'Quality Assurance'
                ],
                'gpt_prompts': {
                    'overview': 'Generate business qualification overview...',
                    'training': 'Describe training approach for business learners...'
                }
            },
            {
                'name': 'Diploma - General Template',
                'aqf_level': 'diploma',
                'template_type': 'general',
                'description': 'General template for Diploma level qualifications',
                'default_sections': [
                    'Qualification Context',
                    'Entry Requirements',
                    'Training Delivery Strategy',
                    'Assessment Framework',
                    'Learning Resources',
                    'Trainer Credentials',
                    'Continuous Improvement'
                ],
                'gpt_prompts': {
                    'context': 'Generate context for diploma level study...',
                    'assessment': 'Create diploma-level assessment framework...'
                }
            },
        ]
        
        for data in template_data:
            template, created = TASTemplate.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'created_by': user}
            )
            templates.append(template)
        
        return templates

    def create_tas_documents(self, tenants, users, templates):
        """Create TAS documents"""
        tas_docs = []
        
        qualifications = [
            ('BSB50120', 'Diploma of Business', 'diploma', 'business'),
            ('SIT30816', 'Certificate III in Commercial Cookery', 'certificate_iii', 'hospitality'),
            ('ICT40120', 'Certificate IV in Information Technology', 'certificate_iv', 'technology'),
            ('CHC33015', 'Certificate III in Individual Support', 'certificate_iii', 'health'),
            ('BSB40520', 'Certificate IV in Leadership and Management', 'certificate_iv', 'business'),
        ]
        
        statuses = ['draft', 'in_review', 'approved', 'published']
        
        for tenant in tenants[:2]:  # Create for first 2 tenants
            for i, (code, name, level, type_) in enumerate(qualifications):
                template = next((t for t in templates if t.aqf_level == level), templates[0])
                
                tas = TAS.objects.create(
                    tenant=tenant,
                    title=f"{name} - Training and Assessment Strategy",
                    code=code,
                    qualification_name=name,
                    aqf_level=level,
                    training_package=code[:3],
                    template=template,
                    status=statuses[i % len(statuses)],
                    version=1,
                    sections=[
                        {
                            'name': 'Overview',
                            'content': f'This TAS covers the delivery of {name} ({code})...'
                        },
                        {
                            'name': 'Training Delivery',
                            'content': 'Training will be delivered through a mix of classroom and practical sessions...'
                        },
                        {
                            'name': 'Assessment Strategy',
                            'content': 'Assessment aligns with QA1.2 (Assessment) standards...'
                        }
                    ],
                    content={
                        'overview': f'Comprehensive TAS for {name}',
                        'duration': '52 weeks',
                        'delivery_mode': 'Blended'
                    },
                    metadata={
                        'units': 12,
                        'core_units': 8,
                        'elective_units': 4
                    },
                    created_by=users[random.randint(0, len(users)-1)],
                    gpt_generated=random.choice([True, False])
                )
                tas_docs.append(tas)
        
        return tas_docs

    def create_tas_conversions(self, tas_docs, users):
        """Create TAS conversion sessions"""
        conversions = []
        
        statuses = ['pending', 'analyzing', 'mapping', 'converting', 'validating', 'completed', 'failed']
        
        for tas in tas_docs[:3]:  # Convert first 3 TAS documents
            status = random.choice(statuses)
            
            conversion = TASConversionSession.objects.create(
                tenant=tas.tenant,
                source_tas=tas,
                session_name=f"Convert {tas.code} to 2025 Standards",
                status=status,
                ai_model='gpt-4o',
                standards_mapping={
                    '1.1': {'targets': ['QA1.1', 'QA1.2'], 'mapping_type': 'split'},
                    '1.2': {'targets': ['QA3.2'], 'mapping_type': 'direct'}
                },
                conversion_changes=[
                    {
                        'section': 'Training Delivery',
                        'change_type': 'standard_reference',
                        'old': 'Standard 1.1',
                        'new': 'QA1.1 and QA1.2'
                    }
                ],
                quality_score=random.uniform(75, 95) if status == 'completed' else None,
                processing_time_seconds=random.uniform(120, 600) if status == 'completed' else 0,
                ai_tokens_used=random.randint(5000, 25000) if status == 'completed' else 0,
                created_by=users[0],
                created_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            
            if status == 'completed':
                conversion.completed_at = conversion.created_at + timedelta(minutes=random.randint(5, 20))
                conversion.save()
            
            conversions.append(conversion)
        
        return conversions

    def create_policies(self, tenants, users):
        """Create policy documents"""
        policies = []
        
        policy_templates = [
            {
                'policy_number': 'POL-001',
                'title': 'Assessment Policy',
                'policy_type': 'assessment',
                'content': '''This policy outlines our approach to assessment practices.

Assessment Principles:
- Assessments must be fair, flexible, valid and reliable
- Assessment aligns with Standard 1.1 requirements
- All trainers maintain current industry currency
- Assessment evidence is collected and stored securely

Quality Assurance:
- Regular moderation of assessment judgments
- Continuous improvement processes in place
- Compliance with ASQA Standards for RTOs 2015'''
            },
            {
                'policy_number': 'POL-002',
                'title': 'Student Support Policy',
                'policy_type': 'student_support',
                'content': '''Student Support Services

We provide comprehensive support to all students:
- Pre-enrollment information and counseling
- Language, literacy and numeracy support
- Learning support for students with special needs
- Complaint and appeal processes (Standard 6.1-6.6)
- Access to facilities and resources (Standard 1.8)'''
            },
            {
                'policy_number': 'POL-003',
                'title': 'Trainer and Assessor Credentials Policy',
                'policy_type': 'staff_management',
                'content': '''Trainer and Assessor Requirements

All trainers and assessors must meet Standard 1.2 requirements:
- Hold required TAE qualifications or demonstrate equivalence
- Maintain vocational competency in the field
- Demonstrate current industry currency
- Participate in professional development annually

Industry Currency:
- Minimum 20 hours per year in industry engagement
- Documentation of industry experience maintained'''
            },
            {
                'policy_number': 'POL-004',
                'title': 'Continuous Improvement Policy',
                'policy_type': 'quality_assurance',
                'content': '''Continuous Improvement Framework

Systematic approach to quality improvement:
- Annual review of all policies and procedures
- Student feedback collection and analysis
- Industry engagement to ensure currency
- Compliance monitoring aligned with Standard 8.1-8.6
- Regular management reviews'''
            },
            {
                'policy_number': 'POL-005',
                'title': 'Complaints and Appeals Policy',
                'policy_type': 'complaints_appeals',
                'content': '''Complaints and Appeals Process

Aligns with Standards 6.1 to 6.6:
- Clear process for lodging complaints
- Timeframes for resolution clearly stated
- Appeals handled independently
- Records maintained securely
- Natural justice principles upheld'''
            },
        ]
        
        for tenant in tenants[:2]:
            for template in policy_templates:
                policy = Policy.objects.create(
                    tenant=tenant,
                    **template,
                    status=random.choice(['draft', 'under_review', 'approved']),
                    version='1.0',
                    effective_date=timezone.now().date(),
                    review_date=(timezone.now() + timedelta(days=365)).date(),
                    compliance_score=random.uniform(65, 95),
                    last_compared_at=timezone.now() - timedelta(days=random.randint(1, 60)),
                    created_by=users[random.randint(0, len(users)-1)]
                )
                policies.append(policy)
        
        return policies

    def create_policy_conversions(self, policies, users):
        """Create policy conversion sessions"""
        conversions = []
        
        statuses = ['pending', 'analyzing', 'mapping', 'converting', 'validating', 'completed']
        
        for policy in policies[:4]:  # Convert first 4 policies
            status = random.choice(statuses)
            
            conversion = PolicyConversionSession.objects.create(
                tenant=policy.tenant,
                source_policy=policy,
                session_name=f"Convert {policy.title} to 2025",
                status=status,
                progress_percentage=0 if status == 'pending' else random.randint(20, 100),
                ai_model='gpt-4o',
                standards_mapping={
                    '1.1': {'targets': ['QA1.1', 'QA1.2']},
                    '1.2': {'targets': ['QA3.2']}
                },
                quality_score=random.uniform(80, 95) if status == 'completed' else None,
                processing_time_seconds=random.uniform(60, 300) if status == 'completed' else 0,
                created_by=users[0],
                created_at=timezone.now() - timedelta(days=random.randint(1, 20))
            )
            
            if status == 'completed':
                conversion.completed_at = conversion.created_at + timedelta(minutes=random.randint(2, 10))
                conversion.save()
            
            conversions.append(conversion)
        
        return conversions

    def create_comparison_sessions(self, policies, users):
        """Create comparison sessions"""
        sessions = []
        
        # Get some ASQA standards
        standards = ASQAStandard.objects.filter(version='2025')[:5]
        
        for i, policy in enumerate(policies[:3]):
            status = random.choice(['pending', 'processing', 'completed'])
            total_clauses = random.randint(10, 20)
            compliant = random.randint(6, 12)
            partial = random.randint(2, 5)
            gaps = total_clauses - compliant - partial
            
            session = ComparisonSession.objects.create(
                tenant=policy.tenant,
                policy=policy,
                session_name=f"Compliance Check - {policy.title}",
                status=status,
                standards_compared=[str(s.id) for s in standards[:3]] if standards.exists() else [],
                total_clauses_checked=total_clauses,
                compliant_count=compliant,
                partial_match_count=partial,
                gap_count=gaps,
                overall_compliance_score=random.uniform(70, 95),
                processing_time_seconds=random.uniform(2.5, 15.5),
                created_by=users[random.randint(0, len(users)-1)],
            )
            
            if status == 'completed':
                session.completed_at = timezone.now() - timedelta(hours=random.randint(1, 48))
                session.save()
            
            sessions.append(session)
        
        return sessions

    def create_api_keys(self, tenants, users):
        """Create API keys"""
        api_keys = []
        
        for tenant in tenants[:2]:
            # Generate a valid API key
            raw_key = TenantAPIKey.generate_key()
            key_hash = TenantAPIKey.hash_key(raw_key)
            key_prefix = raw_key[:8]  # First 8 characters as prefix
            
            api_key = TenantAPIKey.objects.create(
                tenant=tenant,
                name=f"{tenant.name} Production API Key",
                description=f"Production API key for {tenant.name}",
                key_prefix=key_prefix,
                key_hash=key_hash,
                expires_at=timezone.now() + timedelta(days=365),
                is_active=True,
                scopes=["read", "write"]
            )
            api_keys.append(api_key)
            self.stdout.write(f"  Created API key for {tenant.name}: {raw_key}")
        
        return api_keys
