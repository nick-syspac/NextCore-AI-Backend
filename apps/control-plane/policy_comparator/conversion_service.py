"""
Policy Conversion Service: 2015 → 2025 ASQA Standards
Converts RTO policy documents from Standards for RTOs 2015 to Standards for RTOs 2025
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


# Comprehensive mapping from 2015 Standards to 2025 Standards
# Based on official ASQA guidance and standards alignment
STANDARDS_2015_TO_2025_MAPPING = {
    # Standard 1: Training and Assessment
    "1.1": {
        "2025_standards": ["QA1.1", "QA1.2", "QA3.2"],
        "quality_areas": ["Quality Area 1: Training and Assessment", "Quality Area 3: VET Workforce"],
        "description": "Training and assessment by qualified trainers → Training delivery, Assessment practices, Trainer credentials"
    },
    "1.2": {
        "2025_standards": ["QA1.1", "QA1.2"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Training and assessment strategies → Training delivery and Assessment practices"
    },
    "1.3": {
        "2025_standards": ["QA1.1"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Supervision of training and assessment → Training delivery"
    },
    "1.4": {
        "2025_standards": ["QA2.2"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Language, literacy and numeracy → Training support"
    },
    "1.5": {
        "2025_standards": ["QA2.1", "QA2.2"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Training and assessment strategies → Information provision and Training support"
    },
    "1.6": {
        "2025_standards": ["QA2.2"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Training and assessment support → Training support"
    },
    "1.7": {
        "2025_standards": ["QA1.1", "QA1.2"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Industry engagement → Training delivery and Assessment practices"
    },
    "1.8": {
        "2025_standards": ["QA1.2"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Validation of assessment → Assessment practices"
    },
    "1.9": {
        "2025_standards": ["QA1.2"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Assessment validation → Assessment practices"
    },
    "1.10": {
        "2025_standards": ["QA1.2"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Recognition of prior learning → Assessment practices"
    },
    "1.11": {
        "2025_standards": ["QA1.3"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Credit transfer → RPL and Credit Transfer"
    },
    "1.12": {
        "2025_standards": ["QA1.3"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Credit arrangements → RPL and Credit Transfer"
    },
    "1.13": {
        "2025_standards": ["QA1.4"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Resources and facilities → Facilities and Resources"
    },
    "1.14": {
        "2025_standards": ["QA1.4"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Industry currency of training resources → Facilities and Resources"
    },
    "1.15": {
        "2025_standards": ["QA1.4"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Training facilities → Facilities and Resources"
    },
    "1.16": {
        "2025_standards": ["QA1.4"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Simulated learning environments → Facilities and Resources"
    },

    # Standard 2: Educational and Support Services
    "2.1": {
        "2025_standards": ["QA2.1", "QA2.2"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Information and support services → Information provision and Training support"
    },
    "2.2": {
        "2025_standards": ["QA2.1"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Information provision → Information provision"
    },
    "2.3": {
        "2025_standards": ["QA2.3"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Welfare and guidance → Diversity and Inclusion"
    },

    # Standard 3: Certification
    "3.1": {
        "2025_standards": ["C2"],
        "quality_areas": ["Compliance Requirements"],
        "description": "Issuing AQF certification → Integrity of NRT Products"
    },
    "3.2": {
        "2025_standards": ["C2"],
        "quality_areas": ["Compliance Requirements"],
        "description": "Packaging qualifications → Integrity of NRT Products"
    },
    "3.3": {
        "2025_standards": ["C2"],
        "quality_areas": ["Compliance Requirements"],
        "description": "Issuing statements of attainment → Integrity of NRT Products"
    },
    "3.4": {
        "2025_standards": ["C2"],
        "quality_areas": ["Compliance Requirements"],
        "description": "Replacement testamurs → Integrity of NRT Products"
    },
    "3.5": {
        "2025_standards": ["C2"],
        "quality_areas": ["Compliance Requirements"],
        "description": "Records retention → Integrity of NRT Products"
    },

    # Standard 4: Employer Engagement
    "4.1": {
        "2025_standards": ["QA1.1"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Industry engagement → Training delivery"
    },
    "4.2": {
        "2025_standards": ["QA1.1"],
        "quality_areas": ["Quality Area 1: Training and Assessment"],
        "description": "Employer satisfaction → Training delivery"
    },

    # Standard 5: Continuous Improvement
    "5.1": {
        "2025_standards": ["QA4.3"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Continuous improvement → Continuous Improvement"
    },
    "5.2": {
        "2025_standards": ["QA4.3"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Systematic monitoring → Continuous Improvement"
    },
    "5.3": {
        "2025_standards": ["QA4.3"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Data collection and analysis → Continuous Improvement"
    },

    # Standard 6: Complaints and Appeals
    "6.1": {
        "2025_standards": ["QA2.5"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Complaints and appeals process → Complaints and Appeals"
    },
    "6.2": {
        "2025_standards": ["QA2.5"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Access to complaints process → Complaints and Appeals"
    },
    "6.3": {
        "2025_standards": ["QA2.5"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Review of decisions → Complaints and Appeals"
    },
    "6.4": {
        "2025_standards": ["QA2.5"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Records of complaints and appeals → Complaints and Appeals"
    },
    "6.5": {
        "2025_standards": ["QA2.5"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Complaint analysis → Complaints and Appeals"
    },
    "6.6": {
        "2025_standards": ["QA2.5"],
        "quality_areas": ["Quality Area 2: VET Student Support"],
        "description": "Independent review → Complaints and Appeals"
    },

    # Standard 7: Governance and Administration
    "7.1": {
        "2025_standards": ["QA4.1"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Governance framework → Leadership and Accountability"
    },
    "7.2": {
        "2025_standards": ["QA4.1"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Management responsibilities → Leadership and Accountability"
    },
    "7.3": {
        "2025_standards": ["QA4.2"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Risk management → Risk Management"
    },
    "7.4": {
        "2025_standards": ["QA4.1"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Quality assurance → Leadership and Accountability"
    },
    "7.5": {
        "2025_standards": ["C1"],
        "quality_areas": ["Compliance Requirements"],
        "description": "Provision of information → Information and Transparency"
    },
    "7.6": {
        "2025_standards": ["C3"],
        "quality_areas": ["Compliance Requirements"],
        "description": "Obligations under funding contracts → Accountability"
    },

    # Standard 8: Financial Management
    "8.1": {
        "2025_standards": ["QA4.2"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Financial management → Risk Management"
    },
    "8.2": {
        "2025_standards": ["QA4.2"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Fee protection → Risk Management"
    },
    "8.3": {
        "2025_standards": ["QA4.2"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Financial viability → Risk Management"
    },
    "8.4": {
        "2025_standards": ["C1"],
        "quality_areas": ["Compliance Requirements"],
        "description": "Fee transparency → Information and Transparency"
    },
    "8.5": {
        "2025_standards": ["QA4.2"],
        "quality_areas": ["Quality Area 4: Governance"],
        "description": "Written agreements → Risk Management"
    },
    "8.6": {
        "2025_standards": ["C1"],
        "quality_areas": ["Compliance Requirements"],
        "description": "Consumer protection → Information and Transparency"
    },
}


class PolicyConversionService:
    """
    Service to convert RTO policies from 2015 to 2025 ASQA Standards
    
    Conversion Process:
    1. ANALYZE: Parse source policy and identify 2015 standards references
    2. MAP: Map 2015 standards to 2025 Quality Areas and Standards
    3. CONVERT: Transform policy content with AI assistance
    4. VALIDATE: Check compliance against 2025 Standards
    5. REPORT: Generate comprehensive conversion summary
    """

    def __init__(self):
        self.standards_mapping = STANDARDS_2015_TO_2025_MAPPING

    def create_conversion_session(
        self,
        tenant,
        source_policy,
        user,
        session_name: Optional[str] = None,
        ai_model: str = "gpt-4o",
        options: Optional[Dict] = None
    ):
        """
        Create a new policy conversion session
        
        Args:
            tenant: Tenant object
            source_policy: Policy object (based on 2015 Standards)
            user: User initiating conversion
            session_name: Optional name for the session
            ai_model: AI model to use (gpt-4o, claude-3-opus)
            options: Conversion options
        
        Returns:
            PolicyConversionSession object
        """
        from .models import PolicyConversionSession
        
        if not session_name:
            session_name = f"{source_policy.title} - 2025 Conversion"
        
        session = PolicyConversionSession.objects.create(
            tenant=tenant,
            source_policy=source_policy,
            session_name=session_name,
            ai_model=ai_model,
            created_by=user,
            status="pending"
        )
        
        logger.info(f"Created policy conversion session {session.id} for policy {source_policy.id}")
        return session

    def execute_conversion(self, session, options: Optional[Dict] = None):
        """
        Execute the full conversion process
        
        Args:
            session: PolicyConversionSession object
            options: Conversion options dict
                - preserve_formatting: bool (default: True)
                - update_terminology: bool (default: True)
                - add_conversion_notes: bool (default: True)
                - use_ai: bool (default: True)
        
        Returns:
            Updated session with conversion results
        """
        if options is None:
            options = {}
        
        try:
            session.mark_as_started()
            
            # Stage 1: Analyze source policy (15%)
            session.status = "analyzing"
            session.save()
            source_analysis = self._analyze_source_policy(session.source_policy)
            session.source_analysis = source_analysis
            session.progress_percentage = 15
            session.save()
            
            # Stage 2: Map standards (30%)
            session.status = "mapping"
            session.save()
            standards_mapping = self._map_standards(source_analysis)
            session.standards_mapping = standards_mapping
            session.progress_percentage = 30
            session.save()
            
            # Stage 3: Convert content (60%)
            session.status = "converting"
            session.save()
            converted_content, changes = self._convert_content(
                session.source_policy,
                standards_mapping,
                options
            )
            session.conversion_changes = changes
            session.progress_percentage = 60
            session.save()
            
            # Stage 4: Create target policy
            target_policy = self._create_target_policy(
                session.source_policy,
                converted_content,
                session
            )
            session.target_policy = target_policy
            session.save()
            
            # Stage 5: Validate compliance (85%)
            session.status = "validating"
            session.save()
            compliance_report = self._validate_compliance(target_policy, standards_mapping)
            session.compliance_report = compliance_report
            session.quality_score = compliance_report.get("quality_score", 0)
            session.requires_human_review = compliance_report.get("requires_review", True)
            session.progress_percentage = 85
            session.save()
            
            # Mark as completed (100%)
            session.mark_as_completed()
            
            logger.info(f"Completed conversion session {session.id}")
            return session
            
        except Exception as e:
            logger.error(f"Conversion failed for session {session.id}: {str(e)}")
            session.mark_as_failed(str(e))
            raise

    def _analyze_source_policy(self, policy) -> Dict:
        """
        Analyze source policy to identify structure and standards references
        
        Returns dict with:
        - total_sections: int
        - standards_found: list of 2015 standard numbers
        - complexity_score: float (0-10)
        - estimated_changes: int
        """
        content = policy.content
        
        # Find all 2015 standards references (e.g., "1.1", "Standard 1.1", "Clause 1.1")
        standards_pattern = r'(?:Standard|Clause|Section)?\s*([1-8]\.\d+)'
        matches = re.findall(standards_pattern, content)
        
        # Deduplicate
        standards_found = list(set(matches))
        standards_found.sort()
        
        # Count sections (basic heuristic: look for headers)
        sections = len(re.findall(r'\n#{1,3}\s+', content)) or content.count('\n\n') // 5
        
        # Estimate complexity
        word_count = len(content.split())
        complexity_score = min(10, (word_count / 500) + (len(standards_found) * 0.5))
        
        return {
            "total_sections": sections,
            "standards_found": standards_found,
            "standards_count": len(standards_found),
            "word_count": word_count,
            "complexity_score": round(complexity_score, 2),
            "estimated_changes": len(standards_found) * 2,  # Conservative estimate
            "analysis_timestamp": datetime.utcnow().isoformat()
        }

    def _map_standards(self, source_analysis: Dict) -> Dict:
        """
        Map 2015 standards found in policy to 2025 equivalents
        
        Returns dict with detailed mapping for each 2015 standard
        """
        standards_found = source_analysis.get("standards_found", [])
        mapping_results = {}
        
        for std_2015 in standards_found:
            if std_2015 in self.standards_mapping:
                mapping = self.standards_mapping[std_2015]
                mapping_results[std_2015] = {
                    "2025_standards": mapping["2025_standards"],
                    "quality_areas": mapping["quality_areas"],
                    "description": mapping["description"],
                    "occurrences": source_analysis.get("standards_count", 1)
                }
            else:
                # Unmapped standard - flag for manual review
                mapping_results[std_2015] = {
                    "2025_standards": [],
                    "quality_areas": [],
                    "description": "No automatic mapping available - requires manual review",
                    "requires_review": True
                }
        
        return {
            "total_mapped": len([m for m in mapping_results.values() if m["2025_standards"]]),
            "total_unmapped": len([m for m in mapping_results.values() if not m["2025_standards"]]),
            "mappings": mapping_results,
            "mapping_timestamp": datetime.utcnow().isoformat()
        }

    def _convert_content(
        self,
        source_policy,
        standards_mapping: Dict,
        options: Dict
    ) -> Tuple[str, List[Dict]]:
        """
        Convert policy content from 2015 to 2025 standards
        
        Returns:
            (converted_content, changes_list)
        """
        content = source_policy.content
        changes = []
        
        use_ai = options.get("use_ai", True)
        update_terminology = options.get("update_terminology", True)
        add_notes = options.get("add_conversion_notes", True)
        
        # If AI is enabled, use AI-powered conversion
        if use_ai:
            content, ai_changes = self._ai_convert_content(
                content,
                standards_mapping,
                options
            )
            changes.extend(ai_changes)
        else:
            # Rules-based conversion
            content, rule_changes = self._rules_based_conversion(
                content,
                standards_mapping,
                options
            )
            changes.extend(rule_changes)
        
        # Add conversion note at top if requested
        if add_notes:
            note = self._generate_conversion_note(source_policy)
            content = note + "\n\n" + content
            changes.append({
                "type": "metadata",
                "description": "Added conversion note",
                "location": "document_header"
            })
        
        return content, changes

    def _ai_convert_content(
        self,
        content: str,
        standards_mapping: Dict,
        options: Dict
    ) -> Tuple[str, List[Dict]]:
        """
        Use AI to intelligently convert policy content
        
        This is a placeholder for AI integration.
        In production, this would call the AI Gateway service.
        """
        # TODO: Implement AI Gateway integration
        # For now, fall back to rules-based conversion
        logger.info("AI conversion requested but not yet implemented - using rules-based fallback")
        return self._rules_based_conversion(content, standards_mapping, options)

    def _rules_based_conversion(
        self,
        content: str,
        standards_mapping: Dict,
        options: Dict
    ) -> Tuple[str, List[Dict]]:
        """
        Rules-based policy content conversion
        Replaces 2015 standards references with 2025 equivalents
        """
        converted_content = content
        changes = []
        
        mappings = standards_mapping.get("mappings", {})
        
        for std_2015, mapping_data in mappings.items():
            standards_2025 = mapping_data.get("2025_standards", [])
            
            if not standards_2025:
                continue  # Skip unmapped standards
            
            # Create replacement text
            replacement_text = ", ".join(standards_2025)
            
            # Pattern to match various formats of 2015 standard references
            patterns = [
                (rf'\bStandard\s+{re.escape(std_2015)}\b', f'Standard {replacement_text}'),
                (rf'\bClause\s+{re.escape(std_2015)}\b', f'Standard {replacement_text}'),
                (rf'\bSection\s+{re.escape(std_2015)}\b', f'Standard {replacement_text}'),
                (rf'(?<!\d\.)\b{re.escape(std_2015)}\b(?!\.\d)', replacement_text),  # Bare number
            ]
            
            for pattern, replacement in patterns:
                matches = list(re.finditer(pattern, converted_content, re.IGNORECASE))
                if matches:
                    converted_content = re.sub(pattern, replacement, converted_content, flags=re.IGNORECASE)
                    changes.append({
                        "type": "standards_reference",
                        "old_standard": std_2015,
                        "new_standards": standards_2025,
                        "occurrences": len(matches),
                        "pattern": pattern,
                        "description": f"Replaced {len(matches)} reference(s) to {std_2015} with {replacement_text}"
                    })
        
        # Update terminology if requested
        if options.get("update_terminology", True):
            terminology_changes = [
                (r'\bClause\b', 'Standard'),
                (r'\bclauses\b', 'standards'),
                (r'\b2015 Standards\b', '2025 Standards'),
                (r'\bStandards for RTOs 2015\b', 'Standards for RTOs 2025'),
            ]
            
            for old_term, new_term in terminology_changes:
                matches = list(re.finditer(old_term, converted_content, re.IGNORECASE))
                if matches:
                    converted_content = re.sub(old_term, new_term, converted_content, flags=re.IGNORECASE)
                    changes.append({
                        "type": "terminology",
                        "old_term": old_term,
                        "new_term": new_term,
                        "occurrences": len(matches),
                        "description": f"Updated terminology: '{old_term}' → '{new_term}' ({len(matches)} occurrences)"
                    })
        
        return converted_content, changes

    def _create_target_policy(self, source_policy, converted_content: str, session):
        """
        Create a new policy object with converted content
        """
        from .models import Policy
        
        # Generate new version number
        old_version = source_policy.version
        new_version = f"{old_version}.2025"
        
        target_policy = Policy.objects.create(
            tenant=source_policy.tenant,
            policy_number=f"{source_policy.policy_number}-2025",
            title=f"{source_policy.title} (2025 Standards)",
            description=f"Converted from 2015 Standards - {source_policy.description}",
            policy_type=source_policy.policy_type,
            content=converted_content,
            version=new_version,
            status="draft",
            created_by=session.created_by
        )
        
        logger.info(f"Created target policy {target_policy.id} from source {source_policy.id}")
        return target_policy

    def _validate_compliance(self, target_policy, standards_mapping: Dict) -> Dict:
        """
        Validate converted policy against 2025 Standards requirements
        
        Returns compliance report dict
        """
        content = target_policy.content
        mappings = standards_mapping.get("mappings", {})
        
        # Identify which 2025 standards are now covered
        standards_2025_covered = set()
        quality_areas_covered = set()
        
        for mapping_data in mappings.values():
            for std_2025 in mapping_data.get("2025_standards", []):
                standards_2025_covered.add(std_2025)
            for qa in mapping_data.get("quality_areas", []):
                quality_areas_covered.add(qa)
        
        # Check for 2025 standards in content
        standards_2025_mentioned = []
        qa_pattern = r'\b(QA[1-4]\.\d+|C[1-4]|CP[1-2])\b'
        standards_2025_mentioned = list(set(re.findall(qa_pattern, content)))
        
        # Calculate coverage
        total_qa = 4  # 4 Quality Areas in 2025 Standards
        qa_covered_count = len([qa for qa in quality_areas_covered if "Quality Area" in qa])
        coverage_percentage = (qa_covered_count / total_qa) * 100
        
        # Calculate quality score (0-100)
        quality_score = min(100, coverage_percentage + 50)  # Base score + coverage bonus
        
        # Determine if review is needed
        requires_review = (
            quality_score < 80 or
            standards_mapping.get("total_unmapped", 0) > 0 or
            len(standards_2025_covered) < 5
        )
        
        return {
            "status": "passed" if quality_score >= 70 else "needs_improvement",
            "quality_score": round(quality_score, 2),
            "standards_2025_covered": list(standards_2025_covered),
            "standards_2025_mentioned": standards_2025_mentioned,
            "quality_areas_covered": list(quality_areas_covered),
            "coverage_percentage": round(coverage_percentage, 2),
            "requires_review": requires_review,
            "recommendations": self._generate_compliance_recommendations(
                quality_score,
                standards_2025_covered,
                quality_areas_covered
            ),
            "validation_timestamp": datetime.utcnow().isoformat()
        }

    def _generate_compliance_recommendations(
        self,
        quality_score: float,
        standards_covered: set,
        quality_areas_covered: set
    ) -> List[str]:
        """Generate recommendations to improve compliance"""
        recommendations = []
        
        if quality_score < 70:
            recommendations.append("Quality score is below threshold - comprehensive review recommended")
        
        if len(standards_covered) < 5:
            recommendations.append("Limited 2025 standards coverage - consider expanding policy scope")
        
        qa_count = len([qa for qa in quality_areas_covered if "Quality Area" in qa])
        if qa_count < 4:
            missing_qa = []
            for i in range(1, 5):
                if not any(f"Quality Area {i}" in qa for qa in quality_areas_covered):
                    missing_qa.append(f"QA{i}")
            recommendations.append(f"Consider addressing Quality Areas: {', '.join(missing_qa)}")
        
        if quality_score >= 90:
            recommendations.append("High quality conversion - ready for final review and approval")
        
        return recommendations

    def _generate_conversion_note(self, source_policy) -> str:
        """Generate a note to add at the top of converted policy"""
        note = f"""---
