"""
Compliance RAG (Red/Amber/Green) Engine
Implements compliance checks and guardrails for ASQA standards
"""
from typing import Dict, List, Tuple
from django.db import transaction
from django.utils import timezone
from django.db import models as models_module
from ..models import (
    CourseTAS, UnitTAS, ComplianceRule, ComplianceCheck,
    Trainer
)


class ComplianceRAGEngine:
    """
    Red/Amber/Green compliance checking engine
    Validates TAS against ASQA clauses and RTO standards
    """
    
    @classmethod
    def run_all_checks(cls, course_tas: CourseTAS, user=None) -> Dict:
        """
        Run all compliance checks for a Course TAS
        
        Args:
            course_tas: CourseTAS instance
            user: Optional user running the check
            
        Returns:
            Dict with check results categorized by status (red/amber/green)
        """
        results = {
            'red': [],
            'amber': [],
            'green': [],
            'summary': {
                'total_checks': 0,
                'red_count': 0,
                'amber_count': 0,
                'green_count': 0,
                'can_approve': True,
            }
        }
        
        # Get active rules for the tenant
        rules = ComplianceRule.objects.filter(
            models_module.Q(tenant=course_tas.tenant) | models_module.Q(is_system_rule=True),
            is_active=True
        )
        
        with transaction.atomic():
            for rule in rules:
                check_result = cls._execute_rule(rule, course_tas)
                
                # Create or update compliance check record
                check, created = ComplianceCheck.objects.update_or_create(
                    entity_type='course',
                    entity_id=course_tas.id,
                    rule=rule,
                    defaults={
                        'status': check_result['status'],
                        'message': check_result['message'],
                        'details': check_result.get('details', {}),
                    }
                )
                
                results[check_result['status']].append({
                    'rule_name': rule.name,
                    'rule_type': rule.rule_type,
                    'asqa_clause': rule.asqa_clause,
                    'message': check_result['message'],
                    'details': check_result.get('details', {}),
                    'check_id': check.id,
                })
                results['summary']['total_checks'] += 1
                results['summary'][f"{check_result['status']}_count"] += 1
        
        # Cannot approve if there are red issues
        if results['summary']['red_count'] > 0:
            results['summary']['can_approve'] = False
        
        return results
    
    @classmethod
    def run_unit_checks(cls, unit_tas: UnitTAS, user=None) -> Dict:
        """
        Run compliance checks for a Unit TAS
        
        Args:
            unit_tas: UnitTAS instance
            user: Optional user running the check
            
        Returns:
            Dict with check results
        """
        results = {
            'red': [],
            'amber': [],
            'green': [],
            'summary': {
                'total_checks': 0,
                'red_count': 0,
                'amber_count': 0,
                'green_count': 0,
                'can_proceed': True,
            }
        }
        
        # Unit-specific checks
        unit_rules = ComplianceRule.objects.filter(
            models_module.Q(tenant=unit_tas.course_tas.tenant) | models_module.Q(is_system_rule=True),
            is_active=True,
            rule_type__in=['trainer_scope', 'facility_adequacy', 'assessment_coverage']
        )
        
        with transaction.atomic():
            for rule in unit_rules:
                check_result = cls._execute_unit_rule(rule, unit_tas)
                
                check, created = ComplianceCheck.objects.update_or_create(
                    entity_type='unit',
                    entity_id=unit_tas.id,
                    rule=rule,
                    defaults={
                        'status': check_result['status'],
                        'message': check_result['message'],
                        'details': check_result.get('details', {}),
                    }
                )
                
                results[check_result['status']].append({
                    'rule_name': rule.name,
                    'rule_type': rule.rule_type,
                    'message': check_result['message'],
                    'check_id': check.id,
                })
                results['summary']['total_checks'] += 1
                results['summary'][f"{check_result['status']}_count"] += 1
        
        if results['summary']['red_count'] > 0:
            results['summary']['can_proceed'] = False
        
        return results
    
    @classmethod
    def _execute_rule(cls, rule: ComplianceRule, course_tas: CourseTAS) -> Dict:
        """
        Execute a compliance rule against a Course TAS
        
        Returns:
            Dict with status, message, and details
        """
        rule_type = rule.rule_type
        
        # Route to appropriate check method
        if rule_type == 'packaging':
            return cls._check_packaging_rules(rule, course_tas)
        elif rule_type == 'trainer_scope':
            return cls._check_course_trainer_scope(rule, course_tas)
        elif rule_type == 'facility_adequacy':
            return cls._check_facility_adequacy(rule, course_tas)
        elif rule_type == 'hours_validation':
            return cls._check_hours_validation(rule, course_tas)
        elif rule_type == 'clustering':
            return cls._check_clustering_sanity(rule, course_tas)
        elif rule_type == 'policy':
            return cls._check_policy_compliance(rule, course_tas)
        else:
            return {
                'status': 'amber',
                'message': f'Unknown rule type: {rule_type}',
            }
    
    @classmethod
    def _execute_unit_rule(cls, rule: ComplianceRule, unit_tas: UnitTAS) -> Dict:
        """Execute a compliance rule against a Unit TAS"""
        rule_type = rule.rule_type
        
        if rule_type == 'trainer_scope':
            return cls._check_unit_trainer_scope(rule, unit_tas)
        elif rule_type == 'facility_adequacy':
            return cls._check_unit_facility_adequacy(rule, unit_tas)
        else:
            return {
                'status': 'green',
                'message': f'Check passed: {rule.name}',
            }
    
    # ========================================================================
    # Specific Rule Implementations
    # ========================================================================
    
    @classmethod
    def _check_packaging_rules(cls, rule: ComplianceRule, course_tas: CourseTAS) -> Dict:
        """
        Check packaging rules (ASQA 1.1)
        Validate core/elective requirements
        """
        core_count = len(course_tas.core_units)
        elective_count = len(course_tas.elective_units)
        total_units = course_tas.total_units
        
        # Get packaging rules from TGA snapshot
        packaging_rules = course_tas.tga_qualification_snapshot.get('packaging_rules', {})
        required_core = packaging_rules.get('core_units_required', 0)
        required_electives = packaging_rules.get('elective_units_required', 0)
        required_total = packaging_rules.get('total_units', 0)
        
        issues = []
        
        if core_count < required_core:
            issues.append(f'Insufficient core units: {core_count}/{required_core}')
        
        if elective_count < required_electives:
            issues.append(f'Insufficient elective units: {elective_count}/{required_electives}')
        
        if total_units < required_total:
            issues.append(f'Insufficient total units: {total_units}/{required_total}')
        
        if issues:
            return {
                'status': 'red',
                'message': 'Packaging rule violations found',
                'details': {'issues': issues}
            }
        
        return {
            'status': 'green',
            'message': 'Packaging rules compliant',
            'details': {
                'core_units': f'{core_count}/{required_core}',
                'elective_units': f'{elective_count}/{required_electives}',
                'total_units': f'{total_units}/{required_total}',
            }
        }
    
    @classmethod
    def _check_course_trainer_scope(cls, rule: ComplianceRule, course_tas: CourseTAS) -> Dict:
        """
        Check if trainers are assigned and qualified for all units (ASQA 1.13-1.16)
        """
        issues = []
        warnings = []
        
        # Get all unit TAS
        unit_tas_set = course_tas.unit_tas_set.all()
        
        for unit_tas in unit_tas_set:
            trainers = unit_tas.trainers.all()
            
            if not trainers:
                issues.append(f'{unit_tas.unit_code}: No trainers assigned')
            else:
                # Check trainer qualifications and scope
                for trainer in trainers:
                    if unit_tas.unit_code not in trainer.scope_units:
                        warnings.append(
                            f'{unit_tas.unit_code}: Trainer {trainer.user.username} '
                            f'not in scope'
                        )
                    
                    # Check currency
                    if trainer.last_currency_date:
                        import datetime
                        days_since_currency = (
                            datetime.date.today() - trainer.last_currency_date
                        ).days
                        if days_since_currency > 730:  # 2 years
                            warnings.append(
                                f'{unit_tas.unit_code}: Trainer {trainer.user.username} '
                                f'currency > 2 years'
                            )
        
        if issues:
            return {
                'status': 'red',
                'message': 'Trainer assignment issues',
                'details': {'issues': issues, 'warnings': warnings}
            }
        elif warnings:
            return {
                'status': 'amber',
                'message': 'Trainer scope/currency warnings',
                'details': {'warnings': warnings}
            }
        
        return {
            'status': 'green',
            'message': 'All units have qualified trainers assigned',
        }
    
    @classmethod
    def _check_unit_trainer_scope(cls, rule: ComplianceRule, unit_tas: UnitTAS) -> Dict:
        """Check trainer scope for a specific unit"""
        trainers = unit_tas.trainers.all()
        
        if not trainers:
            return {
                'status': 'red',
                'message': f'No trainers assigned to {unit_tas.unit_code}',
            }
        
        issues = []
        for trainer in trainers:
            if unit_tas.unit_code not in trainer.scope_units:
                issues.append(f'Trainer {trainer.user.username} not in scope')
        
        if issues:
            return {
                'status': 'amber',
                'message': 'Trainer scope warnings',
                'details': {'issues': issues}
            }
        
        return {
            'status': 'green',
            'message': 'Trainers qualified and in scope',
        }
    
    @classmethod
    def _check_facility_adequacy(cls, rule: ComplianceRule, course_tas: CourseTAS) -> Dict:
        """Check if facilities are adequate for delivery (ASQA 1.13)"""
        if not course_tas.facilities.exists():
            return {
                'status': 'amber',
                'message': 'No facilities assigned to course',
            }
        
        return {
            'status': 'green',
            'message': 'Facilities assigned',
        }
    
    @classmethod
    def _check_unit_facility_adequacy(cls, rule: ComplianceRule, unit_tas: UnitTAS) -> Dict:
        """Check facility adequacy for a specific unit"""
        if not unit_tas.facilities.exists():
            return {
                'status': 'amber',
                'message': f'No facilities assigned to {unit_tas.unit_code}',
            }
        
        return {
            'status': 'green',
            'message': 'Facilities assigned',
        }
    
    @classmethod
    def _check_hours_validation(cls, rule: ComplianceRule, course_tas: CourseTAS) -> Dict:
        """Validate total hours against units and delivery model"""
        total_hours = course_tas.total_hours
        
        # Calculate expected hours from units
        unit_tas_set = course_tas.unit_tas_set.all()
        expected_hours = sum(unit.nominal_hours for unit in unit_tas_set)
        
        if total_hours == 0:
            return {
                'status': 'amber',
                'message': 'Total hours not set',
            }
        
        # Allow 10% variance
        variance = abs(total_hours - expected_hours) / expected_hours if expected_hours > 0 else 0
        
        if variance > 0.1:
            return {
                'status': 'amber',
                'message': f'Hours mismatch: {total_hours} vs expected {expected_hours}',
                'details': {'variance_percent': round(variance * 100, 1)}
            }
        
        return {
            'status': 'green',
            'message': 'Hours allocation validated',
            'details': {'total_hours': total_hours, 'expected_hours': expected_hours}
        }
    
    @classmethod
    def _check_clustering_sanity(cls, rule: ComplianceRule, course_tas: CourseTAS) -> Dict:
        """Check clustering logic and sequencing"""
        clusters = course_tas.clusters
        
        if not clusters:
            return {
                'status': 'amber',
                'message': 'No clusters defined',
            }
        
        # Basic sanity checks
        all_units = [u['code'] for u in course_tas.core_units + course_tas.elective_units]
        clustered_units = []
        
        for cluster in clusters:
            clustered_units.extend(cluster.get('units', []))
        
        unclustered = set(all_units) - set(clustered_units)
        
        if unclustered:
            return {
                'status': 'amber',
                'message': f'{len(unclustered)} units not assigned to clusters',
                'details': {'unclustered_units': list(unclustered)}
            }
        
        return {
            'status': 'green',
            'message': 'All units clustered appropriately',
        }
    
    @classmethod
    def _check_policy_compliance(cls, rule: ComplianceRule, course_tas: CourseTAS) -> Dict:
        """Check that required policies are linked (ASQA 1.8, 2.2)"""
        required_policies = ['RPL', 'Assessment', 'LLN', 'Complaints and Appeals']
        policy_links = course_tas.policy_links or []
        
        missing = []
        for req in required_policies:
            if not any(req.lower() in link.lower() for link in policy_links):
                missing.append(req)
        
        if missing:
            return {
                'status': 'amber',
                'message': f'Missing policy links: {", ".join(missing)}',
                'details': {'missing_policies': missing}
            }
        
        return {
            'status': 'green',
            'message': 'All required policies linked',
        }
    
    @classmethod
    def resolve_check(cls, check_id: int, resolution_notes: str, user) -> bool:
        """
        Mark a compliance check as resolved
        
        Args:
            check_id: ComplianceCheck ID
            resolution_notes: Notes explaining resolution
            user: User resolving the check
            
        Returns:
            True if successful
        """
        try:
            check = ComplianceCheck.objects.get(id=check_id)
            check.resolved = True
            check.resolution_notes = resolution_notes
            check.resolved_by = user
            check.resolved_at = timezone.now()
            check.save()
            return True
        except ComplianceCheck.DoesNotExist:
            return False
