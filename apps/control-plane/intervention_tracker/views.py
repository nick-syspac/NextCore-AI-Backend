from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Q, Avg
from datetime import datetime, timedelta

from .models import (
    Intervention, InterventionRule, InterventionWorkflow,
    InterventionStep, InterventionOutcome, AuditLog
)
from .serializers import (
    InterventionSerializer, InterventionListSerializer,
    InterventionRuleSerializer, InterventionWorkflowSerializer,
    InterventionStepSerializer, InterventionOutcomeSerializer,
    AuditLogSerializer, CreateInterventionRequestSerializer,
    EvaluateRulesRequestSerializer, UpdateStepRequestSerializer,
    RecordOutcomeRequestSerializer
)


class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer
    
    def get_queryset(self):
        tenant = self.kwargs.get('tenant_slug')
        queryset = Intervention.objects.filter(tenant=tenant)
        
        # Filters
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        intervention_type = self.request.query_params.get('type')
        if intervention_type:
            queryset = queryset.filter(intervention_type=intervention_type)
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority_level=priority)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return InterventionListSerializer
        return InterventionSerializer
    
    def perform_create(self, serializer):
        tenant = self.kwargs.get('tenant_slug')
        intervention = serializer.save(tenant=tenant)
        
        # Create audit log
        AuditLog.objects.create(
            tenant=tenant,
            intervention=intervention,
            action_type='created',
            action_description=f"Intervention created: {intervention.intervention_type}",
            performed_by=intervention.action_taken_by,
            performed_by_role=intervention.action_taken_by_role
        )
    
    @action(detail=False, methods=['post'])
    def create_intervention(self, request, tenant_slug=None):
        """Create a new intervention with workflow initialization"""
        serializer = CreateInterventionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        # Create intervention
        intervention = Intervention.objects.create(
            tenant=tenant_slug,
            student_id=data['student_id'],
            student_name=data['student_name'],
            course_id=data.get('course_id', ''),
            course_name=data.get('course_name', ''),
            intervention_type=data['intervention_type'],
            priority_level=data.get('priority_level', 'medium'),
            action_description=data['action_description'],
            action_taken_by=data['action_taken_by'],
            action_taken_by_role=data.get('action_taken_by_role', ''),
            communication_method=data.get('communication_method', ''),
            communication_notes=data.get('communication_notes', ''),
            trigger_type=data.get('trigger_type', 'manual'),
            trigger_details=data.get('trigger_details', {})
        )
        
        # Initialize workflow steps if applicable
        workflows = InterventionWorkflow.objects.filter(
            tenant=tenant_slug,
            is_active=True,
            intervention_types__contains=[data['intervention_type']]
        )
        
        if workflows.exists():
            workflow = workflows.first()
            for step_data in workflow.steps:
                InterventionStep.objects.create(
                    intervention=intervention,
                    workflow=workflow,
                    step_number=step_data['step_number'],
                    step_name=step_data['step_name'],
                    step_description=step_data.get('description', ''),
                    status='pending'
                )
        
        # Create audit log
        AuditLog.objects.create(
            tenant=tenant_slug,
            intervention=intervention,
            action_type='created',
            action_description=f"Intervention created via API: {intervention.intervention_type}",
            performed_by=data['action_taken_by'],
            performed_by_role=data.get('action_taken_by_role', '')
        )
        
        return Response(InterventionSerializer(intervention).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None, tenant_slug=None):
        """Update intervention status"""
        intervention = self.get_object()
        new_status = request.data.get('status')
        notes = request.data.get('notes', '')
        updated_by = request.data.get('updated_by', 'System')
        
        old_status = intervention.status
        intervention.status = new_status
        
        if new_status == 'completed':
            intervention.completed_at = timezone.now()
        
        intervention.save()
        
        # Create audit log
        AuditLog.objects.create(
            tenant=tenant_slug,
            intervention=intervention,
            action_type='status_changed',
            action_description=f"Status changed from {old_status} to {new_status}. {notes}",
            performed_by=updated_by,
            changes={'status': {'old': old_status, 'new': new_status}}
        )
        
        return Response(InterventionSerializer(intervention).data)
    
    @action(detail=True, methods=['post'])
    def update_step(self, request, pk=None, tenant_slug=None):
        """Update workflow step status"""
        intervention = self.get_object()
        serializer = UpdateStepRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        step = InterventionStep.objects.get(id=data['step_id'], intervention=intervention)
        old_status = step.status
        step.status = data['status']
        step.completed_by = data.get('completed_by', '')
        step.completion_notes = data.get('completion_notes', '')
        step.duration_minutes = data.get('duration_minutes')
        step.evidence_provided = data.get('evidence_provided', [])
        
        if data['status'] == 'completed':
            step.completed_at = timezone.now()
        
        step.save()
        
        # Create audit log
        AuditLog.objects.create(
            tenant=tenant_slug,
            intervention=intervention,
            action_type='step_completed',
            action_description=f"Step {step.step_number}: {step.step_name} - {data['status']}",
            performed_by=data.get('completed_by', 'System')
        )
        
        return Response(InterventionStepSerializer(step).data)
    
    @action(detail=True, methods=['post'])
    def record_outcome(self, request, pk=None, tenant_slug=None):
        """Record intervention outcome"""
        intervention = self.get_object()
        serializer = RecordOutcomeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        outcome = InterventionOutcome.objects.create(
            intervention=intervention,
            metric_type=data['metric_type'],
            baseline_value=data.get('baseline_value'),
            target_value=data.get('target_value'),
            actual_value=data['actual_value'],
            evidence_description=data.get('evidence_description', ''),
            notes=data.get('notes', '')
        )
        
        # Update intervention outcome status
        if outcome.target_achieved:
            intervention.outcome_achieved = 'successful'
        elif outcome.actual_value and outcome.baseline_value and outcome.actual_value > outcome.baseline_value:
            intervention.outcome_achieved = 'partial'
        else:
            intervention.outcome_achieved = 'unsuccessful'
        
        intervention.save()
        
        # Create audit log
        AuditLog.objects.create(
            tenant=tenant_slug,
            intervention=intervention,
            action_type='outcome_recorded',
            action_description=f"Outcome recorded: {data['metric_type']} - {outcome.actual_value}",
            performed_by=request.data.get('recorded_by', 'System')
        )
        
        return Response(InterventionOutcomeSerializer(outcome).data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request, tenant_slug=None):
        """Get dashboard statistics"""
        queryset = Intervention.objects.filter(tenant=tenant_slug)
        
        total_interventions = queryset.count()
        active_interventions = queryset.filter(status__in=['initiated', 'in_progress']).count()
        
        # By type
        by_type = queryset.values('intervention_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # By status
        by_status = queryset.values('status').annotate(
            count=Count('id')
        )
        
        # Success rate
        completed = queryset.filter(status='completed')
        successful = completed.filter(outcome_achieved='successful').count()
        success_rate = (successful / completed.count() * 100) if completed.count() > 0 else 0
        
        # Priority breakdown
        by_priority = queryset.values('priority_level').annotate(
            count=Count('id')
        )
        
        # Recent interventions
        recent = queryset.select_related()[:10]
        
        # Follow-up required
        followup_required = queryset.filter(
            requires_followup=True,
            status__in=['completed', 'in_progress']
        ).count()
        
        return Response({
            'total_interventions': total_interventions,
            'active_interventions': active_interventions,
            'success_rate': round(success_rate, 1),
            'followup_required': followup_required,
            'by_type': list(by_type),
            'by_status': list(by_status),
            'by_priority': list(by_priority),
            'recent_interventions': InterventionListSerializer(recent, many=True).data
        })
    
    @action(detail=False, methods=['get'])
    def audit_report(self, request, tenant_slug=None):
        """Generate audit report"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = Intervention.objects.filter(tenant=tenant_slug)
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        # Compile audit data
        report = {
            'period': {
                'start': start_date,
                'end': end_date
            },
            'summary': {
                'total_interventions': queryset.count(),
                'by_type': list(queryset.values('intervention_type').annotate(count=Count('id'))),
                'by_outcome': list(queryset.values('outcome_achieved').annotate(count=Count('id'))),
                'compliance_categories': list(queryset.exclude(compliance_category='').values('compliance_category').annotate(count=Count('id')))
            },
            'interventions': InterventionSerializer(queryset, many=True).data
        }
        
        return Response(report)


class InterventionRuleViewSet(viewsets.ModelViewSet):
    queryset = InterventionRule.objects.all()
    serializer_class = InterventionRuleSerializer
    
    def get_queryset(self):
        tenant = self.kwargs.get('tenant_slug')
        return InterventionRule.objects.filter(tenant=tenant)
    
    def perform_create(self, serializer):
        tenant = self.kwargs.get('tenant_slug')
        serializer.save(tenant=tenant)
    
    @action(detail=False, methods=['post'])
    def evaluate_rules(self, request, tenant_slug=None):
        """Evaluate rules against student metrics"""
        serializer = EvaluateRulesRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        student_id = data['student_id']
        metrics = data['metrics']
        
        # Get active rules
        rules = InterventionRule.objects.filter(
            tenant=tenant_slug,
            is_active=True
        ).order_by('-priority')
        
        triggered_rules = []
        
        for rule in rules:
            if self._evaluate_rule(rule, metrics):
                triggered_rules.append({
                    'rule_number': rule.rule_number,
                    'rule_name': rule.rule_name,
                    'intervention_type': rule.intervention_type,
                    'priority_level': rule.priority_level,
                    'conditions': rule.conditions,
                    'notification_recipients': rule.notification_recipients
                })
                
                # Update rule stats
                rule.last_triggered = timezone.now()
                rule.trigger_count += 1
                rule.save()
        
        return Response({
            'student_id': student_id,
            'metrics_evaluated': metrics,
            'rules_triggered': triggered_rules,
            'trigger_count': len(triggered_rules)
        })
    
    def _evaluate_rule(self, rule, metrics):
        """Evaluate if rule conditions are met"""
        conditions = rule.conditions
        condition_type = rule.condition_type
        
        if condition_type == 'attendance':
            metric_value = metrics.get('attendance_rate', 100)
            threshold = conditions.get('threshold', 75)
            operator = conditions.get('operator', 'less_than')
            
            if operator == 'less_than':
                return metric_value < threshold
            elif operator == 'less_than_or_equal':
                return metric_value <= threshold
        
        elif condition_type == 'grade':
            metric_value = metrics.get('average_grade', 100)
            threshold = conditions.get('threshold', 50)
            operator = conditions.get('operator', 'less_than')
            
            if operator == 'less_than':
                return metric_value < threshold
        
        elif condition_type == 'engagement':
            metric_value = metrics.get('engagement_score', 100)
            threshold = conditions.get('threshold', 60)
            operator = conditions.get('operator', 'less_than')
            
            if operator == 'less_than':
                return metric_value < threshold
        
        elif condition_type == 'risk_score':
            metric_value = metrics.get('risk_score', 0)
            threshold = conditions.get('threshold', 70)
            operator = conditions.get('operator', 'greater_than')
            
            if operator == 'greater_than':
                return metric_value > threshold
        
        elif condition_type == 'composite':
            # Multiple conditions must all be met
            all_conditions = conditions.get('conditions', [])
            results = []
            for cond in all_conditions:
                metric_value = metrics.get(cond['metric'], 0)
                threshold = cond['threshold']
                operator = cond['operator']
                
                if operator == 'less_than':
                    results.append(metric_value < threshold)
                elif operator == 'greater_than':
                    results.append(metric_value > threshold)
            
            return all(results)
        
        return False


class InterventionWorkflowViewSet(viewsets.ModelViewSet):
    queryset = InterventionWorkflow.objects.all()
    serializer_class = InterventionWorkflowSerializer
    
    def get_queryset(self):
        tenant = self.kwargs.get('tenant_slug')
        return InterventionWorkflow.objects.filter(tenant=tenant)
    
    def perform_create(self, serializer):
        tenant = self.kwargs.get('tenant_slug')
        serializer.save(tenant=tenant)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    
    def get_queryset(self):
        tenant = self.kwargs.get('tenant_slug')
        queryset = AuditLog.objects.filter(tenant=tenant)
        
        # Filter by intervention
        intervention_id = self.request.query_params.get('intervention_id')
        if intervention_id:
            queryset = queryset.filter(intervention_id=intervention_id)
        
        # Filter by action type
        action_type = self.request.query_params.get('action_type')
        if action_type:
            queryset = queryset.filter(action_type=action_type)
        
        return queryset
