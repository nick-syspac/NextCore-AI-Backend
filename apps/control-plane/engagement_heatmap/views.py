from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict

from .models import (
    EngagementHeatmap,
    AttendanceRecord,
    LMSActivity,
    DiscussionSentiment,
    EngagementAlert,
)
from .serializers import (
    EngagementHeatmapSerializer,
    AttendanceRecordSerializer,
    LMSActivitySerializer,
    DiscussionSentimentSerializer,
    EngagementAlertSerializer,
    HeatmapGenerationRequestSerializer,
)


class EngagementHeatmapViewSet(viewsets.ModelViewSet):
    queryset = EngagementHeatmap.objects.all()
    serializer_class = EngagementHeatmapSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_slug = self.kwargs.get("tenant_slug")
        if tenant_slug:
            queryset = queryset.filter(tenant=tenant_slug)

        # Filter by student
        student_id = self.request.query_params.get("student_id")
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        # Filter by risk level
        risk_level = self.request.query_params.get("risk_level")
        if risk_level:
            queryset = queryset.filter(risk_level=risk_level)

        return queryset

    @action(detail=False, methods=["post"])
    def generate_heatmap(self, request, tenant_slug=None):
        """
        Generate engagement heatmap with attendance tracking, LMS activity analysis,
        and sentiment analysis of discussions.
        """
        serializer = HeatmapGenerationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        student_id = data["student_id"]
        student_name = data["student_name"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        time_period = data["time_period"]

        # Step 1: Gather attendance data
        attendance_score, attendance_data = self._analyze_attendance(
            student_id, tenant_slug, start_date, end_date
        )

        # Step 2: Analyze LMS activity
        lms_score, lms_data = self._analyze_lms_activity(
            student_id, tenant_slug, start_date, end_date
        )

        # Step 3: Perform sentiment analysis on discussions
        sentiment_score, sentiment_data = self._analyze_discussion_sentiment(
            student_id, tenant_slug, start_date, end_date
        )

        # Step 4: Generate heatmap visualization data
        heatmap_data = self._generate_heatmap_data(
            student_id,
            tenant_slug,
            start_date,
            end_date,
            attendance_data,
            lms_data,
            sentiment_data,
        )

        # Step 5: Identify risk flags
        risk_flags = self._identify_risk_flags(
            attendance_score,
            lms_score,
            sentiment_score,
            attendance_data,
            lms_data,
            sentiment_data,
        )

        # Step 6: Calculate engagement trend
        engagement_trend, change_percentage = self._calculate_trend(
            student_id, tenant_slug, start_date, end_date
        )

        # Step 7: Create heatmap record
        heatmap = EngagementHeatmap.objects.create(
            tenant=tenant_slug,
            student_id=student_id,
            student_name=student_name,
            time_period=time_period,
            start_date=start_date,
            end_date=end_date,
            attendance_score=attendance_score,
            lms_activity_score=lms_score,
            sentiment_score=sentiment_score,
            risk_flags=risk_flags,
            heatmap_data=heatmap_data,
            engagement_trend=engagement_trend,
            change_percentage=change_percentage,
        )

        # Step 8: Generate alerts for high-risk indicators
        alerts_created = self._generate_alerts(heatmap, risk_flags)
        heatmap.alerts_triggered = alerts_created
        heatmap.save()

        # Serialize and return
        serializer = EngagementHeatmapSerializer(heatmap)
        return Response(
            {
                "heatmap": serializer.data,
                "analysis": {
                    "attendance": {
                        "score": attendance_score,
                        "present_days": attendance_data["present_count"],
                        "absent_days": attendance_data["absent_count"],
                        "attendance_rate": attendance_data["attendance_rate"],
                    },
                    "lms_activity": {
                        "score": lms_score,
                        "total_activities": lms_data["total_activities"],
                        "total_minutes": lms_data["total_minutes"],
                        "daily_average": lms_data["daily_average"],
                    },
                    "sentiment": {
                        "score": sentiment_score,
                        "avg_sentiment": sentiment_data["avg_sentiment"],
                        "positive_ratio": sentiment_data["positive_ratio"],
                        "negative_count": sentiment_data["negative_count"],
                    },
                },
                "alerts_created": alerts_created,
            }
        )

    def _analyze_attendance(self, student_id, tenant_slug, start_date, end_date):
        """Analyze attendance patterns and calculate score"""
        records = AttendanceRecord.objects.filter(
            student_id=student_id,
            tenant=tenant_slug,
            date__gte=start_date,
            date__lte=end_date,
        )

        total_days = (end_date - start_date).days + 1
        present_count = records.filter(status="present").count()
        late_count = records.filter(status="late").count()
        absent_count = records.filter(status="absent").count()

        # Calculate attendance rate
        if total_days > 0:
            attendance_rate = ((present_count + (late_count * 0.5)) / total_days) * 100
        else:
            attendance_rate = 0

        # Attendance score (0-100)
        score = min(100, attendance_rate)

        data = {
            "total_days": total_days,
            "present_count": present_count,
            "late_count": late_count,
            "absent_count": absent_count,
            "attendance_rate": attendance_rate,
        }

        return score, data

    def _analyze_lms_activity(self, student_id, tenant_slug, start_date, end_date):
        """Analyze LMS usage patterns and calculate engagement score"""
        activities = LMSActivity.objects.filter(
            student_id=student_id,
            tenant=tenant_slug,
            date__gte=start_date,
            date__lte=end_date,
        )

        total_activities = activities.count()
        total_minutes = (
            activities.aggregate(total=Sum("duration_minutes"))["total"] or 0
        )
        total_days = (end_date - start_date).days + 1

        # Daily activity metrics
        daily_average = total_activities / total_days if total_days > 0 else 0
        daily_minutes = total_minutes / total_days if total_days > 0 else 0

        # Activity type breakdown
        activity_breakdown = activities.values("activity_type").annotate(
            count=Count("id")
        )

        # Calculate LMS score (0-100)
        # Based on: activity frequency, time spent, variety of activities
        frequency_score = min(
            100, (daily_average / 5) * 100
        )  # Target: 5 activities/day
        time_score = min(100, (daily_minutes / 60) * 100)  # Target: 60 min/day
        variety_score = min(
            100, (len(activity_breakdown) / 9) * 100
        )  # 9 activity types

        score = (frequency_score * 0.4) + (time_score * 0.4) + (variety_score * 0.2)

        data = {
            "total_activities": total_activities,
            "total_minutes": total_minutes,
            "daily_average": daily_average,
            "daily_minutes": daily_minutes,
            "activity_breakdown": list(activity_breakdown),
        }

        return score, data

    def _analyze_discussion_sentiment(
        self, student_id, tenant_slug, start_date, end_date
    ):
        """Analyze sentiment from discussions and messages"""
        sentiments = DiscussionSentiment.objects.filter(
            student_id=student_id,
            tenant=tenant_slug,
            date__gte=start_date,
            date__lte=end_date,
        )

        if not sentiments.exists():
            # No discussion data - return neutral score
            return 50.0, {
                "avg_sentiment": 0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
                "positive_ratio": 0,
                "total_messages": 0,
            }

        # Calculate average sentiment
        avg_sentiment = sentiments.aggregate(avg=Avg("sentiment_score"))["avg"] or 0

        # Count by sentiment label
        positive_count = sentiments.filter(
            sentiment_label__in=["positive", "very_positive"]
        ).count()
        negative_count = sentiments.filter(
            sentiment_label__in=["negative", "very_negative"]
        ).count()
        neutral_count = sentiments.filter(sentiment_label="neutral").count()
        total_messages = sentiments.count()

        # Calculate ratios
        positive_ratio = positive_count / total_messages if total_messages > 0 else 0

        # Normalize sentiment score to 0-100
        # -1 to +1 becomes 0 to 100
        normalized_score = ((avg_sentiment + 1) / 2) * 100

        data = {
            "avg_sentiment": avg_sentiment,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "positive_ratio": positive_ratio,
            "total_messages": total_messages,
        }

        return normalized_score, data

    def _generate_heatmap_data(
        self,
        student_id,
        tenant_slug,
        start_date,
        end_date,
        attendance_data,
        lms_data,
        sentiment_data,
    ):
        """Generate daily heatmap visualization data"""
        heatmap = {}
        current_date = start_date

        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            # Attendance for this day
            attendance = AttendanceRecord.objects.filter(
                student_id=student_id, tenant=tenant_slug, date=current_date
            ).first()

            # LMS activity for this day
            lms_minutes = (
                LMSActivity.objects.filter(
                    student_id=student_id, tenant=tenant_slug, date=current_date
                ).aggregate(total=Sum("duration_minutes"))["total"]
                or 0
            )

            lms_count = LMSActivity.objects.filter(
                student_id=student_id, tenant=tenant_slug, date=current_date
            ).count()

            # Sentiment for this day
            sentiment = DiscussionSentiment.objects.filter(
                student_id=student_id, tenant=tenant_slug, date=current_date
            ).aggregate(avg=Avg("sentiment_score"))["avg"]

            heatmap[date_str] = {
                "attendance": attendance.status if attendance else "no_data",
                "lms_minutes": lms_minutes,
                "lms_activities": lms_count,
                "sentiment": sentiment if sentiment is not None else 0,
                "engagement_level": self._calculate_daily_engagement(
                    attendance, lms_minutes, sentiment
                ),
            }

            current_date += timedelta(days=1)

        return heatmap

    def _calculate_daily_engagement(self, attendance, lms_minutes, sentiment):
        """Calculate engagement level for a single day"""
        score = 0

        # Attendance contribution (40%)
        if attendance and attendance.status == "present":
            score += 40
        elif attendance and attendance.status == "late":
            score += 20

        # LMS activity contribution (35%)
        if lms_minutes >= 60:
            score += 35
        elif lms_minutes >= 30:
            score += 20
        elif lms_minutes > 0:
            score += 10

        # Sentiment contribution (25%)
        if sentiment is not None:
            if sentiment >= 0.3:
                score += 25
            elif sentiment >= 0:
                score += 15
            elif sentiment >= -0.3:
                score += 5

        # Map to engagement level
        if score >= 80:
            return "high"
        elif score >= 50:
            return "medium"
        elif score > 0:
            return "low"
        else:
            return "none"

    def _identify_risk_flags(
        self,
        attendance_score,
        lms_score,
        sentiment_score,
        attendance_data,
        lms_data,
        sentiment_data,
    ):
        """Identify specific risk indicators"""
        flags = []

        # Attendance risks
        if attendance_score < 60:
            flags.append("low_attendance")
        if attendance_data["absent_count"] >= 3:
            flags.append("frequent_absences")

        # LMS activity risks
        if lms_score < 40:
            flags.append("inactive_lms")
        if lms_data["daily_average"] < 2:
            flags.append("low_activity_frequency")

        # Sentiment risks
        if sentiment_score < 40:
            flags.append("negative_sentiment")
        if sentiment_data.get("negative_count", 0) > sentiment_data.get(
            "positive_count", 0
        ):
            flags.append("sentiment_decline")

        # Combined risks
        overall_score = (
            (attendance_score * 0.4) + (lms_score * 0.35) + (sentiment_score * 0.25)
        )
        if overall_score < 40:
            flags.append("critical_engagement")
        elif overall_score < 60:
            flags.append("at_risk")

        return flags

    def _calculate_trend(self, student_id, tenant_slug, start_date, end_date):
        """Calculate engagement trend compared to previous period"""
        # Get previous period heatmap
        period_length = (end_date - start_date).days
        previous_start = start_date - timedelta(days=period_length)
        previous_end = start_date - timedelta(days=1)

        previous_heatmap = EngagementHeatmap.objects.filter(
            student_id=student_id,
            tenant=tenant_slug,
            start_date=previous_start,
            end_date=previous_end,
        ).first()

        if not previous_heatmap:
            return "stable", 0.0

        # Calculate change
        # Will be calculated after current heatmap is saved
        # For now, return defaults
        return "stable", 0.0

    def _generate_alerts(self, heatmap, risk_flags):
        """Generate engagement alerts based on risk flags"""
        alerts_created = 0

        alert_configs = {
            "low_attendance": {
                "severity": "high",
                "title": "Low Attendance Warning",
                "description": f"Student {heatmap.student_name} has attendance below 60%",
                "actions": [
                    "Contact student to discuss attendance concerns",
                    "Review reasons for absences",
                    "Provide attendance improvement plan",
                ],
            },
            "inactive_lms": {
                "severity": "high",
                "title": "LMS Inactivity Alert",
                "description": f"Student {heatmap.student_name} shows low LMS engagement",
                "actions": [
                    "Check for technical access issues",
                    "Provide LMS training if needed",
                    "Monitor upcoming assignment submissions",
                ],
            },
            "negative_sentiment": {
                "severity": "medium",
                "title": "Negative Sentiment Detected",
                "description": f"Student {heatmap.student_name} shows negative discussion tone",
                "actions": [
                    "Schedule one-on-one check-in",
                    "Assess student wellbeing",
                    "Connect with support services if needed",
                ],
            },
            "critical_engagement": {
                "severity": "critical",
                "title": "Critical Engagement Risk",
                "description": f"Student {heatmap.student_name} shows critically low overall engagement",
                "actions": [
                    "Immediate intervention required",
                    "Contact student and emergency contact",
                    "Arrange urgent support meeting",
                    "Consider academic intervention plan",
                ],
            },
        }

        for flag in risk_flags:
            if flag in alert_configs:
                config = alert_configs[flag]
                EngagementAlert.objects.create(
                    heatmap=heatmap,
                    tenant=heatmap.tenant,
                    student_id=heatmap.student_id,
                    student_name=heatmap.student_name,
                    alert_type=flag,
                    severity=config["severity"],
                    title=config["title"],
                    description=config["description"],
                    trigger_metrics={
                        "attendance_score": float(heatmap.attendance_score),
                        "lms_score": float(heatmap.lms_activity_score),
                        "sentiment_score": float(heatmap.sentiment_score),
                    },
                    recommended_actions=config["actions"],
                )
                alerts_created += 1

        return alerts_created

    @action(detail=False, methods=["get"])
    def risk_dashboard(self, request, tenant_slug=None):
        """Visual risk dashboard with aggregated metrics"""
        heatmaps = EngagementHeatmap.objects.filter(tenant=tenant_slug)

        # Risk level breakdown
        risk_breakdown = heatmaps.values("risk_level").annotate(count=Count("id"))

        # Active alerts
        active_alerts = (
            EngagementAlert.objects.filter(tenant=tenant_slug, status="active")
            .values("severity")
            .annotate(count=Count("id"))
        )

        # Average scores
        avg_scores = heatmaps.aggregate(
            avg_attendance=Avg("attendance_score"),
            avg_lms=Avg("lms_activity_score"),
            avg_sentiment=Avg("sentiment_score"),
            avg_overall=Avg("overall_engagement_score"),
        )

        # Trend analysis
        trends = heatmaps.values("engagement_trend").annotate(count=Count("id"))

        return Response(
            {
                "risk_breakdown": list(risk_breakdown),
                "active_alerts": list(active_alerts),
                "average_scores": avg_scores,
                "trends": list(trends),
                "total_students": heatmaps.values("student_id").distinct().count(),
                "at_risk_count": heatmaps.filter(
                    risk_level__in=["high", "critical"]
                ).count(),
            }
        )


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_slug = self.kwargs.get("tenant_slug")
        if tenant_slug:
            queryset = queryset.filter(tenant=tenant_slug)

        student_id = self.request.query_params.get("student_id")
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset


class LMSActivityViewSet(viewsets.ModelViewSet):
    queryset = LMSActivity.objects.all()
    serializer_class = LMSActivitySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_slug = self.kwargs.get("tenant_slug")
        if tenant_slug:
            queryset = queryset.filter(tenant=tenant_slug)

        student_id = self.request.query_params.get("student_id")
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset


class DiscussionSentimentViewSet(viewsets.ModelViewSet):
    queryset = DiscussionSentiment.objects.all()
    serializer_class = DiscussionSentimentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_slug = self.kwargs.get("tenant_slug")
        if tenant_slug:
            queryset = queryset.filter(tenant=tenant_slug)

        student_id = self.request.query_params.get("student_id")
        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset


class EngagementAlertViewSet(viewsets.ModelViewSet):
    queryset = EngagementAlert.objects.all()
    serializer_class = EngagementAlertSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_slug = self.kwargs.get("tenant_slug")
        if tenant_slug:
            queryset = queryset.filter(tenant=tenant_slug)

        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None, tenant_slug=None):
        """Acknowledge an alert"""
        alert = self.get_object()
        alert.status = "acknowledged"
        alert.acknowledged_by = request.data.get("acknowledged_by", "Unknown")
        alert.acknowledged_at = timezone.now()
        alert.save()

        serializer = self.get_serializer(alert)
        return Response(serializer.data)
