from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q, Prefetch
import re
from datetime import datetime

from .models import Evidence, ClauseEvidence, AuditReport, AuditReportClause
from .serializers import (
    EvidenceSerializer, ClauseEvidenceSerializer,
    AuditReportSerializer, AuditReportDetailSerializer, AuditReportClauseSerializer,
    EvidenceUploadSerializer, ClauseEvidenceGapSerializer
)
from policy_comparator.models import ASQAClause, ASQAStandard


class EvidenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for evidence document management with NER auto-tagging
    """
    serializer_class = EvidenceSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def get_queryset(self):
        tenant_id = self.kwargs.get('tenant_id')
        return Evidence.objects.filter(tenant_id=tenant_id).select_related(
            'uploaded_by', 'reviewed_by'
        ).prefetch_related('auto_tagged_clauses')
    
    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload(self, request, tenant_id=None):
        """
        Upload evidence file and process with NER for auto-tagging
        """
        serializer = EvidenceUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create evidence record
        evidence = Evidence.objects.create(
            tenant_id=tenant_id,
            evidence_number=serializer.validated_data['evidence_number'],
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', ''),
            evidence_type=serializer.validated_data['evidence_type'],
            file=serializer.validated_data['file'],
            evidence_date=serializer.validated_data['evidence_date'],
            tags=serializer.validated_data.get('tags', []),
            uploaded_by=request.user,
            status='uploaded'
        )
        
        # Extract text from file
        extracted_text = self._extract_text_from_file(evidence.file)
        evidence.extracted_text = extracted_text
        evidence.save()
        
        # Process NER if auto-tag is enabled
        if serializer.validated_data.get('auto_tag', True) and extracted_text:
            evidence.status = 'processing'
            evidence.save()
            
            # Run NER processing
            ner_entities = self._process_ner(extracted_text)
            evidence.ner_entities = ner_entities
            evidence.ner_processed_at = timezone.now()
            
            # Auto-tag clauses based on NER + rules
            auto_tagged_count = self._auto_tag_clauses(evidence, extracted_text, ner_entities)
            
            evidence.status = 'tagged' if auto_tagged_count > 0 else 'uploaded'
            evidence.save()
        
        return Response(
            EvidenceSerializer(evidence, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def process_ner(self, request, tenant_id=None, pk=None):
        """
        Manually trigger NER processing and auto-tagging for an evidence document
        """
        evidence = self.get_object()
        
        if not evidence.extracted_text:
            return Response(
                {'error': 'No text extracted from file. Cannot process NER.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        evidence.status = 'processing'
        evidence.save()
        
        # Run NER
        ner_entities = self._process_ner(evidence.extracted_text)
        evidence.ner_entities = ner_entities
        evidence.ner_processed_at = timezone.now()
        
        # Auto-tag clauses
        auto_tagged_count = self._auto_tag_clauses(evidence, evidence.extracted_text, ner_entities)
        
        evidence.status = 'tagged' if auto_tagged_count > 0 else 'uploaded'
        evidence.save()
        
        return Response({
            'message': f'NER processing complete. {len(ner_entities)} entities found. {auto_tagged_count} clauses auto-tagged.',
            'ner_entities': ner_entities,
            'auto_tagged_count': auto_tagged_count,
            'evidence': EvidenceSerializer(evidence, context={'request': request}).data
        })
    
    @action(detail=True, methods=['get'])
    def tagged_clauses(self, request, tenant_id=None, pk=None):
        """
        Get all clauses tagged to this evidence with mapping details
        """
        evidence = self.get_object()
        mappings = ClauseEvidence.objects.filter(evidence=evidence).select_related(
            'asqa_clause', 'asqa_clause__standard', 'verified_by'
        ).order_by('-confidence_score')
        
        serializer = ClauseEvidenceSerializer(mappings, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def verify_tagging(self, request, tenant_id=None, pk=None):
        """
        Verify/approve auto-tagged clauses for evidence
        """
        evidence = self.get_object()
        clause_evidence_ids = request.data.get('clause_evidence_ids', [])
        
        updated_count = ClauseEvidence.objects.filter(
            id__in=clause_evidence_ids,
            evidence=evidence
        ).update(
            is_verified=True,
            verified_by=request.user,
            verified_at=timezone.now()
        )
        
        if updated_count > 0:
            evidence.status = 'reviewed'
            evidence.reviewed_by = request.user
            evidence.reviewed_at = timezone.now()
            evidence.save()
        
        return Response({
            'message': f'{updated_count} clause mappings verified.',
            'evidence': EvidenceSerializer(evidence, context={'request': request}).data
        })
    
    def _extract_text_from_file(self, file):
        """
        Extract text from uploaded file (PDF, DOCX, TXT, etc.)
        TODO: Implement actual text extraction using libraries like PyPDF2, python-docx
        """
        # Placeholder - in production, use libraries for extraction
        file_ext = file.name.split('.')[-1].lower()
        
        if file_ext == 'txt':
            try:
                return file.read().decode('utf-8')
            except:
                return ""
        
        # For other formats, return placeholder
        # In production, implement:
        # - PDF: PyPDF2, pdfplumber
        # - DOCX: python-docx
        # - Images: pytesseract (OCR)
        return f"[Text extraction placeholder for {file_ext} file: {file.name}]"
    
    def _process_ner(self, text):
        """
        Process Named Entity Recognition on text.
        Uses simple regex patterns for now - in production, use spaCy or similar.
        
        Entity types:
        - PERSON: Names of people
        - ORG: Organizations, RTOs
        - DATE: Dates
        - QUALIFICATION: Qualifications, certificates
        - STANDARD: ASQA standard references
        - CLAUSE: Clause references
        - POLICY: Policy references
        """
        entities = []
        
        # STANDARD references (e.g., "Standard 1", "SNR 2.1")
        standard_pattern = r'\b(?:Standard|SNR|Std\.?)\s+(\d+(?:\.\d+)?)\b'
        for match in re.finditer(standard_pattern, text, re.IGNORECASE):
            entities.append({
                'entity': match.group(0),
                'type': 'STANDARD',
                'start': match.start(),
                'end': match.end(),
                'value': match.group(1)
            })
        
        # CLAUSE references (e.g., "Clause 1.1", "1.5.2")
        clause_pattern = r'\b(?:Clause\s+)?(\d+\.\d+(?:\.\d+)?)\b'
        for match in re.finditer(clause_pattern, text):
            entities.append({
                'entity': match.group(0),
                'type': 'CLAUSE',
                'start': match.start(),
                'end': match.end(),
                'value': match.group(1)
            })
        
        # DATE patterns (e.g., "01/01/2024", "January 2024")
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
        ]
        for pattern in date_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    'entity': match.group(0),
                    'type': 'DATE',
                    'start': match.start(),
                    'end': match.end()
                })
        
        # QUALIFICATION codes (e.g., "TAE40116", "BSB50420")
        qual_pattern = r'\b[A-Z]{3}\d{5}\b'
        for match in re.finditer(qual_pattern, text):
            entities.append({
                'entity': match.group(0),
                'type': 'QUALIFICATION',
                'start': match.start(),
                'end': match.end()
            })
        
        # ORG - Common RTO-related organizations
        org_keywords = ['ASQA', 'RTO', 'Training Organisation', 'VET', 'AQF', 'TGA']
        for keyword in org_keywords:
            for match in re.finditer(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                entities.append({
                    'entity': match.group(0),
                    'type': 'ORG',
                    'start': match.start(),
                    'end': match.end()
                })
        
        # POLICY references
        policy_pattern = r'\b(?:Policy|Procedure)\s+([A-Z0-9-]+)\b'
        for match in re.finditer(policy_pattern, text, re.IGNORECASE):
            entities.append({
                'entity': match.group(0),
                'type': 'POLICY',
                'start': match.start(),
                'end': match.end(),
                'value': match.group(1)
            })
        
        # Remove duplicates (keep first occurrence)
        seen = set()
        unique_entities = []
        for entity in entities:
            key = (entity['entity'], entity['type'], entity['start'])
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
        
        return unique_entities
    
    def _auto_tag_clauses(self, evidence, text, ner_entities):
        """
        Auto-tag ASQA clauses based on NER entities and rule-based matching
        """
        text_lower = text.lower()
        auto_tagged_count = 0
        
        # Extract entity values for matching
        standard_refs = [e['value'] for e in ner_entities if e['type'] == 'STANDARD' and 'value' in e]
        clause_refs = [e['value'] for e in ner_entities if e['type'] == 'CLAUSE' and 'value' in e]
        
        # Get all ASQA clauses
        all_clauses = ASQAClause.objects.select_related('standard').all()
        
        for clause in all_clauses:
            mapping_type = None
            confidence_score = 0.0
            matched_entities = []
            matched_keywords = []
            rule_name = None
            
            # Rule 1: Direct clause number reference
            clause_num = clause.clause_number
            if clause_num in clause_refs or f"clause {clause_num}" in text_lower:
                mapping_type = 'auto_rule'
                confidence_score = 0.95
                rule_name = 'direct_clause_reference'
                matched_entities = [e for e in ner_entities if e.get('value') == clause_num]
            
            # Rule 2: Standard reference + keyword matching
            elif not mapping_type:
                standard_num = clause.standard.standard_number
                if standard_num in standard_refs or f"standard {standard_num}" in text_lower:
                    # Check keyword overlap
                    clause_keywords = clause.keywords or []
                    keywords_found = [kw for kw in clause_keywords if kw.lower() in text_lower]
                    
                    if len(keywords_found) >= 2:  # At least 2 keywords match
                        mapping_type = 'auto_ner'
                        confidence_score = min(0.7 + (len(keywords_found) * 0.05), 0.9)
                        rule_name = 'standard_reference_with_keywords'
                        matched_keywords = keywords_found
                        matched_entities = [e for e in ner_entities if e.get('value') == standard_num]
            
            # Rule 3: High keyword density (without standard reference)
            if not mapping_type:
                clause_keywords = clause.keywords or []
                if clause_keywords:
                    keywords_found = [kw for kw in clause_keywords if kw.lower() in text_lower]
                    keyword_ratio = len(keywords_found) / len(clause_keywords)
                    
                    if keyword_ratio >= 0.6:  # 60% of keywords present
                        mapping_type = 'auto_rule'
                        confidence_score = min(0.5 + (keyword_ratio * 0.3), 0.8)
                        rule_name = 'high_keyword_density'
                        matched_keywords = keywords_found
            
            # Rule 4: Title/topic similarity
            if not mapping_type and clause.title:
                title_words = set(clause.title.lower().split())
                title_words = {w for w in title_words if len(w) > 3}  # Filter short words
                
                if title_words:
                    title_matches = [w for w in title_words if w in text_lower]
                    title_ratio = len(title_matches) / len(title_words)
                    
                    if title_ratio >= 0.5:  # 50% of title words present
                        mapping_type = 'suggested'
                        confidence_score = min(0.4 + (title_ratio * 0.2), 0.6)
                        rule_name = 'title_similarity'
                        matched_keywords = title_matches
            
            # Create mapping if any rule matched
            if mapping_type and confidence_score >= 0.4:  # Minimum confidence threshold
                ClauseEvidence.objects.get_or_create(
                    asqa_clause=clause,
                    evidence=evidence,
                    defaults={
                        'mapping_type': mapping_type,
                        'confidence_score': confidence_score,
                        'matched_entities': matched_entities,
                        'matched_keywords': matched_keywords,
                        'rule_name': rule_name,
                        'rule_metadata': {
                            'processed_at': timezone.now().isoformat(),
                            'text_length': len(text),
                            'entity_count': len(ner_entities)
                        }
                    }
                )
                auto_tagged_count += 1
        
        return auto_tagged_count


class ClauseEvidenceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing clause-evidence mappings
    """
    serializer_class = ClauseEvidenceSerializer
    
    def get_queryset(self):
        tenant_id = self.kwargs.get('tenant_id')
        return ClauseEvidence.objects.filter(
            evidence__tenant_id=tenant_id
        ).select_related(
            'asqa_clause', 'asqa_clause__standard',
            'evidence', 'verified_by'
        )
    
    @action(detail=False, methods=['get'])
    def gaps(self, request, tenant_id=None):
        """
        Identify clauses with insufficient evidence (gap analysis)
        """
        standard_ids = request.query_params.getlist('standard_ids')
        
        # Get clauses for specified standards
        clauses_query = ASQAClause.objects.all()
        if standard_ids:
            clauses_query = clauses_query.filter(standard_id__in=standard_ids)
        
        gaps = []
        for clause in clauses_query.select_related('standard'):
            # Count evidence for this clause
            evidence_count = ClauseEvidence.objects.filter(
                asqa_clause=clause,
                evidence__tenant_id=tenant_id,
                evidence__status__in=['tagged', 'reviewed', 'approved']
            ).count()
            
            verified_count = ClauseEvidence.objects.filter(
                asqa_clause=clause,
                evidence__tenant_id=tenant_id,
                evidence__status__in=['tagged', 'reviewed', 'approved'],
                is_verified=True
            ).count()
            
            # Determine if sufficient evidence
            has_sufficient = verified_count >= 2  # At least 2 verified evidence items
            
            # Calculate gap severity
            if clause.compliance_level == 'critical':
                gap_severity = 'critical' if evidence_count == 0 else ('major' if verified_count < 2 else 'none')
            elif clause.compliance_level == 'essential':
                gap_severity = 'major' if evidence_count == 0 else ('minor' if verified_count < 1 else 'none')
            else:
                gap_severity = 'minor' if evidence_count == 0 else 'none'
            
            # Generate recommendations
            recommendations = []
            if evidence_count == 0:
                recommendations.append(f"Upload evidence for {clause.clause_number}")
                recommendations.append(f"Review policies related to: {', '.join(clause.keywords[:3]) if clause.keywords else 'this clause'}")
            elif verified_count < 2:
                recommendations.append(f"Verify existing evidence for {clause.clause_number}")
                recommendations.append("Upload additional supporting evidence")
            
            if gap_severity != 'none':
                gaps.append({
                    'asqa_clause': clause.id,
                    'clause_number': clause.clause_number,
                    'clause_title': clause.title,
                    'compliance_level': clause.compliance_level,
                    'evidence_count': evidence_count,
                    'verified_evidence_count': verified_count,
                    'has_sufficient_evidence': has_sufficient,
                    'gap_severity': gap_severity,
                    'recommendations': recommendations
                })
        
        return Response({
            'total_clauses': clauses_query.count(),
            'clauses_with_gaps': len(gaps),
            'critical_gaps': len([g for g in gaps if g['gap_severity'] == 'critical']),
            'major_gaps': len([g for g in gaps if g['gap_severity'] == 'major']),
            'minor_gaps': len([g for g in gaps if g['gap_severity'] == 'minor']),
            'gaps': gaps
        })


class AuditReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for audit report management
    """
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AuditReportDetailSerializer
        return AuditReportSerializer
    
    def get_queryset(self):
        tenant_id = self.kwargs.get('tenant_id')
        return AuditReport.objects.filter(tenant_id=tenant_id).prefetch_related(
            'asqa_standards',
            Prefetch('clause_entries', queryset=AuditReportClause.objects.select_related('asqa_clause'))
        )
    
    def perform_create(self, serializer):
        tenant_id = self.kwargs.get('tenant_id')
        audit_report = serializer.save(
            tenant_id=tenant_id,
            created_by=self.request.user
        )
        
        # Auto-generate clause entries
        self._generate_clause_entries(audit_report)
        
        # Calculate metrics
        audit_report.calculate_metrics()
    
    @action(detail=True, methods=['post'])
    def generate_report(self, request, tenant_id=None, pk=None):
        """
        Generate clause-by-clause audit report with evidence mapping
        """
        audit_report = self.get_object()
        
        # Regenerate clause entries
        audit_report.clause_entries.all().delete()
        self._generate_clause_entries(audit_report)
        
        # Recalculate metrics
        audit_report.calculate_metrics()
        
        return Response(
            AuditReportDetailSerializer(audit_report, context={'request': request}).data
        )
    
    @action(detail=True, methods=['post'])
    def submit(self, request, tenant_id=None, pk=None):
        """
        Submit audit report (mark as submitted to ASQA)
        """
        audit_report = self.get_object()
        
        if audit_report.status == 'submitted':
            return Response(
                {'error': 'Report already submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        audit_report.status = 'submitted'
        audit_report.submitted_at = timezone.now()
        audit_report.submitted_by = request.user
        audit_report.save()
        
        return Response(
            AuditReportSerializer(audit_report, context={'request': request}).data
        )
    
    def _generate_clause_entries(self, audit_report):
        """
        Generate clause entries for all clauses in selected standards
        """
        all_clauses = ASQAClause.objects.filter(
            standard__in=audit_report.asqa_standards.all()
        ).select_related('standard')
        
        for clause in all_clauses:
            entry = AuditReportClause.objects.create(
                audit_report=audit_report,
                asqa_clause=clause
            )
            
            # Update evidence counts and determine compliance
            entry.update_evidence_counts()
            
            # Link evidence
            evidence_mappings = ClauseEvidence.objects.filter(
                asqa_clause=clause,
                evidence__tenant=audit_report.tenant,
                evidence__status__in=['tagged', 'reviewed', 'approved']
            ).select_related('evidence')
            
            for mapping in evidence_mappings:
                entry.linked_evidence.add(mapping.evidence)
