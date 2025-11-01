from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import date
import json


class JurisdictionRequirement(models.Model):
    """
    Defines funding eligibility requirements by Australian jurisdiction (State/Territory).
    Each jurisdiction has specific rules for VET funding eligibility.
    """
    JURISDICTION_CHOICES = [
        ('nsw', 'New South Wales'),
        ('vic', 'Victoria'),
        ('qld', 'Queensland'),
        ('wa', 'Western Australia'),
        ('sa', 'South Australia'),
        ('tas', 'Tasmania'),
        ('act', 'Australian Capital Territory'),
        ('nt', 'Northern Territory'),
        ('federal', 'Federal (Commonwealth)'),
    ]

    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name='jurisdiction_requirements')
    jurisdiction = models.CharField(max_length=20, choices=JURISDICTION_CHOICES)
    name = models.CharField(max_length=200, help_text="Name of funding program (e.g., 'Smart and Skilled NSW')")
    code = models.CharField(max_length=50, help_text="Program code (e.g., 'SS-NSW', 'STS-VIC')")
    
    # Residency requirements
    requires_australian_citizen = models.BooleanField(default=False)
    requires_permanent_resident = models.BooleanField(default=False)
    requires_jurisdiction_resident = models.BooleanField(default=True)
    min_jurisdiction_residency_months = models.IntegerField(
        default=6,
        validators=[MinValueValidator(0)],
        help_text="Minimum months of residency required"
    )
    
    # Age requirements
    min_age = models.IntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )
    max_age = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )
    
    # Education requirements
    requires_year_12 = models.BooleanField(default=False)
    allows_year_10_completion = models.BooleanField(default=True)
    
    # Employment requirements
    requires_unemployed = models.BooleanField(default=False)
    allows_employed = models.BooleanField(default=True)
    requires_apprentice_trainee = models.BooleanField(default=False)
    
    # Prior qualification restrictions
    restricts_higher_qualifications = models.BooleanField(
        default=False,
        help_text="Student cannot have a higher qualification than what they're enrolling in"
    )
    max_aqf_level = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Maximum AQF level student can already have"
    )
    
    # Income requirements
    has_income_threshold = models.BooleanField(default=False)
    max_annual_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum annual income in AUD"
    )
    
    # Special categories
    allows_concession_card = models.BooleanField(default=True)
    allows_disability = models.BooleanField(default=True)
    allows_indigenous = models.BooleanField(default=True)
    priority_indigenous = models.BooleanField(default=False)
    
    # Program metadata
    funding_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of course fees covered"
    )
    student_contribution = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Student contribution/co-payment amount in AUD"
    )
    
    # API integration
    api_endpoint = models.URLField(
        blank=True,
        null=True,
        help_text="External API endpoint for eligibility verification"
    )
    api_key_required = models.BooleanField(default=False)
    
    # Additional rules (JSON for flexible rule definitions)
    additional_rules = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional eligibility rules in JSON format"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    effective_from = models.DateField(default=date.today)
    effective_to = models.DateField(null=True, blank=True)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_requirements')
    
    class Meta:
        ordering = ['jurisdiction', 'name']
        unique_together = ['tenant', 'jurisdiction', 'code']
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['jurisdiction']),
            models.Index(fields=['effective_from', 'effective_to']),
        ]
    
    def __str__(self):
        return f"{self.get_jurisdiction_display()} - {self.name}"
    
    def is_currently_effective(self):
        """Check if requirement is currently in effect"""
        from datetime import date
        today = date.today()
        if not self.is_active:
            return False
        if self.effective_from > today:
            return False
        if self.effective_to and self.effective_to < today:
            return False
        return True


