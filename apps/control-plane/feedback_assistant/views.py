from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Avg, Count
import time
import random

from .models import FeedbackTemplate, GeneratedFeedback, FeedbackCriterion, FeedbackLog
from .serializers import (
    FeedbackTemplateListSerializer, FeedbackTemplateDetailSerializer,
    GeneratedFeedbackListSerializer, GeneratedFeedbackDetailSerializer,
    FeedbackCriterionSerializer, FeedbackLogSerializer,
    GenerateFeedbackRequestSerializer, BatchGenerateFeedbackRequestSerializer
)


class FeedbackTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for FeedbackTemplate management and feedback generation
    """
    
    def get_queryset(self):
        tenant = self.kwargs.get('tenant_slug')
        queryset = FeedbackTemplate.objects.filter(tenant=tenant)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by feedback type
        feedback_type = self.request.query_params.get('feedback_type')
        if feedback_type:
            queryset = queryset.filter(feedback_type=feedback_type)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(template_number__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.select_related('created_by', 'rubric').prefetch_related('criteria', 'generated_feedbacks')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FeedbackTemplateListSerializer
        return FeedbackTemplateDetailSerializer
    
    def perform_create(self, serializer):
        tenant = self.kwargs.get('tenant_slug')
        serializer.save(
            tenant=tenant,
            created_by=self.request.user
        )
    
    @action(detail=True, methods=['post'])
    def generate_feedback(self, request, tenant_slug=None, pk=None):
        """
        Generate personalized feedback for a single student
        """
        template = self.get_object()
        serializer = GenerateFeedbackRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        start_time = time.time()
        
        feedback_data = serializer.validated_data
        
        # Generate personalized feedback
        generated_feedback = self._generate_feedback(template, feedback_data)
        
        generation_time = time.time() - start_time
        generated_feedback.generation_time = generation_time
        generated_feedback.save()
        
        # Update template statistics
        template.total_feedback_generated += 1
        if template.total_feedback_generated > 0:
            total_time = (template.average_generation_time * (template.total_feedback_generated - 1)) + generation_time
            template.average_generation_time = total_time / template.total_feedback_generated
        template.save()
        
        # Create log
        FeedbackLog.objects.create(
            template=template,
            feedback=generated_feedback,
            action='generate_single',
            performed_by=request.user,
            feedbacks_generated=1,
            total_time=generation_time,
            average_sentiment=generated_feedback.sentiment_score,
            average_personalization=generated_feedback.personalization_score
        )
        
        response_serializer = GeneratedFeedbackDetailSerializer(generated_feedback)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def generate_batch(self, request, tenant_slug=None, pk=None):
        """
        Generate feedback for multiple students in batch
        """
        template = self.get_object()
        serializer = BatchGenerateFeedbackRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        feedbacks_data = serializer.validated_data['feedbacks']
        
        start_time = time.time()
        generated_feedbacks = []
        
        for feedback_data in feedbacks_data:
            feedback = self._generate_feedback(template, feedback_data)
            generated_feedbacks.append(feedback)
        
        total_time = time.time() - start_time
        
        # Update template statistics
        template.total_feedback_generated += len(generated_feedbacks)
        if template.total_feedback_generated > 0:
            total_generation_time = (template.average_generation_time * (template.total_feedback_generated - len(generated_feedbacks))) + total_time
            template.average_generation_time = total_generation_time / template.total_feedback_generated
        template.save()
        
        # Calculate average metrics
        avg_sentiment = sum(f.sentiment_score for f in generated_feedbacks) / len(generated_feedbacks)
        avg_personalization = sum(f.personalization_score for f in generated_feedbacks) / len(generated_feedbacks)
        
        # Create log
        FeedbackLog.objects.create(
            template=template,
            action='generate_batch',
            performed_by=request.user,
            feedbacks_generated=len(generated_feedbacks),
            total_time=total_time,
            average_sentiment=avg_sentiment,
            average_personalization=avg_personalization
        )
        
        response_serializer = GeneratedFeedbackListSerializer(generated_feedbacks, many=True)
        
        return Response({
            'message': f'Successfully generated {len(generated_feedbacks)} feedbacks',
            'total_time': total_time,
            'average_time': total_time / len(generated_feedbacks) if generated_feedbacks else 0,
            'feedbacks': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def _generate_feedback(self, template, feedback_data):
        """
        Internal method to generate personalized feedback
        This is a mock implementation - in production, use GPT-4, Claude, etc.
        """
        student_name = feedback_data['student_name']
        score = feedback_data.get('score')
        max_score = feedback_data.get('max_score')
        rubric_scores = feedback_data.get('rubric_scores', {})
        
        # Calculate percentage
        percentage = None
        if score is not None and max_score and max_score > 0:
            percentage = (score / max_score) * 100
        
        # Generate strengths, improvements, and next steps
        strengths = self._generate_strengths(template, percentage, rubric_scores)
        improvements = self._generate_improvements(template, percentage, rubric_scores)
        next_steps = self._generate_next_steps(template, percentage)
        
        # Build feedback text using template
        feedback_parts = []
        
        # Opening
        if template.include_student_name and template.opening_template:
            opening = template.opening_template.replace('{student_name}', student_name)
            feedback_parts.append(opening)
        
        # Score mention
        if percentage is not None:
            score_text = f"\nYou scored {score:.1f} out of {max_score} ({percentage:.1f}%)."
            if percentage >= 85:
                score_text += " Excellent work!"
            elif percentage >= 70:
                score_text += " Good effort!"
            elif percentage >= 50:
                score_text += " You're making progress."
            else:
                score_text += " Let's work on improving this."
            feedback_parts.append(score_text)
        
        # Strengths
        if template.include_strengths and strengths:
            strengths_text = template.strengths_template.replace(
                '{strengths}',
                self._format_list(strengths, template.positivity_level)
            )
            feedback_parts.append(f"\n\n{strengths_text}")
        
        # Improvements
        if template.include_improvements and improvements:
            improvements_text = template.improvements_template.replace(
                '{improvements}',
                self._format_list(improvements, template.directness_level)
            )
            feedback_parts.append(f"\n\n{improvements_text}")
        
        # Next steps
        if template.include_next_steps and next_steps:
            next_steps_text = template.next_steps_template.replace(
                '{next_steps}',
                self._format_list(next_steps, template.positivity_level)
            )
            feedback_parts.append(f"\n\n{next_steps_text}")
        
        # Closing
        if template.include_encouragement and template.closing_template:
            closing = self._personalize_closing(template.closing_template, template.positivity_level)
            feedback_parts.append(f"\n\n{closing}")
        
        feedback_text = ''.join(feedback_parts)
        
        # Calculate sentiment score based on positivity level
        sentiment_score = (template.positivity_level - 5.5) / 4.5  # Maps 1-10 to roughly -1 to +1
        
        # Calculate personalization score
        personalization_score = 0.7  # Base score
        if template.include_student_name:
            personalization_score += 0.1
        if rubric_scores:
            personalization_score += 0.1
        if len(strengths) > 2:
            personalization_score += 0.1
        personalization_score = min(1.0, personalization_score)
        
        # Create GeneratedFeedback
        feedback = GeneratedFeedback.objects.create(
            template=template,
            student_id=feedback_data['student_id'],
            student_name=student_name,
            assessment_title=feedback_data.get('assessment_title', ''),
            score=score,
            max_score=max_score,
            grade=feedback_data.get('grade', ''),
            rubric_scores=rubric_scores,
            feedback_text=feedback_text,
            strengths_identified=strengths,
            improvements_identified=improvements,
            next_steps_suggested=next_steps,
            sentiment_score=round(sentiment_score, 2),
            tone_consistency=0.85 + random.uniform(0, 0.15),  # Mock
            personalization_score=round(personalization_score, 2),
            reading_level=self._determine_reading_level(feedback_text),
            status='generated'
        )
        
        # Flag for review if needed
        if personalization_score < 0.6 or (percentage is not None and percentage < 50):
            feedback.requires_review = True
            feedback.save()
        
        return feedback
    
    def _generate_strengths(self, template, percentage, rubric_scores):
        """Generate strengths based on score and rubric"""
        strengths = []
        
        if percentage is None:
            percentage = 75  # Default for mock
        
        # Mock strengths generation
        strength_pool = [
            "Clear understanding of key concepts",
            "Well-structured responses",
            "Good use of examples and evidence",
            "Strong analytical skills demonstrated",
            "Effective communication of ideas",
            "Creative approach to problem-solving",
            "Thorough research and preparation",
            "Critical thinking evident throughout"
        ]
        
        # Number of strengths based on performance
        num_strengths = 3 if percentage >= 70 else 2 if percentage >= 50 else 1
        
        # Select random strengths (in production, use AI to generate)
        strengths = random.sample(strength_pool, min(num_strengths, len(strength_pool)))
        
        return strengths
    
    def _generate_improvements(self, template, percentage, rubric_scores):
        """Generate improvement areas"""
        improvements = []
        
        if percentage is None:
            percentage = 75
        
        # Mock improvements generation
        improvement_pool = [
            "Provide more detailed explanations",
            "Include additional supporting evidence",
            "Strengthen your conclusion",
            "Improve organization and structure",
            "Develop arguments more thoroughly",
            "Use more specific examples",
            "Check for grammar and spelling",
            "Clarify some technical terminology"
        ]
        
        # Number of improvements based on performance
        num_improvements = 1 if percentage >= 85 else 2 if percentage >= 70 else 3
        
        improvements = random.sample(improvement_pool, min(num_improvements, len(improvement_pool)))
        
        return improvements
    
    def _generate_next_steps(self, template, percentage):
        """Generate actionable next steps"""
        if percentage is None:
            percentage = 75
        
        next_steps_pool = [
            "Review the feedback and reflect on your approach",
            "Practice similar questions to reinforce learning",
            "Seek clarification on any unclear concepts",
            "Review course materials on weaker areas",
            "Discuss your work with peers or tutors",
            "Create a study plan for improvement",
            "Build on your strengths in future assignments"
        ]
        
        num_steps = 2 if percentage >= 70 else 3
        
        return random.sample(next_steps_pool, min(num_steps, len(next_steps_pool)))
    
    def _format_list(self, items, intensity_level):
        """Format list with appropriate tone"""
        if not items:
            return ""
        
        if len(items) == 1:
            return items[0]
        
        # Adjust language based on intensity
        if intensity_level >= 8:
            connector = "Additionally, "
        elif intensity_level >= 5:
            connector = "Also, "
        else:
            connector = ""
        
        formatted = "\n• " + "\n• ".join(items)
        return formatted
    
    def _personalize_closing(self, closing, positivity_level):
        """Personalize closing based on positivity level"""
        if positivity_level >= 8:
            closings = [
                "Keep up the excellent work! You're doing wonderfully!",
                "Outstanding effort! Continue to shine!",
                "You're making fantastic progress! Keep it up!"
            ]
        elif positivity_level >= 6:
            closings = [
                "Keep up the good work!",
                "Well done! Continue working hard!",
                "Great effort! Keep learning and growing!"
            ]
        else:
            closings = [
                "Keep working hard.",
                "Continue to improve.",
                "Stay focused on your goals."
            ]
        
        return random.choice(closings) if closing == "Keep up the great work!" else closing
    
    def _determine_reading_level(self, text):
        """Mock reading level determination"""
        word_count = len(text.split())
        avg_word_length = sum(len(word) for word in text.split()) / word_count if word_count > 0 else 0
        
        if avg_word_length > 6:
            return "University"
        elif avg_word_length > 5:
            return "Grade 11-12"
        else:
            return "Grade 9-10"


class GeneratedFeedbackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing generated feedback
    """
    
    def get_queryset(self):
        tenant = self.kwargs.get('tenant_slug')
        queryset = GeneratedFeedback.objects.filter(template__tenant=tenant)
        
        # Filter by template
        template_id = self.request.query_params.get('template')
        if template_id:
            queryset = queryset.filter(template_id=template_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by review flag
        needs_review = self.request.query_params.get('needs_review')
        if needs_review == 'true':
            queryset = queryset.filter(requires_review=True)
        
        # Filter by student
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        return queryset.select_related('template', 'reviewed_by')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GeneratedFeedbackListSerializer
        return GeneratedFeedbackDetailSerializer
    
    @action(detail=True, methods=['post'])
    def review(self, request, tenant_slug=None, pk=None):
        """Review and potentially revise generated feedback"""
        feedback = self.get_object()
        
        previous_version = feedback.feedback_text
        new_text = request.data.get('feedback_text')
        review_notes = request.data.get('review_notes', '')
        
        if new_text:
            feedback.feedback_text = new_text
            feedback.word_count = len(new_text.split())
        
        feedback.review_notes = review_notes
        feedback.reviewed_by = request.user
        feedback.reviewed_at = timezone.now()
        feedback.status = 'reviewed'
        feedback.requires_review = False
        feedback.save()
        
        # Create log
        FeedbackLog.objects.create(
            template=feedback.template,
            feedback=feedback,
            action='review',
            performed_by=request.user,
            feedbacks_generated=1,
            total_time=0,
            changes_made=review_notes,
            previous_version=previous_version if new_text else ''
        )
        
        serializer = self.get_serializer(feedback)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deliver(self, request, tenant_slug=None, pk=None):
        """Mark feedback as delivered"""
        feedback = self.get_object()
        
        delivery_method = request.data.get('delivery_method', 'portal')
        
        feedback.delivered_at = timezone.now()
        feedback.delivery_method = delivery_method
        feedback.status = 'delivered'
        feedback.save()
        
        # Create log
        FeedbackLog.objects.create(
            template=feedback.template,
            feedback=feedback,
            action='deliver',
            performed_by=request.user,
            feedbacks_generated=1,
            total_time=0,
            details={'delivery_method': delivery_method}
        )
        
        serializer = self.get_serializer(feedback)
        return Response(serializer.data)


class FeedbackCriterionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing feedback criteria
    """
    serializer_class = FeedbackCriterionSerializer
    
    def get_queryset(self):
        tenant = self.kwargs.get('tenant_slug')
        queryset = FeedbackCriterion.objects.filter(template__tenant=tenant)
        
        # Filter by template
        template_id = self.request.query_params.get('template')
        if template_id:
            queryset = queryset.filter(template_id=template_id)
        
        return queryset.select_related('template', 'rubric_criterion')
    
    def perform_create(self, serializer):
        template_id = self.request.data.get('template')
        template = FeedbackTemplate.objects.get(id=template_id)
        
        # Ensure tenant matches
        tenant = self.kwargs.get('tenant_slug')
        if template.tenant != tenant:
            raise ValueError("Template does not belong to this tenant")
        
        serializer.save(template=template)


class FeedbackLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing feedback logs
    """
    serializer_class = FeedbackLogSerializer
    
    def get_queryset(self):
        tenant = self.kwargs.get('tenant_slug')
        queryset = FeedbackLog.objects.filter(template__tenant=tenant)
        
        # Filter by template
        template_id = self.request.query_params.get('template')
        if template_id:
            queryset = queryset.filter(template_id=template_id)
        
        # Filter by action
        action = self.request.query_params.get('action')
        if action:
            queryset = queryset.filter(action=action)
        
        return queryset.select_related('template', 'feedback', 'performed_by')
