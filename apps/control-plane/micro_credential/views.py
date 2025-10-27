from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import time
import os

from .models import MicroCredential, MicroCredentialVersion, MicroCredentialEnrollment
from .serializers import (
    MicroCredentialSerializer, 
    MicroCredentialVersionSerializer,
    MicroCredentialEnrollmentSerializer
)
from tenants.models import Tenant


@method_decorator(csrf_exempt, name='dispatch')
class MicroCredentialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing micro-credentials (short courses).
    """
    serializer_class = MicroCredentialSerializer
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production

    def get_queryset(self):
        tenant_slug = self.kwargs.get('tenant_slug')
        tenant = get_object_or_404(Tenant, slug=tenant_slug)
        return MicroCredential.objects.filter(tenant=tenant)

    def perform_create(self, serializer):
        tenant_slug = self.kwargs.get('tenant_slug')
        tenant = get_object_or_404(Tenant, slug=tenant_slug)
        # Use request.user if authenticated, otherwise use None
        created_by = self.request.user if self.request.user.is_authenticated else None
        serializer.save(tenant=tenant, created_by=created_by)

    @action(detail=False, methods=['post'])
    def generate_from_units(self, request, tenant_slug=None):
        """
        Generate a micro-credential using AI from selected units.
        """
        tenant = get_object_or_404(Tenant, slug=tenant_slug)
        
        # Extract request data
        unit_codes = request.data.get('unit_codes', [])
        title = request.data.get('title', '')
        target_duration = request.data.get('target_duration', 40)
        delivery_mode = request.data.get('delivery_mode', 'blended')
        target_audience = request.data.get('target_audience', '')
        
        if not unit_codes:
            return Response(
                {'error': 'At least one unit code is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        start_time = time.time()
        
        # TODO: Replace with actual AI generation using OpenAI/Anthropic
        # For now, create a basic structure
        
        # Mock unit data (in production, fetch from training.gov.au API or database)
        mock_units = [
            {
                'code': code,
                'title': f'Unit Title for {code}',
                'nominal_hours': 20,
                'elements': [
                    'Plan and prepare for work',
                    'Conduct work activities',
                    'Complete and document work'
                ]
            }
            for code in unit_codes
        ]
        
        # Generate learning outcomes from unit elements
        learning_outcomes = []
        skills_covered = []
        for unit in mock_units:
            for element in unit.get('elements', []):
                learning_outcomes.append(f"Apply {element.lower()} in {unit['code']}")
                skills_covered.append(element)
        
        # Create compressed content structure
        compressed_content = {
            'key_competencies': [
                'Professional communication',
                'Problem-solving',
                'Technical skills application'
            ],
            'learning_modules': [
                {
                    'module_number': 1,
                    'title': 'Foundation Skills',
                    'duration_hours': target_duration * 0.3,
                    'topics': ['Industry context', 'Safety requirements', 'Basic procedures']
                },
                {
                    'module_number': 2,
                    'title': 'Core Competencies',
                    'duration_hours': target_duration * 0.5,
                    'topics': ['Practical application', 'Skills development', 'Quality standards']
                },
                {
                    'module_number': 3,
                    'title': 'Advanced Application',
                    'duration_hours': target_duration * 0.2,
                    'topics': ['Complex scenarios', 'Integration', 'Professional practice']
                }
            ],
            'compression_notes': f'Content compressed from {len(unit_codes)} full units into focused micro-credential'
        }
        
        # Generate assessment tasks
        assessment_tasks = [
            {
                'task_number': 1,
                'title': 'Knowledge Assessment',
                'type': 'written',
                'description': 'Written questions covering key concepts and procedures',
                'weighting': 40,
                'mapped_elements': [u['code'] for u in mock_units]
            },
            {
                'task_number': 2,
                'title': 'Practical Demonstration',
                'type': 'practical',
                'description': 'Demonstrate competencies in workplace or simulated environment',
                'weighting': 60,
                'mapped_elements': [u['code'] for u in mock_units]
            }
        ]
        
        # Auto-generate code if not provided
        if not title:
            title = f"Micro-Credential: {', '.join(unit_codes[:2])}"
            if len(unit_codes) > 2:
                title += f" (+{len(unit_codes) - 2} more)"
        
        code = f"MC-{unit_codes[0]}-{int(time.time()) % 10000}"
        
        # Determine tags and industry sectors from unit codes
        tags = ['micro-credential', 'short-course'] + unit_codes
        industry_sectors = self._extract_industry_from_units(unit_codes)
        
        generation_time = time.time() - start_time
        
        # Create the micro-credential
        micro_credential = MicroCredential.objects.create(
            tenant=tenant,
            title=title,
            code=code,
            description=f"Focused micro-credential covering key competencies from {len(unit_codes)} training package units.",
            duration_hours=target_duration,
            delivery_mode=delivery_mode,
            target_audience=target_audience or "Professionals seeking targeted upskilling",
            learning_outcomes=learning_outcomes[:10],  # Limit to top 10
            source_units=mock_units,
            compressed_content=compressed_content,
            tags=tags,
            skills_covered=list(set(skills_covered))[:15],  # Deduplicated top 15
            industry_sectors=industry_sectors,
            assessment_strategy=f"Two-part assessment strategy combining theoretical knowledge and practical demonstration.",
            assessment_tasks=assessment_tasks,
            status='draft',
            gpt_generated=True,
            gpt_model_used=os.getenv('OPENAI_MODEL', 'gpt-4'),
            generation_time_seconds=generation_time,
            created_by=request.user if request.user.is_authenticated else None
        )
        
        serializer = self.get_serializer(micro_credential)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def _extract_industry_from_units(self, unit_codes):
        """Extract industry sectors from unit code prefixes."""
        industry_map = {
            'ICT': 'Information Technology',
            'BSB': 'Business Services',
            'FNS': 'Financial Services',
            'CHC': 'Community Services',
            'SIT': 'Tourism, Hospitality & Events',
            'AUR': 'Automotive',
            'CPC': 'Construction',
            'HLT': 'Health',
        }
        
        industries = []
        for code in unit_codes:
            prefix = code[:3].upper()
            if prefix in industry_map:
                industries.append(industry_map[prefix])
        
        return list(set(industries))
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None, tenant_slug=None):
        """Publish a micro-credential."""
        micro_credential = self.get_object()
        micro_credential.status = 'published'
        micro_credential.published_at = timezone.now()
        micro_credential.save()
        
        serializer = self.get_serializer(micro_credential)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None, tenant_slug=None):
        """Duplicate a micro-credential."""
        original = self.get_object()
        
        # Create a copy
        duplicate = MicroCredential.objects.create(
            tenant=original.tenant,
            title=f"{original.title} (Copy)",
            code=f"{original.code}-COPY-{int(time.time()) % 10000}",
            description=original.description,
            duration_hours=original.duration_hours,
            delivery_mode=original.delivery_mode,
            target_audience=original.target_audience,
            learning_outcomes=original.learning_outcomes.copy(),
            source_units=original.source_units.copy(),
            compressed_content=original.compressed_content.copy(),
            tags=original.tags.copy(),
            skills_covered=original.skills_covered.copy(),
            industry_sectors=original.industry_sectors.copy(),
            aqf_level=original.aqf_level,
            assessment_strategy=original.assessment_strategy,
            assessment_tasks=original.assessment_tasks.copy(),
            price=original.price,
            max_participants=original.max_participants,
            prerequisites=original.prerequisites,
            status='draft',
            created_by=request.user if request.user.is_authenticated else None
        )
        
        serializer = self.get_serializer(duplicate)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MicroCredentialVersionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing micro-credential version history.
    """
    serializer_class = MicroCredentialVersionSerializer
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production

    def get_queryset(self):
        tenant_slug = self.kwargs.get('tenant_slug')
        micro_credential_id = self.kwargs.get('micro_credential_id')
        
        tenant = get_object_or_404(Tenant, slug=tenant_slug)
        micro_credential = get_object_or_404(
            MicroCredential, 
            id=micro_credential_id, 
            tenant=tenant
        )
        
        return MicroCredentialVersion.objects.filter(micro_credential=micro_credential)


class MicroCredentialEnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing micro-credential enrollments.
    """
    serializer_class = MicroCredentialEnrollmentSerializer
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production

    def get_queryset(self):
        tenant_slug = self.kwargs.get('tenant_slug')
        tenant = get_object_or_404(Tenant, slug=tenant_slug)
        
        # Filter by micro_credential if provided in query params
        micro_credential_id = self.request.query_params.get('micro_credential')
        queryset = MicroCredentialEnrollment.objects.filter(
            micro_credential__tenant=tenant
        )
        
        if micro_credential_id:
            queryset = queryset.filter(micro_credential_id=micro_credential_id)
        
        return queryset
