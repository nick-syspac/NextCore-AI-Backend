from rest_framework import serializers
from .models import (
    TrainerProfile, VerificationScan, LinkedInActivity, 
    GitHubActivity, CurrencyEvidence, EntityExtraction
)


class TrainerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerProfile
        fields = '__all__'
        read_only_fields = ['profile_number', 'created_at', 'updated_at']


class TrainerProfileListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing profiles"""
    scans_count = serializers.SerializerMethodField()
    
    class Meta:
        model = TrainerProfile
        fields = [
            'id', 'profile_number', 'trainer_name', 'primary_industry',
            'currency_status', 'currency_score', 'last_verified_date',
            'scans_count', 'updated_at'
        ]
    
    def get_scans_count(self, obj):
        return obj.scans.count()


class LinkedInActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedInActivity
        fields = '__all__'
        read_only_fields = ['activity_number', 'extracted_at']


class GitHubActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubActivity
        fields = '__all__'
        read_only_fields = ['activity_number', 'extracted_at']


class VerificationScanSerializer(serializers.ModelSerializer):
    linkedin_activities = LinkedInActivitySerializer(many=True, read_only=True)
    github_activities = GitHubActivitySerializer(many=True, read_only=True)
    
    class Meta:
        model = VerificationScan
        fields = '__all__'
        read_only_fields = ['scan_number', 'created_at', 'started_at', 'completed_at']


class VerificationScanListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing scans"""
    linkedin_count = serializers.SerializerMethodField()
    github_count = serializers.SerializerMethodField()
    
    class Meta:
        model = VerificationScan
        fields = [
            'id', 'scan_number', 'scan_type', 'scan_status',
            'currency_score', 'linkedin_count', 'github_count',
            'created_at', 'completed_at'
        ]
    
    def get_linkedin_count(self, obj):
        return obj.linkedin_activities.count()
    
    def get_github_count(self, obj):
        return obj.github_activities.count()


class CurrencyEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyEvidence
        fields = '__all__'
        read_only_fields = ['evidence_number', 'created_at']


class EntityExtractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityExtraction
        fields = '__all__'
        read_only_fields = ['extraction_number', 'extracted_at']


# Request/Response Serializers

class StartScanRequestSerializer(serializers.Serializer):
    """Request serializer for starting a verification scan"""
    profile_id = serializers.IntegerField()
    scan_type = serializers.ChoiceField(
        choices=['manual', 'scheduled', 'automatic'],
        default='manual'
    )
    sources_to_scan = serializers.ListField(
        child=serializers.ChoiceField(choices=['linkedin', 'github', 'twitter', 'website']),
        default=['linkedin', 'github']
    )
    linkedin_url = serializers.URLField(required=False, allow_blank=True)
    github_url = serializers.URLField(required=False, allow_blank=True)


class StartScanResponseSerializer(serializers.Serializer):
    """Response serializer for scan initiation"""
    scan_id = serializers.IntegerField()
    scan_number = serializers.CharField()
    status = serializers.CharField()
    sources = serializers.ListField(child=serializers.CharField())
    message = serializers.CharField()


class ScanLinkedInRequestSerializer(serializers.Serializer):
    """Request serializer for LinkedIn scanning"""
    scan_id = serializers.IntegerField()
    linkedin_url = serializers.URLField()
    extract_posts = serializers.BooleanField(default=True)
    extract_certifications = serializers.BooleanField(default=True)
    extract_positions = serializers.BooleanField(default=True)
    max_items = serializers.IntegerField(default=50)


class ScanLinkedInResponseSerializer(serializers.Serializer):
    """Response serializer for LinkedIn scanning"""
    scan_id = serializers.IntegerField()
    activities_found = serializers.IntegerField()
    relevant_count = serializers.IntegerField()
    message = serializers.CharField()


class ScanGitHubRequestSerializer(serializers.Serializer):
    """Request serializer for GitHub scanning"""
    scan_id = serializers.IntegerField()
    github_username = serializers.CharField()
    extract_repos = serializers.BooleanField(default=True)
    extract_commits = serializers.BooleanField(default=True)
    extract_contributions = serializers.BooleanField(default=True)
    max_items = serializers.IntegerField(default=50)


class ScanGitHubResponseSerializer(serializers.Serializer):
    """Response serializer for GitHub scanning"""
    scan_id = serializers.IntegerField()
    activities_found = serializers.IntegerField()
    relevant_count = serializers.IntegerField()
    message = serializers.CharField()


