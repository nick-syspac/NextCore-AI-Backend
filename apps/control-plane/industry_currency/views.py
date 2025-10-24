from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Q
from datetime import datetime, timedelta
import random

from .models import (
    TrainerProfile, VerificationScan, LinkedInActivity,
    GitHubActivity, CurrencyEvidence, EntityExtraction
)
from .serializers import (
    TrainerProfileSerializer, TrainerProfileListSerializer,
    VerificationScanSerializer, VerificationScanListSerializer,
    LinkedInActivitySerializer, GitHubActivitySerializer,
    CurrencyEvidenceSerializer, EntityExtractionSerializer,
    StartScanRequestSerializer, StartScanResponseSerializer,
    ScanLinkedInRequestSerializer, ScanLinkedInResponseSerializer,
    ScanGitHubRequestSerializer, ScanGitHubResponseSerializer,
    AnalyzeCurrencyRequestSerializer, AnalyzeCurrencyResponseSerializer,
    GenerateEvidenceRequestSerializer, GenerateEvidenceResponseSerializer,
    ExtractEntitiesRequestSerializer, ExtractEntitiesResponseSerializer,
    DashboardStatsSerializer, VerifyProfileRequestSerializer, VerifyProfileResponseSerializer
)


class TrainerProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for trainer profiles with industry currency verification"""
    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer
    
    def get_queryset(self):
        queryset = TrainerProfile.objects.all()
        tenant = self.request.query_params.get('tenant')
        trainer_id = self.request.query_params.get('trainer_id')
        currency_status = self.request.query_params.get('currency_status')
        
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        if trainer_id:
            queryset = queryset.filter(trainer_id=trainer_id)
        if currency_status:
            queryset = queryset.filter(currency_status=currency_status)
        
        return queryset.order_by('-updated_at')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TrainerProfileListSerializer
        return TrainerProfileSerializer
    
    @action(detail=False, methods=['post'], url_path='start-scan')
    def start_scan(self, request):
        """
        Start a verification scan for a trainer profile
        POST /api/industry-currency/profiles/start-scan/
        Body: {profile_id, scan_type, sources_to_scan, linkedin_url, github_url}
        """
        serializer = StartScanRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            profile = TrainerProfile.objects.get(id=serializer.validated_data['profile_id'])
        except TrainerProfile.DoesNotExist:
            return Response({'error': 'Trainer profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update profile URLs if provided
        if 'linkedin_url' in serializer.validated_data:
            profile.linkedin_url = serializer.validated_data['linkedin_url']
        if 'github_url' in serializer.validated_data:
            profile.github_url = serializer.validated_data['github_url']
        profile.save()
        
        # Create verification scan
        scan = VerificationScan.objects.create(
            trainer_profile=profile,
            scan_type=serializer.validated_data.get('scan_type', 'manual'),
            sources_to_scan=serializer.validated_data.get('sources_to_scan', ['linkedin', 'github']),
            scan_status='pending',
            started_at=timezone.now()
        )
        
        # Update scan status
        scan.scan_status = 'scanning'
        scan.save()
        
        response_data = {
            'scan_id': scan.id,
            'scan_number': scan.scan_number,
            'status': 'scanning',
            'sources': scan.sources_to_scan,
            'message': f'Verification scan started for {profile.trainer_name}'
        }
        
        response_serializer = StartScanResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='scan-linkedin')
    def scan_linkedin(self, request):
        """
        Scan LinkedIn profile for industry currency evidence
        POST /api/industry-currency/profiles/scan-linkedin/
        Body: {scan_id, linkedin_url, extract_posts, extract_certifications, max_items}
        """
        serializer = ScanLinkedInRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scan = VerificationScan.objects.get(id=serializer.validated_data['scan_id'])
        except VerificationScan.DoesNotExist:
            return Response({'error': 'Verification scan not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Simulate LinkedIn scraping (in production, use Selenium/Playwright)
        # For demo, create mock activities
        sample_activities = [
            {
                'activity_type': 'post',
                'title': 'Thoughts on AI in Education',
                'description': 'Implemented machine learning algorithms to personalize student learning paths...',
                'skills_mentioned': ['Machine Learning', 'Python', 'TensorFlow'],
                'technologies': ['Python', 'TensorFlow', 'Keras'],
                'relevance_score': 0.92
            },
            {
                'activity_type': 'certification',
                'title': 'AWS Certified Solutions Architect',
                'description': 'Completed advanced certification in cloud architecture',
                'skills_mentioned': ['Cloud Computing', 'AWS', 'Architecture'],
                'technologies': ['AWS', 'EC2', 'S3', 'Lambda'],
                'relevance_score': 0.88
            },
            {
                'activity_type': 'position',
                'title': 'Senior Developer at Tech Corp',
                'description': 'Leading development team on enterprise applications',
                'companies': ['Tech Corp'],
                'skills_mentioned': ['Leadership', 'Software Development', 'Agile'],
                'relevance_score': 0.85
            }
        ]
        
        activities_created = 0
        relevant_count = 0
        
        for activity_data in sample_activities[:serializer.validated_data.get('max_items', 50)]:
            is_relevant = activity_data['relevance_score'] >= 0.7
            
            LinkedInActivity.objects.create(
                verification_scan=scan,
                activity_type=activity_data['activity_type'],
                title=activity_data['title'],
                description=activity_data['description'],
                activity_date=timezone.now().date() - timedelta(days=random.randint(1, 365)),
                skills_mentioned=activity_data.get('skills_mentioned', []),
                technologies=activity_data.get('technologies', []),
                companies=activity_data.get('companies', []),
                relevance_score=activity_data['relevance_score'],
                is_industry_relevant=is_relevant,
                relevance_reasoning='Activity demonstrates current industry engagement and technical skills'
            )
            
            activities_created += 1
            if is_relevant:
                relevant_count += 1
        
        # Update scan statistics
        scan.total_items_found += activities_created
        scan.relevant_items_count += relevant_count
        scan.save()
        
        response_data = {
            'scan_id': scan.id,
            'activities_found': activities_created,
            'relevant_count': relevant_count,
            'message': f'LinkedIn scan completed. Found {activities_created} activities, {relevant_count} industry-relevant.'
        }
        
        response_serializer = ScanLinkedInResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='scan-github')
    def scan_github(self, request):
        """
        Scan GitHub profile for industry currency evidence
        POST /api/industry-currency/profiles/scan-github/
        Body: {scan_id, github_username, extract_repos, extract_commits, max_items}
        """
        serializer = ScanGitHubRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scan = VerificationScan.objects.get(id=serializer.validated_data['scan_id'])
        except VerificationScan.DoesNotExist:
            return Response({'error': 'Verification scan not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Simulate GitHub API scraping (in production, use GitHub API)
        sample_repositories = [
            {
                'activity_type': 'repository',
                'repository_name': 'ai-learning-platform',
                'description': 'AI-powered adaptive learning platform for education',
                'language': 'Python',
                'languages_used': ['Python', 'JavaScript', 'TypeScript'],
                'topics': ['machine-learning', 'education', 'ai', 'react'],
                'technologies': ['Python', 'React', 'TensorFlow', 'PostgreSQL'],
                'stars': 45,
                'commits_count': 127,
                'relevance_score': 0.95
            },
            {
                'activity_type': 'repository',
                'repository_name': 'student-analytics-dashboard',
                'description': 'Real-time analytics dashboard for student performance tracking',
                'language': 'JavaScript',
                'languages_used': ['JavaScript', 'TypeScript', 'Python'],
                'topics': ['analytics', 'dashboard', 'education', 'data-visualization'],
                'technologies': ['React', 'D3.js', 'Node.js', 'MongoDB'],
                'stars': 23,
                'commits_count': 89,
                'relevance_score': 0.91
            },
            {
                'activity_type': 'contribution',
                'repository_name': 'open-source-lms',
                'description': 'Contributed to open-source learning management system',
                'language': 'Python',
                'technologies': ['Django', 'PostgreSQL', 'Redis'],
                'contributions_count': 34,
                'relevance_score': 0.87
            }
        ]
        
        activities_created = 0
        relevant_count = 0
        
        for repo_data in sample_repositories[:serializer.validated_data.get('max_items', 50)]:
            is_relevant = repo_data['relevance_score'] >= 0.7
            
            GitHubActivity.objects.create(
                verification_scan=scan,
                activity_type=repo_data['activity_type'],
                repository_name=repo_data.get('repository_name', ''),
                title=repo_data.get('repository_name', ''),
                description=repo_data['description'],
                activity_date=timezone.now().date() - timedelta(days=random.randint(1, 365)),
                last_updated=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                language=repo_data.get('language', ''),
                languages_used=repo_data.get('languages_used', []),
                topics=repo_data.get('topics', []),
                technologies=repo_data.get('technologies', []),
                stars=repo_data.get('stars', 0),
                commits_count=repo_data.get('commits_count', 0),
                contributions_count=repo_data.get('contributions_count', 0),
                relevance_score=repo_data['relevance_score'],
                is_industry_relevant=is_relevant,
                relevance_reasoning='Repository demonstrates active technical work in relevant field'
            )
            
            activities_created += 1
            if is_relevant:
                relevant_count += 1
        
        # Update scan statistics
        scan.total_items_found += activities_created
        scan.relevant_items_count += relevant_count
        scan.save()
        
        response_data = {
            'scan_id': scan.id,
            'activities_found': activities_created,
            'relevant_count': relevant_count,
            'message': f'GitHub scan completed. Found {activities_created} activities, {relevant_count} industry-relevant.'
        }
        
        response_serializer = ScanGitHubResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='analyze-currency')
    def analyze_currency(self, request):
        """
        Analyze industry currency based on scan results
        POST /api/industry-currency/profiles/analyze-currency/
        Body: {scan_id, industry, specializations, recency_weight, relevance_weight, frequency_weight}
        """
        serializer = AnalyzeCurrencyRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scan = VerificationScan.objects.get(id=serializer.validated_data['scan_id'])
        except VerificationScan.DoesNotExist:
            return Response({'error': 'Verification scan not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate currency scores
        recency_weight = serializer.validated_data.get('recency_weight', 0.4)
        relevance_weight = serializer.validated_data.get('relevance_weight', 0.4)
        frequency_weight = serializer.validated_data.get('frequency_weight', 0.2)
        
        # Get activities
        linkedin_activities = scan.linkedin_activities.all()
        github_activities = scan.github_activities.all()
        
        # Recency score (based on how recent activities are)
        recent_threshold = timezone.now().date() - timedelta(days=365)
        recent_linkedin = linkedin_activities.filter(activity_date__gte=recent_threshold).count()
        recent_github = github_activities.filter(activity_date__gte=recent_threshold).count()
        total_activities = linkedin_activities.count() + github_activities.count()
        recency_score = ((recent_linkedin + recent_github) / max(total_activities, 1)) * 100 if total_activities > 0 else 0
        
        # Relevance score (based on industry relevance of activities)
        relevant_linkedin = linkedin_activities.filter(is_industry_relevant=True)
        relevant_github = github_activities.filter(is_industry_relevant=True)
        avg_linkedin_relevance = relevant_linkedin.aggregate(Avg('relevance_score'))['relevance_score__avg'] or 0
        avg_github_relevance = relevant_github.aggregate(Avg('relevance_score'))['relevance_score__avg'] or 0
        relevance_score = ((avg_linkedin_relevance + avg_github_relevance) / 2) * 100
        
        # Frequency score (based on activity frequency)
        frequency_score = min((total_activities / 20) * 100, 100)  # 20+ activities = 100%
        
        # Calculate weighted currency score
        currency_score = (
            recency_score * recency_weight +
            relevance_score * relevance_weight +
            frequency_score * frequency_weight
        )
        
        # Determine currency status
        if currency_score >= 75:
            currency_status = 'current'
        elif currency_score >= 60:
            currency_status = 'expiring_soon'
        else:
            currency_status = 'expired'
        
        # Generate recommendations
        recommendations = []
        if recency_score < 70:
            recommendations.append('Increase recent professional activities and contributions')
        if relevance_score < 70:
            recommendations.append('Focus on activities more directly related to your industry')
        if frequency_score < 70:
            recommendations.append('Maintain more consistent engagement with professional platforms')
        if not recommendations:
            recommendations.append('Excellent currency! Continue maintaining current activity levels')
        
        # Update scan
        scan.scan_status = 'completed'
        scan.currency_score = currency_score
        scan.completed_at = timezone.now()
        scan.save()
        
        # Update profile
        profile = scan.trainer_profile
        profile.currency_status = currency_status
        profile.currency_score = currency_score
        profile.last_verified_date = timezone.now().date()
        profile.next_verification_date = timezone.now().date() + timedelta(days=profile.verification_frequency_days)
        profile.save()
        
        response_data = {
            'scan_id': scan.id,
            'currency_score': round(currency_score, 2),
            'currency_status': currency_status,
            'recency_score': round(recency_score, 2),
            'relevance_score': round(relevance_score, 2),
            'frequency_score': round(frequency_score, 2),
            'recommendations': recommendations,
            'message': f'Currency analysis completed. Status: {currency_status} ({currency_score:.1f}/100)'
        }
        
        response_serializer = AnalyzeCurrencyResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='generate-evidence')
    def generate_evidence(self, request):
        """
        Generate currency evidence document
        POST /api/industry-currency/profiles/generate-evidence/
        Body: {scan_id, evidence_type, file_format, include_raw_data, start_date, end_date}
        """
        serializer = GenerateEvidenceRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scan = VerificationScan.objects.get(id=serializer.validated_data['scan_id'])
        except VerificationScan.DoesNotExist:
            return Response({'error': 'Verification scan not found'}, status=status.HTTP_404_NOT_FOUND)
        
        evidence_type = serializer.validated_data['evidence_type']
        file_format = serializer.validated_data.get('file_format', 'markdown')
        
        # Get activities
        linkedin_activities = scan.linkedin_activities.filter(is_industry_relevant=True)
        github_activities = scan.github_activities.filter(is_industry_relevant=True)
        
        # Generate evidence title
        type_titles = {
            'linkedin_summary': 'LinkedIn Activity Summary',
            'github_summary': 'GitHub Activity Summary',
            'combined_report': 'Industry Currency Verification Report',
            'timeline': 'Professional Activity Timeline',
            'skills_matrix': 'Skills & Technologies Matrix',
            'currency_certificate': 'Industry Currency Certificate'
        }
        
        title = f"{type_titles.get(evidence_type, 'Evidence Document')} - {scan.trainer_profile.trainer_name}"
        
        # Generate content (in production, use templates or LLMs)
        content = f"""
