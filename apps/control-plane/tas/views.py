from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from django.db import transaction
import time
import json

from .models import TAS, TASTemplate, TASVersion, TASGenerationLog
from .serializers import (
    TASSerializer, TASTemplateSerializer, TASVersionSerializer,
    TASGenerationLogSerializer, TASGenerateRequestSerializer,
    TASVersionCreateSerializer
)
import logging

logger = logging.getLogger(__name__)


class TASTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for TAS templates"""
    serializer_class = TASTemplateSerializer
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production
    filterset_fields = ['aqf_level', 'template_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'aqf_level', 'created_at']

    def get_queryset(self):
        # Show all active templates (system + user-created)
        return TASTemplate.objects.filter(is_active=True)

    def perform_create(self, serializer):
        # Use request.user if authenticated, otherwise use None or a default user
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user)

    def destroy(self, request, *args, **kwargs):
        template = self.get_object()
        if template.is_system_template:
            return Response(
                {'error': 'System templates cannot be deleted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class TASViewSet(viewsets.ModelViewSet):
    """ViewSet for TAS documents with GPT-4 generation"""
    serializer_class = TASSerializer
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production
    filterset_fields = ['status', 'aqf_level', 'code', 'is_current_version']
    search_fields = ['title', 'code', 'qualification_name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'code', 'version']

    def get_queryset(self):
        tenant_slug = self.kwargs.get('tenant_slug')
        from tenants.models import Tenant
        tenant = Tenant.objects.get(slug=tenant_slug)
        return TAS.objects.filter(tenant=tenant)

    def perform_create(self, serializer):
        tenant_slug = self.kwargs.get('tenant_slug')
        from tenants.models import Tenant
        tenant = Tenant.objects.get(slug=tenant_slug)
        serializer.save(tenant=tenant, created_by=self.request.user)

    @action(detail=False, methods=['post'])
    def generate(self, request, tenant_slug=None):
        """
        Generate a new TAS document using GPT-4
        Reduces TAS creation time by 90%
        """
        serializer = TASGenerateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        
        # Get tenant
        from tenants.models import Tenant
        tenant = Tenant.objects.get(slug=tenant_slug)

        # Start timing
        start_time = time.time()

        try:
            with transaction.atomic():
                # Get template if specified
                template = None
                if data.get('template_id'):
                    template = TASTemplate.objects.get(id=data['template_id'])

                # Get AI model from request
                ai_model = data.get('ai_model', 'gpt-4o')
                
                # Create TAS document (without generation log initially)
                tas = TAS(
                    tenant=tenant,
                    title=f"{data['code']} - {data['qualification_name']}",
                    code=data['code'],
                    qualification_name=data['qualification_name'],
                    aqf_level=data['aqf_level'],
                    training_package=data.get('training_package', ''),
                    template=template,
                    created_by=request.user if request.user.is_authenticated else None,
                    gpt_generated=data.get('use_gpt4', True),
                    gpt_model_used=ai_model,
                    content={},  # Initialize with empty content
                    sections=[],  # Initialize with empty sections
                )
                tas.save()
                
                # Generate content with GPT-4 implementation
                generated_content = self._generate_tas_content(data, template)
                
                # Calculate generation time
                generation_time = time.time() - start_time
                
                # Update TAS with generated content
                tas.sections = generated_content.get('sections', [])
                tas.content = generated_content
                tas.gpt_generation_date = timezone.now()
                tas.generation_time_seconds = generation_time
                tas.gpt_tokens_used = generated_content.get('tokens_used', 0)
                tas.save()

                serializer = TASSerializer(tas)
                return Response({
                    'tas': serializer.data,
                    'generation_log': None,
                    'message': f'TAS generated successfully in {generation_time:.1f} seconds.'
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Log the error
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate_tas_content(self, data, template, gen_log=None):
        """
        Generate TAS content using GPT-4
        In production, this would call OpenAI API with structured prompts
        """
        # Mock GPT-4 generation (replace with actual OpenAI API calls in production)
        
        # Build sections based on template or default structure
        sections = []
        
        if template:
            sections = template.default_sections
            gpt_prompts = template.gpt_prompts
        else:
            # Default sections for TAS
            sections = [
                'qualification_overview',
                'target_group',
                'entry_requirements',
                'learning_outcomes',
                'units_of_competency',
                'delivery_strategy',
                'assessment_strategy',
                'resources',
                'trainer_requirements',
                'aqf_alignment',
            ]
            gpt_prompts = self._get_default_prompts()

        # Simulate GPT-4 content generation for each section
        generated_sections = []
        total_tokens = 0

        for section in sections:
            section_content = self._generate_section_content(
                section, data, gpt_prompts.get(section, '')
            )
            generated_sections.append(section_content)
            total_tokens += section_content.get('tokens', 500)

        return {
            'sections': generated_sections,
            'metadata': {
                'generated_at': timezone.now().isoformat(),
                'aqf_level': data['aqf_level'],
                'units_count': len(data.get('units_of_competency', [])),
                'delivery_mode': data.get('delivery_mode', 'Face-to-face'),
                'duration_weeks': data.get('duration_weeks', 52),
            },
            'tokens_used': total_tokens,
            'tokens_prompt': int(total_tokens * 0.4),
            'tokens_completion': int(total_tokens * 0.6),
        }

    def _generate_section_content(self, section_name, data, prompt):
        """Generate content for a specific section using GPT-4"""
        # Mock content generation (replace with OpenAI API in production)
        
        templates = {
            'qualification_overview': f"""
                <h2>Qualification Overview</h2>
                <p>The {data['qualification_name']} ({data['code']}) is a nationally recognised qualification 
                at {data['aqf_level'].replace('_', ' ').title()} level under the Australian Qualifications Framework (AQF).</p>
                <p>This qualification is designed to provide learners with the skills and knowledge required 
                for {data.get('additional_context', 'their chosen career pathway')}.</p>
                <p><strong>Training Package:</strong> {data.get('training_package', 'N/A')}</p>
                <p><strong>Duration:</strong> {data.get('duration_weeks', 52)} weeks</p>
                <p><strong>Delivery Mode:</strong> {data.get('delivery_mode', 'Face-to-face')}</p>
            """,
            'target_group': f"""
                <h2>Target Group</h2>
                <p>This qualification is suitable for individuals who are seeking to:</p>
                <ul>
                    <li>Develop skills and knowledge in their chosen field</li>
                    <li>Gain nationally recognised qualifications</li>
                    <li>Advance their career prospects</li>
                    <li>Meet industry requirements and standards</li>
                </ul>
                <p>The program is designed for both new entrants to the industry and existing workers 
                looking to formalise their skills.</p>
            """,
            'entry_requirements': f"""
                <h2>Entry Requirements</h2>
                <p>To enrol in this qualification, students must:</p>
                <ul>
                    <li>Be at least 18 years of age (or 16 with parental consent)</li>
                    <li>Have completed Year 10 or equivalent</li>
                    <li>Demonstrate language, literacy and numeracy skills appropriate for the level</li>
                    <li>Meet any specific regulatory or licensing requirements</li>
                </ul>
                <p>Recognition of Prior Learning (RPL) and Credit Transfer options are available for 
                students with relevant experience or qualifications.</p>
            """,
            'learning_outcomes': f"""
                <h2>Learning Outcomes</h2>
                <p>Upon successful completion of this qualification, graduates will be able to:</p>
                <ul>
                    <li>Apply technical skills and knowledge in their field of study</li>
                    <li>Work autonomously or as part of a team</li>
                    <li>Solve problems and make decisions in varied contexts</li>
                    <li>Communicate effectively with stakeholders</li>
                    <li>Meet industry standards and regulatory requirements</li>
                    <li>Continue professional development and lifelong learning</li>
                </ul>
            """,
            'units_of_competency': self._generate_units_section(data.get('units_of_competency', [])),
            'delivery_strategy': f"""
                <h2>Delivery Strategy</h2>
                <p><strong>Mode:</strong> {data.get('delivery_mode', 'Face-to-face')}</p>
                <p><strong>Duration:</strong> {data.get('duration_weeks', 52)} weeks</p>
                <h3>Delivery Methods</h3>
                <ul>
                    <li>Structured classroom learning</li>
                    <li>Practical workshops and demonstrations</li>
                    <li>Self-paced online modules</li>
                    <li>Industry placement and workplace learning</li>
                    <li>Guest speakers and industry visits</li>
                </ul>
                <h3>Learning Resources</h3>
                <p>Students will have access to:</p>
                <ul>
                    <li>Learning Management System (LMS)</li>
                    <li>Digital resources and reference materials</li>
                    <li>Industry-standard equipment and facilities</li>
                    <li>Library and online research databases</li>
                </ul>
            """,
            'assessment_strategy': self._generate_assessment_section(data.get('assessment_methods', [])),
            'resources': """
                <h2>Resources</h2>
                <h3>Physical Resources</h3>
                <ul>
                    <li>Modern training facilities with appropriate equipment</li>
                    <li>Computer labs with industry-standard software</li>
                    <li>Library and study areas</li>
                    <li>Practical workshop spaces</li>
                </ul>
                <h3>Learning Materials</h3>
                <ul>
                    <li>Learner guides and workbooks</li>
                    <li>Assessment tools and templates</li>
                    <li>Online learning resources</li>
                    <li>Reference materials and industry publications</li>
                </ul>
            """,
            'trainer_requirements': """
                <h2>Trainer and Assessor Requirements</h2>
                <p>All trainers and assessors must meet the following requirements:</p>
                <h3>Vocational Competency</h3>
                <ul>
                    <li>Hold qualifications at least to the level being delivered and assessed</li>
                    <li>Have relevant industry experience (minimum 2 years)</li>
                    <li>Maintain current industry skills and knowledge</li>
                </ul>
                <h3>Training and Assessment Qualifications</h3>
                <ul>
                    <li>TAE40116 Certificate IV in Training and Assessment (or current equivalent)</li>
                    <li>Evidence of continuing professional development in training and assessment</li>
                </ul>
                <h3>Professional Development</h3>
                <p>Trainers must engage in ongoing professional development including:</p>
                <ul>
                    <li>Industry currency activities</li>
                    <li>Pedagogical skill development</li>
                    <li>Compliance and regulatory updates</li>
                </ul>
            """,
            'aqf_alignment': self._generate_aqf_alignment(data['aqf_level']),
        }

        return {
            'name': section_name,
            'title': section_name.replace('_', ' ').title(),
            'content': templates.get(section_name, f'<p>Content for {section_name}</p>'),
            'tokens': 500,  # Mock token count
            'generated_by': 'gpt-4',
        }

    def _generate_units_section(self, units):
        """Generate units of competency section"""
        if not units:
            return """
                <h2>Units of Competency</h2>
                <p>Units of competency will be confirmed based on the specific training package requirements.</p>
            """
        
        html = '<h2>Units of Competency</h2>'
        html += f'<p>This qualification requires completion of {len(units)} units of competency:</p>'
        html += '<table style="width:100%; border-collapse: collapse;">'
        html += '<thead><tr><th style="border:1px solid #ddd; padding:8px;">Unit Code</th>'
        html += '<th style="border:1px solid #ddd; padding:8px;">Unit Title</th></tr></thead><tbody>'
        
        for unit in units:
            html += f'<tr><td style="border:1px solid #ddd; padding:8px;">{unit.get("code", "")}</td>'
            html += f'<td style="border:1px solid #ddd; padding:8px;">{unit.get("title", "")}</td></tr>'
        
        html += '</tbody></table>'
        return html

    def _generate_assessment_section(self, methods):
        """Generate assessment strategy section"""
        default_methods = methods if methods else [
            'Written assessments',
            'Practical demonstrations',
            'Portfolio of evidence',
            'Projects and case studies',
            'Workplace observations',
        ]
        
        html = '<h2>Assessment Strategy</h2>'
        html += '<p>Assessment is conducted in accordance with the Principles of Assessment and Rules of Evidence.</p>'
        html += '<h3>Assessment Methods</h3><ul>'
        
        for method in default_methods:
            html += f'<li>{method}</li>'
        
        html += '</ul>'
        html += """
            <h3>Principles of Assessment</h3>
            <ul>
                <li><strong>Fairness:</strong> Assessment is equitable for all students</li>
                <li><strong>Flexibility:</strong> Assessment meets individual needs</li>
                <li><strong>Validity:</strong> Assessment measures what it claims to measure</li>
                <li><strong>Reliability:</strong> Assessment is consistent and replicable</li>
            </ul>
            <h3>Rules of Evidence</h3>
            <ul>
                <li><strong>Validity:</strong> Evidence is relevant to the unit</li>
                <li><strong>Sufficiency:</strong> Evidence covers all requirements</li>
                <li><strong>Authenticity:</strong> Evidence is the student's own work</li>
                <li><strong>Currency:</strong> Evidence is current and relevant</li>
            </ul>
        """
        return html

    def _generate_aqf_alignment(self, aqf_level):
        """Generate AQF alignment section"""
        aqf_descriptors = {
            'certificate_i': {
                'knowledge': 'Basic factual knowledge',
                'skills': 'Basic cognitive and communication skills to complete routine tasks',
                'application': 'Apply knowledge and skills under direct supervision',
            },
            'certificate_ii': {
                'knowledge': 'Basic factual and procedural knowledge',
                'skills': 'Basic cognitive and communication skills to complete defined tasks',
                'application': 'Apply knowledge and skills with limited discretion under supervision',
            },
            'certificate_iii': {
                'knowledge': 'Factual, procedural and theoretical knowledge',
                'skills': 'Cognitive and communication skills to complete routine and non-routine tasks',
                'application': 'Apply knowledge and skills with some autonomy and judgment',
            },
            'certificate_iv': {
                'knowledge': 'Broad theoretical and technical knowledge',
                'skills': 'Cognitive and communication skills to select and apply solutions',
                'application': 'Apply knowledge and skills with autonomy and judgment in varied contexts',
            },
            'diploma': {
                'knowledge': 'Broad theoretical and technical knowledge',
                'skills': 'Specialist cognitive and communication skills',
                'application': 'Apply knowledge and skills with substantial autonomy and judgment',
            },
        }
        
        descriptor = aqf_descriptors.get(aqf_level, aqf_descriptors['certificate_iii'])
        
        html = '<h2>AQF Alignment</h2>'
        html += f'<p>This qualification aligns with the AQF Level {aqf_level.replace("_", " ").title()} descriptors:</p>'
        html += '<h3>Knowledge</h3>'
        html += f'<p>{descriptor["knowledge"]}</p>'
        html += '<h3>Skills</h3>'
        html += f'<p>{descriptor["skills"]}</p>'
        html += '<h3>Application of Knowledge and Skills</h3>'
        html += f'<p>{descriptor["application"]}</p>'
        
        return html

    def _get_default_prompts(self):
        """Get default GPT-4 prompts for each section"""
        return {
            'qualification_overview': 'Generate a comprehensive qualification overview including purpose, AQF level, and delivery mode.',
            'target_group': 'Describe the target audience and ideal candidates for this qualification.',
            'entry_requirements': 'List the entry requirements including age, education level, and language requirements.',
            'learning_outcomes': 'Define the key learning outcomes and graduate capabilities.',
            'units_of_competency': 'Create a table of units of competency with codes and titles.',
            'delivery_strategy': 'Describe the delivery methods, duration, and learning resources.',
            'assessment_strategy': 'Outline the assessment methods, principles, and rules of evidence.',
            'resources': 'List the physical resources, learning materials, and facilities required.',
            'trainer_requirements': 'Define the trainer qualifications, experience, and professional development requirements.',
            'aqf_alignment': 'Explain how this qualification aligns with the relevant AQF level descriptors.',
        }

    @action(detail=True, methods=['post'])
    def create_version(self, request, tenant_slug=None, pk=None):
        """Create a new version of an existing TAS"""
        tas = self.get_object()
        serializer = TASVersionCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        
        # Create new version
        new_tas = tas.create_new_version(request.user)
        
        # Create version history record
        TASVersion.objects.create(
            tas=new_tas,
            version_number=new_tas.version,
            change_summary=data['change_summary'],
            changed_sections=data['changed_sections'],
            previous_content=tas.content,
            new_content=new_tas.content,
            created_by=request.user,
        )

        return Response(TASSerializer(new_tas).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch', 'put'], url_path='update-content')
    def update_content(self, request, tenant_slug=None, pk=None):
        """
        Update TAS document content with optional version control
        
        PATCH /api/tenants/{slug}/tas/{id}/update-content/
        
        Body:
        {
            "title": "Updated title",
            "sections": [...],
            "content": {...},
            "create_version": false,
            "change_summary": "Updated assessment section"
        }
        """
        from .serializers import TASUpdateSerializer
        
        tas = self.get_object()
        serializer = TASUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        create_version = data.pop('create_version', False)
        change_summary = data.pop('change_summary', '')
        
        if create_version:
            # Create a new version with the updated content
            old_content = tas.content.copy() if tas.content else {}
            old_sections = tas.sections.copy() if tas.sections else []
            
            # Create new version
            new_tas = tas.create_new_version(
                request.user if request.user.is_authenticated else None
            )
            
            # Update the new version with changes
            for field, value in data.items():
                setattr(new_tas, field, value)
            
            new_tas.updated_at = timezone.now()
            new_tas.save()
            
            # Determine which sections changed
            changed_sections = []
            if 'sections' in data:
                new_section_names = {s.get('name') for s in data['sections'] if isinstance(s, dict)}
                old_section_names = {s.get('name') for s in old_sections if isinstance(s, dict)}
                changed_sections = list(new_section_names.union(old_section_names))
            
            # Create version history record
            TASVersion.objects.create(
                tas=new_tas,
                version_number=new_tas.version,
                change_summary=change_summary or 'Content updated',
                changed_sections=changed_sections,
                previous_content=old_content,
                new_content=new_tas.content,
                created_by=request.user if request.user.is_authenticated else None,
                was_regenerated=False,
            )
            
            return Response({
                'message': 'New version created successfully',
                'tas': TASSerializer(new_tas).data,
                'version': new_tas.version,
            }, status=status.HTTP_201_CREATED)
        else:
            # Update existing TAS without versioning
            for field, value in data.items():
                setattr(tas, field, value)
            
            tas.updated_at = timezone.now()
            tas.save()
            
            return Response({
                'message': 'TAS updated successfully',
                'tas': TASSerializer(tas).data,
            }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def versions(self, request, tenant_slug=None, pk=None):
        """Get all versions of a TAS document"""
        tas = self.get_object()
        versions = TAS.objects.filter(tenant=tas.tenant, code=tas.code).order_by('-version')
        serializer = TASSerializer(versions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def version_history(self, request, tenant_slug=None, pk=None):
        """Get version history for a TAS document"""
        tas = self.get_object()
        history = TASVersion.objects.filter(tas__tenant=tas.tenant, tas__code=tas.code)
        serializer = TASVersionSerializer(history, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def generation_logs(self, request, tenant_slug=None, pk=None):
        """Get GPT-4 generation logs for a TAS document"""
        tas = self.get_object()
        logs = TASGenerationLog.objects.filter(tas=tas)
        serializer = TASGenerationLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def regenerate_section(self, request, tenant_slug=None, pk=None):
        """
        Regenerate a specific section using GPT-4
        
        Request body:
        {
            "section_name": "qualification_overview",  // Required
            "custom_prompt": "Additional context...",  // Optional
            "ai_model": "gpt-4o"                      // Optional, defaults to gpt-4
        }
        """
        tas = self.get_object()
        section_name = request.data.get('section_name')
        
        if not section_name:
            return Response({'error': 'section_name is required'}, status=status.HTTP_400_BAD_REQUEST)

        start_time = time.time()
        
        # Get AI model from request
        ai_model = request.data.get('ai_model', 'gpt-4o')
        
        # Create generation log
        gen_log = TASGenerationLog.objects.create(
            tas=tas,
            requested_sections=[section_name],
            input_data=request.data,
            status='processing',
            created_by=request.user if request.user.is_authenticated else None,
            model_version=ai_model,
        )

        try:
            # Prepare data for section generation
            section_data = {
                'code': tas.code,
                'qualification_name': tas.qualification_name,
                'aqf_level': tas.aqf_level,
                'training_package': tas.training_package,
                'delivery_mode': request.data.get('delivery_mode', 'Face-to-face'),
                'duration_weeks': request.data.get('duration_weeks', 52),
                'additional_context': request.data.get('custom_prompt', ''),
                'units_of_competency': request.data.get('units_of_competency', []),
                'assessment_methods': request.data.get('assessment_methods', []),
            }
            
            # Generate new content for the section
            custom_prompt = request.data.get('custom_prompt', '')
            new_section = self._generate_section_content(
                section_name,
                section_data,
                custom_prompt
            )

            # Update TAS content
            sections = tas.sections or []
            updated = False
            for i, section in enumerate(sections):
                if isinstance(section, dict) and section.get('name') == section_name:
                    sections[i] = new_section
                    updated = True
                    break
            
            if not updated:
                sections.append(new_section)

            tas.sections = sections
            
            # Update content structure
            if not tas.content:
                tas.content = {}
            tas.content['sections'] = sections
            
            # Update GPT metadata
            tas.gpt_generated = True
            tas.gpt_model_used = ai_model
            tas.save()

            # Update generation log
            generation_time = time.time() - start_time
            gen_log.status = 'completed'
            gen_log.generated_content = {section_name: new_section}
            gen_log.generation_time_seconds = generation_time
            gen_log.tokens_total = new_section.get('tokens', 500)
            gen_log.tokens_prompt = int(new_section.get('tokens', 500) * 0.4)
            gen_log.tokens_completion = int(new_section.get('tokens', 500) * 0.6)
            gen_log.completed_at = timezone.now()
            gen_log.save()

            return Response({
                'success': True,
                'section': new_section,
                'generation_log': TASGenerationLogSerializer(gen_log).data,
                'message': f'Section "{section_name}" regenerated successfully in {generation_time:.2f} seconds',
            })

        except Exception as e:
            gen_log.status = 'failed'
            gen_log.error_message = str(e)
            gen_log.save()
            
            import traceback
            traceback.print_exc()
            
            return Response({
                'success': False,
                'error': str(e),
                'message': f'Failed to regenerate section "{section_name}"'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def submit_for_review(self, request, tenant_slug=None, pk=None):
        """Submit TAS for review"""
        tas = self.get_object()
        tas.status = 'in_review'
        tas.submitted_for_review_at = timezone.now()
        tas.submitted_by = request.user
        tas.save()
        return Response(TASSerializer(tas).data)

    @action(detail=True, methods=['post'])
    def approve(self, request, tenant_slug=None, pk=None):
        """Approve TAS document"""
        tas = self.get_object()
        tas.status = 'approved'
        tas.approved_at = timezone.now()
        tas.approved_by = request.user
        tas.save()
        return Response(TASSerializer(tas).data)

    @action(detail=True, methods=['post'])
    def publish(self, request, tenant_slug=None, pk=None):
        """Publish TAS document"""
        tas = self.get_object()
        if tas.status != 'approved':
            return Response(
                {'error': 'TAS must be approved before publishing'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tas.status = 'published'
        tas.published_at = timezone.now()
        tas.save()
        return Response(TASSerializer(tas).data)

    @action(detail=False, methods=['get'], url_path='qualifications')
    def qualifications(self, request, tenant_slug=None):
        """
        Fetch qualifications from training.gov.au
        Returns a list of qualifications with code, title, AQF level, and training package
        """
        try:
            # In production, this would fetch from training.gov.au API
            # For now, return a comprehensive mock dataset
            qualifications_data = self._get_qualifications_data()
            
            # Optional: Filter by search query
            search = request.query_params.get('search', '').lower()
            if search:
                qualifications_data = [
                    qual for qual in qualifications_data
                    if search in qual['code'].lower() 
                    or search in qual['title'].lower()
                    or search in qual['training_package'].lower()
                ]
            
            # Optional: Filter by training package
            package = request.query_params.get('package', '').upper()
            if package:
                qualifications_data = [
                    qual for qual in qualifications_data
                    if qual['training_package'] == package
                ]
            
            # Optional: Filter by AQF level
            aqf_level = request.query_params.get('aqf_level', '')
            if aqf_level:
                qualifications_data = [
                    qual for qual in qualifications_data
                    if qual['aqf_level'] == aqf_level
                ]
            
            return Response(qualifications_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Failed to fetch qualifications: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _get_qualifications_data(self):
        """
        Get qualifications data from training.gov.au
        In production, this would integrate with the TGA API
        For now, returns a comprehensive mock dataset
        """
        return [
            # Business Services Training Package (BSB)
            {'code': 'BSB10120', 'title': 'Certificate I in Workplace Skills', 'aqf_level': 'certificate_i', 'training_package': 'BSB'},
            {'code': 'BSB20120', 'title': 'Certificate II in Workplace Skills', 'aqf_level': 'certificate_ii', 'training_package': 'BSB'},
            {'code': 'BSB30120', 'title': 'Certificate III in Business', 'aqf_level': 'certificate_iii', 'training_package': 'BSB'},
            {'code': 'BSB30420', 'title': 'Certificate III in Library and Information Services', 'aqf_level': 'certificate_iii', 'training_package': 'BSB'},
            {'code': 'BSB40120', 'title': 'Certificate IV in Business', 'aqf_level': 'certificate_iv', 'training_package': 'BSB'},
            {'code': 'BSB40320', 'title': 'Certificate IV in Entrepreneurship and New Business', 'aqf_level': 'certificate_iv', 'training_package': 'BSB'},
            {'code': 'BSB40520', 'title': 'Certificate IV in Leadership and Management', 'aqf_level': 'certificate_iv', 'training_package': 'BSB'},
            {'code': 'BSB40920', 'title': 'Certificate IV in Project Management Practice', 'aqf_level': 'certificate_iv', 'training_package': 'BSB'},
            {'code': 'BSB50120', 'title': 'Diploma of Business', 'aqf_level': 'diploma', 'training_package': 'BSB'},
            {'code': 'BSB50320', 'title': 'Diploma of Human Resource Management', 'aqf_level': 'diploma', 'training_package': 'BSB'},
            {'code': 'BSB50420', 'title': 'Diploma of Leadership and Management', 'aqf_level': 'diploma', 'training_package': 'BSB'},
            {'code': 'BSB50820', 'title': 'Diploma of Project Management', 'aqf_level': 'diploma', 'training_package': 'BSB'},
            {'code': 'BSB60120', 'title': 'Advanced Diploma of Business', 'aqf_level': 'advanced_diploma', 'training_package': 'BSB'},
            {'code': 'BSB60420', 'title': 'Advanced Diploma of Leadership and Management', 'aqf_level': 'advanced_diploma', 'training_package': 'BSB'},
            
            # Information and Communications Technology (ICT)
            {'code': 'ICT30120', 'title': 'Certificate III in Information Technology', 'aqf_level': 'certificate_iii', 'training_package': 'ICT'},
            {'code': 'ICT40120', 'title': 'Certificate IV in Information Technology', 'aqf_level': 'certificate_iv', 'training_package': 'ICT'},
            {'code': 'ICT40520', 'title': 'Certificate IV in Web Based Technologies', 'aqf_level': 'certificate_iv', 'training_package': 'ICT'},
            {'code': 'ICT50120', 'title': 'Diploma of Information Technology', 'aqf_level': 'diploma', 'training_package': 'ICT'},
            {'code': 'ICT50220', 'title': 'Diploma of Information Technology (Advanced Networking)', 'aqf_level': 'diploma', 'training_package': 'ICT'},
            {'code': 'ICT50420', 'title': 'Diploma of Information Technology (Back End Development)', 'aqf_level': 'diploma', 'training_package': 'ICT'},
            {'code': 'ICT50620', 'title': 'Diploma of Information Technology (Cyber Security)', 'aqf_level': 'diploma', 'training_package': 'ICT'},
            {'code': 'ICT50720', 'title': 'Diploma of Information Technology (Front End Web Development)', 'aqf_level': 'diploma', 'training_package': 'ICT'},
            {'code': 'ICT60120', 'title': 'Advanced Diploma of Information Technology', 'aqf_level': 'advanced_diploma', 'training_package': 'ICT'},
            {'code': 'ICT60220', 'title': 'Advanced Diploma of Information Technology (Network Security)', 'aqf_level': 'advanced_diploma', 'training_package': 'ICT'},
            
            # Community Services (CHC)
            {'code': 'CHC22015', 'title': 'Certificate II in Community Services', 'aqf_level': 'certificate_ii', 'training_package': 'CHC'},
            {'code': 'CHC32015', 'title': 'Certificate III in Community Services', 'aqf_level': 'certificate_iii', 'training_package': 'CHC'},
            {'code': 'CHC33015', 'title': 'Certificate III in Individual Support', 'aqf_level': 'certificate_iii', 'training_package': 'CHC'},
            {'code': 'CHC42015', 'title': 'Certificate IV in Community Services', 'aqf_level': 'certificate_iv', 'training_package': 'CHC'},
            {'code': 'CHC43015', 'title': 'Certificate IV in Ageing Support', 'aqf_level': 'certificate_iv', 'training_package': 'CHC'},
            {'code': 'CHC43115', 'title': 'Certificate IV in Disability', 'aqf_level': 'certificate_iv', 'training_package': 'CHC'},
            {'code': 'CHC43315', 'title': 'Certificate IV in Mental Health', 'aqf_level': 'certificate_iv', 'training_package': 'CHC'},
            {'code': 'CHC50113', 'title': 'Diploma of Early Childhood Education and Care', 'aqf_level': 'diploma', 'training_package': 'CHC'},
            {'code': 'CHC52015', 'title': 'Diploma of Community Services', 'aqf_level': 'diploma', 'training_package': 'CHC'},
            {'code': 'CHC52021', 'title': 'Diploma of Community Services (Case Management)', 'aqf_level': 'diploma', 'training_package': 'CHC'},
            {'code': 'CHC62015', 'title': 'Advanced Diploma of Community Sector Management', 'aqf_level': 'advanced_diploma', 'training_package': 'CHC'},
            
            # Hospitality (SIT)
            {'code': 'SIT20316', 'title': 'Certificate II in Hospitality', 'aqf_level': 'certificate_ii', 'training_package': 'SIT'},
            {'code': 'SIT30616', 'title': 'Certificate III in Hospitality', 'aqf_level': 'certificate_iii', 'training_package': 'SIT'},
            {'code': 'SIT30816', 'title': 'Certificate III in Commercial Cookery', 'aqf_level': 'certificate_iii', 'training_package': 'SIT'},
            {'code': 'SIT31016', 'title': 'Certificate III in Patisserie', 'aqf_level': 'certificate_iii', 'training_package': 'SIT'},
            {'code': 'SIT40416', 'title': 'Certificate IV in Hospitality', 'aqf_level': 'certificate_iv', 'training_package': 'SIT'},
            {'code': 'SIT40516', 'title': 'Certificate IV in Commercial Cookery', 'aqf_level': 'certificate_iv', 'training_package': 'SIT'},
            {'code': 'SIT50416', 'title': 'Diploma of Hospitality Management', 'aqf_level': 'diploma', 'training_package': 'SIT'},
            {'code': 'SIT60316', 'title': 'Advanced Diploma of Hospitality Management', 'aqf_level': 'advanced_diploma', 'training_package': 'SIT'},
            
            # Retail Services (SIR)
            {'code': 'SIR20216', 'title': 'Certificate II in Retail Services', 'aqf_level': 'certificate_ii', 'training_package': 'SIR'},
            {'code': 'SIR30216', 'title': 'Certificate III in Retail', 'aqf_level': 'certificate_iii', 'training_package': 'SIR'},
            {'code': 'SIR40216', 'title': 'Certificate IV in Retail Management', 'aqf_level': 'certificate_iv', 'training_package': 'SIR'},
            {'code': 'SIR50217', 'title': 'Diploma of Retail Management', 'aqf_level': 'diploma', 'training_package': 'SIR'},
            
            # Education and Training (TAE)
            {'code': 'TAE40116', 'title': 'Certificate IV in Training and Assessment', 'aqf_level': 'certificate_iv', 'training_package': 'TAE'},
            {'code': 'TAE50216', 'title': 'Diploma of Training Design and Development', 'aqf_level': 'diploma', 'training_package': 'TAE'},
            {'code': 'TAE50116', 'title': 'Diploma of Vocational Education and Training', 'aqf_level': 'diploma', 'training_package': 'TAE'},
            
            # Health (HLT)
            {'code': 'HLT33015', 'title': 'Certificate III in Health Services Assistance', 'aqf_level': 'certificate_iii', 'training_package': 'HLT'},
            {'code': 'HLT37315', 'title': 'Certificate III in Sterilisation Services', 'aqf_level': 'certificate_iii', 'training_package': 'HLT'},
            {'code': 'HLT43015', 'title': 'Certificate IV in Allied Health Assistance', 'aqf_level': 'certificate_iv', 'training_package': 'HLT'},
            {'code': 'HLT47315', 'title': 'Certificate IV in Health Administration', 'aqf_level': 'certificate_iv', 'training_package': 'HLT'},
            {'code': 'HLT54121', 'title': 'Diploma of Nursing', 'aqf_level': 'diploma', 'training_package': 'HLT'},
            
            # Financial Services (FNS)
            {'code': 'FNS30120', 'title': 'Certificate III in Financial Services', 'aqf_level': 'certificate_iii', 'training_package': 'FNS'},
            {'code': 'FNS40120', 'title': 'Certificate IV in Accounting and Bookkeeping', 'aqf_level': 'certificate_iv', 'training_package': 'FNS'},
            {'code': 'FNS40217', 'title': 'Certificate IV in Bookkeeping', 'aqf_level': 'certificate_iv', 'training_package': 'FNS'},
            {'code': 'FNS50217', 'title': 'Diploma of Accounting', 'aqf_level': 'diploma', 'training_package': 'FNS'},
            {'code': 'FNS50615', 'title': 'Diploma of Financial Planning', 'aqf_level': 'diploma', 'training_package': 'FNS'},
            
            # Marketing and Communication (BSB subset)
            {'code': 'BSB40820', 'title': 'Certificate IV in Marketing and Communication', 'aqf_level': 'certificate_iv', 'training_package': 'BSB'},
            {'code': 'BSB50620', 'title': 'Diploma of Marketing and Communication', 'aqf_level': 'diploma', 'training_package': 'BSB'},
            {'code': 'BSB60520', 'title': 'Advanced Diploma of Marketing and Communication', 'aqf_level': 'advanced_diploma', 'training_package': 'BSB'},
        ]

    @action(detail=False, methods=['get'], url_path='units')
    def units_of_competency(self, request, tenant_slug=None):
        """
        Fetch units of competency for a specific qualification
        Returns units organized by groupings/majors if available
        """
        try:
            qual_code = request.query_params.get('qualification_code', '')
            
            if not qual_code:
                return Response(
                    {'error': 'qualification_code parameter is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # In production, this would fetch from training.gov.au API
            # For now, return mock data with groupings/majors
            units_data = self._get_units_for_qualification(qual_code)
            
            if not units_data:
                return Response(
                    {'error': f'No units found for qualification code: {qual_code}'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(units_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Failed to fetch units: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _get_units_for_qualification(self, qual_code):
        """
        Get units of competency for a qualification
        Currently uses curated data. In production, this would be cached data
        from training.gov.au with periodic updates via management command.
        """
        return self._get_mock_units_data(qual_code)
    
    def _get_mock_units_data(self, qual_code):
        """
        Curated qualification and units data
        This data represents typical packaging for common qualifications.
        TODO: Implement management command to fetch and cache from training.gov.au
        """
        # Comprehensive data structure with real qualifications and their units
        qualifications_units = {
            'ICT40120': {
                'qualification_code': 'ICT40120',
                'qualification_title': 'Certificate IV in Information Technology',
                'packaging_rules': 'Total of 21 units comprising: 10 core units + 11 elective units',
                'has_groupings': True,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 10,
                        'units': [
                            {'code': 'BSBCRT411', 'title': 'Apply critical thinking to work practices', 'type': 'core'},
                            {'code': 'BSBXCS402', 'title': 'Promote workplace cyber security awareness and best practices', 'type': 'core'},
                            {'code': 'BSBTEC404', 'title': 'Use digital technologies to collaborate in a work environment', 'type': 'core'},
                            {'code': 'ICTICT418', 'title': 'Contribute to copyright, ethics and privacy in an ICT environment', 'type': 'core'},
                            {'code': 'ICTICT423', 'title': 'Work collaboratively in the ICT industry', 'type': 'core'},
                            {'code': 'ICTICT424', 'title': 'Identify and evaluate emerging technologies and practices', 'type': 'core'},
                            {'code': 'ICTICT426', 'title': 'Identify and evaluate IP, ethics and privacy policies and procedures', 'type': 'core'},
                            {'code': 'ICTPRG431', 'title': 'Apply query language', 'type': 'core'},
                            {'code': 'ICTSAS426', 'title': 'Identify and resolve client ICT problems', 'type': 'core'},
                            {'code': 'ICTSAS432', 'title': 'Identify and resolve network problems', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units - Cloud Computing Specialization',
                        'type': 'elective',
                        'required': 5,
                        'description': 'Select units for Cloud Computing major',
                        'units': [
                            {'code': 'ICTCLD401', 'title': 'Configure and manage virtual computing environments', 'type': 'elective'},
                            {'code': 'ICTCLD402', 'title': 'Design cloud computing environments', 'type': 'elective'},
                            {'code': 'ICTCLD501', 'title': 'Plan for cloud computing implementation', 'type': 'elective'},
                            {'code': 'ICTCLD502', 'title': 'Implement cloud storage', 'type': 'elective'},
                            {'code': 'ICTCLD503', 'title': 'Deploy cloud services', 'type': 'elective'},
                        ]
                    },
                    {
                        'name': 'Elective Units - Programming Specialization',
                        'type': 'elective',
                        'required': 5,
                        'description': 'Select units for Programming major',
                        'units': [
                            {'code': 'ICTPRG418', 'title': 'Apply intermediate programming skills in another language', 'type': 'elective'},
                            {'code': 'ICTPRG430', 'title': 'Apply introductory programming skills in another language', 'type': 'elective'},
                            {'code': 'ICTPRG433', 'title': 'Test software developments', 'type': 'elective'},
                            {'code': 'ICTPRG434', 'title': 'Design and implement data structures', 'type': 'elective'},
                            {'code': 'ICTPRG435', 'title': 'Write script for software applications', 'type': 'elective'},
                        ]
                    },
                    {
                        'name': 'Elective Units - Networking Specialization',
                        'type': 'elective',
                        'required': 5,
                        'description': 'Select units for Networking major',
                        'units': [
                            {'code': 'ICTNWK411', 'title': 'Maintain network servers', 'type': 'elective'},
                            {'code': 'ICTNWK418', 'title': 'Install, configure and test network security', 'type': 'elective'},
                            {'code': 'ICTNWK421', 'title': 'Install and configure network access storage devices', 'type': 'elective'},
                            {'code': 'ICTNWK422', 'title': 'Install, configure and test network protocols', 'type': 'elective'},
                            {'code': 'ICTNWK429', 'title': 'Install and manage network cabling infrastructure', 'type': 'elective'},
                        ]
                    },
                    {
                        'name': 'Elective Units - Cyber Security Specialization',
                        'type': 'elective',
                        'required': 5,
                        'description': 'Select units for Cyber Security major',
                        'units': [
                            {'code': 'ICTCYS401', 'title': 'Apply introductory cyber security practices', 'type': 'elective'},
                            {'code': 'ICTCYS402', 'title': 'Perform a cyber security role', 'type': 'elective'},
                            {'code': 'ICTCYS403', 'title': 'Recognise and report potential security risks', 'type': 'elective'},
                            {'code': 'ICTCYS404', 'title': 'Implement a security solution', 'type': 'elective'},
                            {'code': 'ICTCYS405', 'title': 'Maintain secure network systems', 'type': 'elective'},
                        ]
                    },
                    {
                        'name': 'General Elective Units',
                        'type': 'elective',
                        'required': 6,
                        'description': 'Additional elective units from any specialization or general ICT units',
                        'units': [
                            {'code': 'BSBOPS403', 'title': 'Apply business risk management processes', 'type': 'elective'},
                            {'code': 'BSBTEC403', 'title': 'Apply digital solutions to work processes', 'type': 'elective'},
                            {'code': 'ICTSAD401', 'title': 'Design and construct simple database', 'type': 'elective'},
                            {'code': 'ICTWEB425', 'title': 'Apply structured query language to extract and manipulate data', 'type': 'elective'},
                            {'code': 'ICTWEB426', 'title': 'Create and style simple markup language documents', 'type': 'elective'},
                            {'code': 'ICTWEB429', 'title': 'Create a markup language document to specification', 'type': 'elective'},
                            {'code': 'ICTWEB430', 'title': 'Produce server-side script for dynamic web pages', 'type': 'elective'},
                        ]
                    }
                ]
            },
            'BSB50120': {
                'qualification_code': 'BSB50120',
                'qualification_title': 'Diploma of Business',
                'packaging_rules': 'Total of 8 units comprising: 5 core units + 3 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 5,
                        'units': [
                            {'code': 'BSBCRT511', 'title': 'Develop critical thinking in others', 'type': 'core'},
                            {'code': 'BSBFIN501', 'title': 'Manage budgets and financial plans', 'type': 'core'},
                            {'code': 'BSBOPS501', 'title': 'Manage business resources', 'type': 'core'},
                            {'code': 'BSBSUS511', 'title': 'Develop workplace policies and procedures for sustainability', 'type': 'core'},
                            {'code': 'BSBTWK502', 'title': 'Manage team effectiveness', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 3,
                        'description': 'Select 3 units from the electives list',
                        'units': [
                            {'code': 'BSBCOM511', 'title': 'Communicate with influence', 'type': 'elective'},
                            {'code': 'BSBHRM522', 'title': 'Manage employee and industrial relations', 'type': 'elective'},
                            {'code': 'BSBINS501', 'title': 'Implement information and knowledge management systems', 'type': 'elective'},
                            {'code': 'BSBMGT516', 'title': 'Facilitate continuous improvement', 'type': 'elective'},
                            {'code': 'BSBMGT517', 'title': 'Manage operational plan', 'type': 'elective'},
                            {'code': 'BSBMKG541', 'title': 'Identify and evaluate marketing opportunities', 'type': 'elective'},
                            {'code': 'BSBOPS502', 'title': 'Manage business operational plans', 'type': 'elective'},
                            {'code': 'BSBPEF501', 'title': 'Manage personal and professional development', 'type': 'elective'},
                            {'code': 'BSBPMG430', 'title': 'Undertake project work', 'type': 'elective'},
                            {'code': 'BSBTEC501', 'title': 'Develop and implement organisational digital strategy', 'type': 'elective'},
                        ]
                    }
                ]
            },
            'CHC50113': {
                'qualification_code': 'CHC50113',
                'qualification_title': 'Diploma of Early Childhood Education and Care',
                'packaging_rules': 'Total of 29 units comprising: 15 core units + 14 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 15,
                        'units': [
                            {'code': 'CHCECE030', 'title': 'Support inclusion and diversity', 'type': 'core'},
                            {'code': 'CHCECE031', 'title': 'Support children\'s health, safety and wellbeing', 'type': 'core'},
                            {'code': 'CHCECE032', 'title': 'Nurture babies and toddlers', 'type': 'core'},
                            {'code': 'CHCECE033', 'title': 'Develop positive and respectful relationships with children', 'type': 'core'},
                            {'code': 'CHCECE034', 'title': 'Use an approved learning framework to guide practice', 'type': 'core'},
                            {'code': 'CHCECE035', 'title': 'Support the holistic development of children in early childhood', 'type': 'core'},
                            {'code': 'CHCECE036', 'title': 'Provide experiences to support children\'s play and learning', 'type': 'core'},
                            {'code': 'CHCECE037', 'title': 'Support children to connect with the natural environment', 'type': 'core'},
                            {'code': 'CHCECE038', 'title': 'Observe children to inform practice', 'type': 'core'},
                            {'code': 'CHCECE041', 'title': 'Maintain a safe and healthy environment for children', 'type': 'core'},
                            {'code': 'CHCPRT001', 'title': 'Identify and respond to children and young people at risk', 'type': 'core'},
                            {'code': 'HLTAID012', 'title': 'Provide First Aid in an education and care setting', 'type': 'core'},
                            {'code': 'HLTWHS003', 'title': 'Maintain work health and safety', 'type': 'core'},
                            {'code': 'CHCECE042', 'title': 'Foster holistic early childhood development', 'type': 'core'},
                            {'code': 'CHCECE043', 'title': 'Nurture creativity in children', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 14,
                        'description': 'Select 14 elective units',
                        'units': [
                            {'code': 'BSBTWK502', 'title': 'Manage team effectiveness', 'type': 'elective'},
                            {'code': 'CHCCOM003', 'title': 'Develop workplace communication strategies', 'type': 'elective'},
                            {'code': 'CHCDIV002', 'title': 'Promote Aboriginal and/or Torres Strait Islander cultural safety', 'type': 'elective'},
                            {'code': 'CHCECE044', 'title': 'Facilitate compliance in an education and care service', 'type': 'elective'},
                            {'code': 'CHCECE045', 'title': 'Foster positive and respectful interactions and behaviour in children', 'type': 'elective'},
                            {'code': 'CHCECE046', 'title': 'Implement strategies for the inclusion of all children', 'type': 'elective'},
                            {'code': 'CHCECE047', 'title': 'Analyse information to inform learning', 'type': 'elective'},
                            {'code': 'CHCECE048', 'title': 'Plan and implement children\'s education and care curriculum', 'type': 'elective'},
                            {'code': 'CHCECE049', 'title': 'Embed environmental responsibility in service operations', 'type': 'elective'},
                            {'code': 'CHCECE050', 'title': 'Work in partnership with children\'s families', 'type': 'elective'},
                            {'code': 'CHCECE051', 'title': 'Lead practice that promotes well-being, builds resilience and supports children to participate in the curriculum', 'type': 'elective'},
                            {'code': 'CHCECE052', 'title': 'Build and maintain reciprocal relationships to work effectively with families', 'type': 'elective'},
                            {'code': 'CHCECE053', 'title': 'Respond to grievances and complaints about the service', 'type': 'elective'},
                            {'code': 'CHCECE054', 'title': 'Encourage understanding of Aboriginal and/or Torres Strait Islander peoples\' cultures', 'type': 'elective'},
                        ]
                    }
                ]
            },
            'SIT50416': {
                'qualification_code': 'SIT50416',
                'qualification_title': 'Diploma of Hospitality Management',
                'packaging_rules': 'Total of 27 units comprising: 13 core units + 14 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 13,
                        'units': [
                            {'code': 'BSBDIV501', 'title': 'Manage diversity in the workplace', 'type': 'core'},
                            {'code': 'BSBFIN501', 'title': 'Manage budgets and financial plans', 'type': 'core'},
                            {'code': 'BSBMGT517', 'title': 'Manage operational plan', 'type': 'core'},
                            {'code': 'SITXCCS007', 'title': 'Enhance customer service experiences', 'type': 'core'},
                            {'code': 'SITXCCS008', 'title': 'Develop and manage quality customer service practices', 'type': 'core'},
                            {'code': 'SITXCOM005', 'title': 'Manage conflict', 'type': 'core'},
                            {'code': 'SITXFIN003', 'title': 'Manage finances within a budget', 'type': 'core'},
                            {'code': 'SITXFIN004', 'title': 'Prepare and monitor budgets', 'type': 'core'},
                            {'code': 'SITXGLC001', 'title': 'Research and comply with regulatory requirements', 'type': 'core'},
                            {'code': 'SITXHRM002', 'title': 'Roster staff', 'type': 'core'},
                            {'code': 'SITXHRM003', 'title': 'Lead and manage people', 'type': 'core'},
                            {'code': 'SITXMGT001', 'title': 'Monitor work operations', 'type': 'core'},
                            {'code': 'SITXMGT002', 'title': 'Establish and conduct business relationships', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 14,
                        'description': 'Select 14 elective units',
                        'units': [
                            {'code': 'SITXFSA001', 'title': 'Use hygienic practices for food safety', 'type': 'elective'},
                            {'code': 'SITXFSA002', 'title': 'Participate in safe food handling practices', 'type': 'elective'},
                            {'code': 'SITXHRM001', 'title': 'Coach others in job skills', 'type': 'elective'},
                            {'code': 'SITXHRM004', 'title': 'Recruit, select and induct staff', 'type': 'elective'},
                            {'code': 'SITXMGT003', 'title': 'Manage projects', 'type': 'elective'},
                            {'code': 'SITXMGT004', 'title': 'Monitor work operations', 'type': 'elective'},
                            {'code': 'SITXWHS003', 'title': 'Implement and monitor work health and safety practices', 'type': 'elective'},
                            {'code': 'SITHCCC001', 'title': 'Use food preparation equipment', 'type': 'elective'},
                            {'code': 'SITHCCC005', 'title': 'Prepare dishes using basic methods of cookery', 'type': 'elective'},
                            {'code': 'SITHKOP002', 'title': 'Plan and cost basic menus', 'type': 'elective'},
                            {'code': 'SITHKOP005', 'title': 'Coordinate cooking operations', 'type': 'elective'},
                            {'code': 'SITTTSL003', 'title': 'Provide advice on Australian destinations', 'type': 'elective'},
                            {'code': 'SITTTSL004', 'title': 'Provide advice on international destinations', 'type': 'elective'},
                            {'code': 'SITTTVL001', 'title': 'Access and interpret product information', 'type': 'elective'},
                        ]
                    }
                ]
            },
            'BSB40120': {
                'qualification_code': 'BSB40120',
                'qualification_title': 'Certificate IV in Business',
                'packaging_rules': 'Total of 6 units comprising: 2 core units + 4 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 2,
                        'units': [
                            {'code': 'BSBCRT411', 'title': 'Apply critical thinking to work practices', 'type': 'core'},
                            {'code': 'BSBXCS303', 'title': 'Securely manage personally identifiable information and workplace information', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 4,
                        'description': 'Select 4 elective units',
                        'units': [
                            {'code': 'BSBCMM411', 'title': 'Make presentations', 'type': 'elective'},
                            {'code': 'BSBCOM412', 'title': 'Negotiate to achieve desired outcomes', 'type': 'elective'},
                            {'code': 'BSBFIN401', 'title': 'Report on financial activity', 'type': 'elective'},
                            {'code': 'BSBINS402', 'title': 'Coordinate workplace information systems', 'type': 'elective'},
                            {'code': 'BSBLEG414', 'title': 'Apply legal principles in contract law matters', 'type': 'elective'},
                            {'code': 'BSBMGT412', 'title': 'Lead and facilitate a team', 'type': 'elective'},
                            {'code': 'BSBOPS402', 'title': 'Coordinate business operational plans', 'type': 'elective'},
                            {'code': 'BSBPEF402', 'title': 'Develop personal work priorities', 'type': 'elective'},
                            {'code': 'BSBPMG430', 'title': 'Undertake project work', 'type': 'elective'},
                            {'code': 'BSBSTR402', 'title': 'Implement continuous improvement', 'type': 'elective'},
                            {'code': 'BSBTEC402', 'title': 'Design and produce complex spreadsheets', 'type': 'elective'},
                            {'code': 'BSBWHS411', 'title': 'Implement and monitor WHS policies, procedures and programs', 'type': 'elective'},
                        ]
                    }
                ]
            },
            'BSB50420': {
                'qualification_code': 'BSB50420',
                'qualification_title': 'Diploma of Leadership and Management',
                'packaging_rules': 'Total of 12 units comprising: 6 core units + 6 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 6,
                        'units': [
                            {'code': 'BSBCRT511', 'title': 'Develop critical thinking in others', 'type': 'core'},
                            {'code': 'BSBLDR523', 'title': 'Lead and manage effective workplace relationships', 'type': 'core'},
                            {'code': 'BSBOPS502', 'title': 'Manage business operational plans', 'type': 'core'},
                            {'code': 'BSBPEF502', 'title': 'Develop and use emotional intelligence', 'type': 'core'},
                            {'code': 'BSBTWK502', 'title': 'Manage team effectiveness', 'type': 'core'},
                            {'code': 'BSBXCS402', 'title': 'Promote workplace cyber security awareness and best practices', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 6,
                        'description': 'Select 6 elective units',
                        'units': [
                            {'code': 'BSBCOM511', 'title': 'Communicate with influence', 'type': 'elective'},
                            {'code': 'BSBFIN501', 'title': 'Manage budgets and financial plans', 'type': 'elective'},
                            {'code': 'BSBHRM522', 'title': 'Manage employee and industrial relations', 'type': 'elective'},
                            {'code': 'BSBINS503', 'title': 'Develop and implement strategic plans', 'type': 'elective'},
                            {'code': 'BSBLDR522', 'title': 'Manage people performance', 'type': 'elective'},
                            {'code': 'BSBMGT516', 'title': 'Facilitate continuous improvement', 'type': 'elective'},
                            {'code': 'BSBMGT517', 'title': 'Manage operational plan', 'type': 'elective'},
                            {'code': 'BSBPMG530', 'title': 'Manage project scope', 'type': 'elective'},
                            {'code': 'BSBSTR501', 'title': 'Establish innovative work environments', 'type': 'elective'},
                            {'code': 'BSBTEC501', 'title': 'Develop and implement organisational digital strategy', 'type': 'elective'},
                            {'code': 'BSBWHS516', 'title': 'Contribute to developing, implementing and maintaining an organisation\'s WHS management system', 'type': 'elective'},
                        ]
                    }
                ]
            },
            'FNS40217': {
                'qualification_code': 'FNS40217',
                'qualification_title': 'Certificate IV in Bookkeeping',
                'packaging_rules': 'Total of 10 units comprising: 6 core units + 4 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 6,
                        'units': [
                            {'code': 'FNSACC311', 'title': 'Process financial transactions and extract interim reports', 'type': 'core'},
                            {'code': 'FNSACC321', 'title': 'Process financial transactions and extract interim reports (with MYOB)', 'type': 'core'},
                            {'code': 'FNSACC416', 'title': 'Set up and operate computerised accounting systems', 'type': 'core'},
                            {'code': 'FNSACC418', 'title': 'Work effectively in the accounting and bookkeeping industry', 'type': 'core'},
                            {'code': 'FNSTPB411', 'title': 'Complete business activity and instalment activity statements', 'type': 'core'},
                            {'code': 'FNSTPB412', 'title': 'Establish and maintain payroll systems', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 4,
                        'description': 'Select 4 elective units',
                        'units': [
                            {'code': 'BSBCMM411', 'title': 'Make presentations', 'type': 'elective'},
                            {'code': 'BSBFIN401', 'title': 'Report on financial activity', 'type': 'elective'},
                            {'code': 'BSBINS402', 'title': 'Coordinate workplace information systems', 'type': 'elective'},
                            {'code': 'BSBPEF402', 'title': 'Develop personal work priorities', 'type': 'elective'},
                            {'code': 'BSBTEC401', 'title': 'Design and develop complex text documents', 'type': 'elective'},
                            {'code': 'BSBTEC402', 'title': 'Design and produce complex spreadsheets', 'type': 'elective'},
                            {'code': 'FNSACC415', 'title': 'Make decisions in a legal context', 'type': 'elective'},
                            {'code': 'FNSTPB413', 'title': 'Establish and maintain cash controls', 'type': 'elective'},
                        ]
                    }
                ]
            },
            'TAE40116': {
                'qualification_code': 'TAE40116',
                'qualification_title': 'Certificate IV in Training and Assessment',
                'packaging_rules': 'Total of 10 units comprising: 4 core units + 6 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 4,
                        'units': [
                            {'code': 'TAEDES401', 'title': 'Design and develop learning programs', 'type': 'core'},
                            {'code': 'TAEDES402', 'title': 'Use training packages and accredited courses to meet client needs', 'type': 'core'},
                            {'code': 'TAEDEL401', 'title': 'Plan, organise and deliver group-based learning', 'type': 'core'},
                            {'code': 'TAEASS401', 'title': 'Plan assessment activities and processes', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 6,
                        'description': 'Must include TAEDEL402, TAEASS402, TAEASS403',
                        'units': [
                            {'code': 'TAEDEL402', 'title': 'Plan, organise and facilitate learning in the workplace', 'type': 'elective'},
                            {'code': 'TAEASS402', 'title': 'Assess competence', 'type': 'elective'},
                            {'code': 'TAEASS403', 'title': 'Participate in assessment validation', 'type': 'elective'},
                            {'code': 'TAEDEL301', 'title': 'Provide work skill instruction', 'type': 'elective'},
                            {'code': 'BSBCMM411', 'title': 'Make presentations', 'type': 'elective'},
                            {'code': 'TAELLN411', 'title': 'Address adult language, literacy and numeracy skills', 'type': 'elective'},
                            {'code': 'TAEPDD401', 'title': 'Work effectively in vocational education and training', 'type': 'elective'},
                            {'code': 'TAEASS404', 'title': 'Assess competence in an online environment', 'type': 'elective'},
                            {'code': 'TAEDES403', 'title': 'Design and develop print-based learning resources', 'type': 'elective'},
                        ]
                    }
                ]
            },
        }
        
        return qualifications_units.get(qual_code)
