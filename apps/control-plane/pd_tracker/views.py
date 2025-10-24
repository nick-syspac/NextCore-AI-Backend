from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import timedelta, date
import json

from .models import PDActivity, TrainerProfile, PDSuggestion, ComplianceRule, ComplianceCheck
from .serializers import (
    PDActivitySerializer, PDActivityDetailSerializer,
    TrainerProfileSerializer, TrainerProfileDetailSerializer,
    PDSuggestionSerializer, PDSuggestionDetailSerializer,
    ComplianceRuleSerializer,
    ComplianceCheckSerializer, ComplianceCheckDetailSerializer,
    LogActivityRequestSerializer,
    GenerateSuggestionsRequestSerializer, GenerateSuggestionsResponseSerializer,
    CheckCurrencyRequestSerializer, CheckCurrencyResponseSerializer,
    DashboardStatsSerializer,
    ComplianceReportRequestSerializer, ComplianceReportResponseSerializer
)


class PDActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for managing PD activities"""
    queryset = PDActivity.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PDActivityDetailSerializer
        return PDActivitySerializer
    
    def get_queryset(self):
        queryset = PDActivity.objects.all()
        tenant = self.request.query_params.get('tenant')
        trainer_id = self.request.query_params.get('trainer_id')
        activity_type = self.request.query_params.get('activity_type')
        status_filter = self.request.query_params.get('status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        if trainer_id:
            queryset = queryset.filter(trainer_id=trainer_id)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        
        return queryset.order_by('-start_date')
    
    @action(detail=False, methods=['post'])
    def log_activity(self, request):
        """Log a new PD activity and update trainer profile"""
        serializer = LogActivityRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        # Create PD activity
        activity = PDActivity.objects.create(
            tenant=data['tenant'],
            trainer_id=data['trainer_id'],
            trainer_name=data['trainer_name'],
            activity_type=data['activity_type'],
            activity_title=data['activity_title'],
            description=data['description'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            hours_completed=data['hours_completed'],
            compliance_areas=data.get('compliance_areas', []),
            maintains_vocational_currency=data.get('maintains_vocational_currency', False),
            maintains_industry_currency=data.get('maintains_industry_currency', False),
            maintains_teaching_currency=data.get('maintains_teaching_currency', False),
            status='completed'
        )
        
        # Update trainer profile
        profile, created = TrainerProfile.objects.get_or_create(
            tenant=data['tenant'],
            trainer_id=data['trainer_id'],
            defaults={
                'trainer_name': data['trainer_name']
            }
        )
        
        # Update hours
        profile.total_pd_hours += data['hours_completed']
        profile.current_year_hours += data['hours_completed']
        
        if data.get('maintains_vocational_currency'):
            profile.vocational_pd_hours += data['hours_completed']
            profile.last_vocational_pd = max(
                profile.last_vocational_pd or data['end_date'],
                data['end_date']
            )
        
        if data.get('maintains_industry_currency'):
            profile.industry_pd_hours += data['hours_completed']
            profile.last_industry_pd = max(
                profile.last_industry_pd or data['end_date'],
                data['end_date']
            )
        
        if data.get('maintains_teaching_currency'):
            profile.teaching_pd_hours += data['hours_completed']
            profile.last_teaching_pd = max(
                profile.last_teaching_pd or data['end_date'],
                data['end_date']
            )
        
        # Update currency status
        self._update_currency_status(profile)
        profile.save()
        
        return Response({
            'activity': PDActivityDetailSerializer(activity).data,
            'profile': TrainerProfileDetailSerializer(profile).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def verify_activity(self, request, pk=None):
        """Verify a PD activity"""
        activity = self.get_object()
        
        activity.verification_status = 'verified'
        activity.verified_by = request.data.get('verified_by', 'System')
        activity.verified_date = timezone.now().date()
        activity.save()
        
        return Response(PDActivityDetailSerializer(activity).data)
    
    def _update_currency_status(self, profile):
        """Update currency status based on last PD dates"""
        today = timezone.now().date()
        
        # Vocational currency (1 year)
        if profile.vocational_currency_required:
            if profile.last_vocational_pd:
                days_since = (today - profile.last_vocational_pd).days
                if days_since > 365:
                    profile.vocational_currency_status = 'expired'
                elif days_since > 335:  # 30 days warning
                    profile.vocational_currency_status = 'expiring_soon'
                else:
                    profile.vocational_currency_status = 'current'
            else:
                profile.vocational_currency_status = 'expired'
        else:
            profile.vocational_currency_status = 'not_applicable'
        
        # Industry currency (2 years)
        if profile.industry_currency_required:
            if profile.last_industry_pd:
                days_since = (today - profile.last_industry_pd).days
                if days_since > 730:
                    profile.industry_currency_status = 'expired'
                elif days_since > 700:  # 30 days warning
                    profile.industry_currency_status = 'expiring_soon'
                else:
                    profile.industry_currency_status = 'current'
            else:
                profile.industry_currency_status = 'expired'
        else:
            profile.industry_currency_status = 'not_applicable'


class TrainerProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for managing trainer profiles"""
    queryset = TrainerProfile.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'check_currency']:
            return TrainerProfileDetailSerializer
        return TrainerProfileSerializer
    
    def get_queryset(self):
        queryset = TrainerProfile.objects.all()
        tenant = self.request.query_params.get('tenant')
        
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        
        return queryset.order_by('trainer_name')
    
    @action(detail=False, methods=['post'])
    def check_currency(self, request):
        """Check trainer currency status"""
        serializer = CheckCurrencyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        trainer_id = serializer.validated_data['trainer_id']
        check_period_months = serializer.validated_data.get('check_period_months', 12)
        
        try:
            profile = TrainerProfile.objects.get(trainer_id=trainer_id)
        except TrainerProfile.DoesNotExist:
            return Response(
                {'error': 'Trainer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate period
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=check_period_months * 30)
        
        # Get activities in period
        activities = PDActivity.objects.filter(
            tenant=profile.tenant,
            trainer_id=trainer_id,
            start_date__gte=start_date,
            end_date__lte=end_date,
            status='completed'
        )
        
        total_hours = activities.aggregate(total=Sum('hours_completed'))['total'] or 0
        
        # Check compliance
        compliance_issues = []
        recommendations = []
        
        if profile.vocational_currency_status == 'expired':
            compliance_issues.append("Vocational currency has expired")
            recommendations.append("Complete vocational competency PD urgently")
        elif profile.vocational_currency_status == 'expiring_soon':
            recommendations.append("Vocational currency expiring soon - plan PD activity")
        
        if profile.industry_currency_status == 'expired':
            compliance_issues.append("Industry currency has expired")
            recommendations.append("Complete industry engagement PD urgently")
        elif profile.industry_currency_status == 'expiring_soon':
            recommendations.append("Industry currency expiring soon - plan industry placement")
        
        if profile.current_year_hours < profile.annual_pd_goal_hours:
            hours_needed = profile.annual_pd_goal_hours - profile.current_year_hours
            recommendations.append(f"Need {hours_needed:.1f} more hours to meet annual goal")
        
        response_data = {
            'trainer_profile': TrainerProfileDetailSerializer(profile).data,
            'vocational_status': profile.vocational_currency_status,
            'industry_status': profile.industry_currency_status,
            'teaching_status': 'current',  # Simplified for now
            'total_hours_period': total_hours,
            'compliance_issues': compliance_issues,
            'recommendations': recommendations
        }
        
        return Response(response_data)


class PDSuggestionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing PD suggestions"""
    queryset = PDSuggestion.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PDSuggestionDetailSerializer
        return PDSuggestionSerializer
    
    def get_queryset(self):
        queryset = PDSuggestion.objects.all()
        trainer_id = self.request.query_params.get('trainer_id')
        priority = self.request.query_params.get('priority')
        status_filter = self.request.query_params.get('status')
        
        if trainer_id:
            queryset = queryset.filter(trainer_profile__trainer_id=trainer_id)
        if priority:
            queryset = queryset.filter(priority_level=priority)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-priority_level', '-generation_date')
    
    @action(detail=False, methods=['post'])
    def generate_suggestions(self, request):
        """Generate LLM-powered PD suggestions for a trainer"""
        serializer = GenerateSuggestionsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        trainer_id = serializer.validated_data['trainer_id']
        focus_areas = serializer.validated_data.get('focus_areas', [])
        include_critical_only = serializer.validated_data.get('include_critical_only', False)
        max_suggestions = serializer.validated_data.get('max_suggestions', 5)
        
        try:
            profile = TrainerProfile.objects.get(trainer_id=trainer_id)
        except TrainerProfile.DoesNotExist:
            return Response(
                {'error': 'Trainer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        suggestions = []
        currency_gaps = {}
        compliance_risks = []
        
        # Check for currency gaps
        if profile.vocational_currency_status == 'expired':
            currency_gaps['vocational'] = 'expired'
            compliance_risks.append("Vocational currency expired - immediate action required")
            
            suggestions.append(PDSuggestion.objects.create(
                trainer_profile=profile,
                suggested_activity_type='formal_course',
                activity_title='Vocational Competency Update Training',
                description='Complete formal training to update vocational skills and knowledge in your teaching area',
                rationale='Your vocational currency has expired. ASQA requires trainers to maintain current vocational competency.',
                addresses_currency_gap='vocational',
                priority_level='critical',
                suggested_timeframe='Within 30 days',
                estimated_hours=20.0,
                generated_by_model='rule-based',
                status='pending_review'
            ))
        elif profile.vocational_currency_status == 'expiring_soon':
            currency_gaps['vocational'] = 'expiring_soon'
            
            suggestions.append(PDSuggestion.objects.create(
                trainer_profile=profile,
                suggested_activity_type='workshop',
                activity_title='Vocational Skills Workshop',
                description='Attend industry workshop to refresh and update vocational skills',
                rationale='Your vocational currency expires soon. Plan ahead to maintain compliance.',
                addresses_currency_gap='vocational',
                priority_level='high',
                suggested_timeframe='Within 60 days',
                estimated_hours=8.0,
                generated_by_model='rule-based',
                status='pending_review'
            ))
        
        if profile.industry_currency_status == 'expired':
            currency_gaps['industry'] = 'expired'
            compliance_risks.append("Industry currency expired - immediate action required")
            
            suggestions.append(PDSuggestion.objects.create(
                trainer_profile=profile,
                suggested_activity_type='industry_placement',
                activity_title='Industry Placement/Work Experience',
                description='Complete industry placement to regain current industry experience',
                rationale='Your industry currency has expired. Engage with current industry practices.',
                addresses_currency_gap='industry',
                priority_level='critical',
                suggested_timeframe='Within 60 days',
                estimated_hours=40.0,
                generated_by_model='rule-based',
                status='pending_review'
            ))
        elif profile.industry_currency_status == 'expiring_soon':
            currency_gaps['industry'] = 'expiring_soon'
            
            suggestions.append(PDSuggestion.objects.create(
                trainer_profile=profile,
                suggested_activity_type='networking',
                activity_title='Industry Networking Event',
                description='Attend industry conference or networking event to maintain industry connections',
                rationale='Your industry currency expires soon. Stay connected with industry developments.',
                addresses_currency_gap='industry',
                priority_level='high',
                suggested_timeframe='Within 90 days',
                estimated_hours=16.0,
                generated_by_model='rule-based',
                status='pending_review'
            ))
        
        # Check annual hours goal
        if profile.current_year_hours < profile.annual_pd_goal_hours:
            hours_needed = profile.annual_pd_goal_hours - profile.current_year_hours
            
            suggestions.append(PDSuggestion.objects.create(
                trainer_profile=profile,
                suggested_activity_type='webinar',
                activity_title='Professional Development Webinar Series',
                description=f'Complete webinar series to meet annual PD hours goal ({hours_needed:.1f} hours needed)',
                rationale='You are below your annual PD hours goal. Regular PD maintains teaching quality.',
                addresses_currency_gap='skill_development',
                priority_level='medium',
                suggested_timeframe='Before year end',
                estimated_hours=hours_needed,
                generated_by_model='rule-based',
                status='pending_review'
            ))
        
        # Add teaching skills suggestion
        if len(suggestions) < max_suggestions:
            suggestions.append(PDSuggestion.objects.create(
                trainer_profile=profile,
                suggested_activity_type='teaching_observation',
                activity_title='Peer Teaching Observation',
                description='Observe experienced trainers and receive feedback on your teaching practice',
                rationale='Regular teaching observations improve instructional quality and student outcomes.',
                addresses_currency_gap='teaching',
                priority_level='medium',
                suggested_timeframe='Next quarter',
                estimated_hours=4.0,
                generated_by_model='rule-based',
                status='pending_review'
            ))
        
        # Filter if critical only
        if include_critical_only:
            suggestions = [s for s in suggestions if s.priority_level == 'critical']
        
        # Limit to max suggestions
        suggestions = suggestions[:max_suggestions]
        
        response_data = {
            'suggestions': PDSuggestionDetailSerializer(suggestions, many=True).data,
            'total_generated': len(suggestions),
            'currency_gaps': currency_gaps,
            'compliance_risks': compliance_risks
        }
        
        return Response(response_data)
    
    @action(detail=True, methods=['post'])
    def accept_suggestion(self, request, pk=None):
        """Accept a suggestion and optionally create linked activity"""
        suggestion = self.get_object()
        suggestion.status = 'accepted'
        suggestion.trainer_feedback = request.data.get('feedback', '')
        suggestion.save()
        
        return Response(PDSuggestionDetailSerializer(suggestion).data)


class ComplianceRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for managing compliance rules"""
    queryset = ComplianceRule.objects.all()
    serializer_class = ComplianceRuleSerializer
    
    def get_queryset(self):
        queryset = ComplianceRule.objects.filter(is_active=True)
        tenant = self.request.query_params.get('tenant')
        regulatory_source = self.request.query_params.get('regulatory_source')
        
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        if regulatory_source:
            queryset = queryset.filter(regulatory_source=regulatory_source)
        
        return queryset.order_by('regulatory_source', 'rule_name')


class ComplianceCheckViewSet(viewsets.ModelViewSet):
    """ViewSet for managing compliance checks"""
    queryset = ComplianceCheck.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ComplianceCheckDetailSerializer
        return ComplianceCheckSerializer
    
    def get_queryset(self):
        queryset = ComplianceCheck.objects.all()
        trainer_id = self.request.query_params.get('trainer_id')
        overall_status = self.request.query_params.get('overall_status')
        
        if trainer_id:
            queryset = queryset.filter(trainer_profile__trainer_id=trainer_id)
        if overall_status:
            queryset = queryset.filter(overall_status=overall_status)
        
        return queryset.order_by('-check_date')
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get dashboard statistics"""
        tenant = request.query_params.get('tenant')
        
        # Base querysets
        activities = PDActivity.objects.all()
        profiles = TrainerProfile.objects.all()
        
        if tenant:
            activities = activities.filter(tenant=tenant)
            profiles = profiles.filter(tenant=tenant)
        
        # Date ranges
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Activity stats
        total_activities = activities.filter(status='completed').count()
        total_hours = activities.filter(status='completed').aggregate(
            total=Sum('hours_completed')
        )['total'] or 0
        
        activities_last_30 = activities.filter(
            status='completed',
            start_date__gte=thirty_days_ago
        ).count()
        
        hours_last_30 = activities.filter(
            status='completed',
            start_date__gte=thirty_days_ago
        ).aggregate(total=Sum('hours_completed'))['total'] or 0
        
        # Currency status
        trainers_current = profiles.filter(
            Q(vocational_currency_status='current') | Q(industry_currency_status='current')
        ).distinct().count()
        
        trainers_expiring = profiles.filter(
            Q(vocational_currency_status='expiring_soon') | Q(industry_currency_status='expiring_soon')
        ).distinct().count()
        
        trainers_expired = profiles.filter(
            Q(vocational_currency_status='expired') | Q(industry_currency_status='expired')
        ).distinct().count()
        
        # Activities by type
        activities_by_type = dict(
            activities.filter(status='completed').values('activity_type').annotate(
                count=Count('id')
            ).values_list('activity_type', 'count')
        )
        
        # Pending items
        pending_suggestions = PDSuggestion.objects.filter(status='pending_review').count()
        pending_verifications = activities.filter(verification_status='pending').count()
        
        # Top trainers
        top_trainers = list(
            profiles.order_by('-current_year_hours')[:5].values(
                'trainer_name', 'current_year_hours', 'annual_pd_goal_hours'
            )
        )
        
        # Monthly hours (last 6 months)
        monthly_hours = []
        for i in range(6):
            month_start = today.replace(day=1) - timedelta(days=i*30)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            month_total = activities.filter(
                status='completed',
                start_date__gte=month_start,
                start_date__lte=month_end
            ).aggregate(total=Sum('hours_completed'))['total'] or 0
            
            monthly_hours.append({
                'month': month_start.strftime('%b %Y'),
                'hours': float(month_total)
            })
        
        monthly_hours.reverse()
        
        response_data = {
            'total_activities': total_activities,
            'total_hours': float(total_hours),
            'activities_last_30_days': activities_last_30,
            'hours_last_30_days': float(hours_last_30),
            'trainers_current': trainers_current,
            'trainers_expiring_soon': trainers_expiring,
            'trainers_expired': trainers_expired,
            'activities_by_type': activities_by_type,
            'compliance_checks_needed': trainers_expired,
            'pending_suggestions': pending_suggestions,
            'pending_verifications': pending_verifications,
            'top_trainers': top_trainers,
            'monthly_hours': monthly_hours
        }
        
        return Response(response_data)
    
    @action(detail=False, methods=['post'])
    def compliance_report(self, request):
        """Generate compliance report"""
        serializer = ComplianceReportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        tenant = data['tenant']
        period_start = data['period_start']
        period_end = data['period_end']
        include_trainers = data.get('include_trainers', [])
        
        # Get trainer profiles
        profiles = TrainerProfile.objects.filter(tenant=tenant)
        if include_trainers:
            profiles = profiles.filter(trainer_id__in=include_trainers)
        
        # Run compliance checks
        compliance_checks = []
        compliant = 0
        at_risk = 0
        non_compliant = 0
        
        for profile in profiles:
            # Get activities in period
            activities = PDActivity.objects.filter(
                tenant=tenant,
                trainer_id=profile.trainer_id,
                start_date__gte=period_start,
                end_date__lte=period_end,
                status='completed'
            )
            
            hours_completed = activities.aggregate(total=Sum('hours_completed'))['total'] or 0
            
            # Determine status
            issues = []
            if profile.vocational_currency_status == 'expired':
                issues.append("Vocational currency expired")
            if profile.industry_currency_status == 'expired':
                issues.append("Industry currency expired")
            
            if issues:
                overall_status = 'non_compliant'
                non_compliant += 1
            elif profile.vocational_currency_status == 'expiring_soon' or profile.industry_currency_status == 'expiring_soon':
                overall_status = 'at_risk'
                at_risk += 1
            else:
                overall_status = 'compliant'
                compliant += 1
            
            # Create check record
            check = ComplianceCheck.objects.create(
                trainer_profile=profile,
                check_date=timezone.now().date(),
                check_period_start=period_start,
                check_period_end=period_end,
                checked_by=request.user.username if request.user.is_authenticated else 'System',
                overall_status=overall_status,
                hours_required=profile.annual_pd_goal_hours,
                hours_completed=hours_completed,
                hours_shortfall=max(0, profile.annual_pd_goal_hours - hours_completed),
                findings=[{'issue': issue} for issue in issues],
                requires_action=len(issues) > 0
            )
            
            compliance_checks.append(check)
        
        response_data = {
            'report_date': timezone.now().date(),
            'period_start': period_start,
            'period_end': period_end,
            'total_trainers': profiles.count(),
            'compliant_trainers': compliant,
            'at_risk_trainers': at_risk,
            'non_compliant_trainers': non_compliant,
            'compliance_checks': ComplianceCheckDetailSerializer(compliance_checks, many=True).data,
            'summary': {
                'compliance_rate': (compliant / profiles.count() * 100) if profiles.count() > 0 else 0,
                'total_hours_period': sum(c.hours_completed for c in compliance_checks),
                'average_hours_per_trainer': sum(c.hours_completed for c in compliance_checks) / profiles.count() if profiles.count() > 0 else 0
            }
        }
        
        return Response(response_data)
