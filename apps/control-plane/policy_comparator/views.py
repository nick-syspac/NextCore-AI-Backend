from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
import time
import re
from difflib import SequenceMatcher

from .models import ASQAStandard, ASQAClause, Policy, ComparisonResult, ComparisonSession
from .serializers import (
    ASQAStandardSerializer, ASQAClauseSerializer, PolicySerializer,
    ComparisonResultSerializer, ComparisonSessionSerializer,
    CompareRequestSerializer, GapAnalysisSerializer
)


class ASQAStandardViewSet(viewsets.ModelViewSet):
    """ViewSet for ASQA standards"""
    serializer_class = ASQAStandardSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['standard_type', 'is_active', 'version']
    search_fields = ['standard_number', 'title', 'description']
    ordering_fields = ['standard_number', 'created_at']

    def get_queryset(self):
        return ASQAStandard.objects.filter(is_active=True).prefetch_related('clauses')


class ASQAClauseViewSet(viewsets.ModelViewSet):
    """ViewSet for ASQA clauses"""
    serializer_class = ASQAClauseSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['standard', 'compliance_level', 'is_active']
    search_fields = ['clause_number', 'title', 'clause_text']
    ordering_fields = ['clause_number', 'created_at']

    def get_queryset(self):
        return ASQAClause.objects.filter(is_active=True).select_related('standard')


