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
from evidence_mapper.models import (
    EvidenceMapping,
    SubmissionEvidence,
    CriteriaTag,
    EvidenceAudit,
    EmbeddingSearch,
)
from feedback_assistant.models import (
    FeedbackTemplate,
    GeneratedFeedback,
    FeedbackCriterion,
    FeedbackLog,
)
from funding_eligibility.models import (
    JurisdictionRequirement,
    EligibilityRule,
    EligibilityCheck,
    EligibilityCheckLog,
)
from industry_currency.models import (
    TrainerProfile,
    VerificationScan,
    LinkedInActivity,
    GitHubActivity,
    CurrencyEvidence,
    EntityExtraction,
)
from integrations.models import (
    Integration,
    IntegrationLog,
    IntegrationMapping,
)
from intervention_tracker.models import (
    Intervention,
    InterventionRule,
    InterventionWorkflow,
    InterventionStep,
    InterventionOutcome,
    AuditLog as InterventionAuditLog,
)
from micro_credential.models import (
    MicroCredential,
    MicroCredentialVersion,
    MicroCredentialEnrollment,
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
        
        # Create evidence mapper data
        evidence_mappings = self.create_evidence_mappings(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(evidence_mappings)} evidence mappings'))
        
        submission_evidence = self.create_submission_evidence(evidence_mappings)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(submission_evidence)} submission evidence'))
        
        criteria_tags = self.create_criteria_tags(submission_evidence)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(criteria_tags)} criteria tags'))
        
        evidence_audits = self.create_evidence_audits(evidence_mappings, submission_evidence, criteria_tags)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(evidence_audits)} evidence audit logs'))
        
        embedding_searches = self.create_embedding_searches(evidence_mappings)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(embedding_searches)} embedding searches'))
        
        # Create feedback assistant data
        feedback_templates = self.create_feedback_templates(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(feedback_templates)} feedback templates'))
        
        feedback_criteria = self.create_feedback_criteria(feedback_templates)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(feedback_criteria)} feedback criteria'))
        
        generated_feedback = self.create_generated_feedback(feedback_templates, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(generated_feedback)} generated feedbacks'))
        
        feedback_logs = self.create_feedback_logs(feedback_templates, generated_feedback)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(feedback_logs)} feedback logs'))
        
        # Create funding eligibility data
        jurisdiction_requirements = self.create_jurisdiction_requirements(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(jurisdiction_requirements)} jurisdiction requirements'))
        
        eligibility_rules = self.create_eligibility_rules(tenants, jurisdiction_requirements, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(eligibility_rules)} eligibility rules'))
        
        eligibility_checks = self.create_eligibility_checks(tenants, jurisdiction_requirements, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(eligibility_checks)} eligibility checks'))
        
        eligibility_check_logs = self.create_eligibility_check_logs(eligibility_checks, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(eligibility_check_logs)} eligibility check logs'))
        
        # Create industry currency verifier data
        trainer_profiles = self.create_trainer_profiles(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(trainer_profiles)} trainer profiles'))
        
        verification_scans = self.create_verification_scans(trainer_profiles)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(verification_scans)} verification scans'))
        
        linkedin_activities = self.create_linkedin_activities(verification_scans)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(linkedin_activities)} LinkedIn activities'))
        
        github_activities = self.create_github_activities(verification_scans)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(github_activities)} GitHub activities'))
        
        entity_extractions = self.create_entity_extractions(verification_scans)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(entity_extractions)} entity extractions'))
        
        currency_evidence = self.create_currency_evidence(trainer_profiles, verification_scans, linkedin_activities, github_activities)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(currency_evidence)} currency evidence documents'))
        
        # Create integrations data
        integrations = self.create_integrations(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(integrations)} integrations'))
        
        integration_logs = self.create_integration_logs(integrations)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(integration_logs)} integration logs'))
        
        integration_mappings = self.create_integration_mappings(integrations)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(integration_mappings)} integration mappings'))
        
        # Create intervention tracker data
        intervention_rules = self.create_intervention_rules(tenants)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(intervention_rules)} intervention rules'))
        
        intervention_workflows = self.create_intervention_workflows(tenants)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(intervention_workflows)} intervention workflows'))
        
        interventions = self.create_interventions(tenants, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(interventions)} interventions'))
        
        intervention_steps = self.create_intervention_steps(interventions, intervention_workflows)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(intervention_steps)} intervention steps'))
        
        intervention_outcomes = self.create_intervention_outcomes(interventions)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(intervention_outcomes)} intervention outcomes'))
        
        intervention_audit_logs = self.create_intervention_audit_logs(interventions, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(intervention_audit_logs)} intervention audit logs'))
        
        # Create micro credential data
        micro_credentials = self.create_micro_credentials(tenants, users, units)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(micro_credentials)} micro credentials'))
        
        micro_credential_versions = self.create_micro_credential_versions(micro_credentials, users)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(micro_credential_versions)} micro credential versions'))
        
        micro_credential_enrollments = self.create_micro_credential_enrollments(micro_credentials)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(micro_credential_enrollments)} micro credential enrollments'))
        
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
        
        # Evidence Mapper
        try:
            EmbeddingSearch.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            EvidenceAudit.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            CriteriaTag.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            SubmissionEvidence.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            EvidenceMapping.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Feedback Assistant
        try:
            FeedbackLog.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            FeedbackCriterion.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            GeneratedFeedback.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            FeedbackTemplate.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Funding Eligibility
        try:
            EligibilityCheckLog.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            EligibilityCheck.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            EligibilityRule.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            JurisdictionRequirement.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Industry Currency Verifier
        try:
            EntityExtraction.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            CurrencyEvidence.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            GitHubActivity.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            LinkedInActivity.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            VerificationScan.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            TrainerProfile.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Integrations
        try:
            IntegrationMapping.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            IntegrationLog.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            Integration.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Intervention Tracker
        try:
            InterventionAuditLog.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            InterventionOutcome.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            InterventionStep.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            Intervention.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            InterventionWorkflow.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            InterventionRule.objects.all().delete()
        except ProgrammingError:
            pass
        
        # Micro Credential
        try:
            MicroCredentialEnrollment.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            MicroCredentialVersion.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            MicroCredential.objects.all().delete()
        except ProgrammingError:
            pass
        
        try:
            InterventionRule.objects.all().delete()
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

    def create_evidence_mappings(self, tenants, users):
        """Create evidence mappings"""
        mappings = []
        
        assessment_templates = [
            {
                'name': 'Certificate III Assessment Portfolio',
                'description': 'Portfolio-based assessment for Certificate III qualification covering multiple units',
                'assessment_type': 'portfolio',
                'assessment_title': 'Certificate III in Business - Portfolio Assessment',
                'unit_code': 'BSB30120',
                'total_criteria': 15,
                'auto_extract_text': True,
                'generate_embeddings': True,
            },
            {
                'name': 'Practical Demonstration Assessment',
                'description': 'Hands-on practical demonstration with video evidence and supporting documentation',
                'assessment_type': 'practical',
                'assessment_title': 'Certificate IV in Training and Assessment - Practical Demo',
                'unit_code': 'TAE40116',
                'total_criteria': 12,
                'auto_extract_text': True,
                'generate_embeddings': False,
            },
            {
                'name': 'Written Assignment Assessment',
                'description': 'Written assignment with research and case study components',
                'assessment_type': 'written',
                'assessment_title': 'Diploma of Leadership - Written Assignment',
                'unit_code': 'BSB50420',
                'total_criteria': 10,
                'auto_extract_text': True,
                'generate_embeddings': True,
            },
            {
                'name': 'Project Work Assessment',
                'description': 'Major project with planning documentation, implementation evidence, and review',
                'assessment_type': 'project',
                'assessment_title': 'Certificate IV in Project Management - Major Project',
                'unit_code': 'BSB40920',
                'total_criteria': 18,
                'auto_extract_text': True,
                'generate_embeddings': True,
            },
        ]
        
        for i, tenant in enumerate(tenants):
            # Create 1-2 mappings per tenant
            for j, template in enumerate(assessment_templates[:2]):
                mapping = EvidenceMapping.objects.create(
                    name=template['name'],
                    description=template['description'],
                    assessment_type=template['assessment_type'],
                    assessment_title=template['assessment_title'],
                    unit_code=template['unit_code'],
                    total_criteria=template['total_criteria'],
                    auto_extract_text=template['auto_extract_text'],
                    generate_embeddings=template['generate_embeddings'],
                    require_evidence_per_criterion=True,
                    min_evidence_length=50,
                    status=random.choice(['active', 'completed', 'draft']),
                    created_by=random.choice(users).username,
                )
                mappings.append(mapping)
        
        return mappings

    def create_submission_evidence(self, mappings):
        """Create submission evidence"""
        submissions = []
        
        sample_texts = [
            {
                'title': 'Business Communication Report',
                'text': '''Business Communication in the Digital Age

Introduction:
Effective business communication is essential in today's fast-paced corporate environment. This report examines key principles of professional communication, including written correspondence, verbal presentations, and digital communication channels.

Key Findings:
1. Written Communication: Clear and concise writing is crucial for professional success. All business correspondence should maintain a professional tone while remaining accessible to the intended audience.

2. Verbal Communication: Face-to-face meetings and presentations require careful preparation. Speaking clearly, maintaining eye contact, and using appropriate body language enhances message delivery.

3. Digital Communication: Email, instant messaging, and video conferencing have become standard business tools. Understanding when to use each channel appropriately demonstrates professional competency.

Best Practices:
- Always proofread written communications before sending
- Tailor your message to your audience
- Use active listening techniques in conversations
- Respond to communications in a timely manner
- Maintain professionalism across all channels

Conclusion:
Mastering business communication skills requires continuous practice and refinement. By following established principles and adapting to new technologies, professionals can communicate effectively in any business context.'''
            },
            {
                'title': 'Workplace Health and Safety Analysis',
                'text': '''Workplace Health and Safety Compliance Report

Executive Summary:
This report analyzes current workplace health and safety practices and identifies areas for improvement to ensure full compliance with regulatory requirements.

Current Safety Measures:
Our organization has implemented several safety protocols including:
- Regular safety inductions for all new staff
- Monthly workplace inspections
- Incident reporting systems
- Personal protective equipment (PPE) provision
- Emergency evacuation procedures

Risk Assessment:
Through comprehensive workplace audits, we have identified the following risk areas:
1. Manual handling tasks requiring proper training
2. Workstation ergonomics needing assessment
3. Emergency exits requiring clearer signage
4. First aid supplies needing restocking

Recommendations:
1. Implement monthly manual handling training sessions
2. Conduct ergonomic assessments for all workstations
3. Install illuminated emergency exit signs
4. Establish quarterly first aid supply audits
5. Create a safety committee with staff representatives

Implementation Timeline:
- Month 1: Address critical safety signage
- Month 2-3: Roll out training programs
- Month 4: Complete workstation assessments
- Ongoing: Regular monitoring and review

By implementing these recommendations, we will create a safer workplace environment and ensure regulatory compliance.'''
            },
            {
                'title': 'Customer Service Case Study',
                'text': '''Customer Service Excellence: A Case Study Analysis

Background:
This case study examines a challenging customer service situation and demonstrates effective problem-solving techniques.

The Situation:
A long-term client contacted our support team expressing frustration about a delayed shipment. The product was critical for their upcoming event, and the delay threatened their business relationship with their own client.

Initial Response:
Upon receiving the complaint, I immediately:
1. Acknowledged the customer's concerns with empathy
2. Apologized for the inconvenience without making excuses
3. Gathered all relevant information about the order
4. Investigated the cause of the delay with the logistics team

Problem-Solving Approach:
After identifying that a warehouse error caused the delay, I took the following actions:
- Arranged for express shipping at no additional cost
- Provided real-time tracking information
- Called the customer personally with updates
- Offered a discount on their next order as compensation

Resolution:
The product arrived one day before the client's event. The customer appreciated the proactive communication and problem-solving approach. They continued their business relationship and later provided positive feedback about the service recovery.

Key Learnings:
1. Prompt acknowledgment and empathy are crucial
2. Taking ownership builds trust
3. Proactive communication reduces anxiety
4. Going above and beyond can turn negatives into positives
5. Following up ensures lasting satisfaction

This experience reinforced the importance of excellent customer service skills in maintaining strong business relationships.'''
            },
            {
                'title': 'Team Leadership Reflection',
                'text': '''Leadership Reflection: Managing a Diverse Team

Introduction:
As team leader for the Q4 project implementation, I gained valuable insights into effective leadership practices, particularly when managing a diverse team with varying skill levels and backgrounds.

Team Composition:
Our team consisted of six members with different experience levels:
- Two senior staff with 5+ years experience
- Three mid-level team members
- One graduate trainee

Leadership Challenges:
Initially, I faced several challenges:
1. Balancing workload distribution fairly
2. Ensuring clear communication across experience levels
3. Motivating team members with different working styles
4. Managing conflicts arising from diverse perspectives

Strategies Implemented:
To address these challenges, I employed several leadership strategies:

Delegation:
- Assigned tasks based on individual strengths and development needs
- Provided clear instructions and expected outcomes
- Allowed autonomy while remaining available for support

Communication:
- Held weekly team meetings for updates and concerns
- Maintained an open-door policy for individual discussions
- Used multiple communication channels (email, meetings, chat)

Team Development:
- Paired experienced staff with junior members for mentoring
- Encouraged knowledge sharing through lunch-and-learn sessions
- Provided constructive feedback regularly

Conflict Resolution:
- Addressed conflicts promptly and privately
- Listened to all perspectives before making decisions
- Focused on solutions rather than blame

Results:
The project was completed two weeks ahead of schedule with all quality standards met. Team satisfaction surveys showed 95% positive feedback about team leadership and collaboration.

Personal Growth:
This experience taught me that effective leadership requires:
- Adaptability to different team member needs
- Active listening and empathy
- Clear communication
- Delegation balanced with support
- Recognition of individual contributions

Moving forward, I will continue developing these leadership competencies and seeking opportunities to enhance team performance.'''
            },
        ]
        
        for mapping in mappings:
            # Create 3-5 submissions per mapping
            num_submissions = random.randint(3, 5)
            
            for i in range(num_submissions):
                student_id = f"STU{random.randint(1000, 9999)}"
                student_name = random.choice([
                    'Emma Wilson', 'James Chen', 'Sarah Johnson', 
                    'Michael Brown', 'Jessica Lee', 'Daniel Kim',
                    'Olivia Martinez', 'Ryan Taylor'
                ])
                
                sample = random.choice(sample_texts)
                
                # Simulate extraction
                extraction_status = random.choices(
                    ['completed', 'processing', 'pending', 'failed'],
                    weights=[0.80, 0.10, 0.05, 0.05]
                )[0]
                
                extracted_text = sample['text'] if extraction_status == 'completed' else ''
                
                # Generate mock embedding (vector of 384 dimensions)
                embedding = []
                if mapping.generate_embeddings and extraction_status == 'completed':
                    embedding = [random.uniform(-1, 1) for _ in range(384)]
                
                submission = SubmissionEvidence.objects.create(
                    mapping=mapping,
                    student_id=student_id,
                    student_name=student_name,
                    submission_id=f"SUB-{random.randint(10000, 99999)}",
                    submission_title=sample['title'],
                    submission_type=random.choice(['PDF', 'DOCX', 'Video', 'Portfolio']),
                    file_path=f"/submissions/{mapping.id}/{student_id}/{sample['title'].replace(' ', '_')}.pdf",
                    file_size_bytes=random.randint(100000, 5000000),
                    extracted_text=extracted_text,
                    extraction_status=extraction_status,
                    extraction_method=random.choice(['PDF Parser', 'OCR', 'Speech-to-text', 'DOCX Parser']),
                    text_embedding=embedding,
                    embedding_model='sentence-transformers/all-MiniLM-L6-v2' if embedding else '',
                    embedding_dimension=384 if embedding else None,
                    metadata={
                        'language': 'en',
                        'readability_score': random.uniform(60, 85),
                        'word_count': len(extracted_text.split()) if extracted_text else 0,
                        'extracted_keywords': ['business', 'communication', 'professional', 'assessment'] if extracted_text else [],
                    },
                    submitted_at=timezone.now() - timedelta(days=random.randint(1, 30)),
                    extracted_at=timezone.now() - timedelta(days=random.randint(0, 25)) if extraction_status == 'completed' else None,
                )
                submissions.append(submission)
                
                # Update mapping statistics
                mapping.total_submissions += 1
                if extraction_status == 'completed':
                    mapping.total_text_extracted += 1
                if embedding:
                    mapping.embeddings_generated += 1
                mapping.save()
        
        return submissions

    def create_criteria_tags(self, submissions):
        """Create criteria tags"""
        tags = []
        
        criteria_templates = [
            {
                'id': 'CRIT-001',
                'name': 'Demonstrate effective written communication',
                'description': 'Student demonstrates clear, professional written communication appropriate to context',
            },
            {
                'id': 'CRIT-002',
                'name': 'Apply workplace health and safety principles',
                'description': 'Student identifies and applies WHS principles in workplace scenarios',
            },
            {
                'id': 'CRIT-003',
                'name': 'Provide quality customer service',
                'description': 'Student demonstrates customer service skills including problem-solving and empathy',
            },
            {
                'id': 'CRIT-004',
                'name': 'Demonstrate leadership capabilities',
                'description': 'Student shows evidence of leadership, delegation, and team management',
            },
            {
                'id': 'CRIT-005',
                'name': 'Conduct risk assessment',
                'description': 'Student identifies workplace risks and proposes mitigation strategies',
            },
            {
                'id': 'CRIT-006',
                'name': 'Resolve conflicts effectively',
                'description': 'Student demonstrates conflict resolution techniques in workplace situations',
            },
        ]
        
        for submission in submissions:
            if submission.extraction_status != 'completed' or not submission.extracted_text:
                continue
            
            # Create 2-4 tags per submission
            num_tags = random.randint(2, 4)
            criteria_used = random.sample(criteria_templates, min(num_tags, len(criteria_templates)))
            
            for criterion in criteria_used:
                # Find relevant text excerpt (simulate intelligent extraction)
                text_paragraphs = submission.extracted_text.split('\n\n')
                relevant_paragraph = random.choice([p for p in text_paragraphs if len(p) > 100])
                
                # Extract a sentence or two
                sentences = [s.strip() + '.' for s in relevant_paragraph.split('.') if len(s.strip()) > 20]
                if not sentences:
                    continue
                
                tagged_text = ' '.join(sentences[:2])
                start_pos = submission.extracted_text.find(tagged_text)
                
                if start_pos == -1:
                    continue
                
                end_pos = start_pos + len(tagged_text)
                
                # Get context
                context_start = max(0, start_pos - 100)
                context_end = min(len(submission.extracted_text), end_pos + 100)
                context_before = submission.extracted_text[context_start:start_pos]
                context_after = submission.extracted_text[end_pos:context_end]
                
                # Determine tag details
                tag_type = random.choices(
                    ['direct', 'indirect', 'supporting', 'reference'],
                    weights=[0.60, 0.25, 0.10, 0.05]
                )[0]
                
                confidence_level = random.choices(
                    ['high', 'medium', 'low', 'manual'],
                    weights=[0.30, 0.25, 0.15, 0.30]
                )[0]
                
                confidence_score = {
                    'high': random.uniform(0.8, 1.0),
                    'medium': random.uniform(0.5, 0.8),
                    'low': random.uniform(0.3, 0.5),
                    'manual': 1.0,
                }[confidence_level]
                
                is_validated = random.random() < 0.6
                
                tag = CriteriaTag.objects.create(
                    evidence=submission,
                    criterion_id=criterion['id'],
                    criterion_name=criterion['name'],
                    criterion_description=criterion['description'],
                    tagged_text=tagged_text,
                    text_start_position=start_pos,
                    text_end_position=end_pos,
                    context_before=context_before,
                    context_after=context_after,
                    tag_type=tag_type,
                    confidence_level=confidence_level,
                    confidence_score=confidence_score,
                    notes=random.choice([
                        'Clear demonstration of competency',
                        'Good example with practical application',
                        'Meets criteria requirements',
                        'Strong evidence of understanding',
                        ''
                    ]),
                    keywords=['assessment', 'competency', 'evidence', criterion['name'].split()[1].lower()],
                    is_validated=is_validated,
                    validated_by=random.choice(['Jane Smith', 'John Doe', 'Mary Johnson']) if is_validated else '',
                    validated_at=timezone.now() - timedelta(days=random.randint(1, 15)) if is_validated else None,
                    tagged_by=random.choice(['Jane Smith', 'John Doe', 'Mary Johnson', 'AI Assistant']),
                )
                tags.append(tag)
                
                # Update submission statistics
                submission.total_tags += 1
                if criterion['id'] not in submission.criteria_covered:
                    submission.criteria_covered.append(criterion['id'])
                submission.save()
                
                # Update mapping statistics
                submission.mapping.total_evidence_tagged += 1
                submission.mapping.save()
        
        # Update coverage percentages for mappings
        for submission in submissions:
            mapping = submission.mapping
            mapping.coverage_percentage = mapping.calculate_coverage()
            mapping.save()
        
        return tags

    def create_evidence_audits(self, mappings, submissions, tags):
        """Create evidence audit logs"""
        audits = []
        
        for mapping in mappings:
            # Mapping created audit
            audit = EvidenceAudit.objects.create(
                mapping=mapping,
                action='mapping_created',
                description=f'Evidence mapping "{mapping.name}" created',
                action_data={
                    'assessment_type': mapping.assessment_type,
                    'total_criteria': mapping.total_criteria,
                    'auto_extract': mapping.auto_extract_text,
                },
                performed_by=mapping.created_by,
                user_role='Assessor',
                timestamp=mapping.created_at,
            )
            audits.append(audit)
        
        for submission in submissions[:10]:  # Audit logs for first 10 submissions
            # Submission added
            audit = EvidenceAudit.objects.create(
                mapping=submission.mapping,
                action='submission_added',
                description=f'Submission "{submission.submission_title}" added for student {submission.student_id}',
                submission_id=submission.submission_id,
                action_data={
                    'student_name': submission.student_name,
                    'submission_type': submission.submission_type,
                    'file_size': submission.file_size_bytes,
                },
                performed_by='System',
                user_role='Automated',
            )
            audits.append(audit)
            
            if submission.extraction_status == 'completed':
                # Text extracted
                audit = EvidenceAudit.objects.create(
                    mapping=submission.mapping,
                    action='text_extracted',
                    description=f'Text extracted from submission {submission.evidence_number}',
                    submission_id=submission.submission_id,
                    action_data={
                        'text_length': submission.text_length,
                        'extraction_method': submission.extraction_method,
                    },
                    processing_time_ms=random.randint(500, 5000),
                    performed_by='System',
                    user_role='Automated',
                )
                audits.append(audit)
            
            if submission.text_embedding:
                # Embedding generated
                audit = EvidenceAudit.objects.create(
                    mapping=submission.mapping,
                    action='embedding_generated',
                    description=f'Embeddings generated for submission {submission.evidence_number}',
                    submission_id=submission.submission_id,
                    action_data={
                        'embedding_model': submission.embedding_model,
                        'embedding_dimension': submission.embedding_dimension,
                    },
                    processing_time_ms=random.randint(1000, 3000),
                    performed_by='System',
                    user_role='Automated',
                )
                audits.append(audit)
        
        for tag in tags[:15]:  # Audit logs for first 15 tags
            # Evidence tagged
            audit = EvidenceAudit.objects.create(
                mapping=tag.evidence.mapping,
                action='evidence_tagged',
                description=f'Evidence tagged for criterion {tag.criterion_id}',
                submission_id=tag.evidence.submission_id,
                criterion_id=tag.criterion_id,
                tag_id=tag.id,
                action_data={
                    'tag_type': tag.tag_type,
                    'confidence': tag.confidence_score,
                    'text_length': len(tag.tagged_text),
                },
                performed_by=tag.tagged_by,
                user_role='Assessor',
            )
            audits.append(audit)
            
            if tag.is_validated:
                # Tag validated
                audit = EvidenceAudit.objects.create(
                    mapping=tag.evidence.mapping,
                    action='tag_validated',
                    description=f'Evidence tag validated for criterion {tag.criterion_id}',
                    submission_id=tag.evidence.submission_id,
                    criterion_id=tag.criterion_id,
                    tag_id=tag.id,
                    action_data={
                        'previous_status': 'unvalidated',
                        'new_status': 'validated',
                    },
                    changes_made={
                        'is_validated': {'from': False, 'to': True},
                        'validated_by': {'from': '', 'to': tag.validated_by},
                    },
                    performed_by=tag.validated_by,
                    user_role='Lead Assessor',
                    timestamp=tag.validated_at,
                )
                audits.append(audit)
        
        return audits

    def create_embedding_searches(self, mappings):
        """Create embedding search logs"""
        searches = []
        
        search_queries = [
            {
                'type': 'similarity',
                'query': 'Demonstrate effective written communication in business context',
                'results': 8,
            },
            {
                'type': 'criteria_match',
                'query': 'Leadership and team management evidence',
                'results': 5,
            },
            {
                'type': 'keyword',
                'query': 'workplace health and safety risk assessment',
                'results': 12,
            },
            {
                'type': 'hybrid',
                'query': 'Customer service problem solving with empathy',
                'results': 7,
            },
            {
                'type': 'similarity',
                'query': 'Conflict resolution in workplace scenarios',
                'results': 4,
            },
        ]
        
        for mapping in mappings:
            if not mapping.generate_embeddings:
                continue
            
            # Create 2-3 search logs per mapping
            for i in range(random.randint(2, 3)):
                query_template = random.choice(search_queries)
                
                # Generate mock embedding for query
                query_embedding = [random.uniform(-1, 1) for _ in range(384)]
                
                # Mock top results
                top_results = []
                for j in range(query_template['results']):
                    top_results.append({
                        'submission_id': f"SUB-{random.randint(10000, 99999)}",
                        'similarity_score': random.uniform(0.6, 0.95),
                        'text_excerpt': 'Sample text excerpt from matching submission...',
                    })
                
                search = EmbeddingSearch.objects.create(
                    mapping=mapping,
                    search_type=query_template['type'],
                    query_text=query_template['query'],
                    query_embedding=query_embedding,
                    filter_criteria={
                        'date_range': 'last_30_days',
                        'min_confidence': 0.7,
                    },
                    results_count=query_template['results'],
                    top_results=top_results,
                    search_time_ms=random.randint(50, 500),
                    performed_by=random.choice(['Jane Smith', 'John Doe', 'Mary Johnson']),
                )
                searches.append(search)
        
        return searches

    def create_feedback_templates(self, tenants, users):
        """Create feedback templates"""
        templates = []
        
        template_configs = [
            {
                'name': 'Formative Assessment Feedback',
                'description': 'Encouraging feedback for ongoing assessments to support student learning',
                'feedback_type': 'formative',
                'sentiment': 'encouraging',
                'tone': 'supportive',
                'positivity_level': 8,
                'directness_level': 5,
                'formality_level': 6,
                'opening_template': 'Hi {student_name},\n\nThank you for submitting your {assessment_title}.',
                'strengths_template': 'You demonstrated strong skills in: {strengths}',
                'improvements_template': 'To further develop your understanding, consider: {improvements}',
                'next_steps_template': 'Recommended next steps:\n{next_steps}',
                'closing_template': 'Keep up the excellent work! I look forward to seeing your continued progress.',
            },
            {
                'name': 'Summative Assessment Feedback',
                'description': 'Professional feedback for final assessments with clear performance indicators',
                'feedback_type': 'summative',
                'sentiment': 'constructive',
                'tone': 'professional',
                'positivity_level': 6,
                'directness_level': 7,
                'formality_level': 8,
                'opening_template': 'Dear {student_name},\n\nYour {assessment_title} has been assessed.',
                'strengths_template': 'Strengths demonstrated:\n{strengths}',
                'improvements_template': 'Areas requiring attention:\n{improvements}',
                'next_steps_template': 'For future assessments:\n{next_steps}',
                'closing_template': 'If you have questions about this feedback, please schedule a consultation.',
            },
            {
                'name': 'Peer Review Feedback',
                'description': 'Constructive peer feedback template with balanced tone',
                'feedback_type': 'peer',
                'sentiment': 'constructive',
                'tone': 'friendly',
                'positivity_level': 7,
                'directness_level': 6,
                'formality_level': 5,
                'opening_template': 'Hey {student_name},\n\nI reviewed your {assessment_title} and have some thoughts to share.',
                'strengths_template': 'What worked really well:\n{strengths}',
                'improvements_template': 'Some suggestions for improvement:\n{improvements}',
                'next_steps_template': 'Consider trying:\n{next_steps}',
                'closing_template': 'Great effort overall! Looking forward to your next submission.',
            },
            {
                'name': 'Motivational Feedback',
                'description': 'Highly encouraging feedback to motivate struggling students',
                'feedback_type': 'formative',
                'sentiment': 'motivational',
                'tone': 'supportive',
                'positivity_level': 9,
                'directness_level': 4,
                'formality_level': 5,
                'opening_template': 'Hello {student_name},\n\nI can see the effort you put into your {assessment_title}!',
                'strengths_template': 'You are making progress in these areas:\n{strengths}',
                'improvements_template': 'Let\'s work together on:\n{improvements}',
                'next_steps_template': 'To help you succeed:\n{next_steps}',
                'closing_template': 'Remember, learning is a journey! You\'re capable of great things. Keep going!',
            },
        ]
        
        for tenant in tenants:
            # Create 2-3 templates per tenant
            for config in template_configs[:random.randint(2, 3)]:
                template = FeedbackTemplate.objects.create(
                    name=config['name'],
                    description=config['description'],
                    tenant=tenant.slug,
                    created_by=random.choice(users),
                    feedback_type=config['feedback_type'],
                    sentiment=config['sentiment'],
                    tone=config['tone'],
                    include_student_name=True,
                    include_strengths=True,
                    include_improvements=True,
                    include_next_steps=True,
                    include_encouragement=True,
                    opening_template=config['opening_template'],
                    strengths_template=config['strengths_template'],
                    improvements_template=config['improvements_template'],
                    next_steps_template=config['next_steps_template'],
                    closing_template=config['closing_template'],
                    positivity_level=config['positivity_level'],
                    directness_level=config['directness_level'],
                    formality_level=config['formality_level'],
                    status=random.choice(['active', 'active', 'draft']),
                )
                templates.append(template)
        
        return templates

    def create_feedback_criteria(self, templates):
        """Create feedback criteria"""
        criteria = []
        
        criterion_templates = [
            {
                'name': 'Content Knowledge',
                'description': 'Demonstration of understanding of subject matter',
                'excellent': 'Demonstrates exceptional understanding of all key concepts with sophisticated analysis and synthesis of information.',
                'good': 'Shows solid understanding of main concepts with good application of knowledge.',
                'satisfactory': 'Demonstrates basic understanding of core concepts with some gaps.',
                'needs_improvement': 'Shows limited understanding of key concepts. Review course materials and seek additional support.',
                'weight': 0.30,
            },
            {
                'name': 'Critical Thinking',
                'description': 'Analysis, evaluation, and problem-solving abilities',
                'excellent': 'Presents insightful analysis with well-supported arguments and creative problem-solving approaches.',
                'good': 'Demonstrates good analytical skills with logical reasoning and valid conclusions.',
                'satisfactory': 'Shows basic analytical thinking but could develop deeper analysis.',
                'needs_improvement': 'Analysis lacks depth. Practice examining issues from multiple perspectives.',
                'weight': 0.25,
            },
            {
                'name': 'Communication',
                'description': 'Clarity and effectiveness of written/verbal expression',
                'excellent': 'Communicates ideas with exceptional clarity, precision, and professional polish.',
                'good': 'Expresses ideas clearly with good structure and appropriate language.',
                'satisfactory': 'Communication is generally clear but could be more refined.',
                'needs_improvement': 'Work on clarity and organization. Consider using writing support services.',
                'weight': 0.20,
            },
            {
                'name': 'Research & Evidence',
                'description': 'Use of appropriate sources and supporting evidence',
                'excellent': 'Incorporates excellent range of credible sources with proper citation and integration.',
                'good': 'Uses relevant sources effectively to support arguments.',
                'satisfactory': 'Includes some supporting evidence but could be more comprehensive.',
                'needs_improvement': 'Strengthen arguments with additional credible sources and proper citations.',
                'weight': 0.15,
            },
            {
                'name': 'Technical Skills',
                'description': 'Application of technical or practical skills',
                'excellent': 'Demonstrates mastery of technical skills with professional-level execution.',
                'good': 'Shows competent application of required technical skills.',
                'satisfactory': 'Basic technical skills present but need further development.',
                'needs_improvement': 'Technical skills require significant improvement. Practice fundamental techniques.',
                'weight': 0.10,
            },
        ]
        
        for template in templates:
            # Create 3-5 criteria per template
            num_criteria = random.randint(3, 5)
            for i, criterion in enumerate(criterion_templates[:num_criteria]):
                fb_criterion = FeedbackCriterion.objects.create(
                    template=template,
                    criterion_name=criterion['name'],
                    description=criterion['description'],
                    excellent_feedback=criterion['excellent'],
                    good_feedback=criterion['good'],
                    satisfactory_feedback=criterion['satisfactory'],
                    needs_improvement_feedback=criterion['needs_improvement'],
                    weight=criterion['weight'],
                    display_order=i + 1,
                )
                criteria.append(fb_criterion)
        
        return criteria

    def create_generated_feedback(self, templates, users):
        """Create generated feedback"""
        feedbacks = []
        
        student_names = [
            'Emma Wilson', 'James Chen', 'Sarah Johnson', 
            'Michael Brown', 'Jessica Lee', 'Daniel Kim',
            'Olivia Martinez', 'Ryan Taylor', 'Sophia Anderson',
            'Liam Thompson', 'Ava Rodriguez', 'Noah Williams'
        ]
        
        assessment_titles = [
            'Business Communication Report',
            'Project Management Assignment',
            'Customer Service Case Study',
            'Workplace Health & Safety Analysis',
            'Team Leadership Reflection',
            'Marketing Strategy Presentation',
            'Financial Analysis Report',
            'Quality Assurance Assessment',
        ]
        
        strengths = [
            ['Clear understanding of core concepts', 'Well-structured analysis', 'Professional presentation'],
            ['Strong research skills', 'Critical thinking demonstrated', 'Effective use of examples'],
            ['Excellent writing quality', 'Good time management', 'Thorough coverage of topics'],
            ['Creative problem-solving', 'Attention to detail', 'Professional formatting'],
            ['Strong analytical skills', 'Good use of evidence', 'Clear communication'],
        ]
        
        improvements = [
            ['Expand analysis of key theories', 'Include more recent sources', 'Strengthen conclusion'],
            ['Develop critical evaluation further', 'Add more practical examples', 'Review citation format'],
            ['Consider alternative perspectives', 'Deepen theoretical analysis', 'Improve paragraph transitions'],
            ['Strengthen evidence base', 'Clarify methodology', 'Expand discussion section'],
        ]
        
        next_steps = [
            ['Review feedback and schedule consultation if needed', 'Practice similar assessments', 'Read suggested resources'],
            ['Work on identified improvement areas', 'Seek peer review before submission', 'Utilize learning support services'],
            ['Apply feedback to future work', 'Develop action plan for skill development', 'Request additional examples'],
        ]
        
        for template in templates:
            # Create 4-6 feedbacks per template
            num_feedbacks = random.randint(4, 6)
            
            for i in range(num_feedbacks):
                student_name = random.choice(student_names)
                student_id = f"STU{random.randint(1000, 9999)}"
                assessment = random.choice(assessment_titles)
                
                # Generate scores
                score = random.uniform(50, 100)
                max_score = 100.0
                
                # Determine grade based on score
                if score >= 85:
                    grade = 'HD'
                    strength_set = random.choice(strengths)
                    improvement_set = random.choice(improvements[:2])
                elif score >= 75:
                    grade = 'D'
                    strength_set = random.choice(strengths[:3])
                    improvement_set = random.choice(improvements[:3])
                elif score >= 65:
                    grade = 'C'
                    strength_set = random.choice(strengths[:3])
                    improvement_set = random.choice(improvements)
                elif score >= 50:
                    grade = 'P'
                    strength_set = random.choice(strengths[:2])
                    improvement_set = random.choice(improvements)
                else:
                    grade = 'F'
                    strength_set = random.choice(strengths[:1])
                    improvement_set = improvements[0]
                
                next_step_set = random.choice(next_steps)
                
                # Generate feedback text using template
                feedback_parts = []
                
                if template.include_student_name:
                    feedback_parts.append(
                        template.opening_template.format(
                            student_name=student_name,
                            assessment_title=assessment
                        )
                    )
                
                feedback_parts.append(f"\nYou achieved a score of {score:.1f}/{max_score} ({grade} grade).\n")
                
                if template.include_strengths:
                    strengths_text = '\n'.join([f'• {s}' for s in strength_set])
                    feedback_parts.append(
                        template.strengths_template.format(strengths=strengths_text)
                    )
                
                if template.include_improvements:
                    improvements_text = '\n'.join([f'• {i}' for i in improvement_set])
                    feedback_parts.append(
                        template.improvements_template.format(improvements=improvements_text)
                    )
                
                if template.include_next_steps:
                    next_steps_text = '\n'.join([f'{idx}. {step}' for idx, step in enumerate(next_step_set, 1)])
                    feedback_parts.append(
                        template.next_steps_template.format(next_steps=next_steps_text)
                    )
                
                if template.include_encouragement:
                    feedback_parts.append(f"\n{template.closing_template}")
                
                feedback_text = '\n\n'.join(feedback_parts)
                
                # Calculate sentiment score based on template settings
                base_sentiment = (template.positivity_level - 5.5) / 4.5  # -1 to 1 scale
                sentiment_score = max(-1.0, min(1.0, base_sentiment + random.uniform(-0.1, 0.1)))
                
                # Determine status
                status = random.choices(
                    ['generated', 'reviewed', 'delivered', 'revised'],
                    weights=[0.20, 0.30, 0.40, 0.10]
                )[0]
                
                requires_review = score < 50 or random.random() < 0.2
                
                feedback = GeneratedFeedback.objects.create(
                    template=template,
                    student_id=student_id,
                    student_name=student_name,
                    assessment_title=assessment,
                    score=score,
                    max_score=max_score,
                    grade=grade,
                    feedback_text=feedback_text,
                    strengths_identified=strength_set,
                    improvements_identified=improvement_set,
                    next_steps_suggested=next_step_set,
                    sentiment_score=sentiment_score,
                    tone_consistency=random.uniform(0.85, 0.98),
                    reading_level=random.choice(['Grade 10', 'Grade 11', 'Grade 12', 'University']),
                    personalization_score=random.uniform(0.75, 0.95),
                    requires_review=requires_review,
                    review_notes=random.choice([
                        'Approved for delivery',
                        'Minor adjustments made',
                        'Content reviewed and verified',
                        ''
                    ]) if status in ['reviewed', 'delivered'] else '',
                    reviewed_by=random.choice([None, random.choice(users)]) if status in ['reviewed', 'delivered'] else None,
                    reviewed_at=timezone.now() - timedelta(hours=random.randint(1, 48)) if status in ['reviewed', 'delivered'] else None,
                    delivered_at=timezone.now() - timedelta(hours=random.randint(1, 24)) if status == 'delivered' else None,
                    delivery_method=random.choice(['email', 'LMS', 'portal', 'manual']) if status == 'delivered' else '',
                    status=status,
                    generation_time=random.uniform(2.5, 8.0),
                )
                feedbacks.append(feedback)
                
                # Update template statistics
                template.total_feedback_generated += 1
                total_time = template.average_generation_time * (template.total_feedback_generated - 1)
                total_time += feedback.generation_time
                template.average_generation_time = total_time / template.total_feedback_generated
                template.save()
        
        return feedbacks

    def create_feedback_logs(self, templates, feedbacks):
        """Create feedback logs"""
        logs = []
        
        # Template creation logs
        for template in templates:
            log = FeedbackLog.objects.create(
                template=template,
                action='template_update',
                performed_by=template.created_by,
                feedbacks_generated=0,
                total_time=0.5,
                average_time_per_feedback=0.0,
                details={
                    'action': 'created',
                    'sentiment': template.sentiment,
                    'tone': template.tone,
                    'positivity_level': template.positivity_level,
                },
                timestamp=template.created_at,
            )
            logs.append(log)
        
        # Batch generation logs
        for template in templates:
            template_feedbacks = [f for f in feedbacks if f.template == template]
            
            if template_feedbacks:
                # Create 1-2 batch generation logs
                for batch_num in range(random.randint(1, 2)):
                    batch_size = random.randint(2, 5)
                    batch_feedbacks = template_feedbacks[:batch_size]
                    
                    total_time = sum(f.generation_time for f in batch_feedbacks)
                    avg_sentiment = sum(f.sentiment_score for f in batch_feedbacks) / len(batch_feedbacks)
                    avg_personalization = sum(f.personalization_score for f in batch_feedbacks) / len(batch_feedbacks)
                    
                    log = FeedbackLog.objects.create(
                        template=template,
                        action='generate_batch',
                        performed_by=template.created_by,
                        feedbacks_generated=len(batch_feedbacks),
                        total_time=total_time,
                        average_sentiment=avg_sentiment,
                        average_personalization=avg_personalization,
                        details={
                            'batch_size': len(batch_feedbacks),
                            'assessment_types': list(set(f.assessment_title for f in batch_feedbacks)),
                            'grade_distribution': {
                                'HD': len([f for f in batch_feedbacks if f.grade == 'HD']),
                                'D': len([f for f in batch_feedbacks if f.grade == 'D']),
                                'C': len([f for f in batch_feedbacks if f.grade == 'C']),
                                'P': len([f for f in batch_feedbacks if f.grade == 'P']),
                                'F': len([f for f in batch_feedbacks if f.grade == 'F']),
                            },
                        },
                    )
                    logs.append(log)
        
        # Review logs for reviewed feedbacks
        reviewed_feedbacks = [f for f in feedbacks if f.status in ['reviewed', 'delivered'] and f.reviewed_by]
        
        for feedback in reviewed_feedbacks[:15]:  # Log first 15 reviews
            log = FeedbackLog.objects.create(
                template=feedback.template,
                feedback=feedback,
                action='review',
                performed_by=feedback.reviewed_by,
                feedbacks_generated=1,
                total_time=random.uniform(3.0, 8.0),
                details={
                    'student_id': feedback.student_id,
                    'grade': feedback.grade,
                    'requires_review': feedback.requires_review,
                    'review_outcome': 'approved',
                },
                timestamp=feedback.reviewed_at,
            )
            logs.append(log)
        
        # Delivery logs
        delivered_feedbacks = [f for f in feedbacks if f.status == 'delivered']
        
        for feedback in delivered_feedbacks[:10]:  # Log first 10 deliveries
            log = FeedbackLog.objects.create(
                template=feedback.template,
                feedback=feedback,
                action='deliver',
                performed_by=feedback.reviewed_by or feedback.template.created_by,
                feedbacks_generated=1,
                total_time=random.uniform(0.5, 2.0),
                details={
                    'student_id': feedback.student_id,
                    'delivery_method': feedback.delivery_method,
                    'grade': feedback.grade,
                },
                timestamp=feedback.delivered_at,
            )
            logs.append(log)
        
        return logs
    
    def create_jurisdiction_requirements(self, tenants, users):
        """Create jurisdiction funding requirements"""
        requirements = []
        
        # Australian jurisdictions and their funding programs
        jurisdictions_data = [
            {
                'jurisdiction': 'nsw',
                'name': 'Smart and Skilled NSW',
                'code': 'SS-NSW',
                'min_age': 15,
                'max_age': None,
                'requires_australian_citizen': True,
                'requires_permanent_resident': False,
                'requires_jurisdiction_resident': True,
                'min_jurisdiction_residency_months': 6,
                'requires_year_12': False,
                'allows_year_10_completion': True,
                'requires_unemployed': False,
                'allows_employed': True,
                'restricts_higher_qualifications': True,
                'max_aqf_level': 5,
                'has_income_threshold': False,
                'funding_percentage': 70.00,
                'student_contribution': 1000.00,
            },
            {
                'jurisdiction': 'vic',
                'name': 'Skills First Victoria',
                'code': 'SF-VIC',
                'min_age': 17,
                'max_age': None,
                'requires_australian_citizen': True,
                'requires_permanent_resident': True,
                'requires_jurisdiction_resident': True,
                'min_jurisdiction_residency_months': 12,
                'requires_year_12': False,
                'allows_year_10_completion': True,
                'requires_unemployed': False,
                'allows_employed': True,
                'restricts_higher_qualifications': True,
                'max_aqf_level': 6,
                'has_income_threshold': True,
                'max_annual_income': 80000.00,
                'funding_percentage': 85.00,
                'student_contribution': 500.00,
            },
            {
                'jurisdiction': 'qld',
                'name': 'Certificate 3 Guarantee QLD',
                'code': 'C3G-QLD',
                'min_age': 15,
                'max_age': None,
                'requires_australian_citizen': True,
                'requires_permanent_resident': False,
                'requires_jurisdiction_resident': True,
                'min_jurisdiction_residency_months': 6,
                'requires_year_12': False,
                'allows_year_10_completion': True,
                'requires_unemployed': False,
                'allows_employed': True,
                'restricts_higher_qualifications': True,
                'max_aqf_level': 3,
                'has_income_threshold': False,
                'funding_percentage': 100.00,
                'student_contribution': 0.00,
            },
            {
                'jurisdiction': 'wa',
                'name': 'Jobs and Skills WA',
                'code': 'JS-WA',
                'min_age': 16,
                'max_age': None,
                'requires_australian_citizen': True,
                'requires_permanent_resident': False,
                'requires_jurisdiction_resident': True,
                'min_jurisdiction_residency_months': 3,
                'requires_year_12': False,
                'allows_year_10_completion': True,
                'requires_unemployed': False,
                'allows_employed': True,
                'restricts_higher_qualifications': False,
                'has_income_threshold': False,
                'funding_percentage': 75.00,
                'student_contribution': 750.00,
            },
            {
                'jurisdiction': 'sa',
                'name': 'Skills for All SA',
                'code': 'SFA-SA',
                'min_age': 15,
                'max_age': None,
                'requires_australian_citizen': True,
                'requires_permanent_resident': False,
                'requires_jurisdiction_resident': True,
                'min_jurisdiction_residency_months': 6,
                'requires_year_12': False,
                'allows_year_10_completion': True,
                'requires_unemployed': False,
                'allows_employed': True,
                'restricts_higher_qualifications': True,
                'max_aqf_level': 4,
                'has_income_threshold': False,
                'funding_percentage': 80.00,
                'student_contribution': 600.00,
            },
            {
                'jurisdiction': 'federal',
                'name': 'Australian Apprenticeships',
                'code': 'AA-FED',
                'min_age': 15,
                'max_age': None,
                'requires_australian_citizen': True,
                'requires_permanent_resident': True,
                'requires_jurisdiction_resident': False,
                'min_jurisdiction_residency_months': 0,
                'requires_year_12': False,
                'allows_year_10_completion': True,
                'requires_unemployed': False,
                'allows_employed': True,
                'requires_apprentice_trainee': True,
                'restricts_higher_qualifications': False,
                'has_income_threshold': False,
                'funding_percentage': 100.00,
                'student_contribution': 0.00,
            },
        ]
        
        for tenant in tenants:
            # Create 2-3 jurisdiction requirements per tenant
            for juris_data in random.sample(jurisdictions_data, random.randint(2, 3)):
                requirement = JurisdictionRequirement.objects.create(
                    tenant=tenant,
                    jurisdiction=juris_data['jurisdiction'],
                    name=juris_data['name'],
                    code=juris_data['code'],
                    requires_australian_citizen=juris_data['requires_australian_citizen'],
                    requires_permanent_resident=juris_data.get('requires_permanent_resident', False),
                    requires_jurisdiction_resident=juris_data['requires_jurisdiction_resident'],
                    min_jurisdiction_residency_months=juris_data['min_jurisdiction_residency_months'],
                    min_age=juris_data.get('min_age'),
                    max_age=juris_data.get('max_age'),
                    requires_year_12=juris_data['requires_year_12'],
                    allows_year_10_completion=juris_data['allows_year_10_completion'],
                    requires_unemployed=juris_data['requires_unemployed'],
                    allows_employed=juris_data['allows_employed'],
                    requires_apprentice_trainee=juris_data.get('requires_apprentice_trainee', False),
                    restricts_higher_qualifications=juris_data['restricts_higher_qualifications'],
                    max_aqf_level=juris_data.get('max_aqf_level'),
                    has_income_threshold=juris_data['has_income_threshold'],
                    max_annual_income=juris_data.get('max_annual_income'),
                    allows_concession_card=True,
                    allows_disability=True,
                    allows_indigenous=True,
                    priority_indigenous=random.choice([True, False]),
                    funding_percentage=juris_data['funding_percentage'],
                    student_contribution=juris_data['student_contribution'],
                    api_endpoint=random.choice([
                        None,
                        f"https://api.funding.{juris_data['jurisdiction']}.gov.au/verify",
                    ]),
                    api_key_required=random.choice([True, False]),
                    additional_rules={
                        'documentation_required': ['proof_of_identity', 'proof_of_residency'],
                        'special_conditions': ['First qualification at this level'],
                    },
                    is_active=random.choice([True, True, True, False]),  # 75% active
                    effective_from=timezone.now().date() - timedelta(days=random.randint(30, 365)),
                    effective_to=timezone.now().date() + timedelta(days=random.randint(365, 730)) if random.random() < 0.3 else None,
                    created_by=random.choice(users),
                )
                requirements.append(requirement)
        
        return requirements
    
    def create_eligibility_rules(self, tenants, requirements, users):
        """Create custom eligibility rules"""
        rules = []
        
        rule_definitions = [
            {
                'rule_type': 'age',
                'name': 'Minimum Age for Youth Programs',
                'description': 'Student must be at least 15 years old for youth-focused programs',
                'field_name': 'age',
                'operator': 'greater_equal',
                'expected_value': '15',
                'error_message': 'Student must be at least 15 years old to be eligible for this program',
                'priority': 5,
            },
            {
                'rule_type': 'age',
                'name': 'Maximum Age for Youth Programs',
                'description': 'Student must be under 25 years old for youth programs',
                'field_name': 'age',
                'operator': 'less_than',
                'expected_value': '25',
                'error_message': 'This program is only available to students under 25 years of age',
                'priority': 5,
                'is_mandatory': False,
            },
            {
                'rule_type': 'citizenship',
                'name': 'Australian Citizenship Required',
                'description': 'Student must be an Australian citizen',
                'field_name': 'citizenship_status',
                'operator': 'equals',
                'expected_value': 'australian_citizen',
                'error_message': 'Australian citizenship is required for this funding program',
                'priority': 1,
            },
            {
                'rule_type': 'citizenship',
                'name': 'Citizen or Permanent Resident',
                'description': 'Student must be an Australian citizen or permanent resident',
                'field_name': 'citizenship_status',
                'operator': 'in_list',
                'expected_value': 'australian_citizen,permanent_resident',
                'error_message': 'You must be an Australian citizen or permanent resident to be eligible',
                'priority': 1,
            },
            {
                'rule_type': 'residency',
                'name': 'State Residency Requirement',
                'description': 'Student must be a resident of the jurisdiction',
                'field_name': 'jurisdiction_resident',
                'operator': 'equals',
                'expected_value': 'true',
                'error_message': 'You must be a resident of this state/territory to access this funding',
                'priority': 2,
            },
            {
                'rule_type': 'residency',
                'name': 'Minimum Residency Duration',
                'description': 'Student must have resided in jurisdiction for at least 6 months',
                'field_name': 'residency_months',
                'operator': 'greater_equal',
                'expected_value': '6',
                'error_message': 'You must have lived in this state for at least 6 months',
                'priority': 3,
            },
            {
                'rule_type': 'education',
                'name': 'Year 10 Completion',
                'description': 'Student must have completed Year 10 or equivalent',
                'field_name': 'education_level',
                'operator': 'in_list',
                'expected_value': 'year_10,year_11,year_12,certificate,diploma,degree',
                'error_message': 'Year 10 completion or equivalent is required',
                'priority': 4,
            },
            {
                'rule_type': 'qualification',
                'name': 'No Higher Qualifications',
                'description': 'Student must not have a qualification at a higher AQF level',
                'field_name': 'highest_aqf_level',
                'operator': 'less_than',
                'expected_value': '4',
                'error_message': 'You already hold a qualification at a higher level than this course',
                'priority': 6,
            },
            {
                'rule_type': 'employment',
                'name': 'Apprenticeship Required',
                'description': 'Student must be enrolled in an apprenticeship or traineeship',
                'field_name': 'employment_type',
                'operator': 'in_list',
                'expected_value': 'apprentice,trainee',
                'error_message': 'This program requires you to be an apprentice or trainee',
                'priority': 7,
            },
            {
                'rule_type': 'income',
                'name': 'Income Threshold',
                'description': 'Student or household income must be below threshold',
                'field_name': 'annual_income',
                'operator': 'less_equal',
                'expected_value': '80000',
                'error_message': 'Your income exceeds the maximum threshold for this funding',
                'priority': 8,
            },
            {
                'rule_type': 'concession',
                'name': 'Concession Card Bonus',
                'description': 'Students with concession cards receive priority',
                'field_name': 'has_concession_card',
                'operator': 'equals',
                'expected_value': 'true',
                'error_message': '',
                'priority': 10,
                'is_mandatory': False,
            },
            {
                'rule_type': 'indigenous',
                'name': 'Indigenous Priority',
                'description': 'Indigenous students receive priority access',
                'field_name': 'is_indigenous',
                'operator': 'equals',
                'expected_value': 'true',
                'error_message': '',
                'priority': 10,
                'is_mandatory': False,
            },
            {
                'rule_type': 'visa',
                'name': 'Valid Visa Requirement',
                'description': 'Student must hold a valid visa with work/study rights',
                'field_name': 'visa_type',
                'operator': 'in_list',
                'expected_value': 'student,skilled,working_holiday,partner',
                'error_message': 'Your visa type does not permit access to this funding program',
                'priority': 2,
            },
            {
                'rule_type': 'language',
                'name': 'English Proficiency',
                'description': 'Minimum English language proficiency required',
                'field_name': 'english_proficiency',
                'operator': 'in_list',
                'expected_value': 'native,advanced,upper_intermediate',
                'error_message': 'Minimum upper-intermediate English proficiency required',
                'priority': 9,
            },
        ]
        
        for tenant in tenants:
            tenant_requirements = [r for r in requirements if r.tenant == tenant]
            
            # Create 3-5 rules per requirement
            for requirement in tenant_requirements:
                for rule_def in random.sample(rule_definitions, random.randint(3, 5)):
                    rule = EligibilityRule.objects.create(
                        tenant=tenant,
                        jurisdiction_requirement=requirement,
                        rule_type=rule_def['rule_type'],
                        name=rule_def['name'],
                        description=rule_def['description'],
                        field_name=rule_def['field_name'],
                        operator=rule_def['operator'],
                        expected_value=rule_def['expected_value'],
                        is_mandatory=rule_def.get('is_mandatory', True),
                        priority=rule_def['priority'],
                        error_message=rule_def['error_message'],
                        override_allowed=random.choice([True, False]),
                        is_active=True,
                        created_by=random.choice(users),
                    )
                    rules.append(rule)
        
        return rules
    
    def create_eligibility_checks(self, tenants, requirements, users):
        """Create eligibility check records"""
        checks = []
        
        first_names = ['Emma', 'Oliver', 'Ava', 'William', 'Sophia', 'Noah', 'Isabella', 'James', 'Mia', 'Lucas',
                      'Charlotte', 'Ethan', 'Amelia', 'Mason', 'Harper', 'Logan', 'Evelyn', 'Alexander', 'Abigail', 'Jackson']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee']
        
        courses = [
            {'code': 'BSB50120', 'name': 'Diploma of Business', 'aqf': 5},
            {'code': 'ICT50220', 'name': 'Diploma of Information Technology', 'aqf': 5},
            {'code': 'CHC33015', 'name': 'Certificate III in Individual Support', 'aqf': 3},
            {'code': 'SIT40516', 'name': 'Certificate IV in Commercial Cookery', 'aqf': 4},
            {'code': 'AUR30620', 'name': 'Certificate III in Light Vehicle Mechanical Technology', 'aqf': 3},
            {'code': 'BSB40520', 'name': 'Certificate IV in Leadership and Management', 'aqf': 4},
            {'code': 'TAE40116', 'name': 'Certificate IV in Training and Assessment', 'aqf': 4},
            {'code': 'CHC50113', 'name': 'Diploma of Early Childhood Education', 'aqf': 5},
        ]
        
        citizenship_statuses = ['australian_citizen', 'permanent_resident', 'temporary_visa', 'international']
        employment_types = ['unemployed', 'employed_full_time', 'employed_part_time', 'apprentice', 'trainee', 'self_employed']
        education_levels = ['year_10', 'year_11', 'year_12', 'certificate', 'diploma']
        
        for tenant in tenants:
            tenant_requirements = [r for r in requirements if r.tenant == tenant and r.is_active]
            
            if not tenant_requirements:
                continue
            
            # Create 4-6 checks per tenant
            for _ in range(random.randint(4, 6)):
                requirement = random.choice(tenant_requirements)
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                dob = timezone.now().date() - timedelta(days=random.randint(365*16, 365*55))
                course = random.choice(courses)
                
                # Generate student data
                age = (timezone.now().date() - dob).days // 365
                citizenship = random.choice(citizenship_statuses)
                employment = random.choice(employment_types)
                education = random.choice(education_levels)
                
                student_data = {
                    'age': age,
                    'citizenship_status': citizenship,
                    'jurisdiction_resident': random.choice(['true', 'false']),
                    'residency_months': random.randint(0, 60),
                    'education_level': education,
                    'highest_aqf_level': random.randint(0, 6),
                    'employment_type': employment,
                    'annual_income': random.randint(20000, 120000),
                    'has_concession_card': random.choice(['true', 'false']),
                    'is_indigenous': random.choice(['true', 'false']),
                    'has_disability': random.choice(['true', 'false']),
                    'visa_type': random.choice(['student', 'skilled', 'working_holiday', 'partner', 'none']),
                    'english_proficiency': random.choice(['native', 'advanced', 'upper_intermediate', 'intermediate']),
                }
                
                # Determine eligibility based on random criteria
                rules_checked = random.randint(5, 12)
                rules_passed = random.randint(3, rules_checked)
                rules_failed = rules_checked - rules_passed
                eligibility_percentage = (rules_passed / rules_checked * 100) if rules_checked > 0 else 0
                
                is_eligible = eligibility_percentage >= 80
                
                if is_eligible:
                    status = random.choice(['eligible', 'eligible', 'conditional'])
                else:
                    status = random.choice(['ineligible', 'pending', 'override'])
                
                # Generate failed rules
                failed_rules_list = []
                if rules_failed > 0:
                    failed_rule_types = random.sample([
                        'Age requirement not met',
                        'Citizenship status does not qualify',
                        'Residency duration insufficient',
                        'Prior qualifications restrict eligibility',
                        'Income exceeds threshold',
                    ], min(rules_failed, 3))
                    
                    for rule_type in failed_rule_types:
                        failed_rules_list.append({
                            'rule': rule_type,
                            'expected': 'Pass',
                            'actual': 'Fail',
                            'can_override': random.choice([True, False]),
                        })
                
                # Create check
                check = EligibilityCheck.objects.create(
                    tenant=tenant,
                    student_first_name=first_name,
                    student_last_name=last_name,
                    student_dob=dob,
                    student_email=f"{first_name.lower()}.{last_name.lower()}@example.com",
                    student_phone=f"+61 4{random.randint(10000000, 99999999)}",
                    course_code=course['code'],
                    course_name=course['name'],
                    aqf_level=course['aqf'],
                    intended_start_date=timezone.now().date() + timedelta(days=random.randint(14, 180)),
                    jurisdiction=requirement.jurisdiction,
                    jurisdiction_requirement=requirement,
                    funding_program_code=requirement.code,
                    student_data=student_data,
                    status=status,
                    is_eligible=is_eligible,
                    eligibility_percentage=eligibility_percentage,
                    rules_checked=rules_checked,
                    rules_passed=rules_passed,
                    rules_failed=rules_failed,
                    check_results={
                        'citizenship_check': 'passed' if citizenship in ['australian_citizen', 'permanent_resident'] else 'failed',
                        'age_check': 'passed' if requirement.min_age <= age <= (requirement.max_age or 100) else 'failed',
                        'residency_check': 'passed' if student_data['jurisdiction_resident'] == 'true' else 'failed',
                        'education_check': 'passed',
                    },
                    failed_rules=failed_rules_list,
                    warnings=[
                        'Documentation required within 14 days',
                        'Proof of residency must be current (within 3 months)',
                    ] if random.random() < 0.5 else [],
                    api_verified=random.choice([True, False]),
                    api_response={'status': 'verified', 'confidence': random.uniform(0.85, 0.99)} if random.random() < 0.6 else {},
                    api_verified_at=timezone.now() if random.random() < 0.6 else None,
                    override_required=(status == 'override'),
                    override_approved=(status == 'override' and random.random() < 0.7),
                    override_reason='Special circumstances - student demonstrates exceptional commitment' if status == 'override' else '',
                    override_approved_by=random.choice(users) if status == 'override' and random.random() < 0.7 else None,
                    override_approved_at=timezone.now() if status == 'override' and random.random() < 0.7 else None,
                    prevents_enrollment=not is_eligible,
                    compliance_notes=f"Checked against {requirement.name} requirements" if random.random() < 0.7 else '',
                    valid_until=timezone.now().date() + timedelta(days=random.randint(90, 365)) if is_eligible else None,
                    checked_by=random.choice(users),
                )
                checks.append(check)
        
        return checks
    
    def create_eligibility_check_logs(self, checks, users):
        """Create eligibility check audit logs"""
        logs = []
        
        for check in checks:
            # Always create check_created log
            log = EligibilityCheckLog.objects.create(
                eligibility_check=check,
                action='check_created',
                details={
                    'student': f"{check.student_first_name} {check.student_last_name}",
                    'course': check.course_name,
                    'jurisdiction': check.get_jurisdiction_display(),
                },
                notes=f"Eligibility check initiated for {check.course_name}",
                performed_by=check.checked_by,
                performed_at=check.checked_at,
            )
            logs.append(log)
            
            # Create rule_evaluated logs for each rule checked
            for i in range(min(check.rules_checked, 5)):  # Log first 5 rules
                log = EligibilityCheckLog.objects.create(
                    eligibility_check=check,
                    action='rule_evaluated',
                    details={
                        'rule_number': i + 1,
                        'result': 'passed' if i < check.rules_passed else 'failed',
                        'evaluation_time': random.uniform(0.1, 0.5),
                    },
                    notes=f"Rule {i + 1} evaluation completed",
                    performed_by=check.checked_by,
                    performed_at=check.checked_at + timedelta(seconds=i * 2),
                )
                logs.append(log)
            
            # API call log if verified
            if check.api_verified:
                log = EligibilityCheckLog.objects.create(
                    eligibility_check=check,
                    action='api_called',
                    details={
                        'endpoint': check.jurisdiction_requirement.api_endpoint if check.jurisdiction_requirement else None,
                        'response_code': 200,
                        'verification_result': 'verified',
                    },
                    notes='External API verification completed successfully',
                    performed_by=check.checked_by,
                    performed_at=check.api_verified_at or check.checked_at + timedelta(minutes=2),
                )
                logs.append(log)
            
            # Status change log
            log = EligibilityCheckLog.objects.create(
                eligibility_check=check,
                action='status_changed',
                details={
                    'old_status': 'pending',
                    'new_status': check.status,
                    'eligibility_percentage': float(check.eligibility_percentage),
                },
                notes=f"Status updated to {check.get_status_display()}",
                performed_by=check.checked_by,
                performed_at=check.checked_at + timedelta(minutes=5),
            )
            logs.append(log)
            
            # Override logs if applicable
            if check.override_required:
                log = EligibilityCheckLog.objects.create(
                    eligibility_check=check,
                    action='override_requested',
                    details={
                        'reason': check.override_reason,
                        'failed_rules': len(check.failed_rules),
                    },
                    notes='Manual override requested due to failed eligibility requirements',
                    performed_by=check.checked_by,
                    performed_at=check.checked_at + timedelta(hours=1),
                )
                logs.append(log)
                
                if check.override_approved:
                    log = EligibilityCheckLog.objects.create(
                        eligibility_check=check,
                        action='override_approved',
                        details={
                            'approver': check.override_approved_by.get_full_name() if check.override_approved_by else 'Unknown',
                            'reason': check.override_reason,
                        },
                        notes='Override approved by authorized personnel',
                        performed_by=check.override_approved_by,
                        performed_at=check.override_approved_at or check.checked_at + timedelta(hours=2),
                    )
                    logs.append(log)
                elif random.random() < 0.3:  # 30% chance of rejection
                    log = EligibilityCheckLog.objects.create(
                        eligibility_check=check,
                        action='override_rejected',
                        details={
                            'reason': 'Does not meet minimum program requirements',
                        },
                        notes='Override request rejected - student does not qualify',
                        performed_by=random.choice(users),
                        performed_at=check.checked_at + timedelta(hours=3),
                    )
                    logs.append(log)
        
        return logs
    
    def create_trainer_profiles(self, tenants, users):
        """Create trainer profiles for industry currency verification"""
        profiles = []
        
        trainer_names = [
            'Sarah Chen', 'Michael O\'Brien', 'Emma Thompson', 'David Kumar', 
            'Rachel Green', 'James Wilson', 'Lisa Anderson', 'Peter Martinez',
            'Sophie Zhang', 'Daniel Brown', 'Jessica Lee', 'Thomas Wright'
        ]
        
        industries = [
            'Information Technology',
            'Business Management',
            'Healthcare',
            'Hospitality',
            'Construction',
            'Automotive',
            'Education & Training',
            'Community Services',
        ]
        
        specializations_by_industry = {
            'Information Technology': [
                ['Python Programming', 'Web Development', 'Cloud Computing'],
                ['Cybersecurity', 'Network Administration', 'DevOps'],
                ['Mobile Development', 'React', 'Node.js'],
                ['Data Science', 'Machine Learning', 'AI'],
            ],
            'Business Management': [
                ['Project Management', 'Agile', 'Scrum'],
                ['Leadership', 'Change Management', 'Strategic Planning'],
                ['Financial Management', 'Accounting', 'Budgeting'],
                ['Marketing', 'Digital Marketing', 'Social Media'],
            ],
            'Healthcare': [
                ['Nursing', 'Patient Care', 'Clinical Practice'],
                ['Allied Health', 'Aged Care', 'Disability Support'],
                ['Mental Health', 'Counseling', 'Wellbeing'],
            ],
            'Hospitality': [
                ['Commercial Cookery', 'Culinary Arts', 'Food Safety'],
                ['Hotel Management', 'Customer Service', 'Front Office'],
                ['Events Management', 'Tourism', 'Travel'],
            ],
        }
        
        for tenant in tenants:
            # Create 3-5 trainer profiles per tenant
            for i in range(random.randint(3, 5)):
                name = random.choice(trainer_names)
                trainer_id = f"TRAIN{random.randint(1000, 9999)}"
                industry = random.choice(industries)
                
                # Get specializations for this industry
                if industry in specializations_by_industry:
                    specializations = random.choice(specializations_by_industry[industry])
                else:
                    specializations = ['Training', 'Assessment', 'Compliance']
                
                # Determine currency status based on last verification
                last_verified = timezone.now().date() - timedelta(days=random.randint(0, 200))
                days_since_verification = (timezone.now().date() - last_verified).days
                
                if days_since_verification < 60:
                    status = 'current'
                    score = random.uniform(75, 95)
                elif days_since_verification < 90:
                    status = 'expiring_soon'
                    score = random.uniform(60, 80)
                elif days_since_verification < 150:
                    status = 'expired'
                    score = random.uniform(40, 65)
                else:
                    status = 'not_verified'
                    score = 0
                
                # Clean name for URLs
                clean_name = name.lower().replace(' ', '').replace("'", '')
                clean_name_dash = name.lower().replace(' ', '-').replace("'", '')
                clean_name_dot = name.lower().replace(' ', '.').replace("'", '')
                
                profile = TrainerProfile.objects.create(
                    tenant=str(tenant.id),
                    trainer_id=trainer_id,
                    trainer_name=name,
                    email=f"{clean_name_dot}@example.com",
                    linkedin_url=f"https://linkedin.com/in/{clean_name_dash}",
                    github_url=f"https://github.com/{clean_name}" if industry == 'Information Technology' else '',
                    twitter_url=f"https://twitter.com/{clean_name}" if random.random() < 0.4 else '',
                    personal_website=f"https://{clean_name}.dev" if random.random() < 0.3 else '',
                    primary_industry=industry,
                    specializations=specializations,
                    years_experience=random.randint(3, 25),
                    last_verified_date=last_verified if status != 'not_verified' else None,
                    currency_status=status,
                    currency_score=score,
                    auto_verify_enabled=random.choice([True, True, True, False]),  # 75% enabled
                    verification_frequency_days=random.choice([30, 60, 90, 180]),
                    next_verification_date=timezone.now().date() + timedelta(days=random.randint(1, 90)) if status == 'current' else None,
                )
                profiles.append(profile)
        
        return profiles
    
    def create_verification_scans(self, profiles):
        """Create verification scans for trainer profiles"""
        scans = []
        
        for profile in profiles:
            # Create 1-3 scans per profile
            num_scans = random.randint(1, 3)
            
            for i in range(num_scans):
                scan_type = random.choice(['manual', 'scheduled', 'automatic'])
                
                # Determine sources to scan based on profile
                sources = ['linkedin']
                if profile.github_url:
                    sources.append('github')
                if profile.twitter_url:
                    sources.append('twitter')
                
                # Determine status (most recent scan more likely to be completed)
                if i == 0:  # Most recent scan
                    status = random.choice(['completed', 'completed', 'completed', 'scanning', 'analyzing'])
                else:
                    status = 'completed'
                
                # Calculate scan metrics
                if status == 'completed':
                    total_items = random.randint(15, 80)
                    relevant_items = int(total_items * random.uniform(0.4, 0.8))
                    currency_score = random.uniform(50, 95)
                    scan_duration = random.uniform(30, 180)
                    
                    started_at = timezone.now() - timedelta(days=random.randint(1, 90), hours=random.randint(0, 23))
                    completed_at = started_at + timedelta(seconds=scan_duration)
                else:
                    total_items = 0
                    relevant_items = 0
                    currency_score = 0
                    scan_duration = None
                    started_at = timezone.now() - timedelta(minutes=random.randint(1, 30))
                    completed_at = None
                
                scan = VerificationScan.objects.create(
                    trainer_profile=profile,
                    scan_type=scan_type,
                    sources_to_scan=sources,
                    scan_status=status,
                    total_items_found=total_items,
                    relevant_items_count=relevant_items,
                    currency_score=currency_score,
                    scan_duration_seconds=scan_duration,
                    error_message='',
                    started_at=started_at,
                    completed_at=completed_at,
                )
                scans.append(scan)
        
        return scans
    
    def create_linkedin_activities(self, scans):
        """Create LinkedIn activities extracted from scans"""
        activities = []
        
        activity_types_data = {
            'post': {
                'titles': [
                    'Excited to share our latest project success',
                    'Key learnings from implementing Agile methodology',
                    'Best practices for cloud security in 2025',
                    'How we improved student engagement by 40%',
                    'Thoughts on the future of vocational education',
                ],
                'technologies': ['Azure', 'AWS', 'Docker', 'Kubernetes', 'React', 'Python', 'Node.js'],
                'skills': ['Leadership', 'Project Management', 'Training Design', 'Cloud Computing', 'DevOps'],
            },
            'certification': {
                'titles': [
                    'AWS Certified Solutions Architect - Associate',
                    'Certified Scrum Master (CSM)',
                    'TAE40116 Certificate IV in Training and Assessment',
                    'Microsoft Certified: Azure Fundamentals',
                    'Project Management Professional (PMP)',
                ],
                'technologies': ['AWS', 'Azure', 'Cloud Computing', 'Kubernetes'],
                'skills': ['Cloud Architecture', 'Agile', 'Training & Assessment', 'Project Management'],
            },
            'course': {
                'titles': [
                    'Completed: Advanced Machine Learning Specialization',
                    'Finished: Full Stack Web Development Bootcamp',
                    'Completed: Leadership in Education',
                    'Finished: Cybersecurity Fundamentals',
                ],
                'technologies': ['Python', 'TensorFlow', 'React', 'Docker', 'Security'],
                'skills': ['Machine Learning', 'Web Development', 'Leadership', 'Cybersecurity'],
            },
            'position': {
                'titles': [
                    'Senior Trainer - Information Technology',
                    'Lead Assessor - Business Management',
                    'Industry Curriculum Developer',
                    'VET Training Coordinator',
                ],
                'technologies': [],
                'skills': ['Training Delivery', 'Assessment', 'Curriculum Development', 'Leadership'],
            },
        }
        
        completed_scans = [s for s in scans if s.scan_status == 'completed' and 'linkedin' in s.sources_to_scan]
        
        for scan in completed_scans:
            # Create 5-15 LinkedIn activities per completed scan
            num_activities = random.randint(5, 15)
            
            for _ in range(num_activities):
                activity_type = random.choice(['post', 'certification', 'course', 'position', 'skill_endorsement'])
                
                if activity_type in activity_types_data:
                    type_data = activity_types_data[activity_type]
                    title = random.choice(type_data['titles'])
                    technologies = random.sample(type_data['technologies'], k=min(random.randint(1, 3), len(type_data['technologies']))) if type_data['technologies'] else []
                    skills = random.sample(type_data['skills'], k=min(random.randint(1, 3), len(type_data['skills'])))
                else:
                    title = 'Skill endorsement received'
                    technologies = []
                    skills = random.sample(['Training', 'Assessment', 'Leadership'], k=2)
                
                activity_date = timezone.now().date() - timedelta(days=random.randint(1, 365))
                
                # Determine relevance
                is_relevant = random.random() < 0.7  # 70% relevant
                relevance_score = random.uniform(0.6, 0.95) if is_relevant else random.uniform(0.2, 0.5)
                
                activity = LinkedInActivity.objects.create(
                    verification_scan=scan,
                    activity_type=activity_type,
                    title=title,
                    description=f"Details about {title.lower()}. Demonstrates industry engagement and professional development.",
                    url=f"https://linkedin.com/posts/activity-{random.randint(100000, 999999)}",
                    activity_date=activity_date,
                    date_text=activity_date.strftime('%B %Y'),
                    skills_mentioned=skills,
                    technologies=technologies,
                    companies=random.sample(['Microsoft', 'AWS', 'Google', 'Training Org', 'RTO'], k=random.randint(0, 2)),
                    keywords=skills + technologies,
                    relevance_score=relevance_score,
                    is_industry_relevant=is_relevant,
                    relevance_reasoning=f"Activity demonstrates current industry practice in {', '.join(skills[:2])}" if is_relevant else "Limited relevance to current teaching role",
                    raw_data={'source': 'linkedin', 'type': activity_type},
                )
                activities.append(activity)
        
        return activities
    
    def create_github_activities(self, scans):
        """Create GitHub activities extracted from scans"""
        activities = []
        
        repo_data = [
            {
                'name': 'python-web-scraper',
                'description': 'Web scraping tool for educational data analysis',
                'language': 'Python',
                'languages': ['Python', 'HTML', 'CSS'],
                'topics': ['web-scraping', 'data-analysis', 'education'],
                'technologies': ['Python', 'BeautifulSoup', 'Pandas'],
            },
            {
                'name': 'react-learning-platform',
                'description': 'Interactive learning platform built with React',
                'language': 'JavaScript',
                'languages': ['JavaScript', 'TypeScript', 'CSS'],
                'topics': ['react', 'education', 'learning-platform'],
                'technologies': ['React', 'Node.js', 'Express', 'MongoDB'],
            },
            {
                'name': 'docker-training-environments',
                'description': 'Docker configurations for training environments',
                'language': 'Dockerfile',
                'languages': ['Dockerfile', 'Shell'],
                'topics': ['docker', 'devops', 'training'],
                'technologies': ['Docker', 'Kubernetes', 'Linux'],
            },
            {
                'name': 'assessment-automation',
                'description': 'Automated assessment marking tools',
                'language': 'Python',
                'languages': ['Python', 'JavaScript'],
                'topics': ['education', 'automation', 'assessment'],
                'technologies': ['Python', 'NLP', 'Machine Learning'],
            },
        ]
        
        completed_scans = [s for s in scans if s.scan_status == 'completed' and 'github' in s.sources_to_scan]
        
        for scan in completed_scans:
            # Create 3-10 GitHub activities per completed scan
            num_activities = random.randint(3, 10)
            
            for _ in range(num_activities):
                activity_type = random.choice(['repository', 'commit', 'pull_request', 'contribution'])
                repo = random.choice(repo_data)
                
                activity_date = timezone.now().date() - timedelta(days=random.randint(1, 365))
                last_updated = activity_date + timedelta(days=random.randint(0, 30))
                
                # Determine relevance
                is_relevant = random.random() < 0.75  # 75% relevant
                relevance_score = random.uniform(0.65, 0.95) if is_relevant else random.uniform(0.25, 0.55)
                
                activity = GitHubActivity.objects.create(
                    verification_scan=scan,
                    activity_type=activity_type,
                    repository_name=repo['name'],
                    title=f"{activity_type.title()} in {repo['name']}",
                    description=repo['description'],
                    url=f"https://github.com/trainer/{repo['name']}",
                    activity_date=activity_date,
                    last_updated=last_updated,
                    language=repo['language'],
                    languages_used=repo['languages'],
                    topics=repo['topics'],
                    stars=random.randint(0, 50),
                    forks=random.randint(0, 15),
                    technologies=repo['technologies'],
                    frameworks=random.sample(['React', 'Django', 'Flask', 'Express', 'Docker'], k=random.randint(1, 3)),
                    keywords=repo['topics'] + repo['technologies'],
                    relevance_score=relevance_score,
                    is_industry_relevant=is_relevant,
                    relevance_reasoning=f"Demonstrates current industry practice with {repo['language']} and {', '.join(repo['technologies'][:2])}" if is_relevant else "Personal project with limited teaching relevance",
                    commits_count=random.randint(5, 200),
                    contributions_count=random.randint(1, 50),
                    raw_data={'source': 'github', 'repository': repo['name']},
                )
                activities.append(activity)
        
        return activities
    
    def create_entity_extractions(self, scans):
        """Create NLP entity extraction results"""
        extractions = []
        
        sample_texts = {
            'linkedin': [
                "Recently completed AWS Solutions Architect certification. Excited to bring cloud computing expertise to our students. Working with Docker and Kubernetes daily.",
                "Led a workshop on React and Node.js for 30 industry professionals. Topics covered: modern web development, microservices, and CI/CD pipelines.",
                "Thrilled to join Microsoft's educator program. Looking forward to integrating Azure services into our curriculum. #CloudComputing #Education",
            ],
            'github': [
                "Implemented automated testing using pytest and GitHub Actions. Repository demonstrates best practices for Python development and CI/CD.",
                "Created learning platform using React, Express, and MongoDB. Features include real-time collaboration and automated assessment.",
                "Docker-based training environment for teaching DevOps. Includes Kubernetes examples and infrastructure as code with Terraform.",
            ],
        }
        
        entity_patterns = {
            'linkedin': {
                'TECH': ['AWS', 'Docker', 'Kubernetes', 'React', 'Node.js', 'Azure', 'Python', 'CI/CD'],
                'SKILL': ['Cloud Computing', 'Web Development', 'Microservices', 'DevOps', 'Teaching'],
                'ORG': ['Microsoft', 'AWS', 'GitHub'],
                'CERT': ['Solutions Architect', 'Educator Program'],
            },
            'github': {
                'TECH': ['pytest', 'GitHub Actions', 'Python', 'React', 'Express', 'MongoDB', 'Docker', 'Kubernetes', 'Terraform'],
                'SKILL': ['Automated Testing', 'CI/CD', 'Web Development', 'DevOps', 'Infrastructure as Code'],
                'LANGUAGE': ['Python', 'JavaScript', 'TypeScript'],
            },
        }
        
        completed_scans = [s for s in scans if s.scan_status == 'completed']
        
        for scan in completed_scans:
            # Create 2-4 entity extractions per scan (one per source)
            for source in scan.sources_to_scan[:2]:  # Limit to first 2 sources
                source_type = source
                text = random.choice(sample_texts.get(source_type, sample_texts['linkedin']))
                patterns = entity_patterns.get(source_type, entity_patterns['linkedin'])
                
                # Build entities dict
                entities = {}
                entity_count = 0
                
                for entity_type, entity_list in patterns.items():
                    # Select 2-4 entities of each type
                    selected = random.sample(entity_list, k=min(random.randint(2, 4), len(entity_list)))
                    entities[entity_type] = selected
                    entity_count += len(selected)
                
                extraction = EntityExtraction.objects.create(
                    verification_scan=scan,
                    source_type=source_type,
                    source_url=f"https://{source_type}.com/trainer/profile",
                    source_text=text,
                    entities=entities,
                    extraction_confidence=random.uniform(0.75, 0.95),
                    entity_count=entity_count,
                    nlp_model_used='spacy-en_core_web_lg',
                    processing_time_ms=random.uniform(50, 500),
                )
                extractions.append(extraction)
        
        return extractions
    
    def create_currency_evidence(self, profiles, scans, linkedin_activities, github_activities):
        """Create currency evidence documents"""
        evidence_docs = []
        
        for profile in profiles:
            # Get scans for this profile
            profile_scans = [s for s in scans if s.trainer_profile_id == profile.id and s.scan_status == 'completed']
            
            if not profile_scans:
                continue
            
            # Use most recent scan
            recent_scan = profile_scans[0]
            
            # Get activities for this scan
            scan_linkedin = [a for a in linkedin_activities if a.verification_scan_id == recent_scan.id]
            scan_github = [a for a in github_activities if a.verification_scan_id == recent_scan.id]
            
            # Create 1-3 evidence documents per profile
            evidence_types = ['combined_report', 'linkedin_summary', 'github_summary', 'skills_matrix']
            
            for evidence_type in random.sample(evidence_types, k=random.randint(1, 3)):
                if evidence_type == 'linkedin_summary' and not scan_linkedin:
                    continue
                if evidence_type == 'github_summary' and not scan_github:
                    continue
                
                # Calculate metrics
                if evidence_type == 'linkedin_summary':
                    activities = scan_linkedin
                    relevant = [a for a in activities if a.is_industry_relevant]
                    title = f"LinkedIn Industry Currency Summary - {profile.trainer_name}"
                elif evidence_type == 'github_summary':
                    activities = scan_github
                    relevant = [a for a in activities if a.is_industry_relevant]
                    title = f"GitHub Industry Currency Summary - {profile.trainer_name}"
                elif evidence_type == 'combined_report':
                    activities = scan_linkedin + scan_github
                    relevant = [a for a in scan_linkedin if a.is_industry_relevant] + [a for a in scan_github if a.is_industry_relevant]
                    title = f"Industry Currency Report - {profile.trainer_name}"
                else:  # skills_matrix
                    activities = scan_linkedin + scan_github
                    relevant = activities
                    title = f"Skills and Technology Matrix - {profile.trainer_name}"
                
                total_count = len(activities)
                relevant_count = len(relevant)
                
                # Generate content
                content = f"""# {title}
                
**Profile:** {profile.profile_number}  
**Industry:** {profile.primary_industry}  
**Specializations:** {', '.join(profile.specializations)}  
**Verification Period:** {recent_scan.started_at.strftime('%Y-%m-%d')} to {recent_scan.completed_at.strftime('%Y-%m-%d') if recent_scan.completed_at else 'In Progress'}

## Summary

Total Activities Found: {total_count}  
Industry Relevant Activities: {relevant_count}  
Currency Score: {recent_scan.currency_score:.1f}/100

## Key Findings

- Active engagement in professional development
- Current with industry technologies and practices
- Demonstrates ongoing learning and skill development

## Evidence of Currency

"""
                
                # Add activity samples
                for i, activity in enumerate(relevant[:5], 1):
                    if hasattr(activity, 'title'):
                        content += f"{i}. **{activity.title}** ({activity.activity_date.strftime('%B %Y')})\n"
                        if hasattr(activity, 'technologies') and activity.technologies:
                            content += f"   Technologies: {', '.join(activity.technologies)}\n"
                    
                content += "\n## Conclusion\n\nTrainer demonstrates current industry currency through active engagement with modern technologies and practices."
                
                # Determine date range
                if activities:
                    dates = [a.activity_date for a in activities if a.activity_date]
                    if dates:
                        start_date = min(dates)
                        end_date = max(dates)
                    else:
                        start_date = timezone.now().date() - timedelta(days=365)
                        end_date = timezone.now().date()
                else:
                    start_date = timezone.now().date() - timedelta(days=365)
                    end_date = timezone.now().date()
                
                evidence = CurrencyEvidence.objects.create(
                    trainer_profile=profile,
                    verification_scan=recent_scan,
                    evidence_type=evidence_type,
                    title=title,
                    content=content,
                    evidence_start_date=start_date,
                    evidence_end_date=end_date,
                    total_activities=total_count,
                    relevant_activities=relevant_count,
                    currency_score=recent_scan.currency_score,
                    linkedin_activities_included=[str(a.id) for a in scan_linkedin[:10]],
                    github_activities_included=[str(a.id) for a in scan_github[:10]],
                    file_format=random.choice(['markdown', 'html', 'pdf']),
                    file_path=f"/evidence/{profile.profile_number}/{evidence_type}_{timezone.now().strftime('%Y%m%d')}.md",
                    file_size_kb=random.uniform(5, 50),
                    meets_rto_standards=recent_scan.currency_score >= 70,
                    compliance_notes="Meets ASQA requirements for industry currency" if recent_scan.currency_score >= 70 else "Additional evidence may be required",
                    is_approved=random.choice([True, True, False]),  # 67% approved
                    approved_by=f"Quality Manager" if random.random() < 0.67 else '',
                    approved_at=timezone.now() if random.random() < 0.67 else None,
                )
                evidence_docs.append(evidence)
        
        return evidence_docs
    
    def create_integrations(self, tenants, users):
        """Create third-party integrations"""
        integrations = []
        
        integration_configs = {
            'axcelerate': {
                'name': 'Axcelerate SMS',
                'description': 'Student Management System integration for syncing student records, enrolments, and outcomes',
                'config': {
                    'sync_students': True,
                    'sync_courses': True,
                    'sync_enrolments': True,
                    'sync_outcomes': True,
                    'sync_direction': 'bidirectional',
                },
                'api_base_url': 'https://api.axcelerate.com.au/v1',
                'sync_interval': 30,
            },
            'canvas': {
                'name': 'Canvas LMS',
                'description': 'Learning Management System for course delivery and assessment',
                'config': {
                    'sync_courses': True,
                    'sync_assignments': True,
                    'sync_grades': True,
                    'auto_create_courses': True,
                    'lti_enabled': True,
                },
                'api_base_url': 'https://canvas.instructure.com/api/v1',
                'sync_interval': 60,
            },
            'xero': {
                'name': 'Xero Accounting',
                'description': 'Accounting integration for invoicing and financial reporting',
                'config': {
                    'sync_invoices': True,
                    'sync_payments': True,
                    'auto_invoice': True,
                    'invoice_template': 'default',
                    'tax_type': 'GST',
                },
                'api_base_url': 'https://api.xero.com/api.xro/2.0',
                'sync_interval': 120,
            },
            'moodle': {
                'name': 'Moodle LMS',
                'description': 'Open-source Learning Management System integration',
                'config': {
                    'sync_users': True,
                    'sync_courses': True,
                    'sync_enrolments': True,
                    'web_services_enabled': True,
                },
                'api_base_url': 'https://moodle.example.com/webservice/rest/server.php',
                'sync_interval': 60,
            },
            'vettrak': {
                'name': 'VETtrak SMS',
                'description': 'VET Student Management System by ReadyTech',
                'config': {
                    'sync_students': True,
                    'sync_qualifications': True,
                    'sync_units': True,
                    'avetmiss_reporting': True,
                },
                'api_base_url': 'https://api.vettrak.com.au/v2',
                'sync_interval': 45,
            },
            'stripe': {
                'name': 'Stripe Payments',
                'description': 'Payment gateway for course fees and student payments',
                'config': {
                    'mode': 'live',
                    'currency': 'AUD',
                    'auto_capture': True,
                    'webhook_events': ['payment_intent.succeeded', 'payment_intent.failed'],
                },
                'api_base_url': 'https://api.stripe.com/v1',
                'sync_interval': 0,  # Event-driven
            },
        }
        
        for tenant in tenants:
            # Each tenant gets 2-4 integrations
            selected_integrations = random.sample(list(integration_configs.keys()), k=random.randint(2, 4))
            
            for integration_type in selected_integrations:
                config_data = integration_configs[integration_type]
                
                # Determine status - most active, some pending/error
                status_options = ['active', 'active', 'active', 'pending', 'error']
                status = random.choice(status_options)
                
                # Generate OAuth tokens for some integrations
                has_oauth = integration_type in ['canvas', 'xero']
                
                if has_oauth and status == 'active':
                    access_token = f"tok_{random.randint(10**20, 10**21)}"
                    refresh_token = f"ref_{random.randint(10**20, 10**21)}"
                    token_expires_at = timezone.now() + timedelta(days=random.randint(1, 60))
                else:
                    access_token = ''
                    refresh_token = ''
                    token_expires_at = None
                
                # API key for non-OAuth integrations
                api_key = f"sk_{integration_type}_{random.randint(10**15, 10**16)}" if not has_oauth else ''
                
                # Last sync details
                if status == 'active':
                    last_sync_at = timezone.now() - timedelta(minutes=random.randint(10, 180))
                    last_sync_status = random.choice(['success', 'success', 'success', 'warning'])
                    last_sync_error = 'Some items could not be synced' if last_sync_status == 'warning' else ''
                elif status == 'error':
                    last_sync_at = timezone.now() - timedelta(hours=random.randint(1, 48))
                    last_sync_status = 'error'
                    last_sync_error = random.choice([
                        'Authentication failed - invalid credentials',
                        'API rate limit exceeded',
                        'Connection timeout',
                        'Invalid response from external API',
                    ])
                else:
                    last_sync_at = None
                    last_sync_status = ''
                    last_sync_error = ''
                
                integration = Integration.objects.create(
                    tenant=tenant,
                    integration_type=integration_type,
                    name=config_data['name'],
                    description=config_data['description'],
                    status=status,
                    config=config_data['config'],
                    client_id=f"client_{integration_type}_{random.randint(1000, 9999)}" if has_oauth else '',
                    client_secret=f"secret_{random.randint(10**20, 10**21)}" if has_oauth else '',
                    access_token=access_token,
                    refresh_token=refresh_token,
                    token_expires_at=token_expires_at,
                    api_base_url=config_data['api_base_url'],
                    api_key=api_key,
                    webhook_url=f"https://nextcore.example.com/webhooks/{integration_type}/{tenant.id}" if integration_type in ['stripe', 'xero'] else '',
                    webhook_secret=f"whsec_{random.randint(10**20, 10**21)}" if integration_type in ['stripe', 'xero'] else '',
                    auto_sync_enabled=(status == 'active' and config_data['sync_interval'] > 0),
                    sync_interval_minutes=config_data['sync_interval'],
                    last_sync_at=last_sync_at,
                    last_sync_status=last_sync_status,
                    last_sync_error=last_sync_error,
                    created_by=random.choice(users).username,
                )
                integrations.append(integration)
        
        return integrations
    
    def create_integration_logs(self, integrations):
        """Create integration activity logs"""
        logs = []
        
        log_messages = {
            'connect': [
                'Successfully connected to {integration}',
                'Integration configured and authenticated',
                'Initial connection established',
            ],
            'disconnect': [
                'Integration disconnected by user',
                'Connection removed',
                'Integration deactivated',
            ],
            'sync': [
                'Synchronization completed successfully',
                'Synced {count} records from {integration}',
                'Data sync finished with no errors',
                'Partial sync completed - {count} items processed',
            ],
            'error': [
                'Authentication failed - please check credentials',
                'API rate limit exceeded - retry after cooldown',
                'Connection timeout - remote server not responding',
                'Invalid API response received',
                'Sync failed due to data validation errors',
            ],
            'config_update': [
                'Integration configuration updated',
                'Sync settings modified',
                'Field mappings reconfigured',
            ],
            'webhook': [
                'Webhook received and processed',
                'Event notification handled: {event}',
                'Incoming webhook validated',
            ],
        }
        
        for integration in integrations:
            # Create connection log
            log = IntegrationLog.objects.create(
                integration=integration,
                action='connect',
                status='success',
                message=random.choice(log_messages['connect']).format(integration=integration.name),
                details={
                    'integration_type': integration.integration_type,
                    'configured_by': integration.created_by,
                },
                created_at=integration.created_at,
            )
            logs.append(log)
            
            # Create 3-8 sync logs for active integrations
            if integration.status == 'active' and integration.last_sync_at:
                num_syncs = random.randint(3, 8)
                
                for i in range(num_syncs):
                    # Calculate sync time going backwards
                    hours_ago = random.randint(i * 2, (i + 1) * 6)
                    sync_time = timezone.now() - timedelta(hours=hours_ago)
                    
                    # Most syncs successful, occasional warnings
                    sync_status = random.choice(['success', 'success', 'success', 'success', 'warning'])
                    
                    if sync_status == 'success':
                        record_count = random.randint(10, 500)
                        message = random.choice(log_messages['sync']).format(
                            integration=integration.name,
                            count=record_count
                        )
                        details = {
                            'records_processed': record_count,
                            'records_created': random.randint(0, record_count // 3),
                            'records_updated': random.randint(0, record_count // 2),
                            'duration_seconds': random.uniform(5, 60),
                        }
                    else:
                        record_count = random.randint(10, 200)
                        failed_count = random.randint(1, 10)
                        message = f"Sync completed with warnings - {failed_count} items failed"
                        details = {
                            'records_processed': record_count,
                            'records_failed': failed_count,
                            'warning_messages': ['Data validation failed for some records'],
                        }
                    
                    log = IntegrationLog.objects.create(
                        integration=integration,
                        action='sync',
                        status=sync_status,
                        message=message,
                        details=details,
                        request_data={'sync_type': 'scheduled', 'entities': list(integration.config.keys())[:3]},
                        response_data={'success': True, 'records': record_count},
                        created_at=sync_time,
                    )
                    logs.append(log)
            
            # Create error logs for integrations with errors
            if integration.status == 'error':
                error_time = integration.last_sync_at or (timezone.now() - timedelta(hours=random.randint(1, 24)))
                
                log = IntegrationLog.objects.create(
                    integration=integration,
                    action='error',
                    status='error',
                    message=integration.last_sync_error or random.choice(log_messages['error']),
                    details={
                        'error_code': random.choice(['AUTH_ERROR', 'RATE_LIMIT', 'TIMEOUT', 'INVALID_RESPONSE']),
                        'retry_count': random.randint(1, 3),
                    },
                    request_data={'endpoint': integration.api_base_url},
                    response_data={'error': integration.last_sync_error},
                    created_at=error_time,
                )
                logs.append(log)
            
            # Create 1-2 config update logs
            for _ in range(random.randint(1, 2)):
                update_time = integration.created_at + timedelta(days=random.randint(1, 30))
                
                log = IntegrationLog.objects.create(
                    integration=integration,
                    action='config_update',
                    status='success',
                    message=random.choice(log_messages['config_update']),
                    details={
                        'updated_fields': random.sample(['sync_interval', 'auto_sync_enabled', 'config'], k=random.randint(1, 2)),
                        'updated_by': integration.created_by,
                    },
                    created_at=update_time,
                )
                logs.append(log)
            
            # Create webhook logs for integrations that support webhooks
            if integration.webhook_url:
                for _ in range(random.randint(2, 5)):
                    webhook_time = timezone.now() - timedelta(hours=random.randint(1, 72))
                    
                    events = {
                        'stripe': ['payment_intent.succeeded', 'payment_intent.failed', 'charge.succeeded'],
                        'xero': ['invoice.created', 'payment.received', 'contact.updated'],
                    }
                    
                    event_type = random.choice(events.get(integration.integration_type, ['event.received']))
                    
                    log = IntegrationLog.objects.create(
                        integration=integration,
                        action='webhook',
                        status='success',
                        message=random.choice(log_messages['webhook']).format(event=event_type),
                        details={
                            'event_type': event_type,
                            'webhook_id': f"wh_{random.randint(10**10, 10**11)}",
                        },
                        request_data={
                            'event': event_type,
                            'data': {'id': f"obj_{random.randint(10**10, 10**11)}"},
                        },
                        created_at=webhook_time,
                    )
                    logs.append(log)
        
        return logs
    
    def create_integration_mappings(self, integrations):
        """Create field mappings between systems"""
        mappings = []
        
        # Define mapping templates for different integration types
        mapping_templates = {
            'axcelerate': [
                {'source_entity': 'user', 'source_field': 'email', 'target_entity': 'contact', 'target_field': 'EmailAddress', 'bidirectional': True},
                {'source_entity': 'user', 'source_field': 'first_name', 'target_entity': 'contact', 'target_field': 'GivenName', 'bidirectional': True},
                {'source_entity': 'user', 'source_field': 'last_name', 'target_entity': 'contact', 'target_field': 'FamilyName', 'bidirectional': True},
                {'source_entity': 'course', 'source_field': 'code', 'target_entity': 'qualification', 'target_field': 'Code', 'bidirectional': False},
                {'source_entity': 'enrolment', 'source_field': 'status', 'target_entity': 'enrolment', 'target_field': 'Status', 'bidirectional': True},
            ],
            'canvas': [
                {'source_entity': 'user', 'source_field': 'email', 'target_entity': 'user', 'target_field': 'login_id', 'bidirectional': False},
                {'source_entity': 'user', 'source_field': 'full_name', 'target_entity': 'user', 'target_field': 'name', 'bidirectional': False},
                {'source_entity': 'course', 'source_field': 'title', 'target_entity': 'course', 'target_field': 'name', 'bidirectional': False},
                {'source_entity': 'assessment', 'source_field': 'title', 'target_entity': 'assignment', 'target_field': 'name', 'bidirectional': False},
                {'source_entity': 'assessment', 'source_field': 'due_date', 'target_entity': 'assignment', 'target_field': 'due_at', 'bidirectional': False},
            ],
            'xero': [
                {'source_entity': 'user', 'source_field': 'email', 'target_entity': 'contact', 'target_field': 'EmailAddress', 'bidirectional': False},
                {'source_entity': 'user', 'source_field': 'full_name', 'target_entity': 'contact', 'target_field': 'Name', 'bidirectional': False},
                {'source_entity': 'invoice', 'source_field': 'amount', 'target_entity': 'invoice', 'target_field': 'Total', 'bidirectional': False},
                {'source_entity': 'invoice', 'source_field': 'due_date', 'target_entity': 'invoice', 'target_field': 'DueDate', 'bidirectional': False},
                {'source_entity': 'invoice', 'source_field': 'status', 'target_entity': 'invoice', 'target_field': 'Status', 'bidirectional': True},
            ],
            'moodle': [
                {'source_entity': 'user', 'source_field': 'username', 'target_entity': 'user', 'target_field': 'username', 'bidirectional': False},
                {'source_entity': 'user', 'source_field': 'email', 'target_entity': 'user', 'target_field': 'email', 'bidirectional': False},
                {'source_entity': 'course', 'source_field': 'code', 'target_entity': 'course', 'target_field': 'shortname', 'bidirectional': False},
                {'source_entity': 'course', 'source_field': 'title', 'target_entity': 'course', 'target_field': 'fullname', 'bidirectional': False},
            ],
            'vettrak': [
                {'source_entity': 'user', 'source_field': 'student_id', 'target_entity': 'client', 'target_field': 'ClientID', 'bidirectional': True},
                {'source_entity': 'course', 'source_field': 'code', 'target_entity': 'qualification', 'target_field': 'QualCode', 'bidirectional': False},
                {'source_entity': 'unit', 'source_field': 'code', 'target_entity': 'unit', 'target_field': 'UnitCode', 'bidirectional': False},
                {'source_entity': 'outcome', 'source_field': 'result', 'target_entity': 'outcome', 'target_field': 'Result', 'bidirectional': True},
            ],
            'stripe': [
                {'source_entity': 'user', 'source_field': 'email', 'target_entity': 'customer', 'target_field': 'email', 'bidirectional': False},
                {'source_entity': 'invoice', 'source_field': 'amount', 'target_entity': 'payment_intent', 'target_field': 'amount', 'bidirectional': False},
                {'source_entity': 'payment', 'source_field': 'status', 'target_entity': 'payment_intent', 'target_field': 'status', 'bidirectional': True},
            ],
        }
        
        # Transform rules for common transformations
        transform_rules = [
            '',  # No transformation
            'value.upper()',  # Uppercase
            'value.strip()',  # Trim whitespace
            'datetime.strptime(value, "%Y-%m-%d").isoformat()',  # Date format conversion
            'float(value) * 100',  # Dollar to cents
            '"ACTIVE" if value == "enrolled" else "INACTIVE"',  # Status mapping
        ]
        
        for integration in integrations:
            # Get mapping template for this integration type
            template = mapping_templates.get(integration.integration_type, [])
            
            # Create 3-5 mappings per integration
            for mapping_data in random.sample(template, k=min(random.randint(3, 5), len(template))):
                mapping = IntegrationMapping.objects.create(
                    integration=integration,
                    source_entity=mapping_data['source_entity'],
                    source_field=mapping_data['source_field'],
                    target_entity=mapping_data['target_entity'],
                    target_field=mapping_data['target_field'],
                    transform_rule=random.choice(transform_rules),
                    is_bidirectional=mapping_data.get('bidirectional', False),
                )
                mappings.append(mapping)
        
        return mappings

    def create_intervention_rules(self, tenants):
        """Create intervention rules for automatic triggering"""
        rules = []
        
        # Rule templates
        rule_templates = [
            {
                'name': 'Low Attendance Alert',
                'description': 'Trigger intervention when student attendance drops below 75% over 2 weeks',
                'condition_type': 'attendance',
                'conditions': {
                    'metric': 'attendance_rate',
                    'operator': 'less_than',
                    'threshold': 75,
                    'period': 'last_2_weeks'
                },
                'intervention_type': 'attendance_followup',
                'priority_level': 'high',
                'assigned_to_role': 'Course Coordinator',
                'compliance_requirement': 'ASQA Standard 1.7 - Student support',
            },
            {
                'name': 'Failing Grades Pattern',
                'description': 'Trigger when student receives 3 or more failing grades',
                'condition_type': 'grade',
                'conditions': {
                    'metric': 'failing_assessments',
                    'operator': 'greater_than_or_equal',
                    'threshold': 3,
                    'period': 'last_4_weeks'
                },
                'intervention_type': 'academic_support',
                'priority_level': 'high',
                'assigned_to_role': 'Learning Support Officer',
                'compliance_requirement': 'ASQA Standard 1.5 - Assessment quality',
            },
            {
                'name': 'No LMS Activity',
                'description': 'Student has not logged into LMS for 7 days',
                'condition_type': 'engagement',
                'conditions': {
                    'metric': 'days_since_last_login',
                    'operator': 'greater_than',
                    'threshold': 7,
                    'period': 'current'
                },
                'intervention_type': 're_engagement',
                'priority_level': 'medium',
                'assigned_to_role': 'Student Success Advisor',
                'compliance_requirement': 'ASQA Standard 1.7 - Student retention',
            },
            {
                'name': 'High Risk Score',
                'description': 'Student risk score indicates high likelihood of withdrawal',
                'condition_type': 'risk_score',
                'conditions': {
                    'metric': 'risk_score',
                    'operator': 'greater_than',
                    'threshold': 80,
                    'period': 'current'
                },
                'intervention_type': 'wellbeing_check',
                'priority_level': 'urgent',
                'assigned_to_role': 'Head of Student Services',
                'compliance_requirement': 'ASQA Standard 1.7 - Student welfare',
            },
            {
                'name': 'Late Submissions Pattern',
                'description': 'Multiple late assessment submissions',
                'condition_type': 'submission',
                'conditions': {
                    'metric': 'late_submissions',
                    'operator': 'greater_than_or_equal',
                    'threshold': 2,
                    'period': 'last_4_weeks'
                },
                'intervention_type': 'progress_review',
                'priority_level': 'medium',
                'assigned_to_role': 'Trainer',
                'compliance_requirement': 'ASQA Standard 1.8 - Assessment completion',
            },
            {
                'name': 'Course Duration Exceeded',
                'description': 'Student has exceeded expected course duration',
                'condition_type': 'duration',
                'conditions': {
                    'metric': 'days_enrolled',
                    'operator': 'greater_than',
                    'threshold': 365,
                    'period': 'current'
                },
                'intervention_type': 'progress_review',
                'priority_level': 'high',
                'assigned_to_role': 'Course Coordinator',
                'compliance_requirement': 'ASQA Standard 1.1 - Training outcomes',
            },
        ]
        
        for tenant in tenants:
            tenant_id = str(tenant.id)
            
            # Create 4-6 rules per tenant
            for template in random.sample(rule_templates, k=random.randint(4, 6)):
                is_active = random.random() < 0.85  # 85% active
                
                rule = InterventionRule.objects.create(
                    tenant=tenant_id,
                    rule_name=template['name'],
                    description=template['description'],
                    is_active=is_active,
                    priority=random.randint(1, 5),
                    condition_type=template['condition_type'],
                    conditions=template['conditions'],
                    intervention_type=template['intervention_type'],
                    priority_level=template['priority_level'],
                    assigned_to_role=template['assigned_to_role'],
                    notify_staff=random.random() < 0.9,  # 90% have notifications
                    notification_recipients=[
                        f"{template['assigned_to_role'].lower().replace(' ', '.')}@example.com"
                    ],
                    notification_template=f"Alert: {template['name']} triggered for {{student_name}}. Please review and take appropriate action.",
                    compliance_requirement=template['compliance_requirement'],
                    trigger_count=random.randint(0, 50) if is_active else 0,
                    last_triggered=timezone.now() - timedelta(days=random.randint(1, 30)) if is_active and random.random() < 0.7 else None,
                )
                rules.append(rule)
        
        return rules

    def create_intervention_workflows(self, tenants):
        """Create intervention workflows for structured processes"""
        workflows = []
        
        # Workflow templates
        workflow_templates = [
            {
                'name': 'Academic Support Workflow',
                'description': 'Structured process for providing academic support to struggling students',
                'intervention_types': ['academic_support', 'progress_review'],
                'steps': [
                    {
                        'step_number': 1,
                        'step_name': 'Initial Assessment',
                        'description': 'Review student academic records and identify specific areas of difficulty',
                        'required': True,
                        'estimated_duration': 20,
                        'fields_required': ['assessment_notes', 'areas_of_concern']
                    },
                    {
                        'step_number': 2,
                        'step_name': 'Student Meeting',
                        'description': 'Meet with student to discuss challenges and available support',
                        'required': True,
                        'estimated_duration': 30,
                        'fields_required': ['meeting_notes', 'student_agreement']
                    },
                    {
                        'step_number': 3,
                        'step_name': 'Support Plan Development',
                        'description': 'Create personalized academic support plan',
                        'required': True,
                        'estimated_duration': 15,
                        'fields_required': ['support_plan', 'goals', 'timeline']
                    },
                    {
                        'step_number': 4,
                        'step_name': 'Follow-up Review',
                        'description': 'Check progress after 2 weeks',
                        'required': True,
                        'estimated_duration': 15,
                        'fields_required': ['progress_notes', 'next_steps']
                    },
                ],
                'requires_approval': False,
                'required_documentation': ['Support plan', 'Student consent', 'Progress notes'],
                'compliance_standard': 'ASQA Standard 1.5 - Assessment support',
            },
            {
                'name': 'Attendance Follow-up Workflow',
                'description': 'Process for addressing attendance issues',
                'intervention_types': ['attendance_followup'],
                'steps': [
                    {
                        'step_number': 1,
                        'step_name': 'Contact Student',
                        'description': 'Initial contact to understand reason for absence',
                        'required': True,
                        'estimated_duration': 10,
                        'fields_required': ['contact_method', 'response_received']
                    },
                    {
                        'step_number': 2,
                        'step_name': 'Document Reason',
                        'description': 'Record and categorize absence reason',
                        'required': True,
                        'estimated_duration': 5,
                        'fields_required': ['absence_reason', 'supporting_evidence']
                    },
                    {
                        'step_number': 3,
                        'step_name': 'Action Plan',
                        'description': 'Develop plan to improve attendance',
                        'required': True,
                        'estimated_duration': 15,
                        'fields_required': ['action_plan', 'student_commitment']
                    },
                ],
                'requires_approval': False,
                'required_documentation': ['Attendance records', 'Contact log', 'Action plan'],
                'compliance_standard': 'ASQA Standard 1.7 - Attendance monitoring',
            },
            {
                'name': 'Wellbeing Check Workflow',
                'description': 'Sensitive process for student wellbeing concerns',
                'intervention_types': ['wellbeing_check', 'referral'],
                'steps': [
                    {
                        'step_number': 1,
                        'step_name': 'Private Conversation',
                        'description': 'Confidential discussion with student',
                        'required': True,
                        'estimated_duration': 30,
                        'fields_required': ['wellbeing_concerns', 'student_disclosure']
                    },
                    {
                        'step_number': 2,
                        'step_name': 'Risk Assessment',
                        'description': 'Assess level of concern and immediate needs',
                        'required': True,
                        'estimated_duration': 10,
                        'fields_required': ['risk_level', 'immediate_action_required']
                    },
                    {
                        'step_number': 3,
                        'step_name': 'Support Referral',
                        'description': 'Connect student with appropriate support services',
                        'required': True,
                        'estimated_duration': 15,
                        'fields_required': ['referral_service', 'student_consent', 'contact_made']
                    },
                    {
                        'step_number': 4,
                        'step_name': 'Follow-up',
                        'description': 'Check in with student within one week',
                        'required': True,
                        'estimated_duration': 15,
                        'fields_required': ['followup_date', 'student_status', 'ongoing_support']
                    },
                ],
                'requires_approval': True,
                'approval_roles': ['Head of Student Services', 'Director of Studies'],
                'required_documentation': ['Wellbeing notes (confidential)', 'Referral confirmation', 'Student consent form'],
                'compliance_standard': 'ASQA Standard 1.7 - Student welfare and duty of care',
            },
        ]
        
        for tenant in tenants:
            tenant_id = str(tenant.id)
            
            # Create 2-3 workflows per tenant
            for template in random.sample(workflow_templates, k=random.randint(2, 3)):
                workflow = InterventionWorkflow.objects.create(
                    tenant=tenant_id,
                    workflow_name=template['name'],
                    description=template['description'],
                    intervention_types=template['intervention_types'],
                    is_active=random.random() < 0.9,  # 90% active
                    steps=template['steps'],
                    requires_approval=template['requires_approval'],
                    approval_roles=template.get('approval_roles', []),
                    required_documentation=template['required_documentation'],
                    compliance_standard=template['compliance_standard'],
                    audit_requirements=[
                        'All steps documented',
                        'Student consent obtained where required',
                        'Follow-up completed within timeframe',
                    ],
                )
                workflows.append(workflow)
        
        return workflows

    def create_interventions(self, tenants, users):
        """Create intervention records"""
        interventions = []
        
        # Sample student data
        student_names = [
            'Sarah Johnson', 'Michael Chen', 'Emma Wilson', 'James Martinez',
            'Olivia Brown', 'Liam Taylor', 'Ava Anderson', 'Noah Thomas',
            'Isabella Garcia', 'Mason Rodriguez', 'Sophia Lee', 'Lucas White',
            'Mia Harris', 'Ethan Clark', 'Charlotte Lewis', 'Alexander Walker'
        ]
        
        course_names = [
            'Certificate IV in Business', 'Diploma of Leadership',
            'Certificate III in Hospitality', 'Diploma of IT',
            'Certificate IV in Education Support', 'Diploma of Accounting',
            'Certificate III in Early Childhood', 'Diploma of Project Management',
        ]
        
        intervention_types_data = {
            'academic_support': {
                'priority': ['medium', 'high'],
                'triggers': ['manual', 'rule_engine'],
                'communication': ['face_to_face', 'video_call', 'email'],
            },
            'attendance_followup': {
                'priority': ['high', 'urgent'],
                'triggers': ['rule_engine', 'system_alert'],
                'communication': ['phone_call', 'email', 'sms'],
            },
            'wellbeing_check': {
                'priority': ['high', 'urgent'],
                'triggers': ['manual', 'third_party'],
                'communication': ['face_to_face', 'phone_call'],
            },
            'behaviour_management': {
                'priority': ['medium', 'high'],
                'triggers': ['manual'],
                'communication': ['face_to_face', 'written_note'],
            },
            'career_guidance': {
                'priority': ['low', 'medium'],
                'triggers': ['manual'],
                'communication': ['face_to_face', 'video_call'],
            },
            'extension_approval': {
                'priority': ['medium'],
                'triggers': ['manual'],
                'communication': ['email', 'lms_message'],
            },
            'progress_review': {
                'priority': ['medium', 'high'],
                'triggers': ['rule_engine', 'manual'],
                'communication': ['face_to_face', 'video_call'],
            },
            're_engagement': {
                'priority': ['high', 'urgent'],
                'triggers': ['rule_engine', 'system_alert'],
                'communication': ['phone_call', 'email', 'sms'],
            },
        }
        
        action_descriptions = {
            'academic_support': [
                'Reviewed assessment results with student and identified knowledge gaps in core competencies. Provided additional learning resources and scheduled follow-up tutoring sessions.',
                'Conducted one-on-one support session focusing on study skills and time management. Student demonstrated improved understanding of assessment requirements.',
                'Arranged peer mentoring support and access to online learning modules. Student committed to weekly check-ins.',
            ],
            'attendance_followup': [
                'Contacted student regarding absences. Student explained work commitments were causing scheduling conflicts. Arranged flexible attendance options.',
                'Met with student to discuss attendance concerns. Discovered transportation issues. Connected student with travel support program.',
                'Phone discussion revealed health issues affecting attendance. Provided information on special consideration process and flexible learning options.',
            ],
            'wellbeing_check': [
                'Sensitive conversation regarding student wellbeing. Student disclosed family pressures. Referred to counseling services with student consent.',
                'Checked in with student after observed changes in engagement. Student appreciated support and agreed to regular check-ins.',
                'Met privately with student regarding concerns. Connected student with external support services. Following up in one week.',
            ],
            'progress_review': [
                'Comprehensive review of student progress. Identified areas requiring additional support. Developed revised study plan with achievable milestones.',
                'Progress meeting indicated student on track but experiencing time pressure. Adjusted deadlines and provided additional resources.',
                'Reviewed competency completion rates. Student making good progress. Encouraged to maintain momentum.',
            ],
            're_engagement': [
                'Reached out to student who had stopped attending. Student experiencing personal challenges. Discussed options to resume studies when ready.',
                'Multiple contact attempts made. Finally connected via SMS. Student agreed to meeting to discuss return to study options.',
                'Contact established after period of non-engagement. Student ready to return. Welcomed back and caught up on missed content.',
            ],
        }
        
        for tenant in tenants:
            tenant_id = str(tenant.id)
            trainer_users = [u for u in users if u.username in ['trainer', 'manager', 'admin']]
            
            # Create 8-15 interventions per tenant
            for _ in range(random.randint(8, 15)):
                student_name = random.choice(student_names)
                student_id = f"STU{random.randint(1000, 9999)}"
                course_name = random.choice(course_names)
                course_id = f"CRS{random.randint(100, 999)}"
                
                intervention_type = random.choice(list(intervention_types_data.keys()))
                type_data = intervention_types_data[intervention_type]
                
                priority_level = random.choice(type_data['priority'])
                trigger_type = random.choice(type_data['triggers'])
                communication_method = random.choice(type_data['communication'])
                
                # Determine status (more recent interventions likely still in progress)
                days_ago = random.randint(1, 90)
                if days_ago < 7:
                    status = random.choice(['initiated', 'in_progress', 'in_progress'])
                elif days_ago < 30:
                    status = random.choice(['in_progress', 'completed', 'completed'])
                else:
                    status = random.choice(['completed', 'closed', 'closed'])
                
                action_date = timezone.now() - timedelta(days=days_ago)
                trainer = random.choice(trainer_users)
                
                # Trigger details
                trigger_details = {}
                if trigger_type == 'rule_engine':
                    if 'attendance' in intervention_type:
                        trigger_details = {
                            'attendance_rate': random.randint(45, 74),
                            'absences': random.randint(3, 8),
                            'period': 'last_2_weeks'
                        }
                    elif intervention_type == 'academic_support':
                        trigger_details = {
                            'failing_assessments': random.randint(3, 5),
                            'average_grade': random.randint(35, 49),
                            'period': 'last_4_weeks'
                        }
                    elif intervention_type == 're_engagement':
                        trigger_details = {
                            'days_since_last_login': random.randint(8, 21),
                            'missed_submissions': random.randint(2, 4)
                        }
                
                action_desc = random.choice(action_descriptions.get(intervention_type, [
                    f'Intervention conducted for {intervention_type}. Student supported and action plan developed.'
                ]))
                
                # Outcome
                if status in ['completed', 'closed']:
                    outcome_achieved = random.choice(['successful', 'successful', 'successful', 'partial', 'unsuccessful'])
                else:
                    outcome_achieved = 'pending'
                
                outcome_desc = ''
                if outcome_achieved == 'successful':
                    outcome_desc = random.choice([
                        'Student engagement improved significantly. All targets met.',
                        'Positive outcome achieved. Student back on track with studies.',
                        'Successful intervention. Student demonstrating improved performance.',
                    ])
                elif outcome_achieved == 'partial':
                    outcome_desc = 'Some improvement noted but ongoing support required.'
                elif outcome_achieved == 'unsuccessful':
                    outcome_desc = 'Student did not respond to intervention. Escalated to senior staff.'
                
                # Follow-up
                requires_followup = False
                followup_date = None
                if status == 'in_progress' or outcome_achieved == 'partial':
                    requires_followup = True
                    followup_date = (timezone.now() + timedelta(days=random.randint(7, 21))).date()
                
                # Referral
                referred_to = ''
                referral_accepted = None
                referral_date = None
                if intervention_type in ['wellbeing_check', 're_engagement'] and random.random() < 0.4:
                    referred_to = random.choice([
                        'Student Counseling Service',
                        'Disability Support Services',
                        'Career Guidance Office',
                        'Learning Skills Workshop',
                        'Mental Health First Aider',
                    ])
                    referral_accepted = random.choice([True, True, False])
                    referral_date = (action_date + timedelta(days=random.randint(1, 3))).date()
                
                intervention = Intervention.objects.create(
                    tenant=tenant_id,
                    student_id=student_id,
                    student_name=student_name,
                    course_id=course_id,
                    course_name=course_name,
                    intervention_type=intervention_type,
                    priority_level=priority_level,
                    status=status,
                    trigger_type=trigger_type,
                    trigger_rule_id=f"RULE-{random.randint(1000, 9999)}" if trigger_type == 'rule_engine' else '',
                    trigger_details=trigger_details,
                    action_description=action_desc,
                    action_taken_by=f"{trainer.first_name} {trainer.last_name}",
                    action_taken_by_role=random.choice(['Trainer', 'Course Coordinator', 'Student Services Officer']),
                    action_date=action_date,
                    communication_method=communication_method,
                    communication_notes=f"Communication conducted via {communication_method}. Student responsive and engaged in discussion.",
                    outcome_achieved=outcome_achieved,
                    outcome_description=outcome_desc,
                    outcome_evidence=[
                        {'type': 'attendance_record', 'url': f'/evidence/{student_id}/attendance.pdf'},
                        {'type': 'meeting_notes', 'url': f'/evidence/{student_id}/meeting_{action_date.strftime("%Y%m%d")}.pdf'},
                    ] if status in ['completed', 'closed'] else [],
                    requires_followup=requires_followup,
                    followup_date=followup_date,
                    followup_notes='Schedule follow-up meeting to review progress' if requires_followup else '',
                    referred_to=referred_to,
                    referral_accepted=referral_accepted,
                    referral_date=referral_date,
                    completed_at=action_date + timedelta(days=random.randint(7, 30)) if status in ['completed', 'closed'] else None,
                    audit_notes=f'Intervention documented in compliance with {random.choice(["ASQA Standard 1.5", "ASQA Standard 1.7", "ASQA Standard 1.8"])}',
                    compliance_category=random.choice([
                        'ASQA Standard 1.5 - Assessment',
                        'ASQA Standard 1.7 - Student support',
                        'ASQA Standard 1.8 - Completion and outcomes',
                    ]),
                    attachments=[
                        {'filename': f'intervention_form_{action_date.strftime("%Y%m%d")}.pdf', 'size': random.randint(50, 500) * 1024},
                        {'filename': f'student_consent_{action_date.strftime("%Y%m%d")}.pdf', 'size': random.randint(20, 100) * 1024},
                    ],
                )
                interventions.append(intervention)
        
        return interventions

    def create_intervention_steps(self, interventions, workflows):
        """Create workflow steps for interventions"""
        steps = []
        
        # Map intervention types to workflows
        workflow_map = {}
        for workflow in workflows:
            for int_type in workflow.intervention_types:
                if int_type not in workflow_map:
                    workflow_map[int_type] = []
                workflow_map[int_type].append(workflow)
        
        for intervention in interventions:
            # 60% of interventions follow a workflow
            if random.random() < 0.6 and intervention.intervention_type in workflow_map:
                workflow_options = workflow_map[intervention.intervention_type]
                # Filter by same tenant
                workflow_options = [w for w in workflow_options if w.tenant == intervention.tenant]
                
                if not workflow_options:
                    continue
                
                workflow = random.choice(workflow_options)
                
                # Create steps from workflow template
                for step_template in workflow.steps:
                    # Determine step status based on intervention status
                    if intervention.status == 'initiated':
                        step_status = 'pending' if step_template['step_number'] == 1 else 'pending'
                    elif intervention.status == 'in_progress':
                        if step_template['step_number'] <= random.randint(1, len(workflow.steps) - 1):
                            step_status = 'completed'
                        elif step_template['step_number'] == random.randint(2, len(workflow.steps)):
                            step_status = 'in_progress'
                        else:
                            step_status = 'pending'
                    else:  # completed, closed, etc.
                        step_status = 'completed'
                    
                    completed_at = None
                    completed_by = ''
                    completion_notes = ''
                    duration_minutes = None
                    
                    if step_status == 'completed':
                        days_offset = step_template['step_number'] * random.randint(1, 3)
                        completed_at = intervention.action_date + timedelta(days=days_offset)
                        completed_by = intervention.action_taken_by
                        completion_notes = f"Step completed successfully. {random.choice(['Student engaged positively.', 'Good progress made.', 'All requirements met.', 'Documentation completed.'])}"
                        duration_minutes = step_template['estimated_duration'] + random.randint(-5, 10)
                    
                    step = InterventionStep.objects.create(
                        intervention=intervention,
                        workflow=workflow,
                        step_number=step_template['step_number'],
                        step_name=step_template['step_name'],
                        step_description=step_template['description'],
                        status=step_status,
                        completed_by=completed_by,
                        completed_at=completed_at,
                        completion_notes=completion_notes,
                        duration_minutes=duration_minutes,
                        evidence_provided=[
                            {'type': field, 'status': 'provided'} 
                            for field in step_template.get('fields_required', [])
                        ] if step_status == 'completed' else [],
                        attachments=[
                            {'filename': f'{step_template["step_name"].lower().replace(" ", "_")}.pdf', 'size': random.randint(50, 200) * 1024}
                        ] if step_status == 'completed' and random.random() < 0.7 else [],
                    )
                    steps.append(step)
        
        return steps

    def create_intervention_outcomes(self, interventions):
        """Create outcome tracking records"""
        outcomes = []
        
        # Only create outcomes for completed/closed interventions
        completed_interventions = [i for i in interventions if i.status in ['completed', 'closed']]
        
        metric_types_by_intervention = {
            'academic_support': ['grade_improvement', 'completion_rate'],
            'attendance_followup': ['attendance_improvement', 'engagement_increase'],
            'wellbeing_check': ['satisfaction', 'engagement_increase'],
            'progress_review': ['completion_rate', 'grade_improvement'],
            're_engagement': ['attendance_improvement', 'engagement_increase'],
            'behaviour_management': ['behaviour_change', 'satisfaction'],
        }
        
        for intervention in completed_interventions:
            # Create 1-2 outcomes per intervention
            metric_types = metric_types_by_intervention.get(
                intervention.intervention_type,
                ['custom']
            )
            
            for metric_type in random.sample(metric_types, k=min(random.randint(1, 2), len(metric_types))):
                # Generate realistic baseline, target, and actual values
                if metric_type in ['attendance_improvement', 'completion_rate', 'engagement_increase']:
                    baseline_value = random.uniform(40, 70)
                    target_value = baseline_value + random.uniform(15, 25)
                    # Success varies
                    if intervention.outcome_achieved == 'successful':
                        actual_value = target_value + random.uniform(-5, 10)
                    elif intervention.outcome_achieved == 'partial':
                        actual_value = baseline_value + random.uniform(5, 15)
                    else:
                        actual_value = baseline_value + random.uniform(-5, 5)
                
                elif metric_type == 'grade_improvement':
                    baseline_value = random.uniform(35, 55)
                    target_value = 65.0
                    if intervention.outcome_achieved == 'successful':
                        actual_value = random.uniform(65, 85)
                    elif intervention.outcome_achieved == 'partial':
                        actual_value = random.uniform(55, 65)
                    else:
                        actual_value = random.uniform(35, 55)
                
                elif metric_type == 'satisfaction':
                    baseline_value = random.uniform(3, 5)
                    target_value = 8.0
                    if intervention.outcome_achieved == 'successful':
                        actual_value = random.uniform(8, 10)
                    else:
                        actual_value = random.uniform(6, 8)
                
                elif metric_type == 'behaviour_change':
                    baseline_value = random.uniform(2, 4)
                    target_value = 8.0
                    if intervention.outcome_achieved == 'successful':
                        actual_value = random.uniform(7, 9)
                    else:
                        actual_value = random.uniform(5, 7)
                
                else:  # custom
                    baseline_value = random.uniform(1, 5)
                    target_value = random.uniform(7, 10)
                    actual_value = random.uniform(5, 10)
                
                # Determine impact rating
                improvement_pct = ((actual_value - baseline_value) / baseline_value) * 100 if baseline_value > 0 else 0
                
                if improvement_pct >= 30:
                    impact_rating = 'significant'
                elif improvement_pct >= 15:
                    impact_rating = 'moderate'
                elif improvement_pct >= 5:
                    impact_rating = 'minimal'
                elif improvement_pct >= 0:
                    impact_rating = 'none'
                else:
                    impact_rating = 'negative'
                
                measurement_date = (intervention.completed_at or timezone.now()).date()
                
                outcome = InterventionOutcome.objects.create(
                    intervention=intervention,
                    metric_type=metric_type,
                    baseline_value=round(baseline_value, 2),
                    target_value=round(target_value, 2),
                    actual_value=round(actual_value, 2),
                    measurement_date=measurement_date,
                    impact_rating=impact_rating,
                    evidence_description=f"Measured {metric_type.replace('_', ' ')} through {random.choice(['student records', 'LMS analytics', 'attendance data', 'assessment results', 'student feedback'])}",
                    evidence_links=[
                        {'type': 'analytics_report', 'url': f'/reports/{metric_type}/{intervention.student_id}.pdf'},
                        {'type': 'comparison_chart', 'url': f'/charts/{metric_type}/{intervention.student_id}.png'},
                    ],
                    notes=f"Improvement of {improvement_pct:.1f}% from baseline. {'Target achieved.' if actual_value >= target_value else 'Target not fully achieved but positive progress made.'}",
                )
                outcomes.append(outcome)
        
        return outcomes

    def create_intervention_audit_logs(self, interventions, users):
        """Create comprehensive audit trail"""
        logs = []
        
        action_types_sequence = [
            'created',
            'status_changed',
            'step_completed',
            'document_attached',
            'outcome_recorded',
            'notification_sent',
            'closed',
        ]
        
        for intervention in interventions:
            # Create creation log
            create_date = intervention.action_date or intervention.created_at
            
            log = InterventionAuditLog.objects.create(
                tenant=intervention.tenant,
                intervention=intervention,
                action_type='created',
                action_description=f'Intervention {intervention.intervention_number} created for student {intervention.student_name}',
                performed_by=intervention.action_taken_by,
                performed_by_role=intervention.action_taken_by_role,
                changes={
                    'status': {'old': None, 'new': 'initiated'},
                    'priority_level': {'old': None, 'new': intervention.priority_level},
                    'intervention_type': {'old': None, 'new': intervention.intervention_type},
                },
                ip_address=f'10.0.{random.randint(1, 255)}.{random.randint(1, 255)}',
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                timestamp=create_date,
            )
            logs.append(log)
            
            # Create 2-5 additional logs based on intervention status
            num_logs = random.randint(2, 5) if intervention.status in ['completed', 'closed'] else random.randint(1, 3)
            
            log_timestamp = create_date
            for i in range(num_logs):
                log_timestamp = log_timestamp + timedelta(days=random.randint(1, 7), hours=random.randint(0, 23))
                
                action_type = random.choice([
                    'updated', 'status_changed', 'step_completed', 
                    'document_attached', 'notification_sent'
                ])
                
                if action_type == 'status_changed':
                    old_status = random.choice(['initiated', 'in_progress'])
                    new_status = intervention.status if i == num_logs - 1 else random.choice(['in_progress', 'completed'])
                    action_description = f'Status changed from {old_status} to {new_status}'
                    changes = {'status': {'old': old_status, 'new': new_status}}
                
                elif action_type == 'step_completed':
                    step_num = i + 1
                    action_description = f'Workflow step {step_num} completed'
                    changes = {'workflow_step': {'step': step_num, 'status': 'completed'}}
                
                elif action_type == 'document_attached':
                    doc_name = random.choice(['meeting_notes.pdf', 'support_plan.pdf', 'student_consent.pdf'])
                    action_description = f'Document attached: {doc_name}'
                    changes = {'documents': {'added': doc_name}}
                
                elif action_type == 'notification_sent':
                    recipient = random.choice(['Course Coordinator', 'Student Services', 'Head of Department'])
                    action_description = f'Notification sent to {recipient}'
                    changes = {'notification': {'recipient': recipient, 'sent': True}}
                
                else:  # updated
                    action_description = 'Intervention details updated'
                    changes = {'notes': {'updated': True}}
                
                performer = random.choice([intervention.action_taken_by] + [f"{u.first_name} {u.last_name}" for u in users[:3]])
                
                log = InterventionAuditLog.objects.create(
                    tenant=intervention.tenant,
                    intervention=intervention,
                    action_type=action_type,
                    action_description=action_description,
                    performed_by=performer,
                    performed_by_role=random.choice(['Trainer', 'Course Coordinator', 'Student Services Officer', 'Admin']),
                    changes=changes,
                    ip_address=f'10.0.{random.randint(1, 255)}.{random.randint(1, 255)}',
                    user_agent=random.choice([
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                        'Mozilla/5.0 (X11; Linux x86_64)',
                    ]),
                    timestamp=log_timestamp,
                )
                logs.append(log)
        
        return logs

    def create_micro_credentials(self, tenants, users, units):
        """Create micro credentials from training package units"""
        credentials = []
        
        # Sample micro credential templates
        credential_templates = [
            {
                'title': 'Digital Marketing Essentials',
                'code': 'MC-DIGMKT-001',
                'description': 'Learn the fundamentals of digital marketing including social media, email marketing, and SEO. Perfect for small business owners and marketing professionals.',
                'duration_hours': 40,
                'delivery_mode': 'online',
                'target_audience': 'Small business owners, marketing professionals, entrepreneurs',
                'skills_covered': ['Social Media Marketing', 'Email Marketing', 'SEO Basics', 'Content Creation', 'Google Analytics'],
                'industry_sectors': ['Marketing', 'Small Business', 'E-commerce'],
                'aqf_level': 'Certificate IV equivalent',
                'price': 495.00,
            },
            {
                'title': 'Cybersecurity Fundamentals',
                'code': 'MC-CYBER-001',
                'description': 'Essential cybersecurity skills for protecting business data and systems. Covers threat awareness, secure practices, and incident response basics.',
                'duration_hours': 30,
                'delivery_mode': 'blended',
                'target_audience': 'IT professionals, business owners, security officers',
                'skills_covered': ['Network Security', 'Risk Assessment', 'Incident Response', 'Security Policies', 'Data Protection'],
                'industry_sectors': ['Information Technology', 'Finance', 'Healthcare'],
                'aqf_level': 'Certificate III equivalent',
                'price': 650.00,
            },
            {
                'title': 'Leadership Foundations',
                'code': 'MC-LEAD-001',
                'description': 'Develop core leadership skills including team management, communication, and strategic thinking. Ideal for emerging leaders and supervisors.',
                'duration_hours': 35,
                'delivery_mode': 'face_to_face',
                'target_audience': 'Supervisors, team leaders, aspiring managers',
                'skills_covered': ['Team Leadership', 'Communication', 'Conflict Resolution', 'Performance Management', 'Strategic Planning'],
                'industry_sectors': ['Management', 'Business', 'Healthcare', 'Education'],
                'aqf_level': 'Diploma equivalent',
                'price': 795.00,
            },
            {
                'title': 'Project Management Basics',
                'code': 'MC-PROJ-001',
                'description': 'Introduction to project management methodologies, tools, and best practices. Learn to plan, execute, and deliver successful projects.',
                'duration_hours': 45,
                'delivery_mode': 'online',
                'target_audience': 'Project coordinators, team members, business professionals',
                'skills_covered': ['Project Planning', 'Risk Management', 'Stakeholder Engagement', 'Agile Methods', 'Project Tools'],
                'industry_sectors': ['Construction', 'IT', 'Engineering', 'Business'],
                'aqf_level': 'Certificate IV equivalent',
                'price': 550.00,
            },
            {
                'title': 'Customer Service Excellence',
                'code': 'MC-CUST-001',
                'description': 'Master customer service skills to deliver exceptional experiences. Covers communication, problem-solving, and complaint handling.',
                'duration_hours': 25,
                'delivery_mode': 'workplace',
                'target_audience': 'Customer service representatives, retail staff, hospitality workers',
                'skills_covered': ['Customer Communication', 'Problem Solving', 'Complaint Handling', 'Service Recovery', 'Product Knowledge'],
                'industry_sectors': ['Retail', 'Hospitality', 'Healthcare', 'Telecommunications'],
                'aqf_level': 'Certificate III equivalent',
                'price': 395.00,
            },
            {
                'title': 'Data Analytics Introduction',
                'code': 'MC-DATA-001',
                'description': 'Introduction to data analytics using Excel and Power BI. Learn to analyze data, create visualizations, and generate insights.',
                'duration_hours': 50,
                'delivery_mode': 'blended',
                'target_audience': 'Business analysts, data enthusiasts, managers',
                'skills_covered': ['Excel Advanced', 'Power BI', 'Data Visualization', 'Statistical Analysis', 'Dashboard Creation'],
                'industry_sectors': ['Business', 'Finance', 'IT', 'Marketing'],
                'aqf_level': 'Certificate IV equivalent',
                'price': 750.00,
            },
            {
                'title': 'Workplace Health & Safety',
                'code': 'MC-WHS-001',
                'description': 'Essential workplace health and safety knowledge for supervisors and safety officers. Covers risk assessment, compliance, and safety culture.',
                'duration_hours': 30,
                'delivery_mode': 'face_to_face',
                'target_audience': 'Supervisors, safety officers, managers',
                'skills_covered': ['Risk Assessment', 'Safety Legislation', 'Incident Investigation', 'Safety Culture', 'Hazard Control'],
                'industry_sectors': ['Construction', 'Manufacturing', 'Healthcare', 'Mining'],
                'aqf_level': 'Certificate IV equivalent',
                'price': 595.00,
            },
            {
                'title': 'Social Media Content Creation',
                'code': 'MC-SOCIAL-001',
                'description': 'Create engaging social media content across platforms. Learn content strategy, visual design, and community management.',
                'duration_hours': 35,
                'delivery_mode': 'online',
                'target_audience': 'Content creators, social media managers, marketers',
                'skills_covered': ['Content Strategy', 'Visual Design', 'Copywriting', 'Video Editing', 'Community Management'],
                'industry_sectors': ['Marketing', 'Media', 'Entertainment', 'E-commerce'],
                'aqf_level': 'Certificate III equivalent',
                'price': 495.00,
            },
        ]
        
        for tenant in tenants:
            # Create 3-5 micro credentials per tenant
            for template in random.sample(credential_templates, k=random.randint(3, 5)):
                # Select 2-4 units from the available units for this tenant
                tenant_units = [u for u in units if u.tenant == tenant]
                selected_units = random.sample(tenant_units, k=min(random.randint(2, 4), len(tenant_units)))
                
                # Build source units data
                source_units = []
                for unit in selected_units:
                    source_units.append({
                        'code': unit.code,
                        'title': unit.title,
                        'nominal_hours': random.randint(8, 25),
                        'elements': [
                            f'Element {i+1}: {random.choice(["Perform", "Apply", "Develop", "Implement", "Manage"])} {random.choice(["procedures", "strategies", "systems", "processes", "techniques"])}' 
                            for i in range(random.randint(2, 4))
                        ]
                    })
                
                # Build learning outcomes
                learning_outcomes = [
                    f'Demonstrate understanding of {skill.lower()}' 
                    for skill in template['skills_covered'][:3]
                ] + [
                    f'Apply {skill.lower()} in workplace contexts' 
                    for skill in template['skills_covered'][3:]
                ]
                
                # Build compressed content
                compressed_content = {
                    'key_competencies': template['skills_covered'],
                    'curriculum_structure': [
                        {
                            'module': i+1,
                            'title': random.choice([
                                'Foundations and Principles',
                                'Core Concepts',
                                'Practical Applications',
                                'Advanced Techniques',
                                'Integration and Practice'
                            ]),
                            'duration_hours': random.randint(5, 15),
                            'topics': random.sample([
                                'Introduction to key concepts',
                                'Theoretical frameworks',
                                'Practical exercises',
                                'Case study analysis',
                                'Tools and techniques',
                                'Industry best practices',
                                'Real-world applications',
                                'Problem-solving strategies'
                            ], k=random.randint(3, 5))
                        }
                        for i in range(random.randint(3, 5))
                    ],
                    'resources': [
                        'Online learning materials',
                        'Video tutorials',
                        'Practice exercises',
                        'Case studies',
                        'Assessment templates',
                        'Reference guides'
                    ]
                }
                
                # Build assessment strategy
                assessment_strategy = random.choice([
                    'Competency-based assessment combining knowledge tests, practical demonstrations, and portfolio evidence.',
                    'Project-based assessment with real-world application scenarios and workplace evidence.',
                    'Continuous assessment through practical tasks, case studies, and reflective practice.',
                    'Mixed assessment including written tasks, presentations, and workplace observations.'
                ])
                
                # Build assessment tasks
                assessment_tasks = [
                    {
                        'task_number': i+1,
                        'task_type': random.choice(['Knowledge Test', 'Practical Task', 'Project', 'Case Study', 'Portfolio']),
                        'title': f'Assessment Task {i+1}',
                        'description': random.choice([
                            'Complete a comprehensive knowledge assessment',
                            'Demonstrate practical skills in workplace context',
                            'Develop and present a project solution',
                            'Analyze and respond to case study scenarios',
                            'Compile portfolio of workplace evidence'
                        ]),
                        'weighting': random.choice([20, 25, 30, 35]),
                        'elements_assessed': [unit['elements'][0] for unit in random.sample(source_units, k=min(2, len(source_units)))]
                    }
                    for i in range(random.randint(3, 5))
                ]
                
                # Determine status (mostly published, some draft/in_review)
                status_weights = [
                    ('published', 0.6),
                    ('approved', 0.2),
                    ('in_review', 0.1),
                    ('draft', 0.1),
                ]
                status = random.choices(
                    [s[0] for s in status_weights],
                    weights=[s[1] for s in status_weights]
                )[0]
                
                days_ago = random.randint(7, 365)
                created_at = timezone.now() - timedelta(days=days_ago)
                published_at = None
                if status == 'published':
                    published_at = created_at + timedelta(days=random.randint(1, 14))
                
                # GPT generation details
                gpt_generated = random.random() < 0.7  # 70% GPT generated
                gpt_model = random.choice(['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo']) if gpt_generated else ''
                generation_time = random.uniform(15.5, 45.8) if gpt_generated else None
                
                credential = MicroCredential.objects.create(
                    tenant=tenant,
                    title=template['title'],
                    code=template['code'],
                    description=template['description'],
                    duration_hours=template['duration_hours'],
                    delivery_mode=template['delivery_mode'],
                    target_audience=template['target_audience'],
                    learning_outcomes=learning_outcomes,
                    source_units=source_units,
                    compressed_content=compressed_content,
                    tags=template['skills_covered'][:3] + [template['delivery_mode'], template['aqf_level'].split()[0]],
                    skills_covered=template['skills_covered'],
                    industry_sectors=template['industry_sectors'],
                    aqf_level=template['aqf_level'],
                    assessment_strategy=assessment_strategy,
                    assessment_tasks=assessment_tasks,
                    price=template['price'],
                    max_participants=random.choice([15, 20, 25, 30, None]),
                    prerequisites=random.choice([
                        '',
                        'No formal prerequisites required',
                        'Basic computer literacy recommended',
                        'Relevant workplace experience preferred',
                        '1-2 years industry experience recommended'
                    ]),
                    status=status,
                    gpt_generated=gpt_generated,
                    gpt_model_used=gpt_model,
                    generation_time_seconds=generation_time,
                    created_by=random.choice(users),
                    created_at=created_at,
                    published_at=published_at,
                )
                credentials.append(credential)
        
        return credentials

    def create_micro_credential_versions(self, micro_credentials, users):
        """Create version history for micro credentials"""
        versions = []
        
        change_types = [
            'Initial version created',
            'Updated learning outcomes based on feedback',
            'Revised assessment tasks for clarity',
            'Added additional resources and materials',
            'Updated duration and delivery mode',
            'Refined target audience description',
            'Enhanced content with industry examples',
            'Updated compliance with latest standards',
            'Restructured modules for better flow',
            'Added prerequisite requirements',
        ]
        
        for credential in micro_credentials:
            # Create 1-3 versions per credential (some have history, some don't)
            if random.random() < 0.6:  # 60% have version history
                num_versions = random.randint(1, 3)
                
                for version_num in range(1, num_versions + 1):
                    days_offset = (num_versions - version_num + 1) * random.randint(7, 30)
                    version_date = credential.created_at + timedelta(days=days_offset)
                    
                    # Create snapshot of content at this version
                    content_snapshot = {
                        'title': credential.title,
                        'code': credential.code,
                        'description': credential.description,
                        'duration_hours': credential.duration_hours,
                        'delivery_mode': credential.delivery_mode,
                        'learning_outcomes': credential.learning_outcomes,
                        'source_units': credential.source_units,
                        'assessment_tasks': credential.assessment_tasks,
                        'status': 'draft' if version_num == 1 else random.choice(['in_review', 'approved']),
                        'version_timestamp': version_date.isoformat(),
                    }
                    
                    change_summary = random.choice(change_types) if version_num > 1 else 'Initial version created'
                    
                    version = MicroCredentialVersion.objects.create(
                        micro_credential=credential,
                        version_number=version_num,
                        change_summary=change_summary,
                        content_snapshot=content_snapshot,
                        created_by=random.choice(users),
                        created_at=version_date,
                    )
                    versions.append(version)
        
        return versions

    def create_micro_credential_enrollments(self, micro_credentials):
        """Create student enrollments in micro credentials"""
        enrollments = []
        
        # Sample student names and emails
        student_data = [
            ('Alex Thompson', 'alex.thompson@example.com'),
            ('Sarah Johnson', 'sarah.j@example.com'),
            ('Michael Chen', 'michael.chen@example.com'),
            ('Emma Wilson', 'emma.wilson@example.com'),
            ('James Brown', 'james.brown@example.com'),
            ('Olivia Martinez', 'olivia.m@example.com'),
            ('Daniel Lee', 'daniel.lee@example.com'),
            ('Sophia Garcia', 'sophia.garcia@example.com'),
            ('William Davis', 'william.d@example.com'),
            ('Isabella Rodriguez', 'isabella.r@example.com'),
            ('Benjamin Moore', 'ben.moore@example.com'),
            ('Mia Taylor', 'mia.taylor@example.com'),
            ('Lucas Anderson', 'lucas.a@example.com'),
            ('Charlotte White', 'charlotte.w@example.com'),
            ('Henry Thomas', 'henry.thomas@example.com'),
            ('Amelia Harris', 'amelia.harris@example.com'),
            ('Alexander Martin', 'alex.martin@example.com'),
            ('Emily Clark', 'emily.clark@example.com'),
            ('Jack Lewis', 'jack.lewis@example.com'),
            ('Lily Walker', 'lily.walker@example.com'),
        ]
        
        # Only create enrollments for published credentials
        published_credentials = [c for c in micro_credentials if c.status == 'published']
        
        for credential in published_credentials:
            # Create 3-8 enrollments per published credential
            num_enrollments = random.randint(3, 8)
            
            # Ensure we don't exceed max_participants if set
            if credential.max_participants:
                num_enrollments = min(num_enrollments, credential.max_participants)
            
            selected_students = random.sample(student_data, k=min(num_enrollments, len(student_data)))
            
            for student_name, student_email in selected_students:
                # Determine enrollment status
                days_enrolled = random.randint(1, 180)
                enrolled_at = timezone.now() - timedelta(days=days_enrolled)
                
                if days_enrolled < 7:
                    status = 'enrolled'
                    started_at = None
                    completed_at = None
                    withdrawn_at = None
                elif days_enrolled < 30:
                    status = random.choice(['enrolled', 'in_progress', 'in_progress'])
                    started_at = enrolled_at + timedelta(days=random.randint(1, 5))
                    completed_at = None
                    withdrawn_at = None
                elif days_enrolled < credential.duration_hours * 2:
                    status = random.choice(['in_progress', 'in_progress', 'completed', 'withdrawn'])
                    started_at = enrolled_at + timedelta(days=random.randint(1, 5))
                    if status == 'completed':
                        completed_at = started_at + timedelta(days=random.randint(credential.duration_hours, credential.duration_hours * 2))
                        withdrawn_at = None
                    elif status == 'withdrawn':
                        withdrawn_at = started_at + timedelta(days=random.randint(7, 30))
                        completed_at = None
                    else:
                        completed_at = None
                        withdrawn_at = None
                else:
                    status = random.choice(['completed', 'completed', 'completed', 'withdrawn'])
                    started_at = enrolled_at + timedelta(days=random.randint(1, 5))
                    if status == 'completed':
                        completed_at = started_at + timedelta(days=random.randint(credential.duration_hours, credential.duration_hours * 3))
                        withdrawn_at = None
                    else:
                        withdrawn_at = started_at + timedelta(days=random.randint(14, 60))
                        completed_at = None
                
                # Build progress data
                progress_data = {}
                if status in ['in_progress', 'completed']:
                    total_outcomes = len(credential.learning_outcomes)
                    total_assessments = len(credential.assessment_tasks)
                    
                    if status == 'completed':
                        completed_outcomes = total_outcomes
                        completed_assessments = total_assessments
                        overall_progress = 100
                    else:
                        completed_outcomes = random.randint(1, total_outcomes - 1)
                        completed_assessments = random.randint(0, total_assessments - 1)
                        overall_progress = random.randint(25, 85)
                    
                    progress_data = {
                        'overall_progress': overall_progress,
                        'learning_outcomes': {
                            'total': total_outcomes,
                            'completed': completed_outcomes,
                            'progress_percentage': round((completed_outcomes / total_outcomes) * 100, 1)
                        },
                        'assessment_tasks': {
                            'total': total_assessments,
                            'completed': completed_assessments,
                            'progress_percentage': round((completed_assessments / total_assessments) * 100, 1) if total_assessments > 0 else 0
                        },
                        'modules_completed': random.randint(1, len(credential.compressed_content.get('curriculum_structure', []))),
                        'hours_logged': random.randint(5, credential.duration_hours) if status == 'in_progress' else credential.duration_hours,
                        'last_activity': (timezone.now() - timedelta(days=random.randint(1, 14))).isoformat(),
                    }
                
                enrollment = MicroCredentialEnrollment.objects.create(
                    micro_credential=credential,
                    student_name=student_name,
                    student_email=student_email,
                    student_id=f'STU{random.randint(1000, 9999)}',
                    status=status,
                    enrolled_at=enrolled_at,
                    started_at=started_at,
                    completed_at=completed_at,
                    withdrawn_at=withdrawn_at,
                    progress_data=progress_data,
                )
                enrollments.append(enrollment)
        
        return enrollments
