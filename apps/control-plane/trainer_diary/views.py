from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
import json

from .models import DiaryEntry, AudioRecording, DailySummary, EvidenceDocument, TranscriptionJob
from .serializers import (
    DiaryEntrySerializer, DiaryEntryListSerializer, AudioRecordingSerializer,
    DailySummarySerializer, EvidenceDocumentSerializer, TranscriptionJobSerializer,
    UploadAudioRequestSerializer, UploadAudioResponseSerializer,
    TranscribeAudioRequestSerializer, TranscribeAudioResponseSerializer,
    GenerateSummaryRequestSerializer, GenerateSummaryResponseSerializer,
    CreateDailySummaryRequestSerializer, CreateDailySummaryResponseSerializer,
    GenerateEvidenceRequestSerializer, GenerateEvidenceResponseSerializer,
    DashboardStatsSerializer, ExportEvidenceRequestSerializer, ExportEvidenceResponseSerializer
)


class DiaryEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for diary entries with speech-to-text and AI summarization"""
    queryset = DiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer
    
    def get_queryset(self):
        queryset = DiaryEntry.objects.all()
        tenant = self.request.query_params.get('tenant')
        trainer_id = self.request.query_params.get('trainer_id')
        status_filter = self.request.query_params.get('status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        if trainer_id:
            queryset = queryset.filter(trainer_id=trainer_id)
        if status_filter:
            queryset = queryset.filter(entry_status=status_filter)
        if start_date:
            queryset = queryset.filter(session_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(session_date__lte=end_date)
        
        return queryset.order_by('-session_date', '-created_at')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DiaryEntryListSerializer
        return DiaryEntrySerializer
    
    @action(detail=False, methods=['post'], url_path='upload-audio')
    def upload_audio(self, request):
        """
        Upload audio recording for a diary entry
        POST /api/diary-entries/upload-audio/
        Body: {diary_entry_id, audio_file, recording_filename, language}
        """
        serializer = UploadAudioRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            diary_entry = DiaryEntry.objects.get(id=serializer.validated_data['diary_entry_id'])
        except DiaryEntry.DoesNotExist:
            return Response({'error': 'Diary entry not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create audio recording
        audio_file = serializer.validated_data['audio_file']
        recording = AudioRecording.objects.create(
            diary_entry=diary_entry,
            recording_filename=serializer.validated_data['recording_filename'],
            recording_file_path=f"/uploads/audio/{audio_file.name}",
            recording_file_size_mb=audio_file.size / (1024 * 1024),
            recording_format=audio_file.name.split('.')[-1].lower(),
            transcript_language=serializer.validated_data.get('language', 'en'),
            processing_status='uploaded'
        )
        
        # Update diary entry status
        diary_entry.entry_status = 'draft'
        diary_entry.save()
        
        response_data = {
            'recording_id': recording.id,
            'recording_number': recording.recording_number,
            'status': 'uploaded',
            'message': 'Audio file uploaded successfully. Ready for transcription.'
        }
        
        response_serializer = UploadAudioResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='transcribe-audio')
    def transcribe_audio(self, request):
        """
        Transcribe audio recording to text using speech-to-text
        POST /api/diary-entries/transcribe-audio/
        Body: {recording_id, transcription_engine, language, enable_speaker_diarization}
        """
        serializer = TranscribeAudioRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            recording = AudioRecording.objects.get(id=serializer.validated_data['recording_id'])
        except AudioRecording.DoesNotExist:
            return Response({'error': 'Audio recording not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create transcription job
        job = TranscriptionJob.objects.create(
            audio_recording=recording,
            transcription_engine=serializer.validated_data.get('transcription_engine', 'whisper'),
            language=serializer.validated_data.get('language', 'en'),
            enable_speaker_diarization=serializer.validated_data.get('enable_speaker_diarization', False),
            job_status='pending'
        )
        
        # Update recording status
        recording.processing_status = 'queued'
        recording.save()
        
        # Update diary entry status
        diary_entry = recording.diary_entry
        diary_entry.entry_status = 'transcribing'
        diary_entry.save()
        
        # Simulate transcription (in production, this would be async with Celery)
        # For now, return job info
        response_data = {
            'job_id': job.id,
            'job_number': job.job_number,
            'status': 'queued',
            'transcript': '',
            'message': 'Transcription job queued. Processing will begin shortly.'
        }
        
        response_serializer = TranscribeAudioResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=False, methods=['post'], url_path='generate-summary')
    def generate_summary(self, request):
        """
        Generate AI-powered summary of teaching session
        POST /api/diary-entries/generate-summary/
        Body: {diary_entry_id, include_transcript, include_manual_notes, summary_style}
        """
        serializer = GenerateSummaryRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            diary_entry = DiaryEntry.objects.get(id=serializer.validated_data['diary_entry_id'])
        except DiaryEntry.DoesNotExist:
            return Response({'error': 'Diary entry not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update status
        diary_entry.entry_status = 'summarizing'
        diary_entry.save()
        
        # Build content for summarization
        content_parts = []
        if serializer.validated_data.get('include_transcript', True) and diary_entry.raw_transcript:
            content_parts.append(f"Transcript: {diary_entry.raw_transcript}")
        if serializer.validated_data.get('include_manual_notes', True) and diary_entry.manual_notes:
            content_parts.append(f"Manual Notes: {diary_entry.manual_notes}")
        
        content_to_summarize = "\n\n".join(content_parts)
        
        # Simulate AI summarization (in production, call OpenAI/Anthropic API)
        summary_text = f"Summary of teaching session for {diary_entry.course_name} on {diary_entry.session_date}. " \
                      f"Duration: {diary_entry.session_duration_minutes} minutes with {diary_entry.student_count} students. " \
                      f"The session covered key learning objectives and engaged students through various activities."
        
        key_topics = ["Learning objective 1", "Key concept 2", "Practical exercise 3"]
        follow_up_actions = ["Prepare additional resources", "Schedule assessment", "Follow up with struggling students"]
        
        # Update diary entry with summary
        diary_entry.session_summary = summary_text
        diary_entry.key_topics_covered = key_topics
        diary_entry.follow_up_actions = follow_up_actions
        diary_entry.summarization_model = 'gpt-4'
        diary_entry.summarization_tokens = 500
        diary_entry.entry_status = 'complete'
        diary_entry.save()
        
        response_data = {
            'diary_entry_id': diary_entry.id,
            'session_summary': summary_text,
            'key_topics_covered': key_topics,
            'follow_up_actions': follow_up_actions,
            'model_used': 'gpt-4',
            'tokens_used': 500
        }
        
        response_serializer = GenerateSummaryResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='create-daily-summary')
    def create_daily_summary(self, request):
        """
        Create daily aggregated summary of teaching activities
        POST /api/diary-entries/create-daily-summary/
        Body: {trainer_id, summary_date, include_draft_entries}
        """
        serializer = CreateDailySummaryRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        trainer_id = serializer.validated_data['trainer_id']
        summary_date = serializer.validated_data['summary_date']
        include_draft = serializer.validated_data.get('include_draft_entries', False)
        
        # Get diary entries for the day
        entries_query = DiaryEntry.objects.filter(
            trainer_id=trainer_id,
            session_date=summary_date
        )
        
        if not include_draft:
            entries_query = entries_query.filter(entry_status='complete')
        
        entries = entries_query.all()
        
        if not entries.exists():
            return Response(
                {'error': 'No diary entries found for this date'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate statistics
        total_sessions = entries.count()
        total_hours = sum(entry.session_duration_minutes for entry in entries) / 60.0
        total_students = sum(entry.student_count for entry in entries)
        courses = list(set(entry.course_name for entry in entries))
        
        # Get first entry for trainer name and tenant
        first_entry = entries.first()
        
        # Check if daily summary already exists
        daily_summary, created = DailySummary.objects.get_or_create(
            tenant=first_entry.tenant,
            trainer_id=trainer_id,
            summary_date=summary_date,
            defaults={
                'trainer_name': first_entry.trainer_name,
                'total_sessions': total_sessions,
                'total_teaching_hours': total_hours,
                'total_students': total_students,
                'courses_taught': courses,
                'diary_entries_included': [entry.id for entry in entries],
                'generated_by_model': 'gpt-4'
            }
        )
        
        if not created:
            # Update existing summary
            daily_summary.total_sessions = total_sessions
            daily_summary.total_teaching_hours = total_hours
            daily_summary.total_students = total_students
            daily_summary.courses_taught = courses
            daily_summary.diary_entries_included = [entry.id for entry in entries]
            daily_summary.save()
        
        response_data = {
            'summary_id': daily_summary.id,
            'summary_number': daily_summary.summary_number,
            'total_sessions': total_sessions,
            'total_teaching_hours': total_hours,
            'message': 'Daily summary created successfully' if created else 'Daily summary updated successfully'
        }
        
        response_serializer = CreateDailySummaryResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], url_path='generate-evidence')
    def generate_evidence(self, request):
        """
        Generate evidence document from diary entry
        POST /api/diary-entries/generate-evidence/
        Body: {diary_entry_id, document_type, document_format, include_attachments}
        """
        serializer = GenerateEvidenceRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            diary_entry = DiaryEntry.objects.get(id=serializer.validated_data['diary_entry_id'])
        except DiaryEntry.DoesNotExist:
            return Response({'error': 'Diary entry not found'}, status=status.HTTP_404_NOT_FOUND)
        
        document_type = serializer.validated_data['document_type']
        document_format = serializer.validated_data.get('document_format', 'markdown')
        
        # Generate document title
        type_titles = {
            'session_plan': 'Session Plan',
            'attendance_record': 'Attendance Record',
            'teaching_evidence': 'Teaching Evidence',
            'assessment_record': 'Assessment Record',
            'student_feedback': 'Student Feedback Summary',
            'compliance_report': 'Compliance Report',
            'professional_reflection': 'Professional Reflection'
        }
        
        document_title = f"{type_titles.get(document_type, 'Document')} - {diary_entry.course_name} ({diary_entry.session_date})"
        
        # Generate document content (in production, use templates or AI)
        document_content = f"""
