from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Avg, Count, Sum, Q
import random
import time
from datetime import timedelta

from .models import (
    StudentMessage, DraftReply, MessageTemplate,
    ConversationThread, ToneProfile, ReplyHistory
)
from .serializers import *


class StudentMessageViewSet(viewsets.ModelViewSet):
    queryset = StudentMessage.objects.all()
    serializer_class = StudentMessageSerializer
    
    def get_queryset(self):
        queryset = StudentMessage.objects.all()
        tenant = self.request.query_params.get('tenant')
        status_filter = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')
        
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def generate_reply(self, request):
        """Generate AI draft reply to a student message"""
        serializer = GenerateReplyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message_id = serializer.validated_data['message_id']
        tone = serializer.validated_data['tone']
        formality_level = serializer.validated_data['formality_level']
        include_greeting = serializer.validated_data['include_greeting']
        include_signature = serializer.validated_data['include_signature']
        template_id = serializer.validated_data.get('template_id')
        additional_context = serializer.validated_data.get('additional_context', '')
        max_words = serializer.validated_data['max_words']
        
        try:
            message = StudentMessage.objects.get(id=message_id)
        except StudentMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Simulate LLM generation (in production, this would call OpenAI/Anthropic)
        start_time = time.time()
        
        # Generate reply based on tone
        greeting = f"Hi {message.student_name},\n\n" if include_greeting else ""
        signature = "\n\nBest regards,\nSupport Team" if include_signature else ""
        
        # Sample generated replies based on tone
        tone_responses = {
            'professional': f"{greeting}Thank you for your inquiry regarding {message.subject}.\n\nI understand your concern and would like to assist you with this matter. Based on the information provided, I can confirm that we will review your request and provide you with a detailed response within 24-48 hours.\n\nPlease don't hesitate to reach out if you have any additional questions in the meantime.{signature}",
            
            'friendly': f"{greeting}Thanks so much for reaching out!\n\nI totally understand your question about {message.subject}. Let me help you with that! We'll take a look at this and get back to you super soon - probably within a day or two.\n\nFeel free to shoot me another message if you think of anything else!{signature}",
            
            'empathetic': f"{greeting}Thank you for getting in touch, and I'm sorry to hear you're experiencing difficulty with {message.subject}.\n\nI completely understand how frustrating this must be for you. Please know that we're here to help and will do everything we can to resolve this for you as quickly as possible.\n\nWe'll review your situation carefully and get back to you within the next 24-48 hours with a solution.{signature}",
            
            'formal': f"{greeting}We acknowledge receipt of your communication regarding {message.subject}.\n\nYour inquiry has been received and is currently under review by the appropriate department. You may expect a comprehensive response within two business days.\n\nShould you require further clarification, please do not hesitate to contact us.{signature}",
            
            'casual': f"{greeting}Hey! Thanks for the message.\n\nI saw your question about {message.subject} - we'll check that out for you. Should have an answer back to you in a day or two.\n\nJust let us know if there's anything else!{signature}"
        }
        
        reply_body = tone_responses.get(tone, tone_responses['professional'])
        
        # If template provided, merge it
        if template_id:
            try:
                template = MessageTemplate.objects.get(id=template_id)
                template.usage_count += 1
                template.last_used_at = timezone.now()
                template.save()
                
                # Replace placeholders
                template_body = template.template_body
                template_body = template_body.replace('{student_name}', message.student_name)
                template_body = template_body.replace('{subject}', message.subject)
                reply_body = template_body
            except MessageTemplate.DoesNotExist:
                pass
        
        generation_time_ms = int((time.time() - start_time) * 1000)
        
        # Create draft
        draft = DraftReply.objects.create(
            student_message=message,
            reply_body=reply_body,
            reply_subject=f"Re: {message.subject}",
            tone_used=tone,
            formality_level=formality_level,
            include_greeting=include_greeting,
            include_signature=include_signature,
            template_used_id=template_id,
            confidence_score=random.uniform(0.75, 0.95),
            generation_time_ms=generation_time_ms,
            llm_model_used='gpt-4',
            generation_prompt=f"Generate {tone} reply to: {message.subject}"
        )
        
        # Update message status
        message.status = 'draft_generated'
        message.save()
        
        response_serializer = GenerateReplyResponseSerializer(data={
            'draft_id': draft.id,
            'draft_number': draft.draft_number,
            'reply_body': draft.reply_body,
            'reply_subject': draft.reply_subject,
            'confidence_score': draft.confidence_score,
            'word_count': draft.word_count,
            'generation_time_ms': generation_time_ms,
            'message': f'Draft reply generated successfully with {tone} tone'
        })
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def refine_tone(self, request):
        """Refine the tone of an existing draft"""
        serializer = RefineToneRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        draft_id = serializer.validated_data['draft_id']
        new_tone = serializer.validated_data['new_tone']
        make_shorter = serializer.validated_data['make_shorter']
        make_longer = serializer.validated_data['make_longer']
        add_empathy = serializer.validated_data['add_empathy']
        
        try:
            draft = DraftReply.objects.get(id=draft_id)
        except DraftReply.DoesNotExist:
            return Response({'error': 'Draft not found'}, status=status.HTTP_404_NOT_FOUND)
        
        original_reply = draft.reply_body
        original_word_count = draft.word_count
        
        # Simulate tone refinement (in production, this would use LLM)
        refined_reply = original_reply
        changes_made = []
        
        if new_tone != draft.tone_used:
            # Adjust tone markers
            if new_tone == 'formal':
                refined_reply = refined_reply.replace("Thanks", "Thank you")
                refined_reply = refined_reply.replace("can't", "cannot")
                changes_made.append(f"Changed tone to {new_tone}")
            elif new_tone == 'casual':
                refined_reply = refined_reply.replace("Thank you", "Thanks")
                refined_reply = refined_reply.replace("cannot", "can't")
                changes_made.append(f"Made more casual")
        
        if make_shorter:
            # Simulate shortening
            lines = refined_reply.split('\n')
            refined_reply = '\n'.join(lines[:max(3, len(lines)-2)])
            changes_made.append("Made response more concise")
        
        if make_longer:
            refined_reply += "\n\nAdditionally, please feel free to reach out if you need any further clarification on this matter."
            changes_made.append("Added additional context")
        
        if add_empathy:
            if "I understand" not in refined_reply:
                refined_reply = refined_reply.replace(
                    "Thank you for your inquiry",
                    "Thank you for your inquiry. I understand this may be concerning"
                )
                changes_made.append("Increased empathy level")
        
        # Update draft
        draft.reply_body = refined_reply
        draft.tone_used = new_tone
        draft.was_edited = True
        draft.save()
        
        response_serializer = RefineToneResponseSerializer(data={
            'draft_id': draft.id,
            'original_reply': original_reply,
            'refined_reply': refined_reply,
            'original_word_count': original_word_count,
            'refined_word_count': draft.word_count,
            'tone_used': new_tone,
            'changes_made': changes_made,
            'message': 'Tone refined successfully'
        })
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data)
    
    @action(detail=False, methods=['post'])
    def save_template(self, request):
        """Save a draft or custom text as a reusable template"""
        serializer = SaveTemplateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tenant = request.query_params.get('tenant', 'default')
        draft_id = serializer.validated_data.get('draft_id')
        template_body = serializer.validated_data['template_body']
        name = serializer.validated_data['name']
        description = serializer.validated_data.get('description', '')
        template_type = serializer.validated_data['template_type']
        default_tone = serializer.validated_data['default_tone']
        placeholders = serializer.validated_data.get('placeholders', [])
        
        # Create template
        template = MessageTemplate.objects.create(
            tenant=tenant,
            name=name,
            description=description,
            template_type=template_type,
            template_body=template_body,
            default_tone=default_tone,
            placeholders=placeholders,
            is_system_template=False
        )
        
        response_serializer = SaveTemplateResponseSerializer(data={
            'template_id': template.id,
            'template_number': template.template_number,
            'name': template.name,
            'template_type': template.template_type,
            'placeholders': template.placeholders,
            'message': 'Template saved successfully'
        })
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def suggest_replies(self, request):
        """Generate multiple reply suggestions with different tones"""
        serializer = SuggestRepliesRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message_id = serializer.validated_data['message_id']
        num_suggestions = serializer.validated_data['num_suggestions']
        
        try:
            message = StudentMessage.objects.get(id=message_id)
        except StudentMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate suggestions with different tones
        tones = ['professional', 'friendly', 'empathetic']
        suggestions = []
        
        for i in range(min(num_suggestions, len(tones))):
            tone = tones[i]
            
            # Quick draft generation
            greeting = f"Hi {message.student_name},\n\n"
            
            if tone == 'professional':
                body = f"Thank you for your inquiry regarding {message.subject}. We will review this and respond within 24 hours."
            elif tone == 'friendly':
                body = f"Thanks for reaching out! I'll look into your question about {message.subject} and get back to you soon."
            else:  # empathetic
                body = f"I understand your concern about {message.subject}. Let me help you with this right away."
            
            suggestions.append({
                'tone': tone,
                'preview': greeting + body,
                'word_count': len((greeting + body).split()),
                'confidence': random.uniform(0.75, 0.92)
            })
        
        response_serializer = SuggestRepliesResponseSerializer(data={
            'message_id': message.id,
            'suggestions': suggestions,
            'message': f'Generated {len(suggestions)} reply suggestions'
        })
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data)
    
    @action(detail=False, methods=['post'])
    def analyze_sentiment(self, request):
        """Analyze sentiment and urgency of a message"""
        serializer = AnalyzeSentimentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        message_id = serializer.validated_data['message_id']
        
        try:
            message = StudentMessage.objects.get(id=message_id)
        except StudentMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Simulate sentiment analysis (in production, use NLP model)
        message_lower = message.message_body.lower()
        
        # Detect sentiment
        negative_words = ['angry', 'frustrated', 'disappointed', 'upset', 'complaint', 'unacceptable']
        positive_words = ['thank', 'appreciate', 'great', 'excellent', 'wonderful']
        urgent_words = ['urgent', 'asap', 'immediately', 'emergency', 'deadline']
        
        negative_count = sum(word in message_lower for word in negative_words)
        positive_count = sum(word in message_lower for word in positive_words)
        urgent_count = sum(word in message_lower for word in urgent_words)
        
        if negative_count > positive_count:
            sentiment = 'negative'
            sentiment_score = 0.3
            recommended_tone = 'empathetic'
        elif positive_count > negative_count:
            sentiment = 'positive'
            sentiment_score = 0.8
            recommended_tone = 'friendly'
        else:
            sentiment = 'neutral'
            sentiment_score = 0.5
            recommended_tone = 'professional'
        
        if urgent_count > 0 or message.priority == 'urgent':
            urgency_level = 'high'
            recommended_priority = 'urgent'
        else:
            urgency_level = 'medium'
            recommended_priority = 'medium'
        
        # Extract topics (simplified)
        detected_topics = []
        if 'assessment' in message_lower or 'exam' in message_lower:
            detected_topics.append('assessment')
        if 'deadline' in message_lower or 'extension' in message_lower:
            detected_topics.append('deadline')
        if 'enroll' in message_lower:
            detected_topics.append('enrollment')
        if 'technical' in message_lower or 'login' in message_lower or 'access' in message_lower:
            detected_topics.append('technical_support')
        
        # Update message
        message.detected_sentiment = sentiment
        message.detected_topics = detected_topics
        message.priority = recommended_priority
        message.save()
        
        response_serializer = AnalyzeSentimentResponseSerializer(data={
            'message_id': message.id,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'urgency_level': urgency_level,
            'detected_topics': detected_topics,
            'recommended_tone': recommended_tone,
            'recommended_priority': recommended_priority,
            'analysis_details': {
                'negative_indicators': negative_count,
                'positive_indicators': positive_count,
                'urgent_indicators': urgent_count
            },
            'message': 'Sentiment analysis completed'
        })
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data)
    
    @action(detail=False, methods=['post'])
    def send_reply(self, request):
        """Mark a draft as sent and record metrics"""
        serializer = SendReplyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        draft_id = serializer.validated_data['draft_id']
        final_reply_body = serializer.validated_data['final_reply_body']
        final_subject = serializer.validated_data['final_subject']
        sent_by = serializer.validated_data['sent_by']
        edit_count = serializer.validated_data['edit_count']
        
        try:
            draft = DraftReply.objects.get(id=draft_id)
        except DraftReply.DoesNotExist:
            return Response({'error': 'Draft not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Mark draft as sent
        draft.was_sent = True
        draft.sent_at = timezone.now()
        if edit_count > 0:
            draft.was_edited = True
        draft.save()
        
        # Update message status
        message = draft.student_message
        message.status = 'replied'
        message.save()
        
        # Calculate time metrics
        time_to_first_draft = (draft.generated_at - message.received_date).total_seconds()
        time_to_send = (timezone.now() - message.received_date).total_seconds()
        
        # Create history record
        history = ReplyHistory.objects.create(
            student_message=message,
            draft_reply=draft,
            final_reply_body=final_reply_body,
            final_subject=final_subject,
            time_to_first_draft_seconds=int(time_to_first_draft),
            time_to_send_seconds=int(time_to_send),
            edit_count=edit_count,
            estimated_manual_time_seconds=300,  # 5 minutes estimate
            sent_by=sent_by,
            sent_at=timezone.now()
        )
        
        response_serializer = SendReplyResponseSerializer(data={
            'history_id': history.id,
            'history_number': history.history_number,
            'time_saved_seconds': history.time_saved_seconds,
            'time_saved_percentage': history.time_saved_percentage,
            'message': f'Reply sent successfully. Time saved: {history.time_saved_percentage:.1f}%'
        })
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get dashboard statistics and metrics"""
        tenant = request.query_params.get('tenant')
        
        if not tenant:
            return Response({'error': 'Tenant parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Message statistics
        messages = StudentMessage.objects.filter(tenant=tenant)
        total_messages = messages.count()
        new_messages = messages.filter(status='new').count()
        draft_generated = messages.filter(status='draft_generated').count()
        replied_messages = messages.filter(status='replied').count()
        
        # Draft statistics
        drafts = DraftReply.objects.filter(student_message__tenant=tenant)
        total_drafts = drafts.count()
        drafts_sent = drafts.filter(was_sent=True).count()
        drafts_rejected = drafts.filter(was_rejected=True).count()
        avg_confidence = drafts.aggregate(avg=Avg('confidence_score'))['avg'] or 0.0
        
        # Template statistics
        templates = MessageTemplate.objects.filter(tenant=tenant)
        total_templates = templates.count()
        active_templates = templates.filter(is_active=True).count()
        
        # Time saved statistics
        history = ReplyHistory.objects.filter(student_message__tenant=tenant)
        total_time_saved = history.aggregate(total=Sum('time_saved_seconds'))['total'] or 0
        total_time_saved_hours = total_time_saved / 3600
        avg_time_saved = history.aggregate(avg=Avg('time_saved_seconds'))['avg'] or 0
        avg_time_saved_pct = history.aggregate(avg=Avg('time_saved_percentage'))['avg'] or 0
        total_replies_sent = history.count()
        
        # Messages by priority
        messages_by_priority = {
            'urgent': messages.filter(priority='urgent').count(),
            'high': messages.filter(priority='high').count(),
            'medium': messages.filter(priority='medium').count(),
            'low': messages.filter(priority='low').count(),
        }
        
        # Messages by sentiment
        messages_by_sentiment = {
            'positive': messages.filter(detected_sentiment='positive').count(),
            'neutral': messages.filter(detected_sentiment='neutral').count(),
            'negative': messages.filter(detected_sentiment='negative').count(),
        }
        
        # Recent data
        recent_messages = messages.order_by('-received_date')[:10]
        recent_drafts = drafts.order_by('-generated_at')[:10]
        top_templates = templates.filter(is_active=True).order_by('-usage_count')[:5]
        
        dashboard_data = {
            'total_messages': total_messages,
            'new_messages': new_messages,
            'draft_generated': draft_generated,
            'replied_messages': replied_messages,
            'total_drafts': total_drafts,
            'drafts_sent': drafts_sent,
            'drafts_rejected': drafts_rejected,
            'avg_confidence_score': round(avg_confidence, 2),
            'total_templates': total_templates,
            'active_templates': active_templates,
            'total_time_saved_hours': round(total_time_saved_hours, 2),
            'avg_time_saved_per_reply_seconds': int(avg_time_saved),
            'time_saved_percentage': round(avg_time_saved_pct, 1),
            'total_replies_sent': total_replies_sent,
            'messages_by_priority': messages_by_priority,
            'messages_by_sentiment': messages_by_sentiment,
            'recent_messages': StudentMessageListSerializer(recent_messages, many=True).data,
            'recent_drafts': DraftReplyListSerializer(recent_drafts, many=True).data,
            'top_templates': MessageTemplateListSerializer(top_templates, many=True).data,
        }
        
        serializer = DashboardStatsSerializer(data=dashboard_data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)


class DraftReplyViewSet(viewsets.ModelViewSet):
    queryset = DraftReply.objects.all()
    serializer_class = DraftReplySerializer


class MessageTemplateViewSet(viewsets.ModelViewSet):
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer
    
    def get_queryset(self):
        queryset = MessageTemplate.objects.all()
        tenant = self.request.query_params.get('tenant')
        template_type = self.request.query_params.get('type')
        is_active = self.request.query_params.get('is_active')
        
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        if template_type:
            queryset = queryset.filter(template_type=template_type)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset


class ConversationThreadViewSet(viewsets.ModelViewSet):
    queryset = ConversationThread.objects.all()
    serializer_class = ConversationThreadSerializer


class ToneProfileViewSet(viewsets.ModelViewSet):
    queryset = ToneProfile.objects.all()
    serializer_class = ToneProfileSerializer


class ReplyHistoryViewSet(viewsets.ModelViewSet):
    queryset = ReplyHistory.objects.all()
    serializer_class = ReplyHistorySerializer