**CONVERSION NOTE**
This policy has been converted from Standards for RTOs 2015 to Standards for RTOs 2025.

Original Policy: {source_policy.policy_number} - {source_policy.title}
Original Version: {source_policy.version}
Conversion Date: {datetime.utcnow().strftime('%Y-%m-%d')}

Please review all standards references and ensure alignment with the 2025 Standards framework.
---
"""
        return note

    def get_conversion_summary(self, session) -> Dict:
        """
        Generate comprehensive summary of conversion session
        
        Returns dict with all conversion details for display
        """
        return {
            "session_id": session.id,
            "session_name": session.session_name,
            "status": session.status,
            "progress": session.progress_percentage,
            "quality_score": session.quality_score,
            "processing_time": session.processing_time_seconds,
            "source_policy": {
                "id": session.source_policy.id,
                "policy_number": session.source_policy.policy_number,
                "title": session.source_policy.title,
                "version": session.source_policy.version,
            },
            "target_policy": {
                "id": session.target_policy.id if session.target_policy else None,
                "policy_number": session.target_policy.policy_number if session.target_policy else None,
                "title": session.target_policy.title if session.target_policy else None,
                "version": session.target_policy.version if session.target_policy else None,
            } if session.target_policy else None,
            "source_analysis": session.source_analysis,
            "standards_mapping": session.standards_mapping,
            "changes_count": len(session.conversion_changes),
            "compliance_report": session.compliance_report,
            "requires_review": session.requires_human_review,
            "ai_model_used": session.ai_model,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "completed_at": session.completed_at.isoformat() if session.completed_at else None,
        }
