from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, StdDev, Count, Q
from datetime import datetime
import random
import statistics

from .models import (
    ModerationSession,
    AssessorDecision,
    OutlierDetection,
    BiasScore,
    ModerationLog,
)
from .serializers import (
    ModerationSessionSerializer,
    AssessorDecisionSerializer,
    OutlierDetectionSerializer,
    BiasScoreSerializer,
    ModerationLogSerializer,
    CompareDecisionsRequestSerializer,
    DetectOutliersRequestSerializer,
    CalculateBiasRequestSerializer,
)


class ModerationSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing moderation sessions and running comparisons.
    """

    queryset = ModerationSession.objects.all()
    serializer_class = ModerationSessionSerializer

    @action(detail=True, methods=["post"])
    def compare_decisions(self, request, pk=None):
        """
        Compare assessor decisions for a specific student or across all submissions.
        """
        session = self.get_object()
        serializer = CompareDecisionsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        student_id = serializer.validated_data.get("student_id")
        submission_id = serializer.validated_data.get("submission_id", "")

        # Get decisions for this student
        decisions_query = session.decisions.filter(student_id=student_id)
        if submission_id:
            decisions_query = decisions_query.filter(submission_id=submission_id)

        decisions = list(decisions_query)

        if len(decisions) < 2:
            return Response(
                {"error": "Need at least 2 decisions to compare"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate comparison metrics
        scores = [d.get_percentage_score() for d in decisions]
        mean_score = statistics.mean(scores)
        std_dev = statistics.stdev(scores) if len(scores) > 1 else 0
        score_range = max(scores) - min(scores)

        # Calculate agreement rate
        agreement_threshold = 10  # 10% difference
        agreements = 0
        total_comparisons = 0

        for i in range(len(scores)):
            for j in range(i + 1, len(scores)):
                total_comparisons += 1
                if abs(scores[i] - scores[j]) <= agreement_threshold:
                    agreements += 1

        agreement_rate = agreements / total_comparisons if total_comparisons > 0 else 0

        # Build comparison data
        comparison_data = {
            "student_id": student_id,
            "submission_id": submission_id,
            "total_decisions": len(decisions),
            "assessors": [
                {
                    "assessor_id": d.assessor_id,
                    "assessor_name": d.assessor_name,
                    "score": d.score,
                    "percentage": d.get_percentage_score(),
                    "grade": d.grade,
                    "deviation_from_mean": d.get_percentage_score() - mean_score,
                }
                for d in decisions
            ],
            "statistics": {
                "mean_score": round(mean_score, 2),
                "std_dev": round(std_dev, 2),
                "score_range": round(score_range, 2),
                "min_score": min(scores),
                "max_score": max(scores),
                "agreement_rate": round(agreement_rate, 2),
            },
            "consistency": (
                "high" if std_dev < 5 else "medium" if std_dev < 10 else "low"
            ),
        }

        # Log comparison
        ModerationLog.objects.create(
            session=session,
            action="comparison_run",
            description=f"Compared {len(decisions)} decisions for student {student_id}",
            decisions_processed=len(decisions),
        )

        return Response(comparison_data)

    @action(detail=True, methods=["post"])
    def detect_outliers(self, request, pk=None):
        """
        Detect outliers in assessor decisions using statistical analysis.
        """
        session = self.get_object()
        serializer = DetectOutliersRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        threshold = serializer.validated_data.get(
            "threshold", session.outlier_threshold
        )
        auto_flag = serializer.validated_data.get("auto_flag", True)

        start_time = datetime.now()

        # Get all decisions
        decisions = list(session.decisions.all())

        if len(decisions) < 3:
            return Response(
                {"error": "Need at least 3 decisions to detect outliers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate cohort statistics
        percentage_scores = [d.get_percentage_score() for d in decisions]
        cohort_mean = statistics.mean(percentage_scores)
        cohort_std_dev = (
            statistics.stdev(percentage_scores) if len(percentage_scores) > 1 else 0
        )

        # Calculate assessor averages
        assessor_stats = {}
        for decision in decisions:
            if decision.assessor_id not in assessor_stats:
                assessor_decisions = [
                    d for d in decisions if d.assessor_id == decision.assessor_id
                ]
                assessor_scores = [d.get_percentage_score() for d in assessor_decisions]
                assessor_stats[decision.assessor_id] = statistics.mean(assessor_scores)

        outliers_detected = []

        # Detect outliers using z-score
        for decision in decisions:
            percentage_score = decision.get_percentage_score()

            if cohort_std_dev == 0:
                z_score = 0
            else:
                z_score = (percentage_score - cohort_mean) / cohort_std_dev

            if abs(z_score) >= threshold:
                # Determine outlier type and severity
                if z_score > 0:
                    outlier_type = "high_scorer"
                else:
                    outlier_type = "low_scorer"

                if abs(z_score) >= 3:
                    severity = "critical"
                elif abs(z_score) >= 2.5:
                    severity = "high"
                elif abs(z_score) >= 2:
                    severity = "medium"
                else:
                    severity = "low"

                deviation_percentage = (
                    ((percentage_score - cohort_mean) / cohort_mean) * 100
                    if cohort_mean > 0
                    else 0
                )

                outlier = OutlierDetection.objects.create(
                    session=session,
                    decision=decision,
                    outlier_type=outlier_type,
                    severity=severity,
                    z_score=z_score,
                    deviation_percentage=deviation_percentage,
                    expected_score=cohort_mean,
                    actual_score=percentage_score,
                    cohort_mean=cohort_mean,
                    cohort_std_dev=cohort_std_dev,
                    assessor_mean=assessor_stats.get(decision.assessor_id, cohort_mean),
                    explanation=f"Score deviates {abs(z_score):.2f} standard deviations from cohort mean. "
                    f"Expected ~{cohort_mean:.1f}%, got {percentage_score:.1f}%.",
                    confidence_score=min(abs(z_score) / 3, 1.0),
                )

                if auto_flag:
                    decision.is_outlier = True
                    decision.requires_review = True
                    decision.save()

                outliers_detected.append(outlier)

        # Update session statistics
        session.outliers_detected = len(outliers_detected)
        session.save()

        # Log detection
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        ModerationLog.objects.create(
            session=session,
            action="outlier_detected",
            description=f"Detected {len(outliers_detected)} outliers using threshold {threshold}",
            decisions_processed=len(decisions),
            outliers_found=len(outliers_detected),
            processing_time_ms=int(processing_time),
        )

        return Response(
            {
                "outliers_detected": len(outliers_detected),
                "total_decisions": len(decisions),
                "detection_rate": (
                    len(outliers_detected) / len(decisions) if decisions else 0
                ),
                "cohort_statistics": {
                    "mean": round(cohort_mean, 2),
                    "std_dev": round(cohort_std_dev, 2),
                },
                "outliers": OutlierDetectionSerializer(
                    outliers_detected, many=True
                ).data,
            }
        )

    @action(detail=True, methods=["post"])
    def calculate_bias(self, request, pk=None):
        """
        Calculate bias scores for assessors.
        """
        session = self.get_object()
        serializer = CalculateBiasRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assessor_id = serializer.validated_data.get("assessor_id", "")
        bias_types = serializer.validated_data.get(
            "bias_types", ["leniency", "severity", "central_tendency"]
        )

        start_time = datetime.now()

        # Get decisions
        if assessor_id:
            assessor_decisions = list(session.decisions.filter(assessor_id=assessor_id))
            if not assessor_decisions:
                return Response(
                    {"error": f"No decisions found for assessor {assessor_id}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            assessors_to_check = [(assessor_id, assessor_decisions[0].assessor_name)]
        else:
            # Check all assessors
            assessor_map = {}
            for decision in session.decisions.all():
                if decision.assessor_id not in assessor_map:
                    assessor_map[decision.assessor_id] = decision.assessor_name
            assessors_to_check = list(assessor_map.items())

        all_decisions = list(session.decisions.all())
        cohort_scores = [d.get_percentage_score() for d in all_decisions]
        cohort_mean = statistics.mean(cohort_scores) if cohort_scores else 0
        cohort_std_dev = (
            statistics.stdev(cohort_scores) if len(cohort_scores) > 1 else 0
        )

        bias_scores = []

        for assessor_id, assessor_name in assessors_to_check:
            assessor_decisions = [
                d for d in all_decisions if d.assessor_id == assessor_id
            ]

            if len(assessor_decisions) < 3:
                continue

            assessor_scores = [d.get_percentage_score() for d in assessor_decisions]
            assessor_mean = statistics.mean(assessor_scores)
            assessor_std_dev = (
                statistics.stdev(assessor_scores) if len(assessor_scores) > 1 else 0
            )

            mean_difference = assessor_mean - cohort_mean
            std_dev_ratio = (
                assessor_std_dev / cohort_std_dev if cohort_std_dev > 0 else 1.0
            )

            for bias_type in bias_types:
                bias_score_value = 0.0
                evidence = {}
                recommendation = ""
                severity = 5

                if bias_type == "leniency":
                    # Leniency bias: consistently scoring higher than cohort
                    if mean_difference > 5:
                        bias_score_value = min(mean_difference / 20, 1.0)
                        evidence = {
                            "mean_difference": round(mean_difference, 2),
                            "assessor_mean": round(assessor_mean, 2),
                            "cohort_mean": round(cohort_mean, 2),
                            "pattern": "Consistently awards higher scores than peers",
                        }
                        severity = int(min(mean_difference / 2, 10))
                        recommendation = f"Review marking criteria application. Consider standardization training. Mean difference: {mean_difference:.1f}%"

                elif bias_type == "severity":
                    # Severity bias: consistently scoring lower than cohort
                    if mean_difference < -5:
                        bias_score_value = min(abs(mean_difference) / 20, 1.0)
                        evidence = {
                            "mean_difference": round(mean_difference, 2),
                            "assessor_mean": round(assessor_mean, 2),
                            "cohort_mean": round(cohort_mean, 2),
                            "pattern": "Consistently awards lower scores than peers",
                        }
                        severity = int(min(abs(mean_difference) / 2, 10))
                        recommendation = f"Review marking standards. Consider recalibration session. Mean difference: {mean_difference:.1f}%"

                elif bias_type == "central_tendency":
                    # Central tendency bias: avoiding extremes
                    if std_dev_ratio < 0.7:
                        bias_score_value = (0.7 - std_dev_ratio) / 0.7
                        evidence = {
                            "std_dev_ratio": round(std_dev_ratio, 2),
                            "assessor_std_dev": round(assessor_std_dev, 2),
                            "cohort_std_dev": round(cohort_std_dev, 2),
                            "pattern": "Scores cluster around the middle, avoiding extremes",
                        }
                        severity = int((0.7 - std_dev_ratio) * 14)
                        recommendation = "Encourage use of full marking scale. Review high/low exemplars."

                # Only create bias score if significant
                if bias_score_value > 0.15:
                    affected_student_ids = [d.student_id for d in assessor_decisions]

                    bias_obj = BiasScore.objects.create(
                        session=session,
                        assessor_id=assessor_id,
                        assessor_name=assessor_name,
                        bias_type=bias_type,
                        bias_score=bias_score_value,
                        sample_size=len(assessor_decisions),
                        mean_difference=mean_difference,
                        std_dev_ratio=std_dev_ratio,
                        evidence=evidence,
                        affected_students=affected_student_ids,
                        recommendation=recommendation,
                        severity_level=severity,
                    )
                    bias_scores.append(bias_obj)

                    # Flag decisions
                    for decision in assessor_decisions:
                        decision.has_bias_flag = True
                        decision.save()

        # Update session
        session.bias_flags_raised = len(bias_scores)
        session.save()

        # Log calculation
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        ModerationLog.objects.create(
            session=session,
            action="bias_calculated",
            description=f"Calculated bias scores for {len(assessors_to_check)} assessors",
            decisions_processed=len(all_decisions),
            bias_flags=len(bias_scores),
            processing_time_ms=int(processing_time),
        )

        return Response(
            {
                "bias_scores_created": len(bias_scores),
                "assessors_analyzed": len(assessors_to_check),
                "bias_scores": BiasScoreSerializer(bias_scores, many=True).data,
            }
        )


class AssessorDecisionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing individual assessor decisions.
    """

    queryset = AssessorDecision.objects.all()
    serializer_class = AssessorDecisionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        session_id = self.request.query_params.get("session_id")
        if session_id:
            queryset = queryset.filter(session_id=session_id)
        return queryset


class OutlierDetectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing outlier detections.
    """

    queryset = OutlierDetection.objects.all()
    serializer_class = OutlierDetectionSerializer

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        """Mark an outlier as resolved."""
        outlier = self.get_object()
        outlier.is_resolved = True
        outlier.resolution_notes = request.data.get("notes", "")
        outlier.resolved_by = request.data.get("resolved_by", "system")
        outlier.resolved_at = datetime.now()
        outlier.save()

        return Response(OutlierDetectionSerializer(outlier).data)


class BiasScoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bias scores.
    """

    queryset = BiasScore.objects.all()
    serializer_class = BiasScoreSerializer

    @action(detail=True, methods=["post"])
    def validate(self, request, pk=None):
        """Validate a bias score."""
        bias_score = self.get_object()
        bias_score.is_validated = True
        bias_score.validation_notes = request.data.get("notes", "")
        bias_score.validated_by = request.data.get("validated_by", "system")
        bias_score.validated_at = datetime.now()
        bias_score.save()

        return Response(BiasScoreSerializer(bias_score).data)


class ModerationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing moderation logs (read-only).
    """

    queryset = ModerationLog.objects.all()
    serializer_class = ModerationLogSerializer
