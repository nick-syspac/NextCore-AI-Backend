"""
Management command to populate database with realistic test data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from tenants.models import Tenant, TenantUser, TenantAPIKey
from users.models import UserInvitation, EmailVerification
from authenticity_check.models import (
    AuthenticityCheck,
    SubmissionAnalysis,
    PlagiarismMatch,
    MetadataVerification,
    AnomalyDetection,
)
from continuous_improvement.models import (
    ImprovementCategory,
    ImprovementAction,
    ActionTracking,
    ImprovementReview,
)
from email_assistant.models import (
    StudentMessage,
    DraftReply,
    MessageTemplate,
    ConversationThread,
    ToneProfile,
    ReplyHistory,
)
from engagement_heatmap.models import (
    EngagementHeatmap,
    AttendanceRecord,
    LMSActivity,
    DiscussionSentiment,
    EngagementAlert,
)
from tas.models import TAS, TASTemplate, TASConversionSession
from policy_comparator.models import (
    Policy, ASQAStandard, ASQAClause, 
    ComparisonResult, ComparisonSession,
    PolicyConversionSession
)
from assessment_builder.models import Assessment, AssessmentTask, AssessmentCriteria, AssessmentGenerationLog
from audit_assistant.models import Evidence, ClauseEvidence, AuditReport, AuditReportClause
from auto_marker.models import AutoMarker, MarkedResponse, MarkingCriterion, CriterionScore
from competency_gap.models import TrainerQualification, UnitOfCompetency, TrainerAssignment, CompetencyGap
from adaptive_pathway.models import LearningPathway, LearningStep, StudentProgress, PathwayRecommendation


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
        
        # Create units of competency
        units = self.create_units_of_competency(tenants)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(units)} units of competency'))
        
        # Create trainer qualifications
        qualifications = self.create_trainer_qualifications(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(qualifications)} trainer qualifications'))
        
        # Create trainer assignments
        assignments = self.create_trainer_assignments(tenants, users, units)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(assignments)} trainer assignments'))
        
        # Create competency gaps
        gaps = self.create_competency_gaps(assignments, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(gaps)} competency gaps'))
        
        # Create assessments
        assessments = self.create_assessments(tenants, users, tas_docs)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(assessments)} assessments'))
        
        # Create assessment tasks
        tasks = self.create_assessment_tasks(assessments, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(tasks)} assessment tasks'))
        
        # Create evidence
        evidence_items = self.create_evidence(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(evidence_items)} evidence items'))
        
        # Create audit reports
        audit_reports = self.create_audit_reports(tenants, users, evidence_items)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(audit_reports)} audit reports'))
        
        # Create auto markers
        markers = self.create_auto_markers(tenants, assessments, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(markers)} auto markers'))
        
        # Create learning pathways
        pathways = self.create_learning_pathways(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(pathways)} learning pathways'))
        
        # Create learning steps
        steps = self.create_learning_steps(pathways)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(steps)} learning steps'))
        
        # Create student progress
        progress = self.create_student_progress(pathways, steps, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(progress)} progress records'))
        
        # Create pathway recommendations
        recommendations = self.create_pathway_recommendations(tenants, users, pathways)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(recommendations)} pathway recommendations'))
        
        # Create user invitations
        invitations = self.create_user_invitations(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(invitations)} user invitations'))
        
        # Create email verifications
        verifications = self.create_email_verifications(users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(verifications)} email verifications'))
        
        # Create authenticity checks
        authenticity_checks = self.create_authenticity_checks(tenants, users, assessments)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(authenticity_checks)} authenticity checks'))
        
        # Create submission analyses
        submission_analyses = self.create_submission_analyses(authenticity_checks, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(submission_analyses)} submission analyses'))
        
        # Create plagiarism matches
        plagiarism_matches = self.create_plagiarism_matches(submission_analyses)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(plagiarism_matches)} plagiarism matches'))
        
        # Create metadata verifications
        metadata_verifications = self.create_metadata_verifications(submission_analyses)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(metadata_verifications)} metadata verifications'))
        
        # Create anomaly detections
        anomaly_detections = self.create_anomaly_detections(submission_analyses)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(anomaly_detections)} anomaly detections'))
        
        # Create improvement categories
        improvement_categories = self.create_improvement_categories(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(improvement_categories)} improvement categories'))
        
        # Create improvement actions
        improvement_actions = self.create_improvement_actions(tenants, users, improvement_categories)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(improvement_actions)} improvement actions'))
        
        # Create action tracking updates
        action_tracking = self.create_action_tracking(improvement_actions, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(action_tracking)} action tracking updates'))
        
        # Create improvement reviews
        improvement_reviews = self.create_improvement_reviews(tenants, users, improvement_actions)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(improvement_reviews)} improvement reviews'))
        
        # Create message templates
        message_templates = self.create_message_templates(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(message_templates)} message templates'))
        
        # Create tone profiles
        tone_profiles = self.create_tone_profiles(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(tone_profiles)} tone profiles'))
        
        # Create conversation threads
        conversation_threads = self.create_conversation_threads(tenants)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(conversation_threads)} conversation threads'))
        
        # Create student messages
        student_messages = self.create_student_messages(tenants, conversation_threads, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(student_messages)} student messages'))
        
        # Create draft replies
        draft_replies = self.create_draft_replies(student_messages, message_templates, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(draft_replies)} draft replies'))
        
        # Create reply history
        reply_history = self.create_reply_history(student_messages, draft_replies, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(reply_history)} reply history records'))
        
        # Create engagement heatmap data
        engagement_heatmaps = self.create_engagement_heatmaps(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(engagement_heatmaps)} engagement heatmaps'))
        
        attendance_records = self.create_attendance_records(engagement_heatmaps)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(attendance_records)} attendance records'))
        
        lms_activities = self.create_lms_activities(engagement_heatmaps)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(lms_activities)} LMS activities'))
        
        discussion_sentiments = self.create_discussion_sentiments(engagement_heatmaps)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(discussion_sentiments)} discussion sentiments'))
        
        engagement_alerts = self.create_engagement_alerts(engagement_heatmaps)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(engagement_alerts)} engagement alerts'))
        
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
        # Engagement Heatmap
        try:
            EngagementAlert.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            DiscussionSentiment.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            LMSActivity.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            AttendanceRecord.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            EngagementHeatmap.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Email Assistant
        try:
            ReplyHistory.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            DraftReply.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            StudentMessage.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            ConversationThread.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            ToneProfile.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            MessageTemplate.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Continuous Improvement
        try:
            ImprovementReview.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            ActionTracking.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            ImprovementAction.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            ImprovementCategory.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Authenticity Check
        try:
            AnomalyDetection.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            MetadataVerification.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            PlagiarismMatch.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            SubmissionAnalysis.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            AuthenticityCheck.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Users & Auth
        try:
            UserInvitation.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            EmailVerification.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Adaptive Pathway
        try:
            PathwayRecommendation.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            StudentProgress.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            LearningStep.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            LearningPathway.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Assessment Builder
        try:
            AssessmentGenerationLog.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            AssessmentCriteria.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            AssessmentTask.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            Assessment.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Auto Marker
        try:
            CriterionScore.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            MarkingCriterion.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            MarkedResponse.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            AutoMarker.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Competency Gap
        try:
            CompetencyGap.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            TrainerAssignment.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            TrainerQualification.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            UnitOfCompetency.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Audit Assistant
        try:
            AuditReportClause.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            ClauseEvidence.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            AuditReport.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            Evidence.objects.all().delete()
        except ProgrammingError:
            pass
        
        # TAS & Policy
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

    def create_units_of_competency(self, tenants):
        """Create units of competency"""
        units = []
        
        unit_data = [
            {'code': 'BSBWHS521', 'name': 'Ensure a safe workplace for a work area', 'qual': 'BSB50120', 'type': 'core'},
            {'code': 'BSBMGT502', 'name': 'Manage people performance', 'qual': 'BSB40520', 'type': 'core'},
            {'code': 'SITHCCC023', 'name': 'Use food preparation equipment', 'qual': 'SIT30816', 'type': 'core'},
            {'code': 'SITHCCC027', 'name': 'Prepare dishes using basic methods of cookery', 'qual': 'SIT30816', 'type': 'core'},
            {'code': 'ICTICT451', 'name': 'Comply with IP, ethics and privacy policies in ICT', 'qual': 'ICT40120', 'type': 'core'},
            {'code': 'ICTPRG302', 'name': 'Apply introductory programming techniques', 'qual': 'ICT40120', 'type': 'elective'},
            {'code': 'CHCCCS023', 'name': 'Support independence and wellbeing', 'qual': 'CHC33015', 'type': 'core'},
            {'code': 'CHCDIV001', 'name': 'Work with diverse people', 'qual': 'CHC33015', 'type': 'core'},
        ]
        
        for tenant in tenants[:2]:
            for data in unit_data:
                unit, created = UnitOfCompetency.objects.get_or_create(
                    tenant=tenant.slug,
                    unit_code=data['code'],
                    defaults={
                        'unit_name': data['name'],
                        'unit_type': data['type'],
                        'qualification_code': data['qual'],
                        'required_qualifications': ['TAE40116'],
                        'required_competency_areas': ['Training and Assessment', data['qual'][:3]],
                        'required_industry_experience': 2,
                        'requires_tae': True,
                        'requires_industry_currency': True,
                        'learning_outcomes': ['LO1', 'LO2', 'LO3'],
                        'assessment_methods': ['Written Assessment', 'Practical Demonstration'],
                        'technical_skills': ['Communication', 'Problem Solving'],
                        'prerequisite_units': [],
                        'related_units': []
                    }
                )
                if created:
                    units.append(unit)
        
        return units

    def create_trainer_qualifications(self, tenants, users):
        """Create trainer qualifications"""
        qualifications = []
        
        qual_types = ['tae_cert_iv', 'bachelor', 'industry_cert', 'diploma']
        qual_names = {
            'tae_cert_iv': ('TAE40116', 'Certificate IV in Training and Assessment'),
            'bachelor': ('DEGREE2023', 'Bachelor of Education'),
            'industry_cert': ('CERT2023', 'Industry Professional Certification'),
            'diploma': ('DIP50120', 'Diploma of Vocational Education and Training')
        }
        
        for user in users[2:]:  # trainers and assessors
            for tenant in tenants[:2]:
                qual_type = random.choice(qual_types)
                qual_code, qual_name = qual_names[qual_type]
                
                qual = TrainerQualification.objects.create(
                    tenant=tenant.slug,
                    trainer_id=str(user.id),
                    trainer_name=user.get_full_name(),
                    qualification_type=qual_type,
                    qualification_code=qual_code,
                    qualification_name=qual_name,
                    issuing_organization=random.choice(['ASQA Accredited RTO', 'University of Sydney', 'TAFE NSW']),
                    date_obtained=timezone.now().date() - timedelta(days=random.randint(365, 1825)),
                    expiry_date=timezone.now().date() + timedelta(days=random.randint(365, 1095)) if random.random() > 0.5 else None,
                    verification_status=random.choice(['verified', 'pending', 'verified']),
                    competency_areas=['Training and Assessment', 'VET Sector'],
                    units_covered=['TAESS00001', 'TAESS00003'],
                    industry_experience_years=random.randint(2, 10),
                    recent_industry_work=random.choice([True, False])
                )
                qualifications.append(qual)
        
        return qualifications

    def create_trainer_assignments(self, tenants, users, units):
        """Create trainer assignments"""
        assignments = []
        
        trainers = users[2:4]  # trainer and assessor users
        
        for tenant in tenants[:2]:
            tenant_units = [u for u in units if u.tenant == tenant.slug]
            for trainer in trainers:
                # Assign 2-4 units per trainer
                assigned_units = random.sample(tenant_units, min(random.randint(2, 4), len(tenant_units)))
                for unit in assigned_units:
                    assignment, created = TrainerAssignment.objects.get_or_create(
                        tenant=tenant.slug,
                        trainer_id=str(trainer.id),
                        unit=unit,
                        defaults={
                            'trainer_name': trainer.get_full_name(),
                            'assignment_status': random.choice(['approved', 'pending', 'approved']),
                            'assigned_date': timezone.now().date() - timedelta(days=random.randint(30, 365)),
                            'meets_requirements': True,
                            'compliance_score': random.uniform(85, 100),
                            'gaps_identified': [],
                            'matching_qualifications': ['TAE40116'],
                            'assignment_notes': f'{trainer.get_full_name()} is qualified to deliver this unit'
                        }
                    )
                    if created:
                        assignments.append(assignment)
        
        return assignments

    def create_competency_gaps(self, assignments, users):
        """Create competency gaps"""
        gaps = []
        
        gap_types = ['insufficient_experience', 'missing_currency', 'missing_tae', 'competency_mismatch']
        severities = ['low', 'medium', 'high']
        
        # Create some gaps for testing
        for assignment in random.sample(list(assignments), min(3, len(assignments))):
            gap_type = random.choice(gap_types)
            gap = CompetencyGap.objects.create(
                tenant=assignment.tenant,
                trainer_id=assignment.trainer_id,
                trainer_name=assignment.trainer_name,
                unit=assignment.unit,
                assignment=assignment,
                gap_type=gap_type,
                gap_severity=random.choice(severities),
                gap_description=f'Gap identified in {gap_type.replace("_", " ")}',
                required_qualification='TAE40116' if gap_type == 'missing_tae' else '',
                required_competency='Industry Currency' if gap_type == 'missing_currency' else '',
                required_experience_years=3 if gap_type == 'insufficient_experience' else None,
                current_qualifications=['QUAL2020'],
                recommended_action='Complete professional development or obtain required qualifications',
                estimated_resolution_time='3-6 months'
            )
            gaps.append(gap)
        
        return gaps

    def create_assessments(self, tenants, users, tas_docs):
        """Create assessments"""
        assessments = []
        
        assessment_types = ['knowledge', 'practical', 'project', 'portfolio']
        
        for tas in tas_docs[:5]:
            assessment = Assessment.objects.create(
                tenant=tas.tenant,
                unit_code=tas.code,
                unit_title=tas.qualification_name,
                training_package=tas.code[:3],
                title=f'{tas.code} - {random.choice(["Knowledge Assessment", "Practical Assessment", "Project Assessment", "Portfolio"])}',
                assessment_type=random.choice(assessment_types),
                instructions='Complete all tasks according to the instructions provided.',
                context=f'This assessment is for {tas.qualification_name}',
                conditions='Standard assessment conditions apply',
                version='1.0',
                estimated_duration_hours=random.uniform(1.5, 4.0),
                status=random.choice(['draft', 'review', 'approved']),
                ai_generated=random.choice([True, False]),
                ai_model='gpt-4' if random.random() > 0.5 else '',
                is_compliant=True,
                compliance_score=random.randint(85, 100),
                elements_covered=['Element 1', 'Element 2'],
                performance_criteria_covered=['PC1.1', 'PC1.2', 'PC2.1'],
                created_by=users[random.randint(0, len(users)-1)]
            )
            assessments.append(assessment)
        
        return assessments

    def create_assessment_tasks(self, assessments, users):
        """Create assessment tasks"""
        tasks = []
        
        task_types = ['multiple_choice', 'short_answer', 'practical', 'project']
        blooms_levels = ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']
        
        for assessment in assessments:
            # Create 3-5 tasks per assessment
            for i in range(random.randint(3, 5)):
                task = AssessmentTask.objects.create(
                    assessment=assessment,
                    task_number=str(i + 1),
                    task_type=random.choice(task_types),
                    question=f'Task {i + 1}: {random.choice(["Describe the key principles", "Demonstrate your understanding", "Complete the following", "Analyze the scenario"])}',
                    context='This task assesses your understanding of the unit requirements.',
                    ai_generated=random.choice([True, False]),
                    ai_rationale='Generated to assess performance criteria' if random.random() > 0.5 else '',
                    blooms_level=random.choice(blooms_levels),
                    blooms_verbs=['describe', 'explain', 'demonstrate'],
                    maps_to_elements=['Element 1', 'Element 2'],
                    maps_to_performance_criteria=['PC1.1', 'PC1.2', 'PC2.1'],
                    maps_to_knowledge_evidence=['KE1', 'KE2'],
                    question_count=1,
                    estimated_time_minutes=random.randint(30, 120),
                    marks_available=random.randint(10, 50),
                    display_order=i
                )
                tasks.append(task)
        
        return tasks

    def create_evidence(self, tenants, users):
        """Create evidence items"""
        evidence_items = []
        
        evidence_types = ['policy', 'procedure', 'record', 'assessment', 'training_material']
        
        # Note: Evidence requires an actual file upload, so we'll create minimal records
        # In a real scenario, you'd upload actual files
        for tenant in tenants[:2]:
            for i in range(3):
                # Create a simple text file content
                from django.core.files.base import ContentFile
                import uuid
                
                evidence_number = f"EV-{timezone.now().strftime('%Y%m')}-{str(uuid.uuid4())[:8].upper()}"
                content = f"Test evidence document {i+1} for {tenant.name}"
                file_content = ContentFile(content.encode('utf-8'))
                
                evidence = Evidence.objects.create(
                    tenant=tenant,
                    evidence_number=evidence_number,
                    title=f'Evidence {i+1} - {random.choice(["Assessment Report", "Training Records", "Student Work Sample", "Policy Document"])}',
                    evidence_type=random.choice(evidence_types),
                    description=f'Evidence collected for compliance audit',
                    evidence_date=timezone.now().date() - timedelta(days=random.randint(30, 180)),
                    extracted_text=content,
                    ner_entities=[],
                    status=random.choice(['uploaded', 'tagged', 'reviewed']),
                    uploaded_by=users[random.randint(0, len(users)-1)]
                )
                # Save file separately to handle upload_to path
                evidence.file.save(f'evidence_{evidence_number}.txt', file_content, save=True)
                evidence_items.append(evidence)
        
        return evidence_items

    def create_audit_reports(self, tenants, users, evidence_items):
        """Create audit reports"""
        reports = []
        
        import uuid
        
        for tenant in tenants[:2]:
            for i in range(2):
                start_date = timezone.now().date() - timedelta(days=random.randint(180, 365))
                end_date = start_date + timedelta(days=90)
                report_number = f"AR-{timezone.now().strftime('%Y')}-{str(uuid.uuid4())[:8].upper()}"
                
                report = AuditReport.objects.create(
                    tenant=tenant,
                    report_number=report_number,
                    title=f'{timezone.now().year} {random.choice(["Annual", "Mid-Year", "Compliance"])} Audit Report',
                    description='Comprehensive audit of RTO operations and compliance',
                    audit_period_start=start_date,
                    audit_period_end=end_date,
                    status=random.choice(['draft', 'in_progress', 'completed']),
                    total_clauses=random.randint(50, 100),
                    clauses_with_evidence=random.randint(40, 80),
                    clauses_without_evidence=random.randint(5, 20),
                    compliance_percentage=random.uniform(75, 95),
                    critical_clauses_count=random.randint(10, 20),
                    critical_clauses_covered=random.randint(8, 18),
                    critical_compliance_percentage=random.uniform(80, 100),
                    total_evidence_count=len([e for e in evidence_items if e.tenant == tenant]),
                    auto_tagged_count=random.randint(5, 10),
                    manually_tagged_count=random.randint(2, 5),
                    verified_evidence_count=random.randint(3, 8),
                    findings=[{'clause': '1.1', 'finding': 'Compliant', 'severity': 'low'}],
                    recommendations=['Continue current practices', 'Update policies annually'],
                    created_by=users[0]
                )
                reports.append(report)
        
        return reports

    def create_auto_markers(self, tenants, assessments, users):
        """Create auto markers"""
        markers = []
        
        for assessment in assessments[:3]:
            marker = AutoMarker.objects.create(
                tenant=assessment.tenant.slug,
                title=f'Auto Marker - {assessment.title}',
                description=f'Automated marking for {assessment.title}',
                answer_type=random.choice(['short_answer', 'essay', 'explanation']),
                question_text='Explain the key principles and demonstrate understanding',
                model_answer='The key principles include proper assessment, validation, and continuous improvement in accordance with VET standards.',
                max_marks=random.randint(10, 50),
                similarity_model='sentence_transformers',
                similarity_threshold=0.70,
                partial_credit_enabled=True,
                min_similarity_for_credit=0.40,
                use_keywords=True,
                keywords=['assessment', 'validation', 'standards', 'compliance'],
                keyword_weight=0.20,
                status='active',
                created_by=users[0]
            )
            markers.append(marker)
        
        return markers

    def create_learning_pathways(self, tenants, users):
        """Create learning pathways"""
        pathways = []
        
        pathway_templates = [
            {
                'name': 'Introduction to Training and Assessment',
                'difficulty': 'beginner',
                'duration': 40.0,
                'description': 'Complete pathway for new trainers to understand VET sector requirements'
            },
            {
                'name': 'Advanced Compliance Management',
                'difficulty': 'advanced',
                'duration': 60.0,
                'description': 'Deep dive into ASQA standards and compliance frameworks'
            },
            {
                'name': 'Assessment Design Mastery',
                'difficulty': 'intermediate',
                'duration': 50.0,
                'description': 'Learn to create effective assessments aligned with industry standards'
            },
        ]
        
        # Create pathways for trainers
        for user in users[2:4]:  # trainers
            for tenant in tenants[:2]:
                for template in pathway_templates:
                    pathway = LearningPathway.objects.create(
                        tenant=tenant.slug,
                        student_id=str(user.id),
                        student_name=user.get_full_name(),
                        pathway_name=template['name'],
                        description=template['description'],
                        difficulty_level=template['difficulty'],
                        estimated_duration_hours=template['duration'],
                        recommendation_confidence=random.uniform(75, 95),
                        similarity_score=random.uniform(0.75, 0.95),
                        status=random.choice(['active', 'active', 'completed']),
                        total_steps=random.randint(5, 10),
                        completed_steps=random.randint(0, 5),
                        personalization_factors={
                            'learning_style': random.choice(['visual', 'auditory', 'kinesthetic']),
                            'pace': random.choice(['slow', 'moderate', 'fast']),
                            'interests': ['compliance', 'assessment', 'training'],
                            'prior_knowledge': template['difficulty']
                        },
                        similar_students=['student_123', 'student_456']
                    )
                    
                    if pathway.status == 'active':
                        pathway.started_at = timezone.now() - timedelta(days=random.randint(1, 30))
                    elif pathway.status == 'completed':
                        pathway.started_at = timezone.now() - timedelta(days=random.randint(30, 90))
                        pathway.completed_at = timezone.now() - timedelta(days=random.randint(1, 15))
                    
                    pathway.save()
                    pathways.append(pathway)
        
        return pathways

    def create_learning_steps(self, pathways):
        """Create learning steps for pathways"""
        steps = []
        
        content_types = ['video', 'reading', 'quiz', 'assignment', 'interactive']
        
        step_templates = [
            {'title': 'Introduction to VET Standards', 'type': 'video', 'minutes': 15, 'difficulty': 2.0},
            {'title': 'Understanding ASQA Requirements', 'type': 'reading', 'minutes': 30, 'difficulty': 3.0},
            {'title': 'Compliance Framework Overview', 'type': 'interactive', 'minutes': 20, 'difficulty': 2.5},
            {'title': 'Assessment Design Principles', 'type': 'video', 'minutes': 25, 'difficulty': 3.5},
            {'title': 'Knowledge Check Quiz', 'type': 'quiz', 'minutes': 15, 'difficulty': 3.0},
            {'title': 'Practical Assessment Task', 'type': 'assignment', 'minutes': 60, 'difficulty': 4.0},
            {'title': 'Industry Standards Deep Dive', 'type': 'reading', 'minutes': 40, 'difficulty': 4.5},
        ]
        
        for pathway in pathways:
            num_steps = pathway.total_steps
            for i in range(num_steps):
                template = random.choice(step_templates)
                
                step = LearningStep.objects.create(
                    pathway=pathway,
                    title=template['title'],
                    description=f'Learning content for {template["title"]}',
                    content_type=template['type'],
                    content_url=f'https://learning.example.com/content/{i+1}',
                    sequence_order=i + 1,
                    is_prerequisite=(i == 0),
                    prerequisites=[f'STEP-{i}'] if i > 0 else [],
                    estimated_minutes=template['minutes'],
                    difficulty_rating=template['difficulty'],
                    learning_objectives=[
                        f'Understand key concepts of {template["title"]}',
                        'Apply knowledge in practical scenarios',
                        'Demonstrate mastery through assessment'
                    ],
                    tags=['VET', 'compliance', 'training', template['type']],
                    status=random.choice(['completed', 'in_progress', 'not_started']) if i < pathway.completed_steps else 'not_started'
                )
                
                if step.status == 'completed':
                    step.started_at = timezone.now() - timedelta(days=random.randint(5, 30))
                    step.completed_at = timezone.now() - timedelta(days=random.randint(1, 20))
                    step.completion_score = random.uniform(70, 100)
                elif step.status == 'in_progress':
                    step.started_at = timezone.now() - timedelta(days=random.randint(1, 5))
                
                step.save()
                steps.append(step)
        
        return steps

    def create_student_progress(self, pathways, steps, users):
        """Create student progress records"""
        progress_records = []
        
        for pathway in pathways:
            pathway_steps = [s for s in steps if s.pathway == pathway]
            
            for step in pathway_steps[:pathway.completed_steps]:
                progress = StudentProgress.objects.create(
                    tenant=pathway.tenant,
                    student_id=pathway.student_id,
                    pathway=pathway,
                    step=step,
                    time_spent_minutes=random.randint(step.estimated_minutes, step.estimated_minutes * 2),
                    completion_score=random.uniform(70, 100),
                    attempts=random.randint(1, 2),
                    struggle_indicators={
                        'multiple_attempts': random.choice([True, False]),
                        'extended_time': random.choice([True, False]),
                        'help_requests': random.randint(0, 3)
                    },
                    engagement_level=random.choice(['high', 'medium', 'low']),
                    recommended_next_steps=[],
                    difficulty_adjustment=random.choice(['maintain', 'maintain', 'easier']),
                    is_completed=True
                )
                
                progress.completed_at = timezone.now() - timedelta(days=random.randint(1, 30))
                progress.save()
                progress_records.append(progress)
        
        return progress_records

    def create_pathway_recommendations(self, tenants, users, pathways):
        """Create pathway recommendations"""
        recommendations = []
        
        recommendation_reasons = [
            'Similar students with your background found this pathway effective',
            'Based on your learning style and pace preferences',
            'Recommended to fill identified competency gaps',
            'Popular choice among trainers in your field',
            'Aligns with your career development goals'
        ]
        
        for user in users[2:4]:  # trainers
            for tenant in tenants[:2]:
                tenant_pathways = [p for p in pathways if p.tenant == tenant.slug and p.student_id != str(user.id)]
                
                if tenant_pathways:
                    for i in range(min(2, len(tenant_pathways))):
                        sample_pathway = random.choice(tenant_pathways)
                        
                        recommendation = PathwayRecommendation.objects.create(
                            tenant=tenant.slug,
                            student_id=str(user.id),
                            student_name=user.get_full_name(),
                            recommended_pathway=sample_pathway,
                            algorithm_used=random.choice(['collaborative_filtering', 'content_based', 'hybrid']),
                            recommendation_score=random.uniform(0.75, 0.95),
                            collaborative_score=random.uniform(0.70, 0.90),
                            embedding_similarity=random.uniform(0.75, 0.95),
                            similar_students_count=random.randint(5, 50),
                            similar_students_list=['student_123', 'student_456', 'student_789'],
                            common_pathways=['PATH-001', 'PATH-002'],
                            recommendation_reasons=[random.choice(recommendation_reasons) for _ in range(2)],
                            is_accepted=random.choice([True, False, None]),
                            feedback_score=random.randint(3, 5) if random.random() > 0.5 else None,
                            expires_at=timezone.now() + timedelta(days=30)
                        )
                        
                        recommendations.append(recommendation)
        
        return recommendations

    def create_user_invitations(self, tenants, users):
        """Create user invitations with various states"""
        invitations = []
        
        invitation_messages = [
            'We would love to have you join our training team.',
            'Your expertise would be a great addition to our organization.',
            'Join us to help deliver quality education and training.',
            'We think you would be a perfect fit for our team.',
            'Please accept this invitation to collaborate with us.'
        ]
        
        # Pending invitations (future expiry)
        for i, tenant in enumerate(tenants):
            for j in range(2):
                email = f'pending{i}_{j}@example.com'
                role = random.choice(['member', 'viewer', 'admin'])
                
                invitation = UserInvitation.objects.create(
                    tenant=tenant,
                    email=email,
                    role=role,
                    invited_by=users[0],  # admin user
                    message=random.choice(invitation_messages),
                    status='pending',
                    expires_at=timezone.now() + timedelta(days=random.randint(3, 7))
                )
                invitations.append(invitation)
        
        # Accepted invitations (linked to existing TenantUser relationships)
        for i, tenant in enumerate(tenants):
            for user in users[1:3]:  # manager and trainer
                invitation = UserInvitation.objects.create(
                    tenant=tenant,
                    email=user.email,
                    role='member',
                    invited_by=users[0],
                    message=invitation_messages[0],
                    status='accepted',
                    expires_at=timezone.now() + timedelta(days=7),
                    accepted_at=timezone.now() - timedelta(days=random.randint(1, 10)),
                    accepted_by=user
                )
                invitations.append(invitation)
        
        # Expired invitations (past expiry)
        for i, tenant in enumerate(tenants[:2]):
            email = f'expired{i}@example.com'
            
            invitation = UserInvitation.objects.create(
                tenant=tenant,
                email=email,
                role='viewer',
                invited_by=users[0],
                message='This invitation has expired',
                status='expired',
                expires_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            invitations.append(invitation)
        
        # Cancelled invitation
        invitation = UserInvitation.objects.create(
            tenant=tenants[0],
            email='cancelled@example.com',
            role='member',
            invited_by=users[0],
            message='This invitation was cancelled',
            status='cancelled',
            expires_at=timezone.now() + timedelta(days=7)
        )
        invitations.append(invitation)
        
        return invitations

    def create_email_verifications(self, users):
        """Create email verification records"""
        verifications = []
        
        # Verified users (admin and manager)
        for user in users[:2]:
            verification = EmailVerification.objects.create(
                user=user,
                verified=True,
                verified_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            verifications.append(verification)
        
        # Unverified users (trainer and assessor)
        for user in users[2:4]:
            verification = EmailVerification.objects.create(
                user=user,
                verified=False
            )
            verifications.append(verification)
        
        return verifications

    def create_authenticity_checks(self, tenants, users, assessments):
        """Create authenticity check records"""
        checks = []
        
        for i, assessment in enumerate(assessments[:3]):  # Create checks for first 3 assessments
            check = AuthenticityCheck.objects.create(
                assessment=assessment,
                name=f"Authenticity Check - {assessment.unit_code}",
                description=f"Comprehensive authenticity verification for {assessment.unit_title} submissions",
                plagiarism_threshold=random.choice([0.6, 0.7, 0.75, 0.8]),
                metadata_verification_enabled=True,
                anomaly_detection_enabled=True,
                academic_integrity_mode=random.choice([True, True, False]),
                status=random.choice(['completed', 'completed', 'processing', 'flagged']),
                total_submissions_checked=random.randint(5, 15),
                plagiarism_cases_detected=random.randint(0, 3),
                metadata_issues_found=random.randint(0, 2),
                anomalies_detected=random.randint(0, 4),
                overall_integrity_score=random.uniform(75.0, 95.0),
                created_by=users[0]
            )
            checks.append(check)
        
        return checks

    def create_submission_analyses(self, checks, users):
        """Create submission analysis records"""
        analyses = []
        
        sample_submissions = [
            {
                'content': 'This submission demonstrates comprehensive understanding of work health and safety principles. The student has identified key hazards in the workplace including electrical hazards, slips and trips, and manual handling risks. Control measures have been appropriately recommended following the hierarchy of controls, prioritizing elimination and substitution before considering engineering controls and PPE.',
                'student_name': 'Emma Wilson',
            },
            {
                'content': 'Work health safety principles are important in workplace. Hazards include electrical, slips trips, manual handling. Control measures follow hierarchy of controls with elimination and substitution before engineering controls and PPE.',
                'student_name': 'James Chen',
            },
            {
                'content': 'The implementation of WHS management systems requires a systematic approach to identifying, assessing and controlling workplace risks. This involves conducting regular workplace inspections, consulting with workers, reviewing incident reports, and maintaining comprehensive documentation. Risk assessments must consider both the likelihood and consequence of potential hazards.',
                'student_name': 'Sarah Johnson',
            },
            {
                'content': 'In this assignment I will discuss the workplace health and safety requirements. The Work Health and Safety Act 2011 requires employers to provide a safe working environment. This includes providing adequate training, maintaining equipment, and ensuring proper supervision of workers.',
                'student_name': 'Michael Brown',
            },
            {
                'content': 'This submission demonstrates comprehensive understanding of work health and safety principles. The student has identified key hazards in the workplace including electrical hazards, slips and trips, and manual handling risks. Control measures have been appropriately recommended.',
                'student_name': 'Jessica Lee',
            },
        ]
        
        for check in checks:
            num_submissions = min(len(sample_submissions), check.total_submissions_checked)
            
            for i in range(num_submissions):
                submission = sample_submissions[i]
                
                # Generate embedding (mock 384-dimensional vector)
                embedding = [random.uniform(-1, 1) for _ in range(384)]
                
                analysis = SubmissionAnalysis.objects.create(
                    authenticity_check=check,
                    submission_id=f"SUB-{timezone.now().strftime('%Y%m%d')}-{i+1:04d}",
                    student_id=f"STU-{random.randint(1000, 9999)}",
                    student_name=submission['student_name'],
                    submission_content=submission['content'],
                    content_embedding=embedding,
                    plagiarism_score=random.uniform(0.0, 0.85),
                    metadata_verification_score=random.uniform(80.0, 100.0),
                    anomaly_score=random.uniform(0.0, 40.0),
                    plagiarism_detected=(random.random() < 0.3),
                    metadata_issues=(random.random() < 0.2),
                    anomalies_found=(random.random() < 0.25),
                    analysis_metadata={
                        'language': 'en-AU',
                        'submission_time': (timezone.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
                        'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
                        'device_type': random.choice(['Desktop', 'Laptop', 'Tablet']),
                    }
                )
                
                # Calculate combined integrity score
                analysis.calculate_combined_score()
                analyses.append(analysis)
        
        return analyses

    def create_plagiarism_matches(self, analyses):
        """Create plagiarism match records"""
        matches = []
        
        # Create matches between similar submissions
        if len(analyses) >= 2:
            # Match first and last submission (high similarity)
            match = PlagiarismMatch.objects.create(
                source_analysis=analyses[0],
                matched_analysis=analyses[-1],
                similarity_score=random.uniform(0.85, 0.95),
                match_type='embedding',
                matched_text_segments=[
                    {
                        'source_start': 0,
                        'source_end': 150,
                        'match_start': 0,
                        'match_end': 145,
                        'text': 'work health and safety principles... key hazards'
                    }
                ],
                matched_words_count=random.randint(50, 100),
                matched_percentage=random.uniform(70, 90),
                reviewed=random.choice([True, False]),
                false_positive=False
            )
            matches.append(match)
        
        if len(analyses) >= 3:
            # Another match with medium similarity
            match = PlagiarismMatch.objects.create(
                source_analysis=analyses[1],
                matched_analysis=analyses[2],
                similarity_score=random.uniform(0.65, 0.75),
                match_type='paraphrased',
                matched_text_segments=[
                    {
                        'source_start': 20,
                        'source_end': 80,
                        'match_start': 15,
                        'match_end': 75,
                        'text': 'workplace risks... documentation'
                    }
                ],
                matched_words_count=random.randint(20, 40),
                matched_percentage=random.uniform(40, 60),
                reviewed=True,
                false_positive=False,
                review_notes='Legitimate paraphrasing detected, but similarity warrants monitoring'
            )
            matches.append(match)
        
        return matches

    def create_metadata_verifications(self, analyses):
        """Create metadata verification records"""
        verifications = []
        
        for analysis in analyses[:4]:  # Verify first 4 submissions
            anomalies = []
            
            # Randomly add anomalies
            if random.random() < 0.3:
                anomalies.append({
                    'type': 'author_mismatch',
                    'description': 'Document author does not match student name',
                    'severity': 'medium'
                })
            
            if random.random() < 0.2:
                anomalies.append({
                    'type': 'modification_pattern',
                    'description': 'Multiple rapid modifications detected',
                    'severity': 'low'
                })
            
            if random.random() < 0.15:
                anomalies.append({
                    'type': 'creation_timestamp',
                    'description': 'File creation date predates assessment release',
                    'severity': 'high'
                })
            
            verification = MetadataVerification.objects.create(
                submission_analysis=analysis,
                file_metadata={
                    'file_type': random.choice(['docx', 'pdf', 'txt']),
                    'file_size': random.randint(50000, 500000),
                    'page_count': random.randint(3, 15),
                },
                creation_timestamp=timezone.now() - timedelta(days=random.randint(1, 30)),
                modification_timestamp=timezone.now() - timedelta(hours=random.randint(1, 48)),
                modification_history=[
                    {
                        'timestamp': (timezone.now() - timedelta(days=2)).isoformat(),
                        'action': 'created'
                    },
                    {
                        'timestamp': (timezone.now() - timedelta(days=1)).isoformat(),
                        'action': 'modified'
                    }
                ],
                author_info={
                    'name': analysis.student_name,
                    'email': f"{analysis.student_name.lower().replace(' ', '.')}@example.com"
                },
                author_matches_student=(len(anomalies) == 0 or anomalies[0]['type'] != 'author_mismatch'),
                anomalies_detected=anomalies
            )
            verifications.append(verification)
        
        return verifications

    def create_anomaly_detections(self, analyses):
        """Create anomaly detection records"""
        detections = []
        
        anomaly_types_data = [
            {
                'type': 'typing_speed',
                'description': 'Typing speed significantly above student average (250 WPM vs typical 45 WPM)',
                'severity': 'high',
                'confidence': 0.85,
                'data': {'average_wpm': 250, 'student_baseline': 45, 'percentile': 99}
            },
            {
                'type': 'paste_events',
                'description': 'Multiple large paste events detected throughout submission',
                'severity': 'medium',
                'confidence': 0.75,
                'data': {'paste_count': 12, 'avg_paste_size': 350, 'total_pasted_chars': 4200}
            },
            {
                'type': 'time_gaps',
                'description': 'Suspicious time gap: 15 minutes inactive followed by 500 words added',
                'severity': 'medium',
                'confidence': 0.65,
                'data': {'gap_duration_minutes': 15, 'words_after_gap': 500, 'normal_rate': 30}
            },
            {
                'type': 'behavioral',
                'description': 'Writing style differs significantly from previous submissions',
                'severity': 'high',
                'confidence': 0.80,
                'data': {'style_similarity': 0.45, 'vocabulary_overlap': 0.38, 'sentence_structure_diff': 0.72}
            },
            {
                'type': 'pattern',
                'description': 'Unusual editing pattern: minimal corrections compared to student history',
                'severity': 'low',
                'confidence': 0.60,
                'data': {'correction_count': 3, 'student_avg': 45, 'percentile': 5}
            },
        ]
        
        for analysis in analyses:
            # Add 0-2 anomalies per submission
            num_anomalies = random.choices([0, 1, 2], weights=[0.5, 0.3, 0.2])[0]
            
            if analysis.anomalies_found and num_anomalies > 0:
                selected_anomalies = random.sample(anomaly_types_data, min(num_anomalies, len(anomaly_types_data)))
                
                for anomaly_data in selected_anomalies:
                    detection = AnomalyDetection.objects.create(
                        submission_analysis=analysis,
                        anomaly_type=anomaly_data['type'],
                        severity=anomaly_data['severity'],
                        description=anomaly_data['description'],
                        confidence_score=anomaly_data['confidence'],
                        anomaly_data=anomaly_data['data'],
                        acknowledged=(random.random() < 0.3),
                        false_positive=(random.random() < 0.1)
                    )
                    detections.append(detection)
        
        return detections

    def create_improvement_categories(self, tenants, users):
        """Create improvement categories"""
        categories = []
        
        category_templates = [
            {
                'name': 'Training Delivery',
                'type': 'training_assessment',
                'description': 'Improvements related to training delivery methods and effectiveness',
                'color': '#3B82F6',
                'standards': ['Standard 1.1', 'Standard 1.2', 'Standard 1.3']
            },
            {
                'name': 'Assessment Quality',
                'type': 'training_assessment',
                'description': 'Enhancements to assessment tools, validation, and moderation',
                'color': '#8B5CF6',
                'standards': ['Standard 1.8', 'Standard 1.9', 'Standard 1.10']
            },
            {
                'name': 'Trainer Professional Development',
                'type': 'trainer_qualifications',
                'description': 'Professional development and upskilling of training staff',
                'color': '#EC4899',
                'standards': ['Standard 1.13', 'Standard 1.14', 'Standard 1.15']
            },
            {
                'name': 'Student Support',
                'type': 'student_support',
                'description': 'Improvements to student services and support mechanisms',
                'color': '#10B981',
                'standards': ['Standard 1.6', 'Standard 1.7']
            },
            {
                'name': 'Compliance Documentation',
                'type': 'compliance_governance',
                'description': 'Enhancements to compliance processes and documentation',
                'color': '#F59E0B',
                'standards': ['Standard 2.1', 'Standard 2.2', 'Standard 2.3']
            },
            {
                'name': 'Quality Assurance Processes',
                'type': 'quality_assurance',
                'description': 'Improvements to internal quality assurance systems',
                'color': '#06B6D4',
                'standards': ['Standard 1.11', 'Standard 2.4']
            },
        ]
        
        for tenant in tenants:
            for template in category_templates:
                category = ImprovementCategory.objects.create(
                    tenant=tenant,
                    name=template['name'],
                    category_type=template['type'],
                    description=template['description'],
                    color_code=template['color'],
                    related_standards=template['standards'],
                    is_active=True,
                    created_by=users[0]
                )
                categories.append(category)
        
        return categories

    def create_improvement_actions(self, tenants, users, categories):
        """Create improvement actions"""
        actions = []
        
        action_templates = [
            {
                'title': 'Implement online assessment submission system',
                'description': 'Deploy digital assessment submission platform to improve efficiency and reduce paper-based processes. This will enable students to submit assessments online, provide automatic tracking, and streamline the marking workflow.',
                'category_type': 'training_assessment',
                'priority': 'high',
                'source': 'staff_suggestion',
                'root_cause': 'Current paper-based system is time-consuming and prone to loss',
                'proposed_solution': 'Implement Learning Management System with assessment submission module',
                'resources_required': 'LMS software license, staff training, technical support',
                'estimated_cost': 15000.00,
                'success_criteria': 'All assessments submitted digitally, 90% student satisfaction',
                'expected_impact': 'Reduce processing time by 50%, improve tracking accuracy',
                'ai_keywords': ['digital', 'assessment', 'efficiency', 'LMS', 'automation'],
                'ai_standards': ['Standard 1.8', 'Standard 1.9'],
                'status': 'in_progress',
                'days_offset_start': -30,
                'days_offset_due': 60,
            },
            {
                'title': 'Update trainer qualification records in VETtrak',
                'description': 'Comprehensive review and update of all trainer and assessor qualification records in VETtrak to ensure accuracy and compliance with ASQA requirements.',
                'category_type': 'trainer_qualifications',
                'priority': 'critical',
                'source': 'audit',
                'root_cause': 'Quarterly audit identified gaps in currency documentation',
                'proposed_solution': 'Conduct full audit of trainer files and update VETtrak records',
                'resources_required': 'Compliance manager time, trainer cooperation',
                'estimated_cost': 3000.00,
                'success_criteria': '100% trainer records current and compliant',
                'expected_impact': 'Full compliance with Standard 1.13-1.15',
                'ai_keywords': ['compliance', 'qualifications', 'VETtrak', 'audit', 'trainers'],
                'ai_standards': ['Standard 1.13', 'Standard 1.14', 'Standard 1.15'],
                'status': 'completed',
                'days_offset_start': -60,
                'days_offset_due': -10,
                'days_offset_completed': -5,
                'effectiveness': 5,
            },
            {
                'title': 'Establish student feedback collection process',
                'description': 'Create systematic approach to collecting, analyzing, and responding to student feedback across all courses. Implement quarterly feedback surveys and establish response protocols.',
                'category_type': 'student_support',
                'priority': 'high',
                'source': 'self_assessment',
                'root_cause': 'Inconsistent feedback collection limiting improvement insights',
                'proposed_solution': 'Deploy survey tool, create feedback analysis workflow',
                'resources_required': 'Survey platform subscription, staff training',
                'estimated_cost': 5000.00,
                'success_criteria': '80% response rate, documented action items from feedback',
                'expected_impact': 'Improved student satisfaction, data-driven improvements',
                'ai_keywords': ['feedback', 'student', 'survey', 'satisfaction', 'continuous improvement'],
                'ai_standards': ['Standard 1.6', 'Standard 2.4'],
                'status': 'planned',
                'days_offset_start': 14,
                'days_offset_due': 90,
            },
            {
                'title': 'Develop assessment validation schedule',
                'description': 'Create and implement a comprehensive assessment validation schedule to ensure all assessment tools are validated before use and revalidated regularly.',
                'category_type': 'training_assessment',
                'priority': 'high',
                'source': 'regulator_feedback',
                'root_cause': 'ASQA noted inconsistent validation practices during audit',
                'proposed_solution': 'Design validation schedule, assign validators, track completion',
                'resources_required': 'Validation templates, experienced validators',
                'estimated_cost': 8000.00,
                'success_criteria': 'All assessment tools validated, schedule maintained',
                'expected_impact': 'Full compliance with assessment validation requirements',
                'ai_keywords': ['validation', 'assessment', 'compliance', 'quality assurance'],
                'ai_standards': ['Standard 1.9', 'Standard 1.10', 'Standard 1.11'],
                'status': 'in_progress',
                'days_offset_start': -20,
                'days_offset_due': 45,
            },
            {
                'title': 'Enhance compliance documentation system',
                'description': 'Upgrade document management system to improve organization, accessibility, and version control of compliance documentation.',
                'category_type': 'compliance_governance',
                'priority': 'medium',
                'source': 'staff_suggestion',
                'root_cause': 'Difficulty locating current versions of policies and procedures',
                'proposed_solution': 'Implement SharePoint document management system',
                'resources_required': 'SharePoint license, migration support, training',
                'estimated_cost': 12000.00,
                'success_criteria': 'All documents centralized, version control active',
                'expected_impact': 'Improved compliance evidence accessibility',
                'ai_keywords': ['documentation', 'compliance', 'SharePoint', 'version control'],
                'ai_standards': ['Standard 2.1', 'Standard 2.2'],
                'status': 'identified',
                'days_offset_start': 30,
                'days_offset_due': 150,
            },
            {
                'title': 'Implement moderation process for certificate issuance',
                'description': 'Establish moderation process to verify assessment outcomes before certificate issuance, ensuring accuracy and compliance.',
                'category_type': 'training_assessment',
                'priority': 'critical',
                'source': 'audit',
                'root_cause': 'Audit identified certificates issued without proper verification',
                'proposed_solution': 'Create moderation checklist, assign moderators, track completion',
                'resources_required': 'Moderation templates, moderator training',
                'estimated_cost': 4000.00,
                'success_criteria': '100% certificates moderated before issuance',
                'expected_impact': 'Zero non-compliant certificate issuances',
                'ai_keywords': ['moderation', 'certificates', 'compliance', 'verification'],
                'ai_standards': ['Standard 1.10', 'Standard 3.1'],
                'status': 'in_progress',
                'days_offset_start': -15,
                'days_offset_due': 30,
            },
        ]
        
        action_counter = 1
        for i, tenant in enumerate(tenants):
            tenant_categories = [c for c in categories if c.tenant == tenant]
            
            for j, template in enumerate(action_templates):
                # Find matching category
                category = next(
                    (c for c in tenant_categories if c.category_type == template['category_type']),
                    None
                )
                
                action_number = f"CI-{timezone.now().year}-{action_counter:04d}"
                action_counter += 1
                
                action = ImprovementAction.objects.create(
                    tenant=tenant,
                    action_number=action_number,
                    title=template['title'],
                    description=template['description'],
                    category=category,
                    priority=template['priority'],
                    source=template['source'],
                    root_cause=template['root_cause'],
                    proposed_solution=template['proposed_solution'],
                    resources_required=template['resources_required'],
                    estimated_cost=template['estimated_cost'],
                    success_criteria=template['success_criteria'],
                    expected_impact=template['expected_impact'],
                    ai_keywords=template['ai_keywords'],
                    ai_related_standards=template['ai_standards'],
                    ai_classified_category=template['category_type'],
                    ai_classification_confidence=random.uniform(0.85, 0.95),
                    ai_summary=template['title'],
                    ai_processed_at=timezone.now() - timedelta(days=random.randint(1, 10)),
                    status=template['status'],
                    identified_date=timezone.now().date() + timedelta(days=template.get('days_offset_start', -30)),
                    planned_start_date=timezone.now().date() + timedelta(days=template.get('days_offset_start', -30)),
                    target_completion_date=timezone.now().date() + timedelta(days=template.get('days_offset_due', 60)),
                    actual_completion_date=timezone.now().date() + timedelta(days=template['days_offset_completed']) if template.get('days_offset_completed') else None,
                    responsible_person=users[random.randint(0, min(2, len(users)-1))],
                    effectiveness_rating=template.get('effectiveness'),
                    is_critical_compliance=template['priority'] in ['critical', 'high'],
                    created_by=users[0],
                    tags=['ai-classified', 'continuous-improvement']
                )
                
                # Add supporting staff
                if len(users) > 2:
                    action.supporting_staff.add(users[1], users[2])
                
                actions.append(action)
        
        return actions

    def create_action_tracking(self, actions, users):
        """Create action tracking updates"""
        tracking_updates = []
        
        for action in actions:
            # Create initial status update
            if action.status != 'identified':
                tracking = ActionTracking.objects.create(
                    improvement_action=action,
                    update_type='status_change',
                    update_text=f'Action moved from identified to {action.status}',
                    old_status='identified',
                    new_status=action.status,
                    progress_percentage=action.progress_percentage,
                    created_at=action.identified_date,
                    created_by=action.created_by
                )
                tracking_updates.append(tracking)
            
            # Add progress updates for in_progress actions
            if action.status == 'in_progress':
                progress_update = ActionTracking.objects.create(
                    improvement_action=action,
                    update_type='progress',
                    update_text=f'Good progress on {action.title}. Initial implementation phase complete. Working on staff training component.',
                    progress_percentage=random.randint(40, 70),
                    created_at=timezone.now() - timedelta(days=random.randint(5, 15)),
                    created_by=action.responsible_person or action.created_by
                )
                tracking_updates.append(progress_update)
                
                # Some actions have blockers
                if random.random() < 0.3:
                    blocker = ActionTracking.objects.create(
                        improvement_action=action,
                        update_type='issue',
                        update_text='Waiting on vendor quote for required software. Expected by end of week.',
                        is_blocker=True,
                        blocker_resolved=random.choice([True, False]),
                        blocker_resolution='Quote received and approved' if random.choice([True, False]) else '',
                        created_at=timezone.now() - timedelta(days=random.randint(3, 10)),
                        created_by=action.responsible_person or action.created_by
                    )
                    tracking_updates.append(blocker)
            
            # Add milestone updates for completed actions
            if action.status == 'completed':
                milestone = ActionTracking.objects.create(
                    improvement_action=action,
                    update_type='milestone',
                    update_text='All objectives achieved. Solution implemented and tested successfully.',
                    progress_percentage=100,
                    created_at=action.actual_completion_date or timezone.now().date(),
                    created_by=action.responsible_person or action.created_by,
                    evidence_provided=[
                        {'type': 'document', 'name': 'Implementation Report.pdf'},
                        {'type': 'checklist', 'name': 'Completion Checklist.xlsx'}
                    ]
                )
                tracking_updates.append(milestone)
                
                completion = ActionTracking.objects.create(
                    improvement_action=action,
                    update_type='completion',
                    update_text=f'Action completed successfully. Effectiveness rating: {action.effectiveness_rating}/5',
                    old_status='in_progress',
                    new_status='completed',
                    progress_percentage=100,
                    created_at=action.actual_completion_date or timezone.now().date(),
                    created_by=action.created_by,
                    evidence_provided=[
                        {'type': 'report', 'name': 'Final Report.pdf'}
                    ]
                )
                tracking_updates.append(completion)
        
        return tracking_updates

    def create_improvement_reviews(self, tenants, users, actions):
        """Create improvement reviews"""
        reviews = []
        
        for i, tenant in enumerate(tenants):
            tenant_actions = [a for a in actions if a.tenant == tenant]
            
            # Create quarterly review
            review = ImprovementReview.objects.create(
                tenant=tenant,
                review_number=f"REV-Q{random.randint(1,4)}-{timezone.now().year}",
                title=f"Q{random.randint(1,4)} {timezone.now().year} Continuous Improvement Review",
                review_type='quarterly',
                review_date=timezone.now().date() - timedelta(days=random.randint(5, 30)),
                review_period_start=timezone.now().date() - timedelta(days=90),
                review_period_end=timezone.now().date(),
                key_findings='Overall positive progress on improvement initiatives. Strong engagement from staff. Some delays due to resource constraints.',
                areas_of_concern='Three actions are overdue and require immediate attention. Budget constraints affecting implementation timelines.',
                recommendations='Recommend prioritizing critical compliance actions. Consider additional resources for high-priority items.',
                action_items=[
                    {'action': 'Escalate overdue actions to management', 'owner': 'Compliance Manager'},
                    {'action': 'Review budget allocation for CI initiatives', 'owner': 'Finance Manager'},
                    {'action': 'Schedule follow-up review in 30 days', 'owner': 'Quality Manager'}
                ],
                ai_summary='The quarterly review shows strong progress with 2 actions completed and 4 in progress. Key challenges include resource availability and budget constraints. Recommendation to prioritize critical compliance items.',
                ai_trends=[
                    {'trend': 'Increasing staff engagement in CI process', 'impact': 'positive'},
                    {'trend': 'Budget constraints affecting timelines', 'impact': 'negative'},
                    {'trend': 'Strong focus on compliance-related actions', 'impact': 'positive'}
                ],
                ai_recommendations=[
                    'Allocate additional budget to critical compliance actions',
                    'Implement project management tools for better tracking',
                    'Increase frequency of progress reviews for at-risk actions'
                ],
                reviewed_by=users[0],
                notes='Attended by all key stakeholders. General agreement on priorities and recommendations.'
            )
            
            # Add actions to review
            review.actions_reviewed.set(tenant_actions[:4])
            review.attendees.set(users[:3])
            
            # Calculate statistics
            review.calculate_statistics()
            
            reviews.append(review)
        
        return reviews

    def create_message_templates(self, tenants, users):
        """Create message templates"""
        templates = []
        
        template_data = [
            {
                'name': 'Assessment Extension Request',
                'type': 'extension',
                'description': 'Response to student requesting assessment deadline extension',
                'body': '''Hi {student_name},

Thank you for reaching out regarding your assessment extension request for {unit_code}.

I've reviewed your circumstances and I'm pleased to confirm that we can grant an extension until {new_due_date}. This should give you adequate time to complete the assessment to the required standard.

Please ensure you submit your assessment by the new deadline. If you have any questions or need further support, please don't hesitate to contact us.

Best regards,''',
                'placeholders': ['{student_name}', '{unit_code}', '{new_due_date}'],
                'tone': 'professional',
                'formality': 4,
            },
            {
                'name': 'Assessment Submission Confirmation',
                'type': 'assessment',
                'description': 'Confirmation that student assessment was received',
                'body': '''Hi {student_name},

This is to confirm that we have received your assessment submission for {unit_code} - {unit_title}.

Your submission will be marked within {marking_timeframe} business days. You will be notified via email when your results are available in the LMS.

If you have any questions about your submission, please feel free to contact us.

Best regards,''',
                'placeholders': ['{student_name}', '{unit_code}', '{unit_title}', '{marking_timeframe}'],
                'tone': 'friendly',
                'formality': 3,
            },
            {
                'name': 'Technical Support Response',
                'type': 'technical',
                'description': 'Response to technical issues accessing LMS or materials',
                'body': '''Hi {student_name},

Thank you for contacting us about the technical issue you're experiencing with {system_name}.

I've checked your account and {resolution_action}. You should now be able to access the system without issues.

If you continue to experience problems, please try clearing your browser cache and cookies, or try accessing the system from a different browser. If the issue persists, please let me know and I'll escalate this to our IT support team.

Best regards,''',
                'placeholders': ['{student_name}', '{system_name}', '{resolution_action}'],
                'tone': 'empathetic',
                'formality': 3,
            },
            {
                'name': 'General Enrollment Query',
                'type': 'enrollment',
                'description': 'Response to general enrollment questions',
                'body': '''Hi {student_name},

Thank you for your interest in {course_name}.

The next intake for this course begins on {start_date}. The course duration is {duration} and includes {unit_count} units of competency.

To enroll, please complete the online enrollment form at {enrollment_link}. If you have any questions about the enrollment process, course content, or payment options, please don't hesitate to ask.

I'm here to help!

Best regards,''',
                'placeholders': ['{student_name}', '{course_name}', '{start_date}', '{duration}', '{unit_count}', '{enrollment_link}'],
                'tone': 'friendly',
                'formality': 2,
            },
            {
                'name': 'Assessment Results Available',
                'type': 'assessment',
                'description': 'Notification that assessment results are ready',
                'body': '''Hi {student_name},

Your assessment results for {unit_code} - {unit_title} are now available in the LMS.

Result: {result_status}

{additional_feedback}

If you would like to discuss your results or receive additional feedback, please don't hesitate to schedule a call with your trainer.

Best regards,''',
                'placeholders': ['{student_name}', '{unit_code}', '{unit_title}', '{result_status}', '{additional_feedback}'],
                'tone': 'professional',
                'formality': 3,
            },
        ]
        
        for tenant in tenants:
            for template_info in template_data:
                template = MessageTemplate.objects.create(
                    tenant=tenant.slug,
                    name=template_info['name'],
                    description=template_info['description'],
                    template_type=template_info['type'],
                    template_body=template_info['body'],
                    placeholders=template_info['placeholders'],
                    default_tone=template_info['tone'],
                    formality_level=template_info['formality'],
                    usage_count=random.randint(5, 50),
                    success_rate=random.uniform(0.75, 0.95),
                    last_used_at=timezone.now() - timedelta(days=random.randint(1, 30)),
                    is_active=True,
                    is_system_template=True,
                    created_by=users[0].get_full_name()
                )
                templates.append(template)
        
        return templates

    def create_tone_profiles(self, tenants, users):
        """Create tone profiles"""
        profiles = []
        
        profile_data = [
            {
                'name': 'Professional Standard',
                'description': 'Default professional tone for most communications',
                'tone': 'professional',
                'formality': 4,
                'empathy': 3,
                'brevity': 3,
                'contractions': False,
                'emojis': False,
                'greeting': 'Dear {name},',
                'closing': 'Kind regards,',
                'recommended': ['general', 'enrollment', 'assessment'],
                'is_default': True,
            },
            {
                'name': 'Friendly & Approachable',
                'description': 'Warm, friendly tone for student engagement',
                'tone': 'friendly',
                'formality': 2,
                'empathy': 4,
                'brevity': 3,
                'contractions': True,
                'emojis': False,
                'greeting': 'Hi {name},',
                'closing': 'Best regards,',
                'recommended': ['general', 'feedback'],
                'is_default': False,
            },
            {
                'name': 'Empathetic Support',
                'description': 'Highly empathetic tone for complaints and concerns',
                'tone': 'empathetic',
                'formality': 3,
                'empathy': 5,
                'brevity': 4,
                'contractions': True,
                'emojis': False,
                'greeting': 'Hi {name},',
                'closing': 'I\'m here to help,',
                'recommended': ['complaint', 'technical', 'extension'],
                'is_default': False,
            },
            {
                'name': 'Brief & Direct',
                'description': 'Concise responses for simple queries',
                'tone': 'professional',
                'formality': 3,
                'empathy': 2,
                'brevity': 1,
                'contractions': True,
                'emojis': False,
                'greeting': 'Hi {name},',
                'closing': 'Thanks,',
                'recommended': ['technical', 'general'],
                'is_default': False,
            },
        ]
        
        for tenant in tenants:
            for profile_info in profile_data:
                profile = ToneProfile.objects.create(
                    tenant=tenant.slug,
                    name=profile_info['name'],
                    description=profile_info['description'],
                    tone_descriptor=profile_info['tone'],
                    formality_level=profile_info['formality'],
                    empathy_level=profile_info['empathy'],
                    brevity_level=profile_info['brevity'],
                    use_contractions=profile_info['contractions'],
                    use_emojis=profile_info['emojis'],
                    greeting_style=profile_info['greeting'],
                    closing_style=profile_info['closing'],
                    recommended_for=profile_info['recommended'],
                    is_default=profile_info['is_default'],
                    usage_count=random.randint(10, 100) if profile_info['is_default'] else random.randint(0, 30),
                    is_active=True
                )
                profiles.append(profile)
        
        return profiles

    def create_conversation_threads(self, tenants):
        """Create conversation threads"""
        threads = []
        
        student_data = [
            {'name': 'Emma Wilson', 'email': 'emma.wilson@example.com', 'subject': 'Assessment Extension Request'},
            {'name': 'James Chen', 'email': 'james.chen@example.com', 'subject': 'Technical Issue with LMS Access'},
            {'name': 'Sarah Johnson', 'email': 'sarah.johnson@example.com', 'subject': 'Course Enrollment Question'},
            {'name': 'Michael Brown', 'email': 'michael.brown@example.com', 'subject': 'Assessment Feedback Query'},
            {'name': 'Jessica Lee', 'email': 'jessica.lee@example.com', 'subject': 'Unit Materials Not Available'},
        ]
        
        for i, tenant in enumerate(tenants):
            for j, student in enumerate(student_data[:3]):  # 3 threads per tenant
                thread = ConversationThread.objects.create(
                    tenant=tenant.slug,
                    student_email=student['email'],
                    student_name=student['name'],
                    subject=student['subject'],
                    message_count=random.randint(1, 4),
                    first_message_date=timezone.now() - timedelta(days=random.randint(5, 30)),
                    last_message_date=timezone.now() - timedelta(days=random.randint(0, 5)),
                    is_active=random.choice([True, False]),
                    is_resolved=random.choice([True, False]),
                    resolved_at=timezone.now() - timedelta(days=random.randint(1, 3)) if random.choice([True, False]) else None,
                    primary_category=random.choice(['assessment', 'technical', 'enrollment', 'general']),
                    tags=['student-query', 'email']
                )
                threads.append(thread)
        
        return threads

    def create_student_messages(self, tenants, threads, users):
        """Create student messages"""
        messages = []
        
        message_samples = [
            {
                'subject': 'Request for Assessment Extension - BSBWHS521',
                'body': 'Hi, I am writing to request an extension for my BSBWHS521 assessment. I have been dealing with a family emergency and need an additional two weeks to complete the work to a high standard. I have completed about 70% of the assessment and just need more time to finish properly. Is this possible? Thank you.',
                'type': 'email',
                'priority': 'high',
                'category': 'Extension Request',
                'sentiment': 'neutral',
                'topics': ['assessment', 'extension', 'deadline'],
            },
            {
                'subject': 'Cannot Access LMS - Urgent',
                'body': 'Hello, I\'m having trouble logging into the LMS. It keeps saying "invalid credentials" even though I\'m sure my password is correct. I need to access my unit materials for tomorrow\'s class. Can someone help me urgently please?',
                'type': 'email',
                'priority': 'urgent',
                'category': 'Technical Support',
                'sentiment': 'frustrated',
                'topics': ['technical', 'login', 'access', 'urgent'],
            },
            {
                'subject': 'Enrollment for Certificate III in Hospitality',
                'body': 'Hi there, I\'m interested in enrolling in the Certificate III in Hospitality course. Could you please let me know when the next intake is and what the fees are? Also, do you offer payment plans? Thanks!',
                'type': 'email',
                'priority': 'medium',
                'category': 'Enrollment',
                'sentiment': 'positive',
                'topics': ['enrollment', 'hospitality', 'fees', 'payment'],
            },
            {
                'subject': 'Question about Assessment Results',
                'body': 'Hello, I received my results for SITHCCC023 and I\'m marked as "Not Yet Competent". I\'m a bit confused about what I need to improve. Could I please get more detailed feedback or arrange a time to discuss this with my trainer?',
                'type': 'email',
                'priority': 'high',
                'category': 'Assessment Query',
                'sentiment': 'concerned',
                'topics': ['assessment', 'results', 'feedback', 'NYC'],
            },
            {
                'subject': 'Missing Unit Materials',
                'body': 'Hi, I noticed that the learning materials for Unit 5 are not showing up in my LMS dashboard. Other students in my class have access but I don\'t. Can you please check what\'s wrong? The unit starts next week.',
                'type': 'email',
                'priority': 'high',
                'category': 'Technical Support',
                'sentiment': 'neutral',
                'topics': ['materials', 'access', 'LMS', 'unit'],
            },
            {
                'subject': 'Thank you for the support',
                'body': 'Just wanted to say thank you for extending my assessment deadline. I really appreciate the understanding and support. I\'m confident I can now submit quality work. Thanks again!',
                'type': 'email',
                'priority': 'low',
                'category': 'General Query',
                'sentiment': 'positive',
                'topics': ['feedback', 'thanks', 'extension'],
            },
        ]
        
        for tenant in tenants:
            tenant_threads = [t for t in threads if t.tenant == tenant.slug]
            
            for i, sample in enumerate(message_samples):
                # Some messages belong to threads, some are standalone
                thread = tenant_threads[i % len(tenant_threads)] if i < len(tenant_threads) else None
                
                message = StudentMessage.objects.create(
                    tenant=tenant.slug,
                    student_name=thread.student_name if thread else f"Student {i+1}",
                    student_email=thread.student_email if thread else f"student{i+1}@example.com",
                    student_id=f"STU{random.randint(1000, 9999)}",
                    message_type=sample['type'],
                    subject=sample['subject'],
                    message_body=sample['body'],
                    received_date=timezone.now() - timedelta(hours=random.randint(1, 72)),
                    priority=sample['priority'],
                    category=sample['category'],
                    detected_sentiment=sample['sentiment'],
                    detected_topics=sample['topics'],
                    status=random.choice(['new', 'draft_generated', 'replied']),
                    requires_human_review=(sample['priority'] in ['urgent', 'high'] and random.random() < 0.3),
                    conversation_thread=thread,
                    previous_message_count=random.randint(0, 3) if thread else 0
                )
                messages.append(message)
        
        return messages

    def create_draft_replies(self, messages, templates, users):
        """Create draft replies"""
        drafts = []
        
        for message in messages:
            # Only create drafts for messages that have draft_generated or replied status
            if message.status in ['draft_generated', 'replied']:
                # Find matching template
                template = None
                for t in templates:
                    if t.tenant == message.tenant and t.template_type.lower() in message.category.lower():
                        template = t
                        break
                
                # Generate draft reply based on message type
                if 'extension' in message.category.lower():
                    reply_body = f'''Hi {message.student_name},

Thank you for reaching out regarding your assessment extension request for BSBWHS521.

I understand you're dealing with a family emergency, and I appreciate you letting us know. Given your circumstances and the fact that you've already completed 70% of the assessment, I'm pleased to confirm that we can grant an extension of two weeks.

Your new due date is {(timezone.now() + timedelta(days=14)).strftime("%B %d, %Y")}. This should give you adequate time to complete the assessment to the required standard.

Please ensure you submit your assessment by the new deadline. If you have any questions or need further support, please don't hesitate to contact us.

Best regards,
Training Support Team'''
                elif 'technical' in message.category.lower():
                    reply_body = f'''Hi {message.student_name},

Thank you for contacting us about the login issue you're experiencing with the LMS.

I've checked your account and reset your password. You should receive a password reset email within the next few minutes. Please use the link in that email to set a new password.

Once you've reset your password, you should be able to access the system without issues. If you continue to experience problems, please try clearing your browser cache and cookies, or try accessing the system from a different browser.

If the issue persists after trying these steps, please let me know and I'll escalate this to our IT support team immediately.

Best regards,
Technical Support Team'''
                elif 'enrollment' in message.category.lower():
                    reply_body = f'''Hi {message.student_name},

Thank you for your interest in the Certificate III in Hospitality!

The next intake for this course begins on {(timezone.now() + timedelta(days=30)).strftime("%B %d, %Y")}. The course duration is 12 months and includes 33 units of competency.

Course fees are $4,500, and yes, we do offer flexible payment plans! You can choose from:
- Upfront payment with 10% discount ($4,050)
- Monthly installments over 12 months ($395/month)
- Split payment (50% upfront, 50% at 6 months)

To enroll, please complete the online enrollment form at our website. If you have any questions about the enrollment process, course content, or payment options, please don't hesitate to ask.

I'm here to help!

Best regards,
Enrollment Team'''
                else:
                    reply_body = f'''Hi {message.student_name},

Thank you for your message regarding {message.subject}.

{message.message_body[:100]}... 

I've reviewed your query and I'm happy to help. Let me provide you with some information to assist you.

If you have any further questions, please feel free to reach out.

Best regards,
Student Support Team'''
                
                draft = DraftReply.objects.create(
                    student_message=message,
                    reply_body=reply_body,
                    reply_subject=f"Re: {message.subject}",
                    tone_used=random.choice(['professional', 'friendly', 'empathetic']),
                    formality_level=random.randint(2, 4),
                    include_greeting=True,
                    include_signature=True,
                    template_used=template,
                    confidence_score=random.uniform(0.75, 0.95),
                    readability_score=random.uniform(60, 80),
                    was_edited=random.choice([True, False]),
                    was_sent=(message.status == 'replied'),
                    was_rejected=False,
                    generation_status='completed',
                    generation_time_ms=random.randint(800, 2500),
                    llm_model_used=random.choice(['gpt-4', 'gpt-4-turbo', 'claude-3-sonnet']),
                    sent_at=timezone.now() - timedelta(hours=random.randint(1, 48)) if message.status == 'replied' else None
                )
                drafts.append(draft)
        
        return drafts

    def create_reply_history(self, messages, drafts, users):
        """Create reply history records"""
        history = []
        
        # Only create history for replied messages
        replied_messages = [m for m in messages if m.status == 'replied']
        
        for message in replied_messages:
            # Find the draft for this message
            draft = next((d for d in drafts if d.student_message == message and d.was_sent), None)
            
            if draft:
                time_to_first_draft = random.randint(60, 300)  # 1-5 minutes
                time_to_send = random.randint(300, 1800)  # 5-30 minutes
                
                history_record = ReplyHistory.objects.create(
                    student_message=message,
                    draft_reply=draft,
                    final_reply_body=draft.reply_body,
                    final_subject=draft.reply_subject,
                    time_to_first_draft_seconds=time_to_first_draft,
                    time_to_send_seconds=time_to_send,
                    edit_count=random.randint(0, 3) if draft.was_edited else 0,
                    estimated_manual_time_seconds=random.randint(300, 600),  # 5-10 minutes
                    sent_by=users[random.randint(0, min(2, len(users)-1))].get_full_name(),
                    sent_at=draft.sent_at or timezone.now(),
                    student_responded=random.choice([True, False]),
                    student_satisfied=random.choice([True, True, None]),  # Mostly satisfied
                    follow_up_required=random.choice([True, False])
                )
                history.append(history_record)
        
        return history

    def create_engagement_heatmaps(self, tenants, users):
        """Create engagement heatmaps"""
        heatmaps = []
        
        # Create heatmaps for 5 students per tenant over last 4 weeks
        for tenant in tenants:
            for student_idx in range(5):
                student_id = f"STU{random.randint(1000, 9999)}"
                student_name = random.choice([
                    'Emma Wilson', 'James Chen', 'Sarah Johnson', 
                    'Michael Brown', 'Jessica Lee', 'Daniel Kim',
                    'Olivia Martinez', 'Ryan Taylor', 'Sophia Anderson'
                ])
                
                # Create weekly heatmaps for last 4 weeks
                for week in range(4):
                    start_date = timezone.now().date() - timedelta(days=(week+1)*7)
                    end_date = start_date + timedelta(days=6)
                    
                    # Generate realistic scores (some students struggle more)
                    if student_idx in [0, 1]:  # Engaged students
                        attendance_score = random.uniform(85, 100)
                        lms_score = random.uniform(80, 95)
                        sentiment_score = random.uniform(70, 90)
                    elif student_idx in [2, 3]:  # Medium engagement
                        attendance_score = random.uniform(60, 80)
                        lms_score = random.uniform(55, 75)
                        sentiment_score = random.uniform(50, 70)
                    else:  # At-risk student
                        attendance_score = random.uniform(30, 60)
                        lms_score = random.uniform(25, 55)
                        sentiment_score = random.uniform(30, 60)
                    
                    # Generate daily heatmap data
                    heatmap_data = {}
                    for day in range(7):
                        date = start_date + timedelta(days=day)
                        heatmap_data[str(date)] = {
                            'attendance': random.random() < (attendance_score / 100),
                            'lms_minutes': random.randint(0, 180) if random.random() < (lms_score / 100) else 0,
                            'sentiment': (sentiment_score / 100) * 2 - 1,  # Convert to -1 to 1
                        }
                    
                    # Determine risk flags
                    risk_flags = []
                    if attendance_score < 70:
                        risk_flags.append('low_attendance')
                    if lms_score < 60:
                        risk_flags.append('inactive_lms')
                    if sentiment_score < 50:
                        risk_flags.append('negative_sentiment')
                    if attendance_score < 50 and lms_score < 50:
                        risk_flags.append('disengaged')
                    
                    # Determine trend
                    if week == 0:  # Most recent week
                        if student_idx == 4:  # At-risk student
                            trend = random.choice(['declining', 'critical_decline'])
                            change_pct = random.uniform(-25, -10)
                        elif student_idx in [2, 3]:
                            trend = random.choice(['stable', 'declining'])
                            change_pct = random.uniform(-10, 5)
                        else:
                            trend = random.choice(['stable', 'improving'])
                            change_pct = random.uniform(-5, 15)
                    else:
                        trend = 'stable'
                        change_pct = random.uniform(-5, 5)
                    
                    heatmap = EngagementHeatmap.objects.create(
                        tenant=tenant.slug,
                        student_id=student_id,
                        student_name=student_name,
                        time_period='weekly',
                        start_date=start_date,
                        end_date=end_date,
                        attendance_score=attendance_score,
                        lms_activity_score=lms_score,
                        sentiment_score=sentiment_score,
                        risk_flags=risk_flags,
                        heatmap_data=heatmap_data,
                        engagement_trend=trend,
                        change_percentage=change_pct,
                        alerts_triggered=len(risk_flags),
                        interventions_applied=random.randint(0, len(risk_flags))
                    )
                    heatmaps.append(heatmap)
        
        return heatmaps

    def create_attendance_records(self, heatmaps):
        """Create attendance records"""
        records = []
        
        for heatmap in heatmaps:
            # Create 5 attendance records per week (Mon-Fri)
            for day in range(5):
                date = heatmap.start_date + timedelta(days=day)
                
                # Determine status based on attendance score
                if heatmap.attendance_score >= 80:
                    status = random.choices(
                        ['present', 'late', 'absent'],
                        weights=[0.85, 0.10, 0.05]
                    )[0]
                elif heatmap.attendance_score >= 60:
                    status = random.choices(
                        ['present', 'late', 'absent', 'excused'],
                        weights=[0.65, 0.15, 0.15, 0.05]
                    )[0]
                else:
                    status = random.choices(
                        ['present', 'late', 'absent', 'excused'],
                        weights=[0.40, 0.10, 0.40, 0.10]
                    )[0]
                
                session_start = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0).time()
                session_end = timezone.now().replace(hour=17, minute=0, second=0, microsecond=0).time()
                
                # Calculate arrival and minutes
                if status == 'present':
                    actual_arrival = timezone.now().replace(
                        hour=random.randint(8, 9),
                        minute=random.randint(0, 59),
                        second=0,
                        microsecond=0
                    ).time()
                    minutes_late = 0
                    minutes_attended = random.randint(420, 480)  # 7-8 hours
                    participation = random.choice(['high', 'medium'])
                elif status == 'late':
                    actual_arrival = timezone.now().replace(
                        hour=random.randint(9, 10),
                        minute=random.randint(0, 59),
                        second=0,
                        microsecond=0
                    ).time()
                    minutes_late = random.randint(15, 90)
                    minutes_attended = random.randint(360, 450)
                    participation = random.choice(['medium', 'low'])
                elif status == 'excused':
                    actual_arrival = None
                    minutes_late = 0
                    minutes_attended = 0
                    participation = 'none'
                else:  # absent
                    actual_arrival = None
                    minutes_late = 0
                    minutes_attended = 0
                    participation = 'none'
                
                record = AttendanceRecord.objects.create(
                    heatmap=heatmap,
                    tenant=heatmap.tenant,
                    student_id=heatmap.student_id,
                    date=date,
                    status=status,
                    session_name=f"Training Session - {date.strftime('%A')}",
                    scheduled_start=session_start,
                    scheduled_end=session_end,
                    actual_arrival=actual_arrival,
                    minutes_late=minutes_late,
                    minutes_attended=minutes_attended,
                    participation_level=participation
                )
                records.append(record)
        
        return records

    def create_lms_activities(self, heatmaps):
        """Create LMS activity records"""
        activities = []
        
        activity_templates = [
            {'type': 'login', 'name': 'LMS Login', 'duration': 0, 'course': '', 'module': ''},
            {'type': 'content_view', 'name': 'Week {week} Learning Materials', 'duration': 15, 'course': 'Certificate III', 'module': 'Module {mod}'},
            {'type': 'video_watch', 'name': 'Introduction to {topic}', 'duration': 25, 'course': 'Certificate III', 'module': 'Module {mod}'},
            {'type': 'assignment_submit', 'name': 'Assessment Task {task}', 'duration': 120, 'course': 'Certificate III', 'module': 'Module {mod}'},
            {'type': 'quiz_attempt', 'name': 'Knowledge Check {num}', 'duration': 30, 'course': 'Certificate III', 'module': 'Module {mod}'},
            {'type': 'forum_post', 'name': 'Discussion Forum', 'duration': 10, 'course': 'Certificate III', 'module': 'Module {mod}'},
            {'type': 'resource_download', 'name': 'Unit Materials', 'duration': 2, 'course': 'Certificate III', 'module': 'Module {mod}'},
        ]
        
        topics = ['WHS', 'Customer Service', 'Communication', 'Food Safety', 'Industry Standards']
        
        for heatmap in heatmaps[:20]:  # Create activities for first 20 heatmaps only
            # Number of activities based on LMS score
            if heatmap.lms_activity_score >= 80:
                num_activities = random.randint(15, 25)
            elif heatmap.lms_activity_score >= 60:
                num_activities = random.randint(8, 15)
            else:
                num_activities = random.randint(2, 8)
            
            for i in range(num_activities):
                template = random.choice(activity_templates)
                date = heatmap.start_date + timedelta(days=random.randint(0, 6))
                
                activity_name = template['name'].format(
                    week=random.randint(1, 12),
                    mod=random.randint(1, 6),
                    task=random.randint(1, 10),
                    num=random.randint(1, 5),
                    topic=random.choice(topics)
                )
                
                # Determine completion status
                if template['type'] in ['login', 'content_view', 'video_watch', 'resource_download']:
                    completion = random.choices(
                        ['completed', 'in_progress', 'started'],
                        weights=[0.80, 0.15, 0.05]
                    )[0]
                else:
                    completion = random.choices(
                        ['completed', 'in_progress', 'started', 'abandoned'],
                        weights=[0.70, 0.15, 0.10, 0.05]
                    )[0]
                
                # Quality score for assignments and quizzes
                quality = None
                if template['type'] in ['assignment_submit', 'quiz_attempt']:
                    if completion == 'completed':
                        quality = random.uniform(60, 95) if heatmap.lms_activity_score >= 70 else random.uniform(40, 75)
                
                # Ensure duration is never negative
                duration = max(0, template['duration'] + random.randint(-5, 10))
                
                activity = LMSActivity.objects.create(
                    heatmap=heatmap,
                    tenant=heatmap.tenant,
                    student_id=heatmap.student_id,
                    date=date,
                    activity_type=template['type'],
                    activity_name=activity_name,
                    timestamp=timezone.make_aware(
                        timezone.datetime.combine(date, timezone.now().time())
                    ),
                    duration_minutes=duration,
                    completion_status=completion,
                    interaction_count=random.randint(1, 20),
                    course_name=template['course'] if template['course'] else '',
                    module_name=template['module'].format(mod=random.randint(1, 6)) if template['module'] else '',
                    quality_score=quality
                )
                activities.append(activity)
        
        return activities

    def create_discussion_sentiments(self, heatmaps):
        """Create discussion sentiment records"""
        sentiments = []
        
        message_templates = {
            'very_positive': [
                "I really enjoyed today's lesson! The practical examples helped me understand the concepts much better.",
                "Thank you for the detailed feedback on my assessment. It's really helpful!",
                "Great discussion everyone! I learned so much from your different perspectives."
            ],
            'positive': [
                "The video tutorial was helpful. I understand the process now.",
                "Thanks for clarifying that point. Makes sense now.",
                "Good session today, covered a lot of useful material."
            ],
            'neutral': [
                "I've submitted my assessment task 2.",
                "Can someone share the link to the reading materials?",
                "What time is the session tomorrow?"
            ],
            'negative': [
                "I'm finding this topic really difficult to understand.",
                "I'm not sure I follow the instructions for the assessment.",
                "Having some technical issues accessing the materials."
            ],
            'very_negative': [
                "I'm really struggling with this unit and feel quite overwhelmed.",
                "Very frustrated - can't access the LMS again and deadline is approaching.",
                "I don't think I can complete this on time. Too much is happening."
            ]
        }
        
        for heatmap in heatmaps[:15]:  # Create sentiments for first 15 heatmaps only
            # Number of messages based on sentiment score
            if heatmap.sentiment_score >= 70:
                num_messages = random.randint(5, 10)
                sentiment_distribution = {'very_positive': 0.4, 'positive': 0.4, 'neutral': 0.2}
            elif heatmap.sentiment_score >= 50:
                num_messages = random.randint(3, 7)
                sentiment_distribution = {'positive': 0.3, 'neutral': 0.5, 'negative': 0.2}
            else:
                num_messages = random.randint(2, 5)
                sentiment_distribution = {'neutral': 0.3, 'negative': 0.4, 'very_negative': 0.3}
            
            for i in range(num_messages):
                date = heatmap.start_date + timedelta(days=random.randint(0, 6))
                
                # Select sentiment label based on distribution
                sentiment_label = random.choices(
                    list(sentiment_distribution.keys()),
                    weights=list(sentiment_distribution.values())
                )[0]
                
                message_content = random.choice(message_templates.get(sentiment_label, message_templates['neutral']))
                
                # Convert sentiment label to score
                sentiment_score_map = {
                    'very_positive': random.uniform(0.6, 0.9),
                    'positive': random.uniform(0.2, 0.5),
                    'neutral': random.uniform(-0.1, 0.1),
                    'negative': random.uniform(-0.5, -0.2),
                    'very_negative': random.uniform(-0.9, -0.6)
                }
                sentiment_score = sentiment_score_map[sentiment_label]
                
                # Determine emotion
                emotion_map = {
                    'very_positive': 'joy',
                    'positive': 'interest',
                    'neutral': 'interest',
                    'negative': 'confusion',
                    'very_negative': random.choice(['frustration', 'anxiety', 'sadness'])
                }
                primary_emotion = emotion_map[sentiment_label]
                
                # Emotion scores
                emotion_scores = {
                    'joy': 0.1, 'interest': 0.2, 'confusion': 0.1,
                    'frustration': 0.1, 'anxiety': 0.1, 'sadness': 0.05
                }
                emotion_scores[primary_emotion] = random.uniform(0.6, 0.9)
                
                # Detect negative keywords
                negative_keywords = []
                help_keywords = []
                if sentiment_label in ['negative', 'very_negative']:
                    negative_keywords = random.sample(
                        ['difficult', 'struggling', 'confused', 'frustrated', 'overwhelmed', 'stuck'],
                        k=random.randint(1, 2)
                    )
                    help_keywords = random.sample(
                        ['help', 'clarify', 'explain', 'support', 'assistance'],
                        k=random.randint(0, 2)
                    )
                
                sentiment = DiscussionSentiment.objects.create(
                    heatmap=heatmap,
                    tenant=heatmap.tenant,
                    student_id=heatmap.student_id,
                    date=date,
                    timestamp=timezone.make_aware(
                        timezone.datetime.combine(date, timezone.now().time())
                    ),
                    message_type=random.choice(['forum_post', 'forum_reply', 'chat_message']),
                    message_content=message_content,
                    sentiment_score=sentiment_score,
                    confidence=random.uniform(0.75, 0.95),
                    primary_emotion=primary_emotion,
                    emotion_scores=emotion_scores,
                    word_count=len(message_content.split()),
                    question_count=message_content.count('?'),
                    exclamation_count=message_content.count('!'),
                    negative_keywords=negative_keywords,
                    help_seeking_keywords=help_keywords,
                    discussion_topic=random.choice(['Unit Discussion', 'Assessment Help', 'General Questions', 'Technical Support']),
                    reply_count=random.randint(0, 5)
                )
                sentiments.append(sentiment)
        
        return sentiments

    def create_engagement_alerts(self, heatmaps):
        """Create engagement alerts"""
        alerts = []
        
        alert_templates = {
            'attendance': {
                'title': 'Low Attendance Warning',
                'description': 'Student has missed {days} days in the last week. Attendance score: {score}%',
                'recommended_actions': [
                    'Contact student to discuss attendance concerns',
                    'Review any documented reasons for absence',
                    'Offer catch-up session or additional support',
                    'Document communication and follow-up plan'
                ]
            },
            'lms_inactivity': {
                'title': 'LMS Inactivity Detected',
                'description': 'Student has not logged into LMS for {days} days. Last activity: {last_activity}',
                'recommended_actions': [
                    'Send email reminder about upcoming deadlines',
                    'Check if student is experiencing technical issues',
                    'Offer one-on-one support session',
                    'Review course engagement strategies'
                ]
            },
            'negative_sentiment': {
                'title': 'Negative Sentiment Detected',
                'description': 'Recent forum posts show concerning sentiment. Keywords detected: {keywords}',
                'recommended_actions': [
                    'Reach out to student for welfare check',
                    'Offer additional learning support',
                    'Connect with student support services',
                    'Review workload and deadline flexibility'
                ]
            },
            'overall_engagement': {
                'title': 'Overall Engagement Risk',
                'description': 'Multiple engagement metrics below threshold. Overall score: {score}%',
                'recommended_actions': [
                    'Schedule intervention meeting with student',
                    'Develop personalized support plan',
                    'Consider adjustment to learning pathway',
                    'Escalate to course coordinator if needed'
                ]
            }
        }
        
        for heatmap in heatmaps:
            # Only create alerts for at-risk students (medium, high, critical)
            if heatmap.risk_level not in ['medium', 'high', 'critical']:
                continue
            
            # Create 1-3 alerts based on risk flags
            num_alerts = min(len(heatmap.risk_flags), 3) if heatmap.risk_flags else 0
            
            if num_alerts == 0 and heatmap.risk_level in ['high', 'critical']:
                num_alerts = 1  # Ensure critical students have at least one alert
            
            for i in range(num_alerts):
                # Select alert type based on risk flags or random
                if heatmap.risk_flags:
                    if 'low_attendance' in heatmap.risk_flags:
                        alert_type = 'attendance'
                        heatmap.risk_flags.remove('low_attendance')
                    elif 'inactive_lms' in heatmap.risk_flags:
                        alert_type = 'lms_inactivity'
                        heatmap.risk_flags.remove('inactive_lms')
                    elif 'negative_sentiment' in heatmap.risk_flags:
                        alert_type = 'negative_sentiment'
                        heatmap.risk_flags.remove('negative_sentiment')
                    else:
                        alert_type = 'overall_engagement'
                else:
                    alert_type = 'overall_engagement'
                
                template = alert_templates[alert_type]
                
                # Format description
                description = template['description'].format(
                    days=random.randint(2, 5),
                    score=int(heatmap.attendance_score if alert_type == 'attendance' else heatmap.overall_engagement_score),
                    last_activity='5 days ago',
                    keywords=', '.join(['struggling', 'frustrated', 'difficult'])
                )
                
                # Determine severity
                if heatmap.risk_level == 'critical':
                    severity = 'critical'
                elif heatmap.risk_level == 'high':
                    severity = random.choice(['high', 'critical'])
                else:
                    severity = random.choice(['medium', 'high'])
                
                # Determine status
                status = random.choices(
                    ['active', 'acknowledged', 'resolved'],
                    weights=[0.50, 0.30, 0.20]
                )[0]
                
                alert = EngagementAlert.objects.create(
                    heatmap=heatmap,
                    tenant=heatmap.tenant,
                    student_id=heatmap.student_id,
                    student_name=heatmap.student_name,
                    alert_type=alert_type,
                    severity=severity,
                    title=template['title'],
                    description=description,
                    trigger_metrics={
                        'attendance_score': float(heatmap.attendance_score),
                        'lms_score': float(heatmap.lms_activity_score),
                        'sentiment_score': float(heatmap.sentiment_score),
                        'overall_score': float(heatmap.overall_engagement_score)
                    },
                    recommended_actions=template['recommended_actions'],
                    status=status,
                    acknowledged_by='Trainer Support' if status in ['acknowledged', 'resolved'] else '',
                    acknowledged_at=timezone.now() - timedelta(days=random.randint(1, 3)) if status in ['acknowledged', 'resolved'] else None,
                    resolved_at=timezone.now() - timedelta(hours=random.randint(1, 24)) if status == 'resolved' else None,
                    resolution_notes='Student contacted and support plan created' if status == 'resolved' else ''
                )
                alerts.append(alert)
        
        return alerts
