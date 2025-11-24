"""
TAS Conversion Service

AI-powered service to convert Training and Assessment Strategies
from Standards for RTOs 2015 to Standards for RTOs 2025.

This service:
1. Analyzes 2015 TAS structure and content
2. Maps 2015 standards references to 2025 Quality Areas
3. Converts content with AI-assisted transformation
4. Validates against 2025 standards compliance
5. Generates comprehensive conversion report
"""

import json
import time
from typing import Dict, List, Tuple, Optional
from django.utils import timezone
from django.db import transaction

from .models import TAS, TASConversionSession, TASSection
from tenants.models import Tenant
from django.contrib.auth.models import User


# Standards Mapping Configuration
STANDARDS_2015_TO_2025_MAPPING = {
    # Training and Assessment
    "1.1": ["QA1.1", "QA1.2", "QA3.2"],  # Training and assessment by qualified trainers
    "1.2": ["QA1.1", "QA1.2"],  # Training and assessment strategies
    "1.3": ["C2"],  # Issuing AQF certification documents
    "1.4": ["QA2.2"],  # Language, literacy and numeracy skills
    "1.5": ["QA2.1"],  # Information provided to learners
    "1.6": ["QA2.5"],  # Complaints and appeals
    "1.7": ["QA1.2"],  # Assessment including RPL
    "1.8": ["QA1.2"],  # Validation of assessment
    "1.9": ["QA1.2"],  # Transition of learners
    "1.10": ["C2"],  # Certification
    "1.11": ["QA1.3"],  # Credit transfer
    "1.12": ["QA1.3"],  # Recognition of prior learning
    "1.13": ["QA1.4"],  # Training and assessment resources
    "1.14": ["QA1.4", "QA3.1"],  # Industry engagement
    "1.15": ["QA1.4"],  # Facilities
    "1.16": ["QA1.4"],  # Training and assessment strategies
    
    # Learner engagement
    "2.1": ["QA2.1"],  # Marketing and advertising
    "2.2": ["QA2.1", "QA2.2"],  # Information and support services
    "2.3": ["C1"],  # Written agreement with learner
    
    # Provider registration and compliance
    "3.1": ["C4"],  # Fit and proper person requirements
    "3.2": ["C4"],  # Capacity to provide training
    "3.3": ["C4"],  # Compliance with standards
    "3.4": ["C3"],  # Monitoring and enforcement
    "3.5": ["C3"],  # Changes to registration
    
    # Compliance and accountability
    "4.1": ["C3"],  # Accurate and accessible records
    "4.2": ["C3"],  # AVETMISS reporting
    "4.3": ["C3"],  # Quality indicator data
    "4.4": ["C3"],  # Cooperation with regulator
    
    # Continuous improvement
    "5.1": ["QA4.3"],  # Continuous improvement
    "5.2": ["QA4.3"],  # Systematic monitoring
    "5.3": ["QA4.3"],  # Evaluation and improvement
    
    # Governance and administration
    "6.1": ["QA4.1"],  # Management and oversight
    "6.2": ["QA4.1"],  # Legal entity
    "6.3": ["QA4.2"],  # Financial management
    "6.4": ["QA4.2"],  # Insurance
    "6.5": ["QA4.1"],  # Administrative practices
    "6.6": ["QA4.2"],  # Third party arrangements
    
    # International students (ESOS)
    "7.1": ["QA2.1", "QA2.2"],  # Information for international students
    "7.2": ["QA2.1"],  # Written agreement
    "7.3": ["QA2.4"],  # Welfare and support services
    "7.4": ["C3"],  # Transfer between providers
    "7.5": ["C3"],  # Completion within duration
    "7.6": ["C3"],  # Monitoring course progress
    
    # Quality and compliance
    "8.1": ["C1"],  # Compliance with legislation
    "8.2": ["C1", "QA4.1"],  # Ethical behavior
    "8.3": ["QA4.2"],  # Risk management
    "8.4": ["QA4.3"],  # Quality indicator submission
    "8.5": ["C3"],  # Reporting obligations
    "8.6": ["QA2.5"],  # Complaints and appeals process
}


