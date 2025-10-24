from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Q
import random
import hashlib
from datetime import datetime, timedelta

from .models import (
    AuthenticityCheck,
    SubmissionAnalysis,
    PlagiarismMatch,
    MetadataVerification,
    AnomalyDetection
)
from .serializers import (
    AuthenticityCheckSerializer,
    AuthenticityCheckListSerializer,
    SubmissionAnalysisSerializer,
    SubmissionAnalysisListSerializer,
    PlagiarismMatchSerializer,
    MetadataVerificationSerializer,
    AnomalyDetectionSerializer
)


class AuthenticityCheckViewSet(viewsets.ModelViewSet):
    """ViewSet for managing authenticity checks"""
    
    queryset = AuthenticityCheck.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AuthenticityCheckListSerializer
        return AuthenticityCheckSerializer
    
    @action(detail=True, methods=['post'])
    def check_authenticity(self, request, pk=None):
        """Run authenticity check on submission with plagiarism detection"""
        authenticity_check = self.get_object()
        submission_id = request.data.get('submission_id')
        
        if not submission_id:
            return Response(
                {'error': 'submission_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mock submission content (in real implementation, get from Submission model)
        submission_content = request.data.get('content', 'Sample submission content for analysis.')
        
        # Generate content hash
        content_hash = hashlib.sha256(submission_content.encode('utf-8')).hexdigest()
        
        # Generate embedding (mock 384-dimensional vector)
        content_embedding = [random.uniform(-1, 1) for _ in range(384)]
        
        # Create submission analysis
        analysis = SubmissionAnalysis.objects.create(
            authenticity_check=authenticity_check,
            submission_id=submission_id,
            submission_content=submission_content,
            content_hash=content_hash,
            content_embedding=content_embedding,
            word_count=len(submission_content.split()),
            character_count=len(submission_content),
            analysis_metadata={
                'language': 'en',
                'analyzed_by': 'AI System',
                'analysis_timestamp': timezone.now().isoformat()
            }
        )
        
        # Run plagiarism detection
        plagiarism_results = self._detect_plagiarism(analysis, authenticity_check)
        
        # Run metadata verification if enabled
        metadata_results = None
        if authenticity_check.metadata_verification_enabled:
            metadata_results = self._verify_metadata(analysis)
        
        # Run anomaly detection if enabled
        anomaly_results = None
        if authenticity_check.anomaly_detection_enabled:
            anomaly_results = self._detect_anomalies(analysis)
        
        # Calculate combined integrity score
        analysis.calculate_combined_score()
        
        # Update authenticity check statistics
        authenticity_check.total_submissions_checked += 1
        if analysis.plagiarism_detected:
            authenticity_check.plagiarism_cases_detected += 1
        if analysis.metadata_issues:
            authenticity_check.metadata_issues_found += 1
        if analysis.anomalies_found:
            authenticity_check.anomalies_detected += 1
        authenticity_check.save()
        
        # Recalculate overall score
        authenticity_check.calculate_overall_score()
        
        return Response({
            'analysis': SubmissionAnalysisSerializer(analysis).data,
            'plagiarism_results': plagiarism_results,
            'metadata_results': metadata_results,
            'anomaly_results': anomaly_results,
            'message': 'Authenticity check completed'
        })
    
    def _detect_plagiarism(self, current_analysis, authenticity_check):
        """Detect plagiarism by comparing with other submissions"""
        results = {
            'matches_found': 0,
            'highest_similarity': 0.0,
            'matches': []
        }
        
        # Get all other analyses in the same check
        other_analyses = SubmissionAnalysis.objects.filter(
            authenticity_check=authenticity_check
        ).exclude(id=current_analysis.id)
        
        plagiarism_detected = False
        highest_score = 0.0
        
        for other_analysis in other_analyses:
            # Calculate similarity (mock implementation using random score)
            # In real implementation, use cosine similarity on embeddings
            similarity_score = random.uniform(0.1, 0.95)
            
            if similarity_score >= authenticity_check.plagiarism_threshold:
                # Create plagiarism match
                match = PlagiarismMatch.objects.create(
                    source_analysis=current_analysis,
                    matched_analysis=other_analysis,
                    similarity_score=similarity_score,
                    match_type='embedding',
                    matched_text_segments=[
                        {
                            'source_text': 'Sample matched text segment from source',
                            'matched_text': 'Sample matched text segment from match',
                            'start_position': random.randint(0, 100),
                            'end_position': random.randint(100, 200),
                            'similarity': similarity_score
                        }
                    ],
                    matched_words_count=random.randint(50, 200),
                    matched_percentage=similarity_score * 100
                )
                
                plagiarism_detected = True
                highest_score = max(highest_score, similarity_score)
                results['matches_found'] += 1
                results['matches'].append(PlagiarismMatchSerializer(match).data)
        
        # Update analysis plagiarism score
        current_analysis.plagiarism_score = highest_score
        current_analysis.plagiarism_detected = plagiarism_detected
        current_analysis.save()
        
        results['highest_similarity'] = highest_score
        return results
    
    def _verify_metadata(self, analysis):
        """Verify submission metadata for authenticity"""
        # Mock metadata extraction
        now = timezone.now()
        creation_time = now - timedelta(hours=random.randint(1, 48))
        modification_time = creation_time + timedelta(minutes=random.randint(5, 120))
        
        # Generate random anomalies (for demo)
        anomalies = []
        if random.random() < 0.3:  # 30% chance of anomaly
            anomaly_types = [
                'Creation timestamp is in the future',
                'File modified before creation',
                'Author metadata missing',
                'Suspicious modification pattern detected',
                'Multiple authors detected'
            ]
            anomalies.append(random.choice(anomaly_types))
        
        verification = MetadataVerification.objects.create(
            submission_analysis=analysis,
            file_metadata={
                'file_size': random.randint(1000, 50000),
                'file_type': 'text/plain',
                'encoding': 'UTF-8'
            },
            creation_timestamp=creation_time,
            modification_timestamp=modification_time,
            modification_history=[
                {
                    'timestamp': creation_time.isoformat(),
                    'action': 'created',
                    'user': 'student'
                },
                {
                    'timestamp': modification_time.isoformat(),
                    'action': 'modified',
                    'user': 'student'
                }
            ],
            author_info={
                'name': 'Student Name',
                'email': 'student@example.com'
            },
            author_matches_student=True,
            anomalies_detected=anomalies
        )
        
        # Update analysis metadata score
        analysis.metadata_verification_score = verification.verification_score
        analysis.metadata_issues = len(anomalies) > 0
        analysis.save()
        
        return MetadataVerificationSerializer(verification).data
    
    def _detect_anomalies(self, analysis):
        """Detect behavioral and pattern anomalies"""
        anomalies_created = []
        total_impact = 0.0
        
        # Typing speed anomaly (30% chance)
        if random.random() < 0.3:
            typing_speed = random.randint(150, 300)  # words per minute
            severity = 'high' if typing_speed > 200 else 'medium'
            
            anomaly = AnomalyDetection.objects.create(
                submission_analysis=analysis,
                anomaly_type='typing_speed',
                severity=severity,
                anomaly_data={
                    'typing_speed_wpm': typing_speed,
                    'expected_range': [40, 80],
                    'threshold': 120
                },
                description=f'Unusually high typing speed detected: {typing_speed} WPM (expected: 40-80 WPM)',
                confidence_score=random.uniform(0.7, 0.95)
            )
            anomalies_created.append(anomaly)
            total_impact += anomaly.impact_score
        
        # Paste events anomaly (25% chance)
        if random.random() < 0.25:
            paste_count = random.randint(10, 50)
            severity = 'critical' if paste_count > 30 else 'high'
            
            anomaly = AnomalyDetection.objects.create(
                submission_analysis=analysis,
                anomaly_type='paste_events',
                severity=severity,
                anomaly_data={
                    'paste_events_count': paste_count,
                    'total_content_pasted': random.randint(500, 2000),
                    'paste_percentage': random.randint(60, 95)
                },
                description=f'Excessive paste events detected: {paste_count} paste operations',
                confidence_score=random.uniform(0.8, 0.99)
            )
            anomalies_created.append(anomaly)
            total_impact += anomaly.impact_score
        
        # Time gaps anomaly (20% chance)
        if random.random() < 0.2:
            gap_minutes = random.randint(30, 180)
            severity = 'medium' if gap_minutes < 90 else 'high'
            
            anomaly = AnomalyDetection.objects.create(
                submission_analysis=analysis,
                anomaly_type='time_gaps',
                severity=severity,
                anomaly_data={
                    'gap_duration_minutes': gap_minutes,
                    'gaps_detected': random.randint(2, 5),
                    'longest_gap': gap_minutes
                },
                description=f'Suspicious time gap detected: {gap_minutes} minutes of inactivity',
                confidence_score=random.uniform(0.6, 0.85)
            )
            anomalies_created.append(anomaly)
            total_impact += anomaly.impact_score
        
        # Behavioral pattern anomaly (15% chance)
        if random.random() < 0.15:
            anomaly = AnomalyDetection.objects.create(
                submission_analysis=analysis,
                anomaly_type='behavioral',
                severity='medium',
                anomaly_data={
                    'pattern': 'unusual_editing_pattern',
                    'details': 'Non-linear editing detected, suggesting copy from external source'
                },
                description='Unusual behavioral pattern detected in submission process',
                confidence_score=random.uniform(0.5, 0.75)
            )
            anomalies_created.append(anomaly)
            total_impact += anomaly.impact_score
        
        # Update analysis anomaly score
        if anomalies_created:
            analysis.anomaly_score = min(100.0, total_impact / len(anomalies_created))
            analysis.anomalies_found = True
        else:
            analysis.anomaly_score = 0.0
            analysis.anomalies_found = False
        
        analysis.save()
        
        return {
            'anomalies_detected': len(anomalies_created),
            'total_impact_score': total_impact,
            'anomalies': [AnomalyDetectionSerializer(a).data for a in anomalies_created]
        }
    
    @action(detail=True, methods=['get'])
    def integrity_report(self, request, pk=None):
        """Generate comprehensive integrity report"""
        authenticity_check = self.get_object()
        
        analyses = authenticity_check.submission_analyses.all()
        
        report = {
            'check_info': {
                'check_number': authenticity_check.check_number,
                'name': authenticity_check.name,
                'assessment': authenticity_check.assessment.title,
                'status': authenticity_check.status,
                'overall_integrity_score': authenticity_check.overall_integrity_score
            },
            'statistics': {
                'total_submissions': authenticity_check.total_submissions_checked,
                'plagiarism_cases': authenticity_check.plagiarism_cases_detected,
                'metadata_issues': authenticity_check.metadata_issues_found,
                'anomalies_detected': authenticity_check.anomalies_detected,
                'pass_rate': analyses.filter(integrity_status='pass').count() / max(analyses.count(), 1) * 100
            },
            'score_distribution': {
                'pass': analyses.filter(integrity_status='pass').count(),
                'warning': analyses.filter(integrity_status='warning').count(),
                'fail': analyses.filter(integrity_status='fail').count(),
                'under_review': analyses.filter(integrity_status='under_review').count()
            },
            'plagiarism_severity': {
                'critical': PlagiarismMatch.objects.filter(
                    source_analysis__authenticity_check=authenticity_check,
                    severity='critical'
                ).count(),
                'high': PlagiarismMatch.objects.filter(
                    source_analysis__authenticity_check=authenticity_check,
                    severity='high'
                ).count(),
                'medium': PlagiarismMatch.objects.filter(
                    source_analysis__authenticity_check=authenticity_check,
                    severity='medium'
                ).count(),
                'low': PlagiarismMatch.objects.filter(
                    source_analysis__authenticity_check=authenticity_check,
                    severity='low'
                ).count()
            },
            'average_scores': {
                'plagiarism': analyses.aggregate(Avg('plagiarism_score'))['plagiarism_score__avg'] or 0,
                'metadata_verification': analyses.aggregate(Avg('metadata_verification_score'))['metadata_verification_score__avg'] or 0,
                'anomaly': analyses.aggregate(Avg('anomaly_score'))['anomaly_score__avg'] or 0,
                'combined_integrity': analyses.aggregate(Avg('combined_integrity_score'))['combined_integrity_score__avg'] or 0
            },
            'generated_at': timezone.now().isoformat()
        }
        
        return Response(report)


class SubmissionAnalysisViewSet(viewsets.ModelViewSet):
    """ViewSet for managing submission analyses"""
    
    queryset = SubmissionAnalysis.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SubmissionAnalysisListSerializer
        return SubmissionAnalysisSerializer


class PlagiarismMatchViewSet(viewsets.ModelViewSet):
    """ViewSet for managing plagiarism matches"""
    
    queryset = PlagiarismMatch.objects.all()
    serializer_class = PlagiarismMatchSerializer
    
    @action(detail=True, methods=['post'])
    def mark_reviewed(self, request, pk=None):
        """Mark plagiarism match as reviewed"""
        match = self.get_object()
        match.reviewed = True
        match.false_positive = request.data.get('false_positive', False)
        match.review_notes = request.data.get('review_notes', '')
        match.reviewed_by = request.user
        match.reviewed_at = timezone.now()
        match.save()
        
        return Response(PlagiarismMatchSerializer(match).data)


class MetadataVerificationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing metadata verifications"""
    
    queryset = MetadataVerification.objects.all()
    serializer_class = MetadataVerificationSerializer


class AnomalyDetectionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing anomaly detections"""
    
    queryset = AnomalyDetection.objects.all()
    serializer_class = AnomalyDetectionSerializer
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge anomaly with notes"""
        anomaly = self.get_object()
        anomaly.acknowledged = True
        anomaly.false_positive = request.data.get('false_positive', False)
        anomaly.resolution_notes = request.data.get('resolution_notes', '')
        anomaly.save()
        
        return Response(AnomalyDetectionSerializer(anomaly).data)