# {document_title}

**Date:** {diary_entry.session_date}
**Course:** {diary_entry.course_name}
**Trainer:** {diary_entry.trainer_name}
**Duration:** {diary_entry.session_duration_minutes} minutes
**Students:** {diary_entry.student_count}

## Session Summary
{diary_entry.session_summary or 'No summary available'}

## Key Topics Covered
{chr(10).join(f"- {topic}" for topic in diary_entry.key_topics_covered)}

## Follow-up Actions
{chr(10).join(f"- {action}" for action in diary_entry.follow_up_actions)}

## Learning Outcomes Addressed
{chr(10).join(f"- {outcome}" for outcome in diary_entry.learning_outcomes_addressed)}
"""
        
        # Create evidence document
        evidence_doc = EvidenceDocument.objects.create(
            diary_entry=diary_entry,
            document_type=document_type,
            document_title=document_title,
            document_content=document_content,
            document_format=document_format,
            file_path=f"/evidence/{diary_entry.entry_number}_{document_type}.{document_format}",
            generated_by=diary_entry.trainer_name,
            generation_method='auto_ai',
            meets_compliance_standards=True
        )
        
        response_data = {
            'document_id': evidence_doc.id,
            'document_number': evidence_doc.document_number,
            'document_title': document_title,
            'document_content': document_content,
            'file_path': evidence_doc.file_path,
            'message': 'Evidence document generated successfully'
        }
        
        response_serializer = GenerateEvidenceResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        """
        Get dashboard statistics for trainer diary
        GET /api/diary-entries/dashboard/?trainer_id=X&tenant=Y
        """
        trainer_id = request.query_params.get('trainer_id')
        tenant = request.query_params.get('tenant')
        
        if not trainer_id or not tenant:
            return Response(
                {'error': 'trainer_id and tenant are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Date ranges
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Query all entries for trainer
        all_entries = DiaryEntry.objects.filter(tenant=tenant, trainer_id=trainer_id)
        
        # Statistics
        total_entries = all_entries.count()
        entries_this_week = all_entries.filter(session_date__gte=week_ago).count()
        entries_this_month = all_entries.filter(session_date__gte=month_ago).count()
        
        total_teaching_hours = all_entries.aggregate(
            total=Sum('session_duration_minutes')
        )['total'] or 0
        total_teaching_hours = total_teaching_hours / 60.0
        
        total_students_taught = all_entries.aggregate(
            total=Sum('student_count')
        )['total'] or 0
        
        total_recordings = AudioRecording.objects.filter(
            diary_entry__tenant=tenant,
            diary_entry__trainer_id=trainer_id
        ).count()
        
        pending_transcriptions = AudioRecording.objects.filter(
            diary_entry__tenant=tenant,
            diary_entry__trainer_id=trainer_id,
            processing_status__in=['uploaded', 'queued', 'processing']
        ).count()
        
        daily_summaries_count = DailySummary.objects.filter(
            tenant=tenant,
            trainer_id=trainer_id
        ).count()
        
        evidence_documents_count = EvidenceDocument.objects.filter(
            diary_entry__tenant=tenant,
            diary_entry__trainer_id=trainer_id
        ).count()
        
        # Recent entries
        recent_entries = all_entries.order_by('-session_date', '-created_at')[:10]
        recent_entries_data = DiaryEntryListSerializer(recent_entries, many=True).data
        
        # Courses taught
        courses_taught = list(all_entries.values_list('course_name', flat=True).distinct())
        
        dashboard_data = {
            'total_entries': total_entries,
            'entries_this_week': entries_this_week,
            'entries_this_month': entries_this_month,
            'total_teaching_hours': round(total_teaching_hours, 2),
            'total_students_taught': total_students_taught,
            'total_recordings': total_recordings,
            'pending_transcriptions': pending_transcriptions,
            'daily_summaries_count': daily_summaries_count,
            'evidence_documents_count': evidence_documents_count,
            'recent_entries': recent_entries_data,
            'courses_taught': courses_taught
        }
        
        response_serializer = DashboardStatsSerializer(data=dashboard_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='export-evidence')
    def export_evidence(self, request):
        """
        Export evidence documents for date range
        POST /api/diary-entries/export-evidence/
        Body: {trainer_id, start_date, end_date, export_format, include_transcripts, include_summaries, include_evidence_docs}
        """
        serializer = ExportEvidenceRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        trainer_id = serializer.validated_data['trainer_id']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        export_format = serializer.validated_data.get('export_format', 'pdf')
        
        # Get entries in date range
        entries = DiaryEntry.objects.filter(
            trainer_id=trainer_id,
            session_date__gte=start_date,
            session_date__lte=end_date,
            entry_status='complete'
        )
        
        if not entries.exists():
            return Response(
                {'error': 'No completed entries found in this date range'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Simulate export (in production, generate actual file)
        export_file_path = f"/exports/evidence_{trainer_id}_{start_date}_{end_date}.{export_format}"
        export_file_size = 2.5  # MB
        
        response_data = {
            'export_file_path': export_file_path,
            'export_file_size_mb': export_file_size,
            'total_entries': entries.count(),
            'date_range': f"{start_date} to {end_date}",
            'message': f'Evidence exported successfully to {export_format}'
        }
        
        response_serializer = ExportEvidenceResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class AudioRecordingViewSet(viewsets.ModelViewSet):
    """ViewSet for audio recordings"""
    queryset = AudioRecording.objects.all()
    serializer_class = AudioRecordingSerializer
    
    def get_queryset(self):
        queryset = AudioRecording.objects.all()
        diary_entry_id = self.request.query_params.get('diary_entry_id')
        status_filter = self.request.query_params.get('status')
        
        if diary_entry_id:
            queryset = queryset.filter(diary_entry_id=diary_entry_id)
        if status_filter:
            queryset = queryset.filter(processing_status=status_filter)
        
        return queryset.order_by('-uploaded_at')


class DailySummaryViewSet(viewsets.ModelViewSet):
    """ViewSet for daily summaries"""
    queryset = DailySummary.objects.all()
    serializer_class = DailySummarySerializer
    
    def get_queryset(self):
        queryset = DailySummary.objects.all()
        trainer_id = self.request.query_params.get('trainer_id')
        tenant = self.request.query_params.get('tenant')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        if trainer_id:
            queryset = queryset.filter(trainer_id=trainer_id)
        if start_date:
            queryset = queryset.filter(summary_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(summary_date__lte=end_date)
        
        return queryset.order_by('-summary_date')


class EvidenceDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for evidence documents"""
    queryset = EvidenceDocument.objects.all()
    serializer_class = EvidenceDocumentSerializer
    
    def get_queryset(self):
        queryset = EvidenceDocument.objects.all()
        diary_entry_id = self.request.query_params.get('diary_entry_id')
        document_type = self.request.query_params.get('document_type')
        
        if diary_entry_id:
            queryset = queryset.filter(diary_entry_id=diary_entry_id)
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        
        return queryset.order_by('-created_at')


class TranscriptionJobViewSet(viewsets.ModelViewSet):
    """ViewSet for transcription jobs"""
    queryset = TranscriptionJob.objects.all()
    serializer_class = TranscriptionJobSerializer
    
    def get_queryset(self):
        queryset = TranscriptionJob.objects.all()
        recording_id = self.request.query_params.get('recording_id')
        job_status = self.request.query_params.get('status')
        
        if recording_id:
            queryset = queryset.filter(audio_recording_id=recording_id)
        if job_status:
            queryset = queryset.filter(job_status=job_status)
        
        return queryset.order_by('-created_at')
