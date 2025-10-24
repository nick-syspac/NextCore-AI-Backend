from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import (
    LearningPathway, LearningStep, StudentProgress,
    PathwayRecommendation, ContentEmbedding
)
from .serializers import (
    LearningPathwaySerializer, LearningStepSerializer,
    StudentProgressSerializer, PathwayRecommendationSerializer,
    ContentEmbeddingSerializer, RecommendationRequestSerializer
)


class LearningPathwayViewSet(viewsets.ModelViewSet):
    queryset = LearningPathway.objects.all()
    serializer_class = LearningPathwaySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_slug = self.kwargs.get('tenant_slug')
        if tenant_slug:
            queryset = queryset.filter(tenant=tenant_slug)
        
        # Filter by student
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def recommend_pathway(self, request, tenant_slug=None):
        """
        Generate personalized learning pathway recommendations using
        collaborative filtering + content embeddings (hybrid approach).
        """
        serializer = RecommendationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        student_id = data['student_id']
        student_name = data['student_name']
        skill_level = data['current_skill_level']
        interests = data.get('interests', [])
        learning_style = data.get('learning_style', 'visual')
        time_commitment = data.get('time_commitment_hours', 10.0)
        
        # Step 1: Find similar students using collaborative filtering
        similar_students = self._find_similar_students(student_id, tenant_slug)
        
        # Step 2: Get pathways completed by similar students
        candidate_pathways = self._get_candidate_pathways(
            similar_students, 
            tenant_slug, 
            skill_level
        )
        
        # Step 3: Calculate collaborative filtering scores
        cf_scores = self._calculate_collaborative_scores(
            student_id,
            candidate_pathways,
            similar_students
        )
        
        # Step 4: Calculate content-based scores using embeddings
        embedding_scores = self._calculate_embedding_scores(
            interests,
            candidate_pathways
        )
        
        # Step 5: Combine scores (hybrid approach)
        # Weight: 60% collaborative filtering, 40% embeddings
        final_recommendations = []
        for pathway_id in candidate_pathways:
            cf_score = cf_scores.get(pathway_id, 0)
            emb_score = embedding_scores.get(pathway_id, 0)
            
            # Hybrid score
            hybrid_score = (0.6 * cf_score) + (0.4 * emb_score)
            
            final_recommendations.append({
                'pathway_id': pathway_id,
                'collaborative_score': cf_score,
                'embedding_score': emb_score,
                'hybrid_score': hybrid_score
            })
        
        # Sort by hybrid score
        final_recommendations.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        # Take top 5 recommendations
        top_recommendations = final_recommendations[:5]
        
        # Step 6: Create recommendation records
        recommendations = []
        for rec in top_recommendations:
            pathway = LearningPathway.objects.get(id=rec['pathway_id'])
            
            # Generate recommendation reasons
            reasons = self._generate_recommendation_reasons(
                rec,
                similar_students,
                interests,
                pathway
            )
            
            # Create recommendation
            recommendation = PathwayRecommendation.objects.create(
                tenant=tenant_slug,
                student_id=student_id,
                student_name=student_name,
                recommended_pathway=pathway,
                algorithm_used='hybrid',
                recommendation_score=rec['hybrid_score'],
                collaborative_score=rec['collaborative_score'],
                embedding_similarity=rec['embedding_score'],
                similar_students_count=len(similar_students),
                similar_students_list=similar_students[:10],
                recommendation_reasons=reasons,
                expires_at=timezone.now() + timedelta(days=30)
            )
            recommendations.append(recommendation)
        
        # Serialize and return
        serializer = PathwayRecommendationSerializer(recommendations, many=True)
        return Response({
            'recommendations': serializer.data,
            'algorithm': 'Hybrid (Collaborative Filtering + Embeddings)',
            'similar_students_found': len(similar_students),
            'total_candidates_evaluated': len(candidate_pathways)
        })
    
    def _find_similar_students(self, student_id, tenant_slug):
        """
        Find students with similar learning patterns using collaborative filtering.
        Similarity based on: completed pathways, progress patterns, engagement.
        """
        # Get current student's progress
        student_progress = StudentProgress.objects.filter(
            student_id=student_id,
            tenant=tenant_slug,
            is_completed=True
        ).values_list('step_id', flat=True)
        
        if not student_progress:
            return []
        
        student_steps = set(student_progress)
        
        # Find other students who completed similar steps
        other_students = StudentProgress.objects.filter(
            tenant=tenant_slug,
            is_completed=True
        ).exclude(student_id=student_id).values('student_id').annotate(
            completed_count=Count('id')
        )
        
        # Calculate Jaccard similarity for each student
        similarities = []
        for other_student in other_students:
            other_id = other_student['student_id']
            other_steps = set(
                StudentProgress.objects.filter(
                    student_id=other_id,
                    tenant=tenant_slug,
                    is_completed=True
                ).values_list('step_id', flat=True)
            )
            
            # Jaccard similarity: intersection / union
            intersection = len(student_steps & other_steps)
            union = len(student_steps | other_steps)
            
            if union > 0:
                similarity = intersection / union
                if similarity > 0.3:  # Threshold for similarity
                    similarities.append({
                        'student_id': other_id,
                        'similarity': similarity
                    })
        
        # Sort by similarity
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Return top 20 similar students
        return [s['student_id'] for s in similarities[:20]]
    
    def _get_candidate_pathways(self, similar_students, tenant_slug, skill_level):
        """Get pathways completed by similar students"""
        if not similar_students:
            # Fallback: popular pathways for skill level
            return LearningPathway.objects.filter(
                tenant=tenant_slug,
                difficulty_level=skill_level,
                status='completed'
            ).values_list('id', flat=True)[:20]
        
        # Get pathways from similar students
        pathways = LearningPathway.objects.filter(
            tenant=tenant_slug,
            student_id__in=similar_students,
            status='completed',
            difficulty_level=skill_level
        ).values_list('id', flat=True).distinct()[:50]
        
        return list(pathways)
    
    def _calculate_collaborative_scores(self, student_id, candidate_pathways, similar_students):
        """
        Calculate collaborative filtering scores.
        Score based on: popularity among similar students, completion rates, ratings.
        """
        scores = {}
        
        for pathway_id in candidate_pathways:
            # Count how many similar students completed this pathway
            completions = LearningPathway.objects.filter(
                id=pathway_id,
                student_id__in=similar_students,
                status='completed'
            ).count()
            
            # Get average completion percentage
            avg_completion = LearningPathway.objects.filter(
                id=pathway_id,
                student_id__in=similar_students
            ).aggregate(avg=Avg('completion_percentage'))['avg'] or 0
            
            # Calculate score (normalize by number of similar students)
            if similar_students:
                popularity_score = completions / len(similar_students)
                completion_score = avg_completion / 100
                
                # Combined CF score
                scores[pathway_id] = (0.7 * popularity_score) + (0.3 * completion_score)
            else:
                scores[pathway_id] = 0
        
        return scores
    
    def _calculate_embedding_scores(self, interests, candidate_pathways):
        """
        Calculate content-based scores using embeddings.
        Cosine similarity between user interests and pathway content.
        """
        scores = {}
        
        if not interests:
            # No interests provided, return neutral scores
            return {pid: 0.5 for pid in candidate_pathways}
        
        # For each pathway, calculate similarity with interests
        for pathway_id in candidate_pathways:
            pathway = LearningPathway.objects.get(id=pathway_id)
            
            # Get embeddings for pathway steps
            step_embeddings = ContentEmbedding.objects.filter(
                step__pathway=pathway
            )
            
            if not step_embeddings:
                scores[pathway_id] = 0.5
                continue
            
            # Calculate average embedding similarity
            # In production, you'd use actual sentence embeddings
            # This is a simplified simulation
            total_similarity = 0
            count = 0
            
            for embedding in step_embeddings:
                # Check if step tags match interests
                step_tags = set(embedding.step.tags)
                interest_tags = set(interests)
                
                if step_tags & interest_tags:  # Intersection
                    # Simulate cosine similarity
                    overlap = len(step_tags & interest_tags)
                    total = len(step_tags | interest_tags)
                    similarity = overlap / total if total > 0 else 0
                    total_similarity += similarity
                    count += 1
            
            # Average similarity
            scores[pathway_id] = total_similarity / count if count > 0 else 0.3
        
        return scores
    
    def _generate_recommendation_reasons(self, recommendation, similar_students, interests, pathway):
        """Generate human-readable reasons for the recommendation"""
        reasons = []
        
        # Collaborative filtering reasons
        if recommendation['collaborative_score'] > 0.5:
            reasons.append(
                f"Recommended by {len(similar_students)} students with similar learning patterns"
            )
        
        # Content similarity reasons
        if recommendation['embedding_score'] > 0.4:
            reasons.append(
                f"Matches your interests: {', '.join(interests[:3])}"
            )
        
        # Pathway-specific reasons
        if pathway.completion_percentage > 80:
            reasons.append(
                f"High completion rate ({pathway.completion_percentage:.0f}%)"
            )
        
        if pathway.difficulty_level:
            reasons.append(
                f"Appropriate for {pathway.difficulty_level} level"
            )
        
        return reasons
    
    @action(detail=False, methods=['get'])
    def completion_analytics(self, request, tenant_slug=None):
        """Get completion rate analytics for pathways"""
        pathways = LearningPathway.objects.filter(tenant=tenant_slug)
        
        analytics = {
            'total_pathways': pathways.count(),
            'completed': pathways.filter(status='completed').count(),
            'active': pathways.filter(status='active').count(),
            'average_completion_rate': pathways.aggregate(
                avg=Avg('completion_percentage')
            )['avg'] or 0,
            'by_difficulty': {}
        }
        
        # Breakdown by difficulty
        for difficulty in ['beginner', 'intermediate', 'advanced', 'expert']:
            difficulty_pathways = pathways.filter(difficulty_level=difficulty)
            analytics['by_difficulty'][difficulty] = {
                'total': difficulty_pathways.count(),
                'avg_completion': difficulty_pathways.aggregate(
                    avg=Avg('completion_percentage')
                )['avg'] or 0
            }
        
        return Response(analytics)


class LearningStepViewSet(viewsets.ModelViewSet):
    queryset = LearningStep.objects.all()
    serializer_class = LearningStepSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        pathway_id = self.request.query_params.get('pathway')
        if pathway_id:
            queryset = queryset.filter(pathway_id=pathway_id)
        return queryset


class StudentProgressViewSet(viewsets.ModelViewSet):
    queryset = StudentProgress.objects.all()
    serializer_class = StudentProgressSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_slug = self.kwargs.get('tenant_slug')
        if tenant_slug:
            queryset = queryset.filter(tenant=tenant_slug)
        
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        return queryset


class PathwayRecommendationViewSet(viewsets.ModelViewSet):
    queryset = PathwayRecommendation.objects.all()
    serializer_class = PathwayRecommendationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_slug = self.kwargs.get('tenant_slug')
        if tenant_slug:
            queryset = queryset.filter(tenant=tenant_slug)
        
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        return queryset


class ContentEmbeddingViewSet(viewsets.ModelViewSet):
    queryset = ContentEmbedding.objects.all()
    serializer_class = ContentEmbeddingSerializer