class EligibilityRule(models.Model):
    """
    Custom eligibility rules that can be combined with jurisdiction requirements.
    Provides flexible, tenant-specific rule definitions.
    """
    RULE_TYPE_CHOICES = [
        ('age', 'Age Requirement'),
        ('residency', 'Residency Requirement'),
        ('citizenship', 'Citizenship Requirement'),
        ('education', 'Education Requirement'),
        ('employment', 'Employment Status'),
        ('income', 'Income Threshold'),
        ('disability', 'Disability Status'),
        ('concession', 'Concession Card Holder'),
        ('indigenous', 'Indigenous Status'),
        ('language', 'Language Proficiency'),
        ('visa', 'Visa Type'),
        ('qualification', 'Prior Qualification'),
        ('custom', 'Custom Rule'),
    ]
    
    OPERATOR_CHOICES = [
        ('equals', 'Equals'),
        ('not_equals', 'Not Equals'),
        ('greater_than', 'Greater Than'),
        ('less_than', 'Less Than'),
        ('greater_equal', 'Greater Than or Equal'),
        ('less_equal', 'Less Than or Equal'),
        ('contains', 'Contains'),
        ('not_contains', 'Does Not Contain'),
        ('in_list', 'In List'),
        ('not_in_list', 'Not In List'),
        ('between', 'Between'),
        ('regex', 'Matches Pattern'),
    ]
    
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name='eligibility_rules')
    jurisdiction_requirement = models.ForeignKey(
        JurisdictionRequirement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='custom_rules',
        help_text="Link to specific jurisdiction requirement (optional)"
    )
    
    # Rule definition
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # Rule logic
    field_name = models.CharField(
        max_length=100,
        help_text="Field to evaluate (e.g., 'age', 'citizenship_status', 'income')"
    )
    operator = models.CharField(max_length=20, choices=OPERATOR_CHOICES)
    expected_value = models.CharField(
        max_length=500,
        help_text="Expected value or comma-separated list for comparison"
    )
    
    # Rule behavior
    is_mandatory = models.BooleanField(
        default=True,
        help_text="Must pass for eligibility (vs. optional/bonus points)"
    )
    priority = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Evaluation priority (1=highest)"
    )
    
    # Error handling
    error_message = models.TextField(
        help_text="Message shown when rule fails"
    )
    override_allowed = models.BooleanField(
        default=False,
        help_text="Can be manually overridden by authorized staff"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_rules')
    
    class Meta:
        ordering = ['priority', 'rule_type', 'name']
        indexes = [
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['rule_type']),
            models.Index(fields=['priority']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_rule_type_display()})"
    
    def evaluate(self, student_data):
        """
        Evaluate rule against student data.
        Returns (passed: bool, message: str)
        """
        field_value = student_data.get(self.field_name)
        
        if field_value is None:
            return False, f"Missing required field: {self.field_name}"
        
        try:
            # Convert values for comparison
            expected = self.expected_value
            
            if self.operator == 'equals':
                passed = str(field_value) == str(expected)
            elif self.operator == 'not_equals':
                passed = str(field_value) != str(expected)
            elif self.operator == 'greater_than':
                passed = float(field_value) > float(expected)
            elif self.operator == 'less_than':
                passed = float(field_value) < float(expected)
            elif self.operator == 'greater_equal':
                passed = float(field_value) >= float(expected)
            elif self.operator == 'less_equal':
                passed = float(field_value) <= float(expected)
            elif self.operator == 'contains':
                passed = str(expected).lower() in str(field_value).lower()
            elif self.operator == 'not_contains':
                passed = str(expected).lower() not in str(field_value).lower()
            elif self.operator == 'in_list':
                list_values = [v.strip() for v in expected.split(',')]
                passed = str(field_value) in list_values
            elif self.operator == 'not_in_list':
                list_values = [v.strip() for v in expected.split(',')]
                passed = str(field_value) not in list_values
            elif self.operator == 'between':
                min_val, max_val = expected.split(',')
                passed = float(min_val) <= float(field_value) <= float(max_val)
            elif self.operator == 'regex':
                import re
                passed = bool(re.match(expected, str(field_value)))
            else:
                return False, f"Unknown operator: {self.operator}"
            
            if passed:
                return True, "Rule passed"
            else:
                return False, self.error_message
        
        except Exception as e:
            return False, f"Rule evaluation error: {str(e)}"


