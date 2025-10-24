from django.contrib import admin
from .models import (
    Intervention, InterventionRule, InterventionWorkflow,
    InterventionStep, InterventionOutcome, AuditLog
)


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ['intervention_number', 'student_name', 'intervention_type',
                    'priority_level', 'status', 'action_taken_by', 'outcome_achieved',
                    'created_at']
    list_filter = ['status', 'priority_level', 'intervention_type', 'outcome_achieved',
                   'trigger_type', 'created_at']
    search_fields = ['intervention_number', 'student_name', 'student_id',
                     'action_description', 'action_taken_by']
    readonly_fields = ['intervention_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(InterventionRule)
class InterventionRuleAdmin(admin.ModelAdmin):
    list_display = ['rule_number', 'rule_name', 'condition_type', 'intervention_type',
                    'priority', 'is_active', 'trigger_count', 'last_triggered']
    list_filter = ['is_active', 'condition_type', 'intervention_type', 'priority']
    search_fields = ['rule_number', 'rule_name', 'description']
    readonly_fields = ['rule_number', 'last_triggered', 'trigger_count',
                       'created_at', 'updated_at']


@admin.register(InterventionWorkflow)
class InterventionWorkflowAdmin(admin.ModelAdmin):
    list_display = ['workflow_number', 'workflow_name', 'is_active',
                    'requires_approval', 'created_at']
    list_filter = ['is_active', 'requires_approval']
    search_fields = ['workflow_number', 'workflow_name', 'description']
    readonly_fields = ['workflow_number', 'created_at', 'updated_at']


@admin.register(InterventionStep)
class InterventionStepAdmin(admin.ModelAdmin):
    list_display = ['intervention', 'step_number', 'step_name', 'status',
                    'completed_by', 'completed_at']
    list_filter = ['status', 'completed_at']
    search_fields = ['intervention__intervention_number', 'step_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(InterventionOutcome)
class InterventionOutcomeAdmin(admin.ModelAdmin):
    list_display = ['outcome_number', 'intervention', 'metric_type',
                    'baseline_value', 'actual_value', 'improvement_percentage',
                    'target_achieved', 'impact_rating']
    list_filter = ['metric_type', 'target_achieved', 'impact_rating']
    search_fields = ['outcome_number', 'intervention__intervention_number']
    readonly_fields = ['outcome_number', 'improvement_percentage', 'target_achieved',
                       'created_at']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['log_number', 'intervention', 'action_type', 'performed_by',
                    'timestamp']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['log_number', 'intervention__intervention_number',
                     'action_description', 'performed_by']
    readonly_fields = ['log_number', 'timestamp']
    date_hierarchy = 'timestamp'