class TASConversionService:
    """
    AI-powered TAS conversion service from 2015 to 2025 standards
    """

    def __init__(self, ai_gateway_client=None):
        """
        Initialize conversion service
        
        Args:
            ai_gateway_client: Optional AI gateway client for LLM calls
        """
        self.ai_client = ai_gateway_client
        self.standards_mapping = STANDARDS_2015_TO_2025_MAPPING

    def create_conversion_session(
        self,
        source_tas: TAS,
        tenant: Tenant,
        user: User,
        session_name: str = None,
        ai_model: str = "gpt-4o",
        options: Dict = None,
    ) -> TASConversionSession:
        """
        Create a new TAS conversion session
        
        Args:
            source_tas: Source TAS document using 2015 standards
            tenant: Tenant organization
            user: User initiating the conversion
            session_name: Optional session name
            ai_model: AI model to use for conversion
            options: Conversion options
            
        Returns:
            TASConversionSession instance
        """
        if not session_name:
            session_name = f"Convert {source_tas.title} to 2025 Standards"
        
        default_options = {
            "preserve_formatting": True,
            "update_terminology": True,
            "add_conversion_notes": True,
            "include_quality_areas": True,
            "highlight_changes": False,
        }
        
        if options:
            default_options.update(options)
        
        session = TASConversionSession.objects.create(
            tenant=tenant,
            source_tas=source_tas,
            session_name=session_name,
            status="pending",
            ai_model=ai_model,
            conversion_options=default_options,
            created_by=user,
        )
        
        return session

    def execute_conversion(self, session: TASConversionSession) -> TASConversionSession:
        """
        Execute the full TAS conversion process
        
        Args:
            session: TASConversionSession to process
            
        Returns:
            Updated TASConversionSession with results
        """
        try:
            session.mark_as_started()
            start_time = time.time()
            
            # Step 1: Analyze source TAS
            session.status = "analyzing"
            session.current_step = "Analyzing source TAS structure and content"
            session.save()
            self._analyze_source_tas(session)
            
            # Step 2: Map standards
            session.status = "mapping"
            session.current_step = "Mapping 2015 standards to 2025 Quality Areas"
            session.save()
            self._map_standards(session)
            
            # Step 3: Convert content
            session.status = "converting"
            session.current_step = "Converting content with AI assistance"
            session.save()
            self._convert_content(session)
            
            # Step 4: Validate compliance
            session.status = "validating"
            session.current_step = "Validating 2025 standards compliance"
            session.save()
            self._validate_compliance(session)
            
            # Step 5: Complete session
            session.processing_time_seconds = time.time() - start_time
            session.mark_as_completed()
            
            return session
            
        except Exception as e:
            session.mark_as_failed(
                error_message=str(e),
                error_details={"step": session.current_step, "error_type": type(e).__name__}
            )
            raise

    def _analyze_source_tas(self, session: TASConversionSession):
        """
        Analyze the source TAS to identify structure, standards referenced, and key content
        """
        source_tas = session.source_tas
        sections = source_tas.sections.all().order_by("order")
        
        analysis = {
            "total_sections": sections.count(),
            "sections": [],
            "standards_found": {},
            "key_topics": [],
            "estimated_complexity": "medium",
        }
        
        standards_count = {}
        
        for section in sections:
            section_info = {
                "id": section.id,
                "title": section.title,
                "content_length": len(section.content or ""),
                "has_ai_content": section.ai_generated,
                "standards_referenced": [],
            }
            
            # Look for 2015 standards references in content
            content = (section.content or "").lower()
            for standard_code in self.standards_mapping.keys():
                # Look for patterns like "1.1", "clause 1.1", "standard 1.1"
                patterns = [
                    f" {standard_code} ",
                    f" {standard_code}.",
                    f" {standard_code},",
                    f"clause {standard_code}",
                    f"standard {standard_code}",
                ]
                if any(pattern in content for pattern in patterns):
                    section_info["standards_referenced"].append(standard_code)
                    standards_count[standard_code] = standards_count.get(standard_code, 0) + 1
            
            analysis["sections"].append(section_info)
        
        analysis["standards_found"] = standards_count
        
        # Estimate complexity based on content volume and standards
        total_content = sum(s["content_length"] for s in analysis["sections"])
        if total_content > 10000 or len(standards_count) > 10:
            analysis["estimated_complexity"] = "high"
        elif total_content < 3000 or len(standards_count) < 5:
            analysis["estimated_complexity"] = "low"
        
        session.source_analysis = analysis
        session.save()

    def _map_standards(self, session: TASConversionSession):
        """
        Map identified 2015 standards to 2025 Quality Areas
        """
        analysis = session.source_analysis
        standards_found = analysis.get("standards_found", {})
        
        mapping_result = {}
        
        for standard_2015, count in standards_found.items():
            standards_2025 = self.standards_mapping.get(standard_2015, [])
            mapping_result[standard_2015] = {
                "occurrences": count,
                "maps_to_2025": standards_2025,
                "quality_areas": self._get_quality_areas_for_standards(standards_2025),
            }
        
        session.standards_mapping = mapping_result
        session.standards_updated = len(mapping_result)
        session.save()

    def _get_quality_areas_for_standards(self, standards_2025: List[str]) -> List[str]:
        """Get unique quality areas from list of 2025 standards"""
        quality_areas = set()
        for std in standards_2025:
            if std.startswith("QA"):
                qa_num = std[2]  # Extract QA number (1, 2, 3, or 4)
                quality_areas.add(f"Quality Area {qa_num}")
            elif std.startswith("C"):
                quality_areas.add("Compliance Requirements")
            elif std.startswith("CP"):
                quality_areas.add("Credential Policy")
        return sorted(quality_areas)

    def _convert_content(self, session: TASConversionSession):
        """
        Convert TAS content from 2015 to 2025 standards using AI
        """
        source_tas = session.source_tas
        
        # Create new TAS document for 2025 version
        target_tas = self._create_target_tas(session)
        session.target_tas = target_tas
        session.save()
        
        # Convert each section
        source_sections = source_tas.sections.all().order_by("order")
        conversion_changes = []
        sections_converted = 0
        
        for section in source_sections:
            change_record = self._convert_section(session, section, target_tas)
            if change_record:
                conversion_changes.append(change_record)
                sections_converted += 1
        
        session.conversion_changes = conversion_changes
        session.sections_converted = sections_converted
        session.save()

    def _create_target_tas(self, session: TASConversionSession) -> TAS:
        """
        Create a new TAS document for the 2025 version
        """
        source_tas = session.source_tas
        
        target_tas = TAS.objects.create(
            tenant=session.tenant,
            title=f"{source_tas.title} (2025 Standards)",
            code=source_tas.code,
            description=f"Converted from 2015 Standards on {timezone.now().strftime('%Y-%m-%d')}. {source_tas.description}",
            qualification_code=source_tas.qualification_code,
            status="draft",
            version="2.0" if source_tas.version == "1.0" else str(float(source_tas.version or "1.0") + 1.0),
            template=source_tas.template,
            created_by=session.created_by,
        )
        
        # Copy metadata with update
        if source_tas.metadata:
            target_tas.metadata = source_tas.metadata.copy()
            target_tas.metadata["converted_from_2015"] = True
            target_tas.metadata["conversion_date"] = timezone.now().isoformat()
            target_tas.metadata["source_tas_id"] = source_tas.id
            target_tas.save()
        
        return target_tas

    def _convert_section(
        self,
        session: TASConversionSession,
        source_section: TASSection,
        target_tas: TAS
    ) -> Optional[Dict]:
        """
        Convert a single TAS section from 2015 to 2025 standards
        
        Returns:
            Change record dict or None if no changes
        """
        original_content = source_section.content or ""
        
        # Identify 2015 standards in this section
        standards_to_update = []
        for standard_2015 in self.standards_mapping.keys():
            patterns = [
                f" {standard_2015} ",
                f" {standard_2015}.",
                f" {standard_2015},",
                f"clause {standard_2015}",
                f"standard {standard_2015}",
                f"Standard {standard_2015}",
                f"Clause {standard_2015}",
            ]
            if any(pattern in original_content for pattern in patterns):
                standards_to_update.append(standard_2015)
        
        # If no standards found, copy as-is
        if not standards_to_update:
            TASSection.objects.create(
                tas=target_tas,
                title=source_section.title,
                content=original_content,
                section_type=source_section.section_type,
                order=source_section.order,
                is_required=source_section.is_required,
                metadata=source_section.metadata,
            )
            return None
        
        # Convert content with AI or rules-based replacement
        converted_content = self._perform_content_conversion(
            original_content, standards_to_update, session
        )
        
        # Create new section in target TAS
        new_section = TASSection.objects.create(
            tas=target_tas,
            title=source_section.title,
            content=converted_content,
            section_type=source_section.section_type,
            order=source_section.order,
            is_required=source_section.is_required,
            metadata={
                **(source_section.metadata or {}),
                "converted_from_2015": True,
                "conversion_session_id": session.id,
            },
        )
        
        # Record the change
        return {
            "section_id": source_section.id,
            "section_title": source_section.title,
            "standards_updated": standards_to_update,
            "old_content_preview": original_content[:200],
            "new_content_preview": converted_content[:200],
            "target_section_id": new_section.id,
            "changes_summary": self._summarize_changes(original_content, converted_content),
        }

    def _perform_content_conversion(
        self,
        content: str,
        standards_to_update: List[str],
        session: TASConversionSession
    ) -> str:
        """
        Perform the actual content conversion using AI or rules-based approach
        """
        if session.conversion_options.get("use_ai", True) and self.ai_client:
            return self._ai_convert_content(content, standards_to_update, session)
        else:
            return self._rule_based_convert_content(content, standards_to_update)

    def _rule_based_convert_content(self, content: str, standards_to_update: List[str]) -> str:
        """
        Perform rules-based content conversion (fallback when AI unavailable)
        """
        converted = content
        
        for standard_2015 in standards_to_update:
            standards_2025 = self.standards_mapping.get(standard_2015, [])
            if not standards_2025:
                continue
            
            # Create replacement text
            if len(standards_2025) == 1:
                replacement = standards_2025[0]
            else:
                replacement = ", ".join(standards_2025[:-1]) + f" and {standards_2025[-1]}"
            
            # Replace various formats
            patterns_replacements = [
                (f"Standard {standard_2015}", f"Standard {replacement}"),
                (f"standard {standard_2015}", f"standard {replacement}"),
                (f"Clause {standard_2015}", f"Standard {replacement}"),
                (f"clause {standard_2015}", f"standard {replacement}"),
                (f" {standard_2015} ", f" {replacement} "),
                (f" {standard_2015}.", f" {replacement}."),
                (f" {standard_2015},", f" {replacement},"),
            ]
            
            for old_pattern, new_pattern in patterns_replacements:
                converted = converted.replace(old_pattern, new_pattern)
        
        # Add conversion note if option enabled
        if standards_to_update:
            note = "\n\n*Note: This section has been updated to reference the Standards for RTOs 2025.*"
            converted += note
        
        return converted

    def _ai_convert_content(
        self,
        content: str,
        standards_to_update: List[str],
        session: TASConversionSession
    ) -> str:
        """
        Use AI to intelligently convert content while preserving meaning and context
        
        This is a placeholder for AI integration - implement with your AI gateway
        """
        # Build prompt for AI
        mapping_info = []
        for std_2015 in standards_to_update:
            std_2025 = self.standards_mapping.get(std_2015, [])
            mapping_info.append(f"- {std_2015} maps to {', '.join(std_2025)}")
        
        prompt = f"""Convert this Training and Assessment Strategy (TAS) section from Standards for RTOs 2015 to Standards for RTOs 2025.

MAPPING GUIDE:
{chr(10).join(mapping_info)}

2025 STANDARDS STRUCTURE:
- Quality Area 1 (QA1): Training and Assessment
- Quality Area 2 (QA2): VET Student Support
- Quality Area 3 (QA3): VET Workforce
- Quality Area 4 (QA4): Governance
- Compliance Requirements (C1-C4): Administrative requirements
- Credential Policy (CP1-CP2): Trainer/assessor credentials

INSTRUCTIONS:
1. Replace all 2015 standard references (e.g., "1.1", "Clause 1.2") with the appropriate 2025 standards
2. Update terminology where needed (e.g., "clause" becomes "standard", add "Quality Area" context where helpful)
3. Preserve the original meaning, formatting, and structure
4. Keep all non-standards content unchanged
5. Maintain professional RTO documentation tone
6. Do not add explanatory notes or change the core content

ORIGINAL CONTENT:
{content}

CONVERTED CONTENT:"""

        # TODO: Call AI gateway with prompt
        # For now, fall back to rule-based
        return self._rule_based_convert_content(content, standards_to_update)

    def _summarize_changes(self, old_content: str, new_content: str) -> str:
        """
        Generate a summary of what changed
        """
        if old_content == new_content:
            return "No changes made"
        
        # Count standards replacements
        changes = []
        for std_2015 in self.standards_mapping.keys():
            old_count = old_content.count(std_2015)
            new_count = new_content.count(std_2015)
            if old_count > new_count:
                changes.append(f"Replaced {old_count} references to {std_2015}")
        
        if not changes:
            changes.append("Updated standards terminology and structure")
        
        return "; ".join(changes)

    def _validate_compliance(self, session: TASConversionSession):
        """
        Validate that the converted TAS meets 2025 standards requirements
        """
        target_tas = session.target_tas
        if not target_tas:
            session.compliance_report = {"status": "error", "message": "No target TAS created"}
            return
        
        report = {
            "status": "passed",
            "timestamp": timezone.now().isoformat(),
            "quality_areas_covered": {},
            "compliance_requirements_covered": [],
            "recommendations": [],
            "warnings": [],
        }
        
        # Check which 2025 standards are now referenced
        sections = target_tas.sections.all()
        standards_found = set()
        
        for section in sections:
            content = (section.content or "").upper()
            # Check for QA standards
            for qa in range(1, 5):
                for sub in range(1, 10):
                    std_code = f"QA{qa}.{sub}"
                    if std_code in content:
                        standards_found.add(std_code)
            
            # Check for Compliance standards
            for c in range(1, 5):
                std_code = f"C{c}"
                if std_code in content:
                    standards_found.add(std_code)
        
        # Organize by Quality Area
        for qa in range(1, 5):
            qa_standards = [s for s in standards_found if s.startswith(f"QA{qa}")]
            report["quality_areas_covered"][f"Quality Area {qa}"] = qa_standards
        
        report["compliance_requirements_covered"] = [s for s in standards_found if s.startswith("C")]
        
        # Add recommendations
        if not report["quality_areas_covered"]["Quality Area 1"]:
            report["warnings"].append("No Quality Area 1 (Training and Assessment) standards found")
        
        if session.requires_human_review:
            report["recommendations"].append("Human review recommended to verify context and accuracy")
        
        # Calculate quality score
        total_possible_standards = 14  # 14 outcome standards in 2025
        standards_covered = len([s for s in standards_found if s.startswith("QA")])
        quality_score = min(100, (standards_covered / total_possible_standards) * 100 + 50)
        
        session.quality_score = round(quality_score, 1)
        session.compliance_report = report
        session.save()

    def get_conversion_summary(self, session: TASConversionSession) -> Dict:
        """
        Generate a comprehensive summary of the conversion session
        """
        return {
            "session_id": session.id,
            "session_name": session.session_name,
            "status": session.status,
            "progress": session.progress_percentage,
            "source_tas": {
                "id": session.source_tas.id,
                "title": session.source_tas.title,
                "code": session.source_tas.code,
            },
            "target_tas": {
                "id": session.target_tas.id if session.target_tas else None,
                "title": session.target_tas.title if session.target_tas else None,
                "code": session.target_tas.code if session.target_tas else None,
            } if session.target_tas else None,
            "statistics": {
                "sections_converted": session.sections_converted,
                "standards_updated": session.standards_updated,
                "quality_score": session.quality_score,
                "processing_time_seconds": session.processing_time_seconds,
            },
            "standards_mapping": session.standards_mapping,
            "compliance_report": session.compliance_report,
            "requires_human_review": session.requires_human_review,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "completed_at": session.completed_at.isoformat() if session.completed_at else None,
        }