class PolicyViewSet(viewsets.ModelViewSet):
    """ViewSet for policies with comparison capabilities"""
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'policy_type']
    search_fields = ['policy_number', 'title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'compliance_score']

    def get_queryset(self):
        tenant_slug = self.kwargs.get('tenant_slug')
        from tenants.models import Tenant
        tenant = Tenant.objects.get(slug=tenant_slug)
        return Policy.objects.filter(tenant=tenant)

    def perform_create(self, serializer):
        tenant_slug = self.kwargs.get('tenant_slug')
        from tenants.models import Tenant
        tenant = Tenant.objects.get(slug=tenant_slug)
        serializer.save(tenant=tenant, created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def compare(self, request, tenant_slug=None, pk=None):
        """
        Compare policy against ASQA standards using NLP-based text similarity
        Instantly identifies compliance gaps
        """
        policy = self.get_object()
        serializer = CompareRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        
        # Get tenant
        from tenants.models import Tenant
        tenant = Tenant.objects.get(slug=tenant_slug)

        start_time = time.time()

        try:
            with transaction.atomic():
                # Create comparison session
                session = ComparisonSession.objects.create(
                    tenant=tenant,
                    policy=policy,
                    session_name=data.get('session_name', f"Comparison - {timezone.now().strftime('%Y-%m-%d %H:%M')}"),
                    status='processing',
                    created_by=request.user,
                    standards_compared=data.get('standard_ids', []),
                )

                # Get ASQA clauses to compare
                if data.get('standard_ids'):
                    clauses = ASQAClause.objects.filter(
                        standard_id__in=data['standard_ids'],
                        is_active=True
                    ).select_related('standard')
                else:
                    clauses = ASQAClause.objects.filter(is_active=True).select_related('standard')

                # Perform NLP comparison
                results = []
                compliant_count = 0
                partial_count = 0
                gap_count = 0

                for clause in clauses:
                    # Calculate NLP similarity
                    comparison_data = self._compare_text_nlp(
                        policy.content,
                        clause.clause_text,
                        clause.keywords
                    )

                    # Create comparison result
                    result = ComparisonResult.objects.create(
                        policy=policy,
                        asqa_clause=clause,
                        similarity_score=comparison_data['similarity_score'],
                        matched_text=comparison_data['matched_text'],
                        gap_description=comparison_data['gap_description'],
                        recommendations=comparison_data['recommendations'],
                        nlp_metadata=comparison_data['nlp_metadata'],
                        keywords_matched=comparison_data['keywords_matched'],
                        keywords_missing=comparison_data['keywords_missing'],
                        has_sufficient_evidence=comparison_data['has_sufficient_evidence'],
                    )

                    results.append(result)

                    # Count by match type
                    if result.match_type == 'full':
                        compliant_count += 1
                    elif result.match_type in ['partial', 'weak']:
                        partial_count += 1
                    else:
                        gap_count += 1

                # Update session
                session.total_clauses_checked = len(clauses)
                session.compliant_count = compliant_count
                session.partial_match_count = partial_count
                session.gap_count = gap_count
                session.calculate_compliance_score()
                session.processing_time_seconds = time.time() - start_time
                session.status = 'completed'
                session.completed_at = timezone.now()
                session.save()

                # Update policy compliance score
                policy.compliance_score = session.overall_compliance_score
                policy.last_compared_at = timezone.now()
                policy.save()

                return Response({
                    'session': ComparisonSessionSerializer(session).data,
                    'results_summary': {
                        'total_checked': session.total_clauses_checked,
                        'compliant': compliant_count,
                        'partial_match': partial_count,
                        'gaps': gap_count,
                        'compliance_score': session.overall_compliance_score,
                    },
                    'processing_time': session.processing_time_seconds,
                    'message': f'Comparison completed in {session.processing_time_seconds:.2f} seconds. Found {gap_count} compliance gaps.',
                }, status=status.HTTP_200_OK)

        except Exception as e:
            session.status = 'failed'
            session.error_message = str(e)
            session.save()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _compare_text_nlp(self, policy_text, clause_text, keywords):
        """
        NLP-based text similarity comparison
        Uses multiple techniques: keyword matching, sequence similarity, semantic analysis
        """
        # Normalize text
        policy_lower = policy_text.lower()
        clause_lower = clause_text.lower()

        # 1. Keyword matching score (30% weight)
        keyword_score = self._calculate_keyword_score(policy_lower, keywords)

        # 2. Sequence similarity score (40% weight)
        sequence_score = self._calculate_sequence_similarity(policy_lower, clause_lower)

        # 3. Phrase matching score (30% weight)
        phrase_score = self._calculate_phrase_similarity(policy_lower, clause_lower)

        # Combined similarity score
        similarity_score = (
            keyword_score * 0.3 +
            sequence_score * 0.4 +
            phrase_score * 0.3
        )

        # Find matched text sections
        matched_text = self._extract_matched_text(policy_text, clause_text, keywords)

        # Identify gaps
        gap_description = self._generate_gap_description(similarity_score, keywords, policy_lower)

        # Generate recommendations
        recommendations = self._generate_recommendations(similarity_score, keywords, policy_lower)

        # Track keywords
        keywords_matched = [kw for kw in keywords if kw.lower() in policy_lower]
        keywords_missing = [kw for kw in keywords if kw.lower() not in policy_lower]

        return {
            'similarity_score': round(similarity_score, 4),
            'matched_text': matched_text,
            'gap_description': gap_description,
            'recommendations': recommendations,
            'nlp_metadata': {
                'keyword_score': round(keyword_score, 4),
                'sequence_score': round(sequence_score, 4),
                'phrase_score': round(phrase_score, 4),
                'method': 'hybrid_nlp',
            },
            'keywords_matched': keywords_matched,
            'keywords_missing': keywords_missing,
            'has_sufficient_evidence': similarity_score >= 0.6,
        }

    def _calculate_keyword_score(self, text, keywords):
        """Calculate score based on keyword presence"""
        if not keywords:
            return 0.5  # Neutral score if no keywords
        
        matched = sum(1 for kw in keywords if kw.lower() in text)
        return matched / len(keywords)

    def _calculate_sequence_similarity(self, text1, text2):
        """Calculate sequence similarity using SequenceMatcher"""
        # Sample for performance (use first 2000 chars)
        sample1 = text1[:2000]
        sample2 = text2[:2000]
        
        matcher = SequenceMatcher(None, sample1, sample2)
        return matcher.ratio()

    def _calculate_phrase_similarity(self, policy_text, clause_text):
        """Calculate phrase-level similarity"""
        # Extract key phrases from clause (sentences)
        clause_sentences = [s.strip() for s in clause_text.split('.') if len(s.strip()) > 20]
        
        if not clause_sentences:
            return 0.0
        
        matches = 0
        for sentence in clause_sentences[:5]:  # Check first 5 sentences
            # Check if similar sentence exists in policy
            words = set(sentence.lower().split())
            # Remove common words
            words = words - {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
            
            if len(words) == 0:
                continue
            
            # Count word matches in policy
            word_matches = sum(1 for w in words if w in policy_text)
            if word_matches / len(words) > 0.5:
                matches += 1
        
        return matches / min(len(clause_sentences), 5) if clause_sentences else 0.0

    def _extract_matched_text(self, policy_text, clause_text, keywords):
        """Extract relevant sections from policy that match clause"""
        # Find sentences containing keywords
        sentences = policy_text.split('.')
        matched_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(kw.lower() in sentence_lower for kw in keywords):
                matched_sentences.append(sentence.strip())
        
        if matched_sentences:
            return '. '.join(matched_sentences[:3])  # Return first 3 matching sentences
        
        return ''

    def _generate_gap_description(self, similarity_score, keywords, policy_text):
        """Generate description of compliance gaps"""
        if similarity_score >= 0.8:
            return 'Policy appears to fully address this ASQA clause.'
        elif similarity_score >= 0.6:
            return 'Policy partially addresses this clause but may need additional detail or evidence.'
        elif similarity_score >= 0.4:
            missing = [kw for kw in keywords if kw.lower() not in policy_text]
            return f'Policy has weak coverage of this clause. Missing key concepts: {", ".join(missing[:5])}'
        else:
            return 'Policy does not adequately address this ASQA clause. Significant gaps identified.'

    def _generate_recommendations(self, similarity_score, keywords, policy_text):
        """Generate recommendations to improve compliance"""
        recommendations = []
        
        if similarity_score < 0.8:
            missing_keywords = [kw for kw in keywords if kw.lower() not in policy_text]
            
            if missing_keywords:
                recommendations.append(f"Include references to: {', '.join(missing_keywords[:5])}")
            
            if similarity_score < 0.6:
                recommendations.append("Add specific procedures and evidence requirements")
                recommendations.append("Include measurable criteria and timelines")
            
            if similarity_score < 0.4:
                recommendations.append("Consider creating a dedicated policy section for this requirement")
                recommendations.append("Review ASQA guidance materials for this standard")
        
        return recommendations

    @action(detail=True, methods=['get'])
    def gap_analysis(self, request, tenant_slug=None, pk=None):
        """Get detailed gap analysis for a policy"""
        policy = self.get_object()
        
        # Get all comparison results for this policy
        results = ComparisonResult.objects.filter(
            policy=policy
        ).select_related('asqa_clause', 'asqa_clause__standard').order_by('similarity_score')

        # Categorize gaps
        critical_gaps = []
        moderate_gaps = []
        minor_gaps = []

        for result in results:
            gap_data = {
                'clause': ASQAClauseSerializer(result.asqa_clause).data,
                'similarity_score': result.similarity_score,
                'gap_severity': result.match_type,
                'recommendations': result.recommendations,
                'missing_keywords': result.keywords_missing,
            }

            if result.match_type == 'no_match' and result.asqa_clause.compliance_level == 'critical':
                critical_gaps.append(gap_data)
            elif result.match_type in ['no_match', 'weak']:
                moderate_gaps.append(gap_data)
            elif result.match_type == 'partial':
                minor_gaps.append(gap_data)

        return Response({
            'policy': PolicySerializer(policy).data,
            'summary': {
                'total_gaps': len(critical_gaps) + len(moderate_gaps) + len(minor_gaps),
                'critical_gaps': len(critical_gaps),
                'moderate_gaps': len(moderate_gaps),
                'minor_gaps': len(minor_gaps),
                'compliance_score': policy.compliance_score,
            },
            'critical_gaps': critical_gaps[:10],
            'moderate_gaps': moderate_gaps[:10],
            'minor_gaps': minor_gaps[:10],
        })

    @action(detail=True, methods=['get'])
    def comparison_history(self, request, tenant_slug=None, pk=None):
        """Get comparison history for a policy"""
        policy = self.get_object()
        sessions = ComparisonSession.objects.filter(policy=policy).order_by('-created_at')
        serializer = ComparisonSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def results(self, request, tenant_slug=None, pk=None):
        """Get detailed comparison results for a policy"""
        policy = self.get_object()
        results = ComparisonResult.objects.filter(
            policy=policy
        ).select_related('asqa_clause', 'asqa_clause__standard').order_by('-similarity_score')
        
        serializer = ComparisonResultSerializer(results, many=True)
        return Response(serializer.data)


class ComparisonSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for comparison sessions (read-only)"""
    serializer_class = ComparisonSessionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'policy']
    ordering_fields = ['created_at', 'overall_compliance_score']

    def get_queryset(self):
        tenant_slug = self.kwargs.get('tenant_slug')
        from tenants.models import Tenant
        tenant = Tenant.objects.get(slug=tenant_slug)
        return ComparisonSession.objects.filter(tenant=tenant).select_related('policy', 'created_by')
