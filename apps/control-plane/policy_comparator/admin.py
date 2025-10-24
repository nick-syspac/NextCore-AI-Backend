from django.contrib import admin
from .models import ASQAStandard, ASQAClause, Policy, ComparisonResult, ComparisonSession


@admin.register(ASQAStandard)
class ASQAStandardAdmin(admin.ModelAdmin):
    list_display = ['standard_number', 'title', 'standard_type', 'version', 'is_active', 'created_at']
    list_filter = ['standard_type', 'is_active', 'version']
    search_fields = ['standard_number', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('standard_number', 'title', 'description', 'standard_type')
        }),
        ('Content', {
            'fields': ('full_text', 'requirements')
        }),
        ('Metadata', {
            'fields': ('is_active', 'effective_date', 'version')
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ASQAClause)
class ASQAClauseAdmin(admin.ModelAdmin):
    list_display = ['clause_number', 'standard', 'title', 'compliance_level', 'is_active', 'created_at']
    list_filter = ['compliance_level', 'is_active', 'standard']
    search_fields = ['clause_number', 'title', 'clause_text']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('standard', 'clause_number', 'title')
        }),
        ('Content', {
            'fields': ('clause_text', 'evidence_required', 'keywords')
        }),
        ('Compliance', {
            'fields': ('compliance_level', 'is_active')
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_number', 'title', 'tenant', 'policy_type', 'status', 'compliance_score', 'last_compared_at', 'created_at']
    list_filter = ['status', 'policy_type', 'tenant']
    search_fields = ['policy_number', 'title', 'description']
    readonly_fields = ['last_compared_at', 'compliance_score', 'created_by', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tenant', 'policy_number', 'title', 'description', 'policy_type')
        }),
        ('Content', {
            'fields': ('content', 'version', 'file_path')
        }),
        ('Status & Dates', {
            'fields': ('status', 'effective_date', 'review_date')
        }),
        ('Compliance', {
            'fields': ('last_compared_at', 'compliance_score'),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ComparisonResult)
class ComparisonResultAdmin(admin.ModelAdmin):
    list_display = ['policy', 'asqa_clause', 'similarity_score', 'match_type', 'is_compliant', 'requires_action', 'comparison_date']
    list_filter = ['match_type', 'is_compliant', 'requires_action', 'comparison_date']
    search_fields = ['policy__policy_number', 'asqa_clause__clause_number', 'gap_description']
    readonly_fields = ['comparison_date', 'match_type']
    date_hierarchy = 'comparison_date'
    
    fieldsets = (
        ('Comparison', {
            'fields': ('policy', 'asqa_clause', 'similarity_score', 'match_type')
        }),
        ('Analysis', {
            'fields': ('matched_text', 'gap_description', 'recommendations')
        }),
        ('NLP Details', {
            'fields': ('nlp_metadata', 'keywords_matched', 'keywords_missing'),
            'classes': ('collapse',)
        }),
        ('Evidence & Compliance', {
            'fields': ('has_sufficient_evidence', 'evidence_notes', 'is_compliant', 'requires_action')
        }),
        ('Review', {
            'fields': ('reviewed_by', 'reviewed_at'),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('comparison_date',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ComparisonSession)
class ComparisonSessionAdmin(admin.ModelAdmin):
    list_display = ['session_name', 'policy', 'tenant', 'status', 'overall_compliance_score', 'total_clauses_checked', 'created_at', 'completed_at']
    list_filter = ['status', 'tenant', 'created_at']
    search_fields = ['session_name', 'policy__policy_number']
    readonly_fields = ['created_by', 'created_at', 'completed_at', 'processing_time_seconds']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Session Information', {
            'fields': ('tenant', 'policy', 'session_name', 'status')
        }),
        ('Standards', {
            'fields': ('standards_compared',)
        }),
        ('Results', {
            'fields': ('total_clauses_checked', 'compliant_count', 'partial_match_count', 
                      'gap_count', 'overall_compliance_score')
        }),
        ('Performance', {
            'fields': ('processing_time_seconds',),
            'classes': ('collapse',)
        }),
        ('Error Handling', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('created_by', 'created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
