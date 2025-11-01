from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from django.utils import timezone
import random
import math

from .models import (
    RiskAssessment,
    RiskFactor,
    StudentEngagementMetric,
    SentimentAnalysis,
    InterventionAction,
)
from .serializers import (
    RiskAssessmentSerializer,
    RiskAssessmentListSerializer,
    RiskFactorSerializer,
    StudentEngagementMetricSerializer,
    SentimentAnalysisSerializer,
    InterventionActionSerializer,
)


class RiskAssessmentViewSet(viewsets.ModelViewSet):
    queryset = RiskAssessment.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RiskAssessmentListSerializer
        return RiskAssessmentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["post"])
    def predict_risk(self, request):
        """
        Predict dropout risk using logistic regression + sentiment fusion

        Expected payload:
        {
            "student_id": "STU001",
            "student_name": "John Doe",
            "engagement_data": {...},
            "performance_data": {...},
            "attendance_data": {...},
            "sentiment_data": {...}
        }
        """
        student_id = request.data.get("student_id")
        student_name = request.data.get("student_name")
        engagement_data = request.data.get("engagement_data", {})
        performance_data = request.data.get("performance_data", {})
        attendance_data = request.data.get("attendance_data", {})
        sentiment_data = request.data.get("sentiment_data", {})

        if not student_id or not student_name:
            return Response(
                {"error": "student_id and student_name are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate component scores
        engagement_score = self._calculate_engagement_score(engagement_data)
        performance_score = self._calculate_performance_score(performance_data)
        attendance_score = self._calculate_attendance_score(attendance_data)
        sentiment_score = self._calculate_sentiment_score(sentiment_data)

        # Logistic regression model simulation
        dropout_probability = self._logistic_regression_model(
            engagement_score, performance_score, attendance_score, sentiment_score
        )

        # Calculate overall risk score (0-100)
        risk_score = int(dropout_probability * 100)

        # Model confidence (higher confidence when extreme values)
        confidence = self._calculate_model_confidence(
            engagement_score, performance_score, attendance_score, sentiment_score
        )

        # Create assessment
        assessment = RiskAssessment.objects.create(
            student_id=student_id,
            student_name=student_name,
            dropout_probability=dropout_probability,
            risk_score=risk_score,
            engagement_score=engagement_score,
            performance_score=performance_score,
            attendance_score=attendance_score,
            sentiment_score=sentiment_score,
            confidence=confidence,
            created_by=request.user,
        )

        # Generate risk factors
        risk_factors = self._generate_risk_factors(
            assessment,
            engagement_score,
            performance_score,
            attendance_score,
            sentiment_score,
        )

        # Generate sentiment analyses if sentiment data provided
        if sentiment_data:
            self._generate_sentiment_analyses(assessment, sentiment_data)

        # Trigger intervention for high/critical risk
        if assessment.risk_level in ["high", "critical"]:
            self._create_auto_intervention(assessment)

        serializer = RiskAssessmentSerializer(assessment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _calculate_engagement_score(self, data):
        """Calculate engagement score from engagement data"""
        if not data:
            # Generate mock score
            return random.uniform(20.0, 95.0)

        login_freq = data.get("login_frequency", 0)
        time_on_platform = data.get("time_on_platform", 0)
        submission_rate = data.get("assignment_submission_rate", 0)
        participation = data.get("forum_participation", 0)

        # Weighted scoring
        score = (
            (login_freq / 7) * 25  # 25% weight (expect 7 logins/week)
            + (time_on_platform / 10) * 25  # 25% weight (expect 10 hrs/week)
            + submission_rate * 0.30  # 30% weight
            + (participation / 10) * 20  # 20% weight (expect 10 posts)
        )

        return min(100.0, max(0.0, score))

    def _calculate_performance_score(self, data):
        """Calculate performance score from academic data"""
        if not data:
            return random.uniform(30.0, 95.0)

        avg_grade = data.get("average_grade", 0)
        assignment_scores = data.get("assignment_scores", [])
        trend = data.get("trend", "stable")  # improving/stable/declining

        if assignment_scores:
            avg_grade = sum(assignment_scores) / len(assignment_scores)

        score = avg_grade

        # Adjust for trend
        if trend == "declining":
            score *= 0.85
        elif trend == "improving":
            score *= 1.05

        return min(100.0, max(0.0, score))

    def _calculate_attendance_score(self, data):
        """Calculate attendance score"""
        if not data:
            return random.uniform(40.0, 98.0)

        attendance_rate = data.get("attendance_rate", 0)
        consecutive_absences = data.get("consecutive_absences", 0)
        late_arrivals = data.get("late_arrivals", 0)

        score = attendance_rate

        # Penalties
        score -= consecutive_absences * 5
        score -= late_arrivals * 2

        return min(100.0, max(0.0, score))

    def _calculate_sentiment_score(self, data):
        """Calculate sentiment score from text analysis"""
        if not data:
            return random.uniform(-0.3, 0.7)

        # Sentiment score should be -1.0 to 1.0
        sentiment = data.get("sentiment_score", 0.0)
        return max(-1.0, min(1.0, sentiment))

    def _logistic_regression_model(
        self, engagement, performance, attendance, sentiment
    ):
        """
        Logistic regression model for dropout prediction

        P(dropout) = 1 / (1 + e^(-z))
        where z = β0 + β1*x1 + β2*x2 + ... + βn*xn
        """
        # Normalize scores to 0-1 range
        norm_engagement = engagement / 100.0
        norm_performance = performance / 100.0
        norm_attendance = attendance / 100.0
        norm_sentiment = (sentiment + 1.0) / 2.0  # Convert -1,1 to 0,1

        # Model coefficients (weights) - tuned for dropout prediction
        beta_0 = 2.5  # Intercept (baseline dropout tendency)
        beta_engagement = -3.5  # Strong negative effect (high engagement = low dropout)
        beta_performance = -2.8  # Strong negative effect
        beta_attendance = -2.2  # Moderate negative effect
        beta_sentiment = -1.5  # Moderate negative effect

        # Calculate linear combination
        z = (
            beta_0
            + beta_engagement * norm_engagement
            + beta_performance * norm_performance
            + beta_attendance * norm_attendance
            + beta_sentiment * norm_sentiment
        )

        # Apply logistic function
        dropout_prob = 1.0 / (1.0 + math.exp(-z))

        return round(dropout_prob, 4)

    def _calculate_model_confidence(
        self, engagement, performance, attendance, sentiment
    ):
        """Calculate model confidence based on data quality and extremity"""
        # Higher confidence when values are more extreme (clear signals)
        scores = [engagement, performance, attendance, (sentiment + 1) * 50]

        # Calculate variance (more variance = clearer signal = higher confidence)
        mean_score = sum(scores) / len(scores)
        variance = sum((x - mean_score) ** 2 for x in scores) / len(scores)

        # Base confidence
        base_confidence = 75.0

        # Adjust based on variance (0-15 points)
        variance_bonus = min(15.0, variance / 100.0)

        # Adjust based on extremity (0-10 points)
        extremity = sum(1 for s in scores if s < 30 or s > 70) / len(scores)
        extremity_bonus = extremity * 10.0

        confidence = base_confidence + variance_bonus + extremity_bonus

        return round(min(99.0, confidence), 1)

    def _generate_risk_factors(
        self, assessment, engagement, performance, attendance, sentiment
    ):
        """Generate detailed risk factors for the assessment"""
        risk_factors = []

        # Engagement factor
        if engagement < 60:
            severity = (
                "critical"
                if engagement < 30
                else "high" if engagement < 45 else "medium"
            )
            contribution = (100 - engagement) * 0.3
            rf = RiskFactor.objects.create(
                assessment=assessment,
                factor_type="engagement",
                factor_name="Low Engagement",
                description=f"Student engagement score is {engagement:.1f}%, indicating reduced platform activity and participation.",
                weight=0.35,
                contribution=contribution,
                severity=severity,
                current_value=engagement,
                threshold_value=60.0,
                trend="declining" if engagement < 40 else "stable",
            )
            risk_factors.append(rf)

        # Performance factor
        if performance < 65:
            severity = (
                "critical"
                if performance < 40
                else "high" if performance < 50 else "medium"
            )
            contribution = (100 - performance) * 0.28
            rf = RiskFactor.objects.create(
                assessment=assessment,
                factor_type="academic",
                factor_name="Poor Academic Performance",
                description=f"Academic performance score is {performance:.1f}%, below expected standards.",
                weight=0.28,
                contribution=contribution,
                severity=severity,
                current_value=performance,
                threshold_value=65.0,
                trend="declining" if performance < 50 else "stable",
            )
            risk_factors.append(rf)

        # Attendance factor
        if attendance < 75:
            severity = (
                "critical"
                if attendance < 50
                else "high" if attendance < 60 else "medium"
            )
            contribution = (100 - attendance) * 0.22
            rf = RiskFactor.objects.create(
                assessment=assessment,
                factor_type="attendance",
                factor_name="Poor Attendance",
                description=f"Attendance rate is {attendance:.1f}%, below minimum requirement.",
                weight=0.22,
                contribution=contribution,
                severity=severity,
                current_value=attendance,
                threshold_value=75.0,
                trend="declining" if attendance < 60 else "stable",
            )
            risk_factors.append(rf)

        # Sentiment factor
        if sentiment < 0:
            severity = (
                "critical"
                if sentiment < -0.5
                else "high" if sentiment < -0.3 else "medium"
            )
            contribution = abs(sentiment) * 15
            rf = RiskFactor.objects.create(
                assessment=assessment,
                factor_type="sentiment",
                factor_name="Negative Sentiment",
                description=f"Sentiment analysis shows negative emotional state (score: {sentiment:.2f}).",
                weight=0.15,
                contribution=contribution,
                severity=severity,
                current_value=sentiment,
                threshold_value=0.0,
                trend="declining",
            )
            risk_factors.append(rf)

        return risk_factors

    def _generate_sentiment_analyses(self, assessment, sentiment_data):
        """Generate sentiment analysis records"""
        texts = sentiment_data.get("texts", [])

        for text_item in texts[:3]:  # Limit to 3 samples
            text = text_item.get("text", "")
            source = text_item.get("source_type", "email")

            # Mock sentiment calculation
            score = random.uniform(-0.8, 0.5)

            SentimentAnalysis.objects.create(
                assessment=assessment,
                source_type=source,
                text_sample=text[:500],  # Limit text length
                sentiment_score=score,
                confidence=random.uniform(75.0, 95.0),
                frustration_detected=score < -0.4,
                stress_detected=score < -0.3,
                confusion_detected=random.choice([True, False]) if score < 0 else False,
                disengagement_detected=score < -0.5,
                negative_keywords=(
                    ["difficult", "confused", "struggling"] if score < 0 else []
                ),
                risk_indicators=["withdrawal", "frustration"] if score < -0.4 else [],
            )

    def _create_auto_intervention(self, assessment):
        """Automatically create intervention for high-risk students"""
        if assessment.risk_level == "critical":
            priority = "urgent"
            action_type = "phone_call"
            description = f"URGENT: Contact {assessment.student_name} immediately. Critical dropout risk detected."
        else:
            priority = "high"
            action_type = "email_outreach"
            description = f"Reach out to {assessment.student_name} to offer support and assess needs."

        InterventionAction.objects.create(
            assessment=assessment,
            action_type=action_type,
            description=description,
            priority=priority,
            status="planned",
            created_by=assessment.created_by,
        )

        assessment.intervention_assigned = True
        assessment.save()

    @action(detail=False, methods=["get"])
    def alerts_dashboard(self, request):
        """Get dashboard data for risk alerts"""
        # Active alerts
        active_alerts = RiskAssessment.objects.filter(
            alert_triggered=True, alert_acknowledged=False
        ).count()

        # Risk level breakdown
        risk_breakdown = (
            RiskAssessment.objects.values("risk_level")
            .annotate(count=Count("id"))
            .order_by("risk_level")
        )

        # Recent high-risk assessments
        high_risk = RiskAssessment.objects.filter(
            risk_level__in=["high", "critical"]
        ).order_by("-assessment_date")[:10]

        # Average dropout probability
        avg_dropout_prob = (
            RiskAssessment.objects.aggregate(avg=Avg("dropout_probability"))["avg"]
            or 0.0
        )

        return Response(
            {
                "active_alerts": active_alerts,
                "risk_breakdown": list(risk_breakdown),
                "high_risk_students": RiskAssessmentListSerializer(
                    high_risk, many=True
                ).data,
                "average_dropout_probability": round(avg_dropout_prob, 4),
                "total_assessments": RiskAssessment.objects.count(),
            }
        )

    @action(detail=True, methods=["post"])
    def acknowledge_alert(self, request, pk=None):
        """Acknowledge a risk alert"""
        assessment = self.get_object()

        if not assessment.alert_triggered:
            return Response(
                {"error": "No alert triggered for this assessment"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        assessment.alert_acknowledged = True
        assessment.alert_acknowledged_by = request.user
        assessment.alert_acknowledged_at = timezone.now()
        assessment.save()

        return Response({"message": "Alert acknowledged successfully"})


class RiskFactorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RiskFactor.objects.all()
    serializer_class = RiskFactorSerializer


class StudentEngagementMetricViewSet(viewsets.ModelViewSet):
    queryset = StudentEngagementMetric.objects.all()
    serializer_class = StudentEngagementMetricSerializer


class SentimentAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer


class InterventionActionViewSet(viewsets.ModelViewSet):
    queryset = InterventionAction.objects.all()
    serializer_class = InterventionActionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_completed(self, request, pk=None):
        """Mark intervention as completed"""
        intervention = self.get_object()
        intervention.status = "completed"
        intervention.completed_date = timezone.now().date()
        intervention.save()

        return Response({"message": "Intervention marked as completed"})