class AnalyzeCurrencyRequestSerializer(serializers.Serializer):
    """Request serializer for currency analysis"""
    scan_id = serializers.IntegerField()
    industry = serializers.CharField(max_length=200)
    specializations = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list
    )
    recency_weight = serializers.FloatField(default=0.4, min_value=0.0, max_value=1.0)
    relevance_weight = serializers.FloatField(default=0.4, min_value=0.0, max_value=1.0)
    frequency_weight = serializers.FloatField(default=0.2, min_value=0.0, max_value=1.0)


class AnalyzeCurrencyResponseSerializer(serializers.Serializer):
    """Response serializer for currency analysis"""
    scan_id = serializers.IntegerField()
    currency_score = serializers.FloatField()
    currency_status = serializers.CharField()
    recency_score = serializers.FloatField()
    relevance_score = serializers.FloatField()
    frequency_score = serializers.FloatField()
    recommendations = serializers.ListField(child=serializers.CharField())
    message = serializers.CharField()


class GenerateEvidenceRequestSerializer(serializers.Serializer):
    """Request serializer for evidence generation"""
    scan_id = serializers.IntegerField()
    evidence_type = serializers.ChoiceField(
        choices=[
            'linkedin_summary', 'github_summary', 'combined_report',
            'timeline', 'skills_matrix', 'currency_certificate'
        ]
    )
    file_format = serializers.ChoiceField(
        choices=['markdown', 'html', 'pdf', 'json'],
        default='markdown'
    )
    include_raw_data = serializers.BooleanField(default=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)


class GenerateEvidenceResponseSerializer(serializers.Serializer):
    """Response serializer for evidence generation"""
    evidence_id = serializers.IntegerField()
    evidence_number = serializers.CharField()
    title = serializers.CharField()
    file_path = serializers.CharField()
    total_activities = serializers.IntegerField()
    relevant_activities = serializers.IntegerField()
    currency_score = serializers.FloatField()
    message = serializers.CharField()


class ExtractEntitiesRequestSerializer(serializers.Serializer):
    """Request serializer for NLP entity extraction"""
    scan_id = serializers.IntegerField()
    source_type = serializers.ChoiceField(choices=['linkedin', 'github', 'twitter', 'website'])
    source_text = serializers.CharField()
    source_url = serializers.URLField(required=False, allow_blank=True)
    nlp_model = serializers.CharField(default='spacy-en_core_web_lg')


class ExtractEntitiesResponseSerializer(serializers.Serializer):
    """Response serializer for entity extraction"""
    extraction_id = serializers.IntegerField()
    extraction_number = serializers.CharField()
    entities = serializers.DictField()
    entity_count = serializers.IntegerField()
    extraction_confidence = serializers.FloatField()
    message = serializers.CharField()


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_profiles = serializers.IntegerField()
    current_profiles = serializers.IntegerField()
    expiring_soon = serializers.IntegerField()
    expired_profiles = serializers.IntegerField()
    total_scans = serializers.IntegerField()
    scans_this_month = serializers.IntegerField()
    avg_currency_score = serializers.FloatField()
    total_linkedin_activities = serializers.IntegerField()
    total_github_activities = serializers.IntegerField()
    total_evidence_docs = serializers.IntegerField()
    recent_scans = VerificationScanListSerializer(many=True)
    top_industries = serializers.ListField(child=serializers.DictField())


class VerifyProfileRequestSerializer(serializers.Serializer):
    """Request serializer for full profile verification"""
    profile_id = serializers.IntegerField()
    scan_linkedin = serializers.BooleanField(default=True)
    scan_github = serializers.BooleanField(default=True)
    analyze_currency = serializers.BooleanField(default=True)
    generate_evidence = serializers.BooleanField(default=True)
    evidence_type = serializers.ChoiceField(
        choices=['combined_report', 'timeline', 'skills_matrix', 'currency_certificate'],
        default='combined_report'
    )


class VerifyProfileResponseSerializer(serializers.Serializer):
    """Response serializer for profile verification"""
    profile_id = serializers.IntegerField()
    scan_id = serializers.IntegerField()
    currency_score = serializers.FloatField()
    currency_status = serializers.CharField()
    linkedin_activities = serializers.IntegerField()
    github_activities = serializers.IntegerField()
    evidence_generated = serializers.BooleanField()
    evidence_id = serializers.IntegerField(required=False)
    message = serializers.CharField()
