"""
Prefill Service
Aggregates data from TGA, org defaults, and integrations to prefill TAS forms
"""
from typing import Dict, List, Optional
from ..models import CourseTAS, Trainer, Facility, IndustryEngagement


class PrefillService:
    """
    Service to prefill Course TAS and Unit TAS from multiple data sources
    """
    
    @classmethod
    def get_qualification_data(cls, qualification_code: str) -> Dict:
        """
        Fetch qualification data from TGA (Training.gov.au)
        
        Args:
            qualification_code: Qualification code (e.g., BSB50120)
            
        Returns:
            Dict with qualification details, units, packaging rules
        """
        # TODO: Integrate with TGA API/service
        # For now, return mock structure
        return {
            'code': qualification_code,
            'name': f'Qualification {qualification_code}',
            'aqf_level': 'diploma',
            'training_package': 'BSB',
            'release_version': '1.0',
            'core_units': [],
            'elective_groups': [],
            'packaging_rules': {
                'total_units': 12,
                'core_units_required': 6,
                'elective_units_required': 6,
            },
            'tga_snapshot': {},
        }
    
    @classmethod
    def get_unit_data(cls, unit_code: str) -> Dict:
        """
        Fetch unit of competency data from TGA
        
        Args:
            unit_code: Unit code (e.g., BSBWHS411)
            
        Returns:
            Dict with unit details, elements, PC, KE, FS
        """
        # TODO: Integrate with TGA API/service
        return {
            'code': unit_code,
            'title': f'Unit {unit_code}',
            'nominal_hours': 40,
            'elements': [],
            'performance_criteria': [],
            'knowledge_evidence': [],
            'foundation_skills': [],
            'tga_snapshot': {},
        }
    
    @classmethod
    def get_org_defaults(cls, tenant) -> Dict:
        """
        Get organization-specific defaults for TAS prefill
        
        Args:
            tenant: Tenant instance
            
        Returns:
            Dict with org policies, campuses, delivery modes, etc.
        """
        # TODO: Fetch from tenant settings/configuration
        return {
            'campuses': ['Main Campus', 'Online'],
            'delivery_modes': ['Face-to-face', 'Online', 'Blended', 'Workplace'],
            'default_duration_weeks': 52,
            'policies': {
                'rpl': 'RPL and Credit Transfer Policy v2.1',
                'assessment': 'Assessment Policy v3.0',
                'lln': 'Language, Literacy and Numeracy Policy v1.5',
                'complaints_appeals': 'Complaints and Appeals Policy v2.0',
            },
            'default_resources': [
                'Learning Management System',
                'Student Portal',
                'Library Access',
            ],
        }
    
    @classmethod
    def get_available_trainers(cls, tenant, unit_codes: List[str] = None) -> List[Trainer]:
        """
        Get available trainers, optionally filtered by scope
        
        Args:
            tenant: Tenant instance
            unit_codes: Optional list of unit codes to filter by scope
            
        Returns:
            List of Trainer instances
        """
        queryset = Trainer.objects.filter(tenant=tenant, is_active=True)
        
        if unit_codes:
            # Filter trainers who have these units in their scope
            # This is a simplified check - actual implementation may be more complex
            trainers = []
            for trainer in queryset:
                trainer_scope = trainer.scope_units or []
                if any(unit in trainer_scope for unit in unit_codes):
                    trainers.append(trainer)
            return trainers
        
        return list(queryset)
    
    @classmethod
    def get_available_facilities(cls, tenant, facility_types: List[str] = None) -> List[Facility]:
        """
        Get available facilities
        
        Args:
            tenant: Tenant instance
            facility_types: Optional list of facility types to filter
            
        Returns:
            List of Facility instances
        """
        queryset = Facility.objects.filter(tenant=tenant, is_available=True)
        
        if facility_types:
            queryset = queryset.filter(facility_type__in=facility_types)
        
        return list(queryset)
    
    @classmethod
    def get_recent_industry_engagements(cls, tenant, qualification_code: str = None) -> List[IndustryEngagement]:
        """
        Get recent industry engagements relevant to the qualification
        
        Args:
            tenant: Tenant instance
            qualification_code: Optional qualification code to filter
            
        Returns:
            List of IndustryEngagement instances
        """
        queryset = IndustryEngagement.objects.filter(tenant=tenant).order_by('-engagement_date')
        
        if qualification_code:
            # Filter by related qualifications
            queryset = queryset.filter(
                related_qualifications__contains=[qualification_code]
            )
        
        return list(queryset[:10])  # Return last 10 engagements
    
    @classmethod
    def prefill_course_tas(cls, tenant, qualification_code: str) -> Dict:
        """
        Main prefill method - aggregate all data for Course TAS creation
        
        Args:
            tenant: Tenant instance
            qualification_code: Qualification code
            
        Returns:
            Dict with all prefilled data ready for Course TAS creation
        """
        # Fetch data from various sources
        qual_data = cls.get_qualification_data(qualification_code)
        org_defaults = cls.get_org_defaults(tenant)
        
        # Get core and elective unit details
        core_units = []
        for unit_code in qual_data.get('core_units', []):
            unit_data = cls.get_unit_data(unit_code)
            core_units.append(unit_data)
        
        # Prepare prefill data
        prefill_data = {
            'qualification_code': qual_data['code'],
            'qualification_name': qual_data['name'],
            'aqf_level': qual_data['aqf_level'],
            'training_package': qual_data['training_package'],
            'tga_snapshot': qual_data['tga_snapshot'],
            'release_version': qual_data['release_version'],
            'core_units': core_units,
            'elective_groups': qual_data.get('elective_groups', []),
            'packaging_rules': qual_data.get('packaging_rules', {}),
            'delivery_model': org_defaults['delivery_modes'][0],  # Default to first
            'duration_weeks': org_defaults['default_duration_weeks'],
            'policy_links': list(org_defaults['policies'].values()),
            'default_resources': org_defaults['default_resources'],
            'available_trainers': cls.get_available_trainers(tenant),
            'available_facilities': cls.get_available_facilities(tenant),
            'recent_industry_engagements': cls.get_recent_industry_engagements(tenant, qualification_code),
        }
        
        return prefill_data
    
    @classmethod
    def prefill_unit_tas(cls, tenant, unit_code: str, course_tas: CourseTAS = None) -> Dict:
        """
        Prefill data for Unit TAS creation
        
        Args:
            tenant: Tenant instance
            unit_code: Unit code
            course_tas: Optional parent CourseTAS
            
        Returns:
            Dict with prefilled unit data
        """
        unit_data = cls.get_unit_data(unit_code)
        
        # Get trainers qualified for this unit
        available_trainers = cls.get_available_trainers(tenant, [unit_code])
        
        prefill_data = {
            'unit_code': unit_data['code'],
            'unit_title': unit_data['title'],
            'nominal_hours': unit_data['nominal_hours'],
            'elements': unit_data['elements'],
            'performance_criteria': unit_data['performance_criteria'],
            'knowledge_evidence': unit_data['knowledge_evidence'],
            'foundation_skills': unit_data['foundation_skills'],
            'tga_snapshot': unit_data['tga_snapshot'],
            'available_trainers': available_trainers,
            'available_facilities': cls.get_available_facilities(tenant),
        }
        
        # If part of course TAS, inherit some settings
        if course_tas:
            prefill_data['cohort_profile'] = course_tas.cohort_profile
            prefill_data['delivery_model'] = course_tas.delivery_model
        
        return prefill_data