# {title}

**Trainer:** {scan.trainer_profile.trainer_name}
**Verification Date:** {timezone.now().date()}
**Industry:** {scan.trainer_profile.primary_industry}
**Currency Score:** {scan.currency_score:.1f}/100
**Status:** {scan.trainer_profile.currency_status.upper()}

---

## Summary
This report provides evidence of industry currency through analysis of professional activities on LinkedIn and GitHub.

### LinkedIn Activities
- **Total Activities:** {linkedin_activities.count()}
- **Industry-Relevant:** {linkedin_activities.count()}
- **Average Relevance Score:** {linkedin_activities.aggregate(Avg('relevance_score'))['relevance_score__avg'] or 0:.2f}

### GitHub Activities
- **Total Repositories:** {github_activities.count()}
- **Industry-Relevant:** {github_activities.count()}
- **Total Commits:** {sum(a.commits_count for a in github_activities)}

---

## Key Activities

### LinkedIn Highlights
{chr(10).join(f"- **{a.title}** ({a.activity_date}): {a.description[:100]}..." for a in linkedin_activities[:5])}

### GitHub Highlights
{chr(10).join(f"- **{a.repository_name}** ({a.activity_date}): {a.description[:100]}..." for a in github_activities[:5])}

---

## Technologies & Skills
{chr(10).join(f"- {tech}" for tech in set(sum([a.technologies for a in linkedin_activities], []) + sum([a.technologies for a in github_activities], []))[:15])}