class EligibilityCheck(models.Model):
    """
    Records of eligibility checks performed for students.
    Tracks validation results, failures, and overrides.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('eligible', 'Eligible'),
        ('ineligible', 'Not Eligible'),
        ('conditional', 'Conditionally Eligible'),
        ('override', 'Override Approved'),
        ('expired', 'Eligibility Expired'),
    ]
    
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, related_name='eligibility_checks')
    check_number = models.CharField(max_length=50, unique=True, editable=False)
    
    # Student information
    student_first_name = models.CharField(max_length=100)
    student_last_name = models.CharField(max_length=100)
    student_dob = models.DateField(help_text="Date of birth")
    student_email = models.EmailField()
    student_phone = models.CharField(max_length=20, blank=True)
    
    # Enrollment details
    course_code = models.CharField(max_length=50)
    course_name = models.CharField(max_length=200)
    aqf_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="AQF level of course (1-10)"
    )
    intended_start_date = models.DateField()
    
    # Jurisdiction and funding
    jurisdiction = models.CharField(max_length=20, choices=JurisdictionRequirement.JURISDICTION_CHOICES)
    jurisdiction_requirement = models.ForeignKey(
        JurisdictionRequirement,
        on_delete=models.SET_NULL,
        null=True,
        related_name='checks'
    )
    funding_program_code = models.CharField(max_length=50, blank=True)
    
    # Student eligibility data (JSON for flexibility)
    student_data = models.JSONField(
        default=dict,
        help_text="Student eligibility information including citizenship, residency, employment, etc."
    )
    
    # Check results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_eligible = models.BooleanField(default=False)
    eligibility_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Percentage of rules passed"
    )
    
    # Rules evaluation
    rules_checked = models.IntegerField(default=0)
    rules_passed = models.IntegerField(default=0)
    rules_failed = models.IntegerField(default=0)
    
    # Detailed results (JSON)
    check_results = models.JSONField(
        default=dict,
        help_text="Detailed results of each rule evaluation"
    )
    failed_rules = models.JSONField(
        default=list,
        help_text="List of failed rule details"
    )
    warnings = models.JSONField(
        default=list,
        help_text="Non-critical warnings"
    )
    
    # API verification
    api_verified = models.BooleanField(default=False)
    api_response = models.JSONField(
        default=dict,
        blank=True,
        help_text="Response from external API verification"
    )
    api_verified_at = models.DateTimeField(null=True, blank=True)
    
    # Override handling
    override_required = models.BooleanField(default=False)
    override_approved = models.BooleanField(default=False)
    override_reason = models.TextField(blank=True)
    override_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eligibility_overrides'
    )
    override_approved_at = models.DateTimeField(null=True, blank=True)
    
    # Compliance
    prevents_enrollment = models.BooleanField(
        default=True,
        help_text="If ineligible, prevent enrollment"
    )
    compliance_notes = models.TextField(blank=True)
    
    # Validity period
    valid_from = models.DateField(auto_now_add=True)
    valid_until = models.DateField(
        null=True,
        blank=True,
        help_text="Eligibility expiry date"
    )
    
    # Audit
    checked_at = models.DateTimeField(auto_now_add=True)
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='eligibility_checks_performed')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-checked_at']
        indexes = [
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['check_number']),
            models.Index(fields=['jurisdiction']),
            models.Index(fields=['student_email']),
            models.Index(fields=['intended_start_date']),
            models.Index(fields=['is_eligible']),
        ]
    
    def __str__(self):
        return f"{self.check_number} - {self.student_first_name} {self.student_last_name}"
    
    def save(self, *args, **kwargs):
        if not self.check_number:
            # Generate unique check number
            from django.utils.crypto import get_random_string
            today = timezone.now()
            self.check_number = f"EC-{today.strftime('%Y%m%d')}-{get_random_string(6, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
        super().save(*args, **kwargs)
    
    def calculate_age(self):
        """Calculate student's age"""
        today = timezone.now().date()
        return today.year - self.student_dob.year - (
            (today.month, today.day) < (self.student_dob.month, self.student_dob.day)
        )
    
    def is_currently_valid(self):
        """Check if eligibility is still valid"""
        if self.status not in ['eligible', 'conditional', 'override']:
            return False
        if self.valid_until and self.valid_until < timezone.now().date():
            return False
        return True
    
    def get_eligibility_summary(self):
        """Get human-readable eligibility summary"""
        if self.is_eligible:
            return f"Eligible for {self.jurisdiction_requirement.name if self.jurisdiction_requirement else self.jurisdiction} funding"
        else:
            failed_count = len(self.failed_rules)
            return f"Not eligible - {failed_count} requirement(s) not met"


class EligibilityCheckLog(models.Model):
    """
    Audit log for all eligibility check activities.
    """
    ACTION_CHOICES = [
        ('check_created', 'Check Created'),
        ('rule_evaluated', 'Rule Evaluated'),
        ('api_called', 'API Called'),
        ('status_changed', 'Status Changed'),
        ('override_requested', 'Override Requested'),
        ('override_approved', 'Override Approved'),
        ('override_rejected', 'Override Rejected'),
        ('check_expired', 'Check Expired'),
    ]
    
    eligibility_check = models.ForeignKey(EligibilityCheck, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    details = models.JSONField(default=dict)
    notes = models.TextField(blank=True)
    
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    performed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-performed_at']
        indexes = [
            models.Index(fields=['eligibility_check', 'performed_at']),
            models.Index(fields=['action']),
        ]
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.eligibility_check.check_number}"
