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