---

## Verification
This evidence document was automatically generated by the Industry Currency Verifier system.
Scan ID: {scan.scan_number}
Generated: {timezone.now()}
"""
        
        # Create evidence document
        evidence = CurrencyEvidence.objects.create(
            trainer_profile=scan.trainer_profile,
            verification_scan=scan,
            evidence_type=evidence_type,
            title=title,
            content=content,
            evidence_start_date=scan.started_at.date() if scan.started_at else None,
            evidence_end_date=scan.completed_at.date() if scan.completed_at else None,
            total_activities=linkedin_activities.count() + github_activities.count(),
            relevant_activities=linkedin_activities.count() + github_activities.count(),
            currency_score=scan.currency_score,
            linkedin_activities_included=[a.id for a in linkedin_activities],
            github_activities_included=[a.id for a in github_activities],
            file_format=file_format,
            file_path=f"/evidence/currency/{scan.trainer_profile.profile_number}_{evidence_type}.{file_format}",
            meets_rto_standards=True
        )
        
        response_data = {
            'evidence_id': evidence.id,
            'evidence_number': evidence.evidence_number,
            'title': title,
            'file_path': evidence.file_path,
            'total_activities': evidence.total_activities,
            'relevant_activities': evidence.relevant_activities,
            'currency_score': evidence.currency_score,
            'message': 'Evidence document generated successfully'
        }
        
        response_serializer = GenerateEvidenceResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='extract-entities')
    def extract_entities(self, request):
        """
        Extract entities from text using NLP
        POST /api/industry-currency/profiles/extract-entities/
        Body: {scan_id, source_type, source_text, source_url, nlp_model}
        """
        serializer = ExtractEntitiesRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            scan = VerificationScan.objects.get(id=serializer.validated_data['scan_id'])
        except VerificationScan.DoesNotExist:
            return Response({'error': 'Verification scan not found'}, status=status.HTTP_404_NOT_FOUND)
        
        source_text = serializer.validated_data['source_text']
        
        # Simulate NLP entity extraction (in production, use spaCy or similar)
        # Mock entities for demonstration
        extracted_entities = {
            'PERSON': ['John Doe', 'Jane Smith'],
            'ORG': ['Microsoft', 'Google', 'AWS', 'Meta'],
            'TECH': ['Python', 'React', 'TypeScript', 'Docker', 'Kubernetes', 'PostgreSQL'],
            'SKILL': ['Machine Learning', 'Cloud Architecture', 'Web Development', 'Data Science'],
            'DATE': ['2024', '2023', 'January 2024', 'Last 6 months'],
            'PRODUCT': ['GitHub', 'LinkedIn', 'VS Code', 'Azure']
        }
        
        entity_count = sum(len(entities) for entities in extracted_entities.values())
        
        # Create extraction record
        extraction = EntityExtraction.objects.create(
            verification_scan=scan,
            source_type=serializer.validated_data['source_type'],
            source_url=serializer.validated_data.get('source_url', ''),
            source_text=source_text,
            entities=extracted_entities,
            extraction_confidence=0.89,
            entity_count=entity_count,
            nlp_model_used=serializer.validated_data.get('nlp_model', 'spacy-en_core_web_lg'),
            processing_time_ms=245.7
        )
        
        response_data = {
            'extraction_id': extraction.id,
            'extraction_number': extraction.extraction_number,
            'entities': extracted_entities,
            'entity_count': entity_count,
            'extraction_confidence': 0.89,
            'message': f'Extracted {entity_count} entities from {serializer.validated_data["source_type"]} source'
        }
        
        response_serializer = ExtractEntitiesResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        """
        Get dashboard statistics
        GET /api/industry-currency/profiles/dashboard/?tenant=X
        """
        tenant = request.query_params.get('tenant')
        
        if not tenant:
            return Response({'error': 'tenant parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Date ranges
        today = timezone.now().date()
        month_ago = today - timedelta(days=30)
        
        # Query profiles
        all_profiles = TrainerProfile.objects.filter(tenant=tenant)
        
        # Statistics
        total_profiles = all_profiles.count()
        current_profiles = all_profiles.filter(currency_status='current').count()
        expiring_soon = all_profiles.filter(currency_status='expiring_soon').count()
        expired_profiles = all_profiles.filter(currency_status='expired').count()
        
        total_scans = VerificationScan.objects.filter(trainer_profile__tenant=tenant).count()
        scans_this_month = VerificationScan.objects.filter(
            trainer_profile__tenant=tenant,
            created_at__gte=month_ago
        ).count()
        
        avg_currency_score = all_profiles.aggregate(Avg('currency_score'))['currency_score__avg'] or 0
        
        total_linkedin_activities = LinkedInActivity.objects.filter(
            verification_scan__trainer_profile__tenant=tenant
        ).count()
        
        total_github_activities = GitHubActivity.objects.filter(
            verification_scan__trainer_profile__tenant=tenant
        ).count()
        
        total_evidence_docs = CurrencyEvidence.objects.filter(
            trainer_profile__tenant=tenant
        ).count()
        
        # Recent scans
        recent_scans = VerificationScan.objects.filter(
            trainer_profile__tenant=tenant
        ).order_by('-created_at')[:10]
        recent_scans_data = VerificationScanListSerializer(recent_scans, many=True).data
        
        # Top industries
        industries = all_profiles.values('primary_industry').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        top_industries = [{'industry': i['primary_industry'], 'count': i['count']} for i in industries]
        
        dashboard_data = {
            'total_profiles': total_profiles,
            'current_profiles': current_profiles,
            'expiring_soon': expiring_soon,
            'expired_profiles': expired_profiles,
            'total_scans': total_scans,
            'scans_this_month': scans_this_month,
            'avg_currency_score': round(avg_currency_score, 2),
            'total_linkedin_activities': total_linkedin_activities,
            'total_github_activities': total_github_activities,
            'total_evidence_docs': total_evidence_docs,
            'recent_scans': recent_scans_data,
            'top_industries': top_industries
        }
        
        response_serializer = DashboardStatsSerializer(data=dashboard_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='verify-profile')
    def verify_profile(self, request):
        """
        Complete profile verification workflow
        POST /api/industry-currency/profiles/verify-profile/
        Body: {profile_id, scan_linkedin, scan_github, analyze_currency, generate_evidence}
        """
        serializer = VerifyProfileRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            profile = TrainerProfile.objects.get(id=serializer.validated_data['profile_id'])
        except TrainerProfile.DoesNotExist:
            return Response({'error': 'Trainer profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Start scan
        scan = VerificationScan.objects.create(
            trainer_profile=profile,
            scan_type='manual',
            sources_to_scan=[],
            scan_status='scanning',
            started_at=timezone.now()
        )
        
        linkedin_count = 0
        github_count = 0
        
        # Scan LinkedIn if requested
        if serializer.validated_data.get('scan_linkedin', True) and profile.linkedin_url:
            # Simulate scanning (call scan_linkedin internally)
            linkedin_count = 3  # Mock count
            scan.sources_to_scan.append('linkedin')
        
        # Scan GitHub if requested
        if serializer.validated_data.get('scan_github', True) and profile.github_url:
            # Simulate scanning (call scan_github internally)
            github_count = 3  # Mock count
            scan.sources_to_scan.append('github')
        
        scan.total_items_found = linkedin_count + github_count
        scan.relevant_items_count = linkedin_count + github_count
        scan.save()
        
        # Analyze currency
        currency_score = 82.5  # Mock score
        currency_status = 'current'
        
        if serializer.validated_data.get('analyze_currency', True):
            scan.scan_status = 'completed'
            scan.currency_score = currency_score
            scan.completed_at = timezone.now()
            scan.save()
            
            profile.currency_status = currency_status
            profile.currency_score = currency_score
            profile.last_verified_date = timezone.now().date()
            profile.save()
        
        # Generate evidence
        evidence_id = None
        evidence_generated = False
        
        if serializer.validated_data.get('generate_evidence', True):
            evidence = CurrencyEvidence.objects.create(
                trainer_profile=profile,
                verification_scan=scan,
                evidence_type=serializer.validated_data.get('evidence_type', 'combined_report'),
                title=f'Industry Currency Report - {profile.trainer_name}',
                content='Generated evidence content...',
                total_activities=linkedin_count + github_count,
                relevant_activities=linkedin_count + github_count,
                currency_score=currency_score,
                file_format='markdown'
            )
            evidence_id = evidence.id
            evidence_generated = True
        
        response_data = {
            'profile_id': profile.id,
            'scan_id': scan.id,
            'currency_score': currency_score,
            'currency_status': currency_status,
            'linkedin_activities': linkedin_count,
            'github_activities': github_count,
            'evidence_generated': evidence_generated,
            'evidence_id': evidence_id,
            'message': f'Profile verification completed. Status: {currency_status} ({currency_score}/100)'
        }
        
        response_serializer = VerifyProfileResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class VerificationScanViewSet(viewsets.ModelViewSet):
    """ViewSet for verification scans"""
    queryset = VerificationScan.objects.all()
    serializer_class = VerificationScanSerializer
    
    def get_queryset(self):
        queryset = VerificationScan.objects.all()
        profile_id = self.request.query_params.get('profile_id')
        scan_status = self.request.query_params.get('status')
        
        if profile_id:
            queryset = queryset.filter(trainer_profile_id=profile_id)
        if scan_status:
            queryset = queryset.filter(scan_status=scan_status)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VerificationScanListSerializer
        return VerificationScanSerializer


class LinkedInActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for LinkedIn activities"""
    queryset = LinkedInActivity.objects.all()
    serializer_class = LinkedInActivitySerializer
    
    def get_queryset(self):
        queryset = LinkedInActivity.objects.all()
        scan_id = self.request.query_params.get('scan_id')
        is_relevant = self.request.query_params.get('is_relevant')
        
        if scan_id:
            queryset = queryset.filter(verification_scan_id=scan_id)
        if is_relevant is not None:
            queryset = queryset.filter(is_industry_relevant=is_relevant.lower() == 'true')
        
        return queryset.order_by('-activity_date')


class GitHubActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for GitHub activities"""
    queryset = GitHubActivity.objects.all()
    serializer_class = GitHubActivitySerializer
    
    def get_queryset(self):
        queryset = GitHubActivity.objects.all()
        scan_id = self.request.query_params.get('scan_id')
        is_relevant = self.request.query_params.get('is_relevant')
        
        if scan_id:
            queryset = queryset.filter(verification_scan_id=scan_id)
        if is_relevant is not None:
            queryset = queryset.filter(is_industry_relevant=is_relevant.lower() == 'true')
        
        return queryset.order_by('-activity_date')


class CurrencyEvidenceViewSet(viewsets.ModelViewSet):
    """ViewSet for currency evidence documents"""
    queryset = CurrencyEvidence.objects.all()
    serializer_class = CurrencyEvidenceSerializer
    
    def get_queryset(self):
        queryset = CurrencyEvidence.objects.all()
        profile_id = self.request.query_params.get('profile_id')
        scan_id = self.request.query_params.get('scan_id')
        
        if profile_id:
            queryset = queryset.filter(trainer_profile_id=profile_id)
        if scan_id:
            queryset = queryset.filter(verification_scan_id=scan_id)
        
        return queryset.order_by('-created_at')


class EntityExtractionViewSet(viewsets.ModelViewSet):
    """ViewSet for entity extractions"""
    queryset = EntityExtraction.objects.all()
    serializer_class = EntityExtractionSerializer
    
    def get_queryset(self):
        queryset = EntityExtraction.objects.all()
        scan_id = self.request.query_params.get('scan_id')
        source_type = self.request.query_params.get('source_type')
        
        if scan_id:
            queryset = queryset.filter(verification_scan_id=scan_id)
        if source_type:
            queryset = queryset.filter(source_type=source_type)
        
        return queryset.order_by('-extracted_at')
