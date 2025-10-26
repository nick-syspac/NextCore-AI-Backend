"""
Assessment Mapper Service
Maps unit elements/PC/KE/FS to assessment tasks and instruments
Generates mapping matrices
"""
from typing import Dict, List
from ..models import UnitTAS, AssessmentTask


class AssessmentMapper:
    """
    Service to map assessment tasks to unit competency requirements
    """
    
    @classmethod
    def create_mapping_matrix(cls, unit_tas: UnitTAS) -> Dict:
        """
        Generate assessment mapping matrix for a unit
        
        Args:
            unit_tas: UnitTAS instance
            
        Returns:
            Dict with complete mapping matrix
        """
        # Get TGA snapshot data
        tga_snapshot = unit_tas.tga_unit_snapshot or {}
        elements = tga_snapshot.get('elements', [])
        performance_criteria = tga_snapshot.get('performance_criteria', [])
        knowledge_evidence = tga_snapshot.get('knowledge_evidence', [])
        foundation_skills = tga_snapshot.get('foundation_skills', [])
        
        # Get assessment tasks
        assessment_tasks = unit_tas.assessment_tasks.all()
        
        # Build matrix
        matrix = {
            'unit_code': unit_tas.unit_code,
            'unit_title': unit_tas.unit_title,
            'elements': [],
            'performance_criteria': [],
            'knowledge_evidence': [],
            'foundation_skills': [],
            'coverage_summary': {
                'elements_covered': 0,
                'elements_total': len(elements),
                'pc_covered': 0,
                'pc_total': len(performance_criteria),
                'ke_covered': 0,
                'ke_total': len(knowledge_evidence),
                'fs_covered': 0,
                'fs_total': len(foundation_skills),
            }
        }
        
        # Map elements
        for element in elements:
            element_mapping = {
                'code': element.get('code'),
                'title': element.get('title'),
                'covered_by_tasks': [],
            }
            
            for task in assessment_tasks:
                if element.get('code') in task.elements_covered:
                    element_mapping['covered_by_tasks'].append({
                        'task_number': task.task_number,
                        'task_name': task.task_name,
                        'task_type': task.task_type,
                    })
            
            if element_mapping['covered_by_tasks']:
                matrix['coverage_summary']['elements_covered'] += 1
            
            matrix['elements'].append(element_mapping)
        
        # Map performance criteria
        for pc in performance_criteria:
            pc_mapping = {
                'code': pc.get('code'),
                'description': pc.get('description'),
                'covered_by_tasks': [],
            }
            
            for task in assessment_tasks:
                if pc.get('code') in task.performance_criteria_covered:
                    pc_mapping['covered_by_tasks'].append({
                        'task_number': task.task_number,
                        'task_name': task.task_name,
                    })
            
            if pc_mapping['covered_by_tasks']:
                matrix['coverage_summary']['pc_covered'] += 1
            
            matrix['performance_criteria'].append(pc_mapping)
        
        # Map knowledge evidence
        for ke in knowledge_evidence:
            ke_mapping = {
                'description': ke.get('description'),
                'covered_by_tasks': [],
            }
            
            for task in assessment_tasks:
                if ke.get('id') in task.knowledge_evidence_covered:
                    ke_mapping['covered_by_tasks'].append({
                        'task_number': task.task_number,
                        'task_name': task.task_name,
                    })
            
            if ke_mapping['covered_by_tasks']:
                matrix['coverage_summary']['ke_covered'] += 1
            
            matrix['knowledge_evidence'].append(ke_mapping)
        
        # Map foundation skills
        for fs in foundation_skills:
            fs_mapping = {
                'skill': fs.get('skill'),
                'description': fs.get('description'),
                'covered_by_tasks': [],
            }
            
            for task in assessment_tasks:
                if fs.get('id') in task.foundation_skills_covered:
                    fs_mapping['covered_by_tasks'].append({
                        'task_number': task.task_number,
                        'task_name': task.task_name,
                    })
            
            if fs_mapping['covered_by_tasks']:
                matrix['coverage_summary']['fs_covered'] += 1
            
            matrix['foundation_skills'].append(fs_mapping)
        
        # Calculate coverage percentages
        if matrix['coverage_summary']['elements_total'] > 0:
            matrix['coverage_summary']['elements_coverage_percent'] = round(
                (matrix['coverage_summary']['elements_covered'] / 
                 matrix['coverage_summary']['elements_total']) * 100, 1
            )
        
        if matrix['coverage_summary']['pc_total'] > 0:
            matrix['coverage_summary']['pc_coverage_percent'] = round(
                (matrix['coverage_summary']['pc_covered'] / 
                 matrix['coverage_summary']['pc_total']) * 100, 1
            )
        
        return matrix
    
    @classmethod
    def validate_coverage(cls, unit_tas: UnitTAS) -> Dict:
        """
        Validate that all competency requirements are adequately covered
        
        Args:
            unit_tas: UnitTAS instance
            
        Returns:
            Dict with validation results and gaps
        """
        matrix = cls.create_mapping_matrix(unit_tas)
        summary = matrix['coverage_summary']
        
        gaps = []
        warnings = []
        
        # Check elements coverage (must be 100%)
        if summary['elements_covered'] < summary['elements_total']:
            uncovered_elements = [
                e for e in matrix['elements'] 
                if not e['covered_by_tasks']
            ]
            gaps.append({
                'type': 'elements',
                'message': f"{summary['elements_total'] - summary['elements_covered']} elements not covered",
                'uncovered': [e['code'] for e in uncovered_elements]
            })
        
        # Check performance criteria coverage (must be 100%)
        if summary['pc_covered'] < summary['pc_total']:
            uncovered_pc = [
                pc for pc in matrix['performance_criteria'] 
                if not pc['covered_by_tasks']
            ]
            gaps.append({
                'type': 'performance_criteria',
                'message': f"{summary['pc_total'] - summary['pc_covered']} PC not covered",
                'uncovered': [pc['code'] for pc in uncovered_pc]
            })
        
        # Check knowledge evidence (should be high %)
        if summary.get('ke_coverage_percent', 0) < 80:
            warnings.append({
                'type': 'knowledge_evidence',
                'message': f"Knowledge evidence coverage is {summary.get('ke_coverage_percent', 0)}% (target: 80%+)"
            })
        
        # Determine overall status
        if gaps:
            status = 'incomplete'
        elif warnings:
            status = 'warning'
        else:
            status = 'complete'
        
        return {
            'status': status,
            'gaps': gaps,
            'warnings': warnings,
            'coverage_summary': summary,
        }
    
    @classmethod
    def suggest_assessment_tasks(cls, unit_tas: UnitTAS) -> List[Dict]:
        """
        Suggest assessment task structure based on unit requirements
        
        Args:
            unit_tas: UnitTAS instance
            
        Returns:
            List of suggested assessment tasks
        """
        tga_snapshot = unit_tas.tga_unit_snapshot or {}
        elements = tga_snapshot.get('elements', [])
        
        # Basic suggestion: One knowledge task + one practical task per element
        suggestions = []
        
        # Knowledge assessment
        suggestions.append({
            'task_number': 1,
            'task_name': 'Knowledge Assessment',
            'task_type': 'knowledge',
            'description': f'Written assessment covering theoretical knowledge for {unit_tas.unit_code}',
            'elements_covered': [e.get('code') for e in elements],
            'suggested_instruments': [
                'Written questions',
                'Case studies',
                'Short answer questions',
            ],
        })
        
        # Practical demonstration
        suggestions.append({
            'task_number': 2,
            'task_name': 'Practical Demonstration',
            'task_type': 'practical',
            'description': f'Practical demonstration of skills for {unit_tas.unit_code}',
            'elements_covered': [e.get('code') for e in elements],
            'suggested_instruments': [
                'Observation checklist',
                'Practical demonstration',
                'Skills assessment',
            ],
        })
        
        return suggestions
    
    @classmethod
    def auto_map_assessments(cls, unit_tas: UnitTAS) -> bool:
        """
        Automatically create basic assessment task mappings
        
        Args:
            unit_tas: UnitTAS instance
            
        Returns:
            True if successful
        """
        suggestions = cls.suggest_assessment_tasks(unit_tas)
        tga_snapshot = unit_tas.tga_unit_snapshot or {}
        
        elements = tga_snapshot.get('elements', [])
        performance_criteria = tga_snapshot.get('performance_criteria', [])
        knowledge_evidence = tga_snapshot.get('knowledge_evidence', [])
        foundation_skills = tga_snapshot.get('foundation_skills', [])
        
        # Create assessment tasks
        for suggestion in suggestions:
            task = AssessmentTask.objects.create(
                unit_tas=unit_tas,
                task_number=suggestion['task_number'],
                task_name=suggestion['task_name'],
                task_type=suggestion['task_type'],
                description=suggestion['description'],
                elements_covered=suggestion['elements_covered'],
                performance_criteria_covered=[pc.get('code') for pc in performance_criteria],
                knowledge_evidence_covered=[ke.get('id', idx) for idx, ke in enumerate(knowledge_evidence)],
                foundation_skills_covered=[fs.get('id', idx) for idx, fs in enumerate(foundation_skills)],
                instruments=suggestion.get('suggested_instruments', []),
            )
        
        # Update unit TAS mapping matrix
        matrix = cls.create_mapping_matrix(unit_tas)
        unit_tas.mapping_matrix = matrix
        unit_tas.save()
        
        return True
