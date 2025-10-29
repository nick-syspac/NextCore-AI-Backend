"""
Celery tasks for Continuous Improvement Register AI processing.
Handles classification, summarization, clause linking, and compliance scoring.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, TypedDict

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import ImprovementAction
from .models_cir import AIRun, ClauseLink, Embedding, KPISnapshot
from policy_comparator.models import ASQAClause

logger = logging.getLogger(__name__)


class ClassificationResult(TypedDict):
    labels: List[Dict[str, Any]]
    risk_rating: str
    confidence: float
    processing_time_ms: int


class SummarizationResult(TypedDict):
    summary: str
    key_points: List[str]
    processing_time_ms: int


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def classify_improvement_action(
    self,
    action_id: int,
    *,
    auto_link_clauses: bool = True
) -> ClassificationResult:
    """
    Classify an improvement action using AI.
    
    Performs:
    - Category classification
    - Risk rating assessment
    - Keyword extraction
    - Standard/clause identification (if auto_link_clauses=True)
    
    Args:
        action_id: Primary key of the ImprovementAction
        auto_link_clauses: Whether to automatically create clause links
    
    Returns:
        Classification result with labels, risk rating, and confidence
    """
    start_time = time.time()
    
    try:
        action = ImprovementAction.objects.select_related('tenant', 'category').get(pk=action_id)
    except ImprovementAction.DoesNotExist:
        logger.error("ImprovementAction %s not found", action_id)
        raise
    
    logger.info(
        "Starting AI classification",
        extra={"action_id": action_id, "tenant_id": action.tenant_id}
    )
    
    # TODO: Integrate with actual AI service/model
    # For now, using rule-based placeholder logic
    
    # Combine text for analysis
    combined_text = f"{action.title} {action.description} {action.root_cause}"
    text_lower = combined_text.lower()
    
    # Simple keyword-based classification (placeholder for real AI)
    labels = []
    risk_rating = 'medium'
    confidence = 0.75
    
    # Category classification
    if any(word in text_lower for word in ['training', 'assessment', 'delivery']):
        labels.append({'type': 'training_assessment', 'confidence': 0.85})
    if any(word in text_lower for word in ['complaint', 'issue', 'problem']):
        labels.append({'type': 'complaint', 'confidence': 0.80})
        risk_rating = 'high'
    if any(word in text_lower for word in ['qualification', 'competency', 'skill']):
        labels.append({'type': 'trainer_qualifications', 'confidence': 0.75})
    
    # Risk assessment
    if any(word in text_lower for word in ['critical', 'urgent', 'severe', 'registration', 'compliance']):
        risk_rating = 'critical'
        confidence = 0.90
    elif any(word in text_lower for word in ['minor', 'low', 'suggestion']):
        risk_rating = 'low'
    
    # Extract keywords (simple version)
    keywords = _extract_keywords(combined_text)
    
    # Identify related standards (placeholder)
    related_standards = _identify_standards(text_lower)
    
    # Update the action with AI results
    with transaction.atomic():
        action.refresh_from_db()
        action.ai_classified_category = labels[0]['type'] if labels else 'other'
        action.ai_classification_confidence = confidence
        action.ai_keywords = keywords
        action.ai_related_standards = related_standards
        action.ai_processed_at = timezone.now()
        action.save(update_fields=[
            'ai_classified_category',
            'ai_classification_confidence',
            'ai_keywords',
            'ai_related_standards',
            'ai_processed_at'
        ])
    
    # Auto-link clauses if requested
    if auto_link_clauses and related_standards:
        linked_count = _auto_link_clauses(action, related_standards, text_lower)
        logger.info(
            "Auto-linked clauses",
            extra={"action_id": action_id, "linked_count": linked_count}
        )
    
    # Log AI run
    processing_time_ms = int((time.time() - start_time) * 1000)
    AIRun.objects.create(
        tenant=action.tenant,
        target_entity='improvement_action',
        target_id=action_id,
        task_type='classify',
        input_ref=combined_text[:500],
        output_json={
            'labels': labels,
            'risk_rating': risk_rating,
            'keywords': keywords,
            'standards': related_standards
        },
        success=True,
        tokens_used=len(combined_text.split()),  # Placeholder
        latency_ms=processing_time_ms,
        model_name='placeholder-classifier',
        model_version='1.0'
    )
    
    logger.info(
        "Classification complete",
        extra={
            "action_id": action_id,
            "labels_count": len(labels),
            "risk_rating": risk_rating,
            "processing_time_ms": processing_time_ms
        }
    )
    
    return ClassificationResult(
        labels=labels,
        risk_rating=risk_rating,
        confidence=confidence,
        processing_time_ms=processing_time_ms
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def summarize_improvement_action(
    self,
    action_id: int,
    *,
    max_length: int = 80,
    style: str = 'action-oriented'
) -> SummarizationResult:
    """
    Generate a concise AI summary of an improvement action.
    
    Args:
        action_id: Primary key of the ImprovementAction
        max_length: Maximum summary length in words
        style: Summary style (concise, detailed, action-oriented)
    
    Returns:
        Summary text and key points
    """
    start_time = time.time()
    
    try:
        action = ImprovementAction.objects.select_related('tenant').get(pk=action_id)
    except ImprovementAction.DoesNotExist:
        logger.error("ImprovementAction %s not found", action_id)
        raise
    
    logger.info(
        "Starting AI summarization",
        extra={"action_id": action_id, "style": style}
    )
    
    # TODO: Integrate with actual AI summarization service
    # Placeholder: rule-based summary generation
    
    # Extract key information
    description_words = action.description.split()[:50]
    truncated_desc = ' '.join(description_words)
    
    # Generate summary based on style
    if style == 'concise':
        summary = f"{action.title}. {truncated_desc[:100]}..."
    elif style == 'detailed':
        summary = f"""
{action.title}
Source: {action.get_source_display()}
Priority: {action.get_priority_display()}
Description: {truncated_desc}
Root Cause: {action.root_cause[:100] if action.root_cause else 'Not specified'}
        """.strip()
    else:  # action-oriented
        summary = f"{action.title}. Action required: {truncated_desc[:80]}..."
    
    # Extract key points (placeholder)
    key_points = [
        f"Priority: {action.get_priority_display()}",
        f"Source: {action.get_source_display()}",
        f"Target completion: {action.target_completion_date or 'Not set'}"
    ]
    
    if action.responsible_person:
        key_points.append(f"Assigned to: {action.responsible_person.get_full_name()}")
    
    # Ensure summary fits max_length
    words = summary.split()
    if len(words) > max_length:
        summary = ' '.join(words[:max_length]) + '...'
    
    # Update action with AI summary
    with transaction.atomic():
        action.refresh_from_db()
        action.ai_summary = summary
        action.save(update_fields=['ai_summary'])
    
    # Log AI run
    processing_time_ms = int((time.time() - start_time) * 1000)
    AIRun.objects.create(
        tenant=action.tenant,
        target_entity='improvement_action',
        target_id=action_id,
        task_type='summarize',
        input_ref=action.description[:500],
        output_json={
            'summary': summary,
            'key_points': key_points,
            'style': style
        },
        success=True,
        tokens_used=len(action.description.split()),
        latency_ms=processing_time_ms,
        model_name='placeholder-summarizer',
        model_version='1.0'
    )
    
    logger.info(
        "Summarization complete",
        extra={"action_id": action_id, "processing_time_ms": processing_time_ms}
    )
    
    return SummarizationResult(
        summary=summary,
        key_points=key_points,
        processing_time_ms=processing_time_ms
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def compute_kpi_snapshots(
    self,
    tenant_id: int,
    period: str = 'monthly',
    period_start: str = None,
    period_end: str = None
) -> Dict[str, Any]:
    """
    Compute and store KPI snapshots for a tenant.
    
    Metrics computed:
    - Total actions by status
    - Completion rate
    - Average time to close
    - SLA compliance rate
    - Risk distribution
    - Clause coverage
    
    Args:
        tenant_id: Tenant primary key
        period: Period type (daily, weekly, monthly, quarterly, annual)
        period_start: ISO date string for period start
        period_end: ISO date string for period end
    
    Returns:
        Dictionary of computed metrics
    """
    from datetime import datetime, date
    from django.db.models import Avg, Count, Q, F
    from decimal import Decimal
    
    # Parse dates
    if not period_start or not period_end:
        # Default to current month
        today = date.today()
        period_start = today.replace(day=1)
        period_end = today
    else:
        period_start = datetime.fromisoformat(period_start).date()
        period_end = datetime.fromisoformat(period_end).date()
    
    logger.info(
        "Computing KPI snapshots",
        extra={
            "tenant_id": tenant_id,
            "period": period,
            "period_start": period_start,
            "period_end": period_end
        }
    )
    
    # Query actions in period
    actions = ImprovementAction.objects.filter(
        tenant_id=tenant_id,
        created_at__date__gte=period_start,
        created_at__date__lte=period_end
    )
    
    total_actions = actions.count()
    
    # Completion metrics
    completed_actions = actions.filter(status='completed')
    completion_rate = Decimal(
        (completed_actions.count() / total_actions * 100) if total_actions > 0 else 0
    )
    
    # Average time to close
    avg_days_to_close = completed_actions.filter(
        actual_completion_date__isnull=False
    ).annotate(
        days_to_close=F('actual_completion_date') - F('identified_date')
    ).aggregate(avg=Avg('days_to_close'))['avg']
    
    avg_days_value = Decimal(
        str(avg_days_to_close.days) if avg_days_to_close else 0
    )
    
    # SLA compliance
    overdue_count = actions.filter(compliance_status='overdue').count()
    sla_compliance_rate = Decimal(
        ((total_actions - overdue_count) / total_actions * 100) if total_actions > 0 else 100
    )
    
    # Risk distribution
    risk_dist = actions.values('priority').annotate(count=Count('id'))
    
    # Store snapshots
    metrics = {
        'total_actions': (total_actions, 'count'),
        'completion_rate': (completion_rate, '%'),
        'avg_days_to_close': (avg_days_value, 'days'),
        'sla_compliance_rate': (sla_compliance_rate, '%'),
        'overdue_count': (overdue_count, 'count'),
    }
    
    snapshots_created = []
    for metric_key, (metric_value, metric_unit) in metrics.items():
        snapshot = KPISnapshot.objects.create(
            tenant_id=tenant_id,
            period=period,
            period_start=period_start,
            period_end=period_end,
            metric_key=metric_key,
            metric_value=metric_value,
            metric_unit=metric_unit,
            metadata={'risk_distribution': list(risk_dist)}
        )
        snapshots_created.append(snapshot.id)
    
    logger.info(
        "KPI snapshots computed",
        extra={
            "tenant_id": tenant_id,
            "snapshots_created": len(snapshots_created),
            "total_actions": total_actions
        }
    )
    
    return {
        'snapshots_created': snapshots_created,
        'metrics': {k: str(v[0]) for k, v in metrics.items()},
        'period_start': str(period_start),
        'period_end': str(period_end)
    }


# Helper functions

def _extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract key terms from text (placeholder for NLP extraction)"""
    # Simple frequency-based extraction
    words = text.lower().split()
    # Filter common words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been'
    }
    keywords = [w for w in words if len(w) > 4 and w not in stop_words]
    
    # Return unique keywords (most common first)
    from collections import Counter
    return [word for word, _ in Counter(keywords).most_common(max_keywords)]


def _identify_standards(text_lower: str) -> List[str]:
    """Identify ASQA standard references in text"""
    import re
    
    standards = []
    
    # Pattern matching for "Standard 1", "SNR 1.5", etc.
    patterns = [
        r'\bstandard\s+(\d+(?:\.\d+)?)\b',
        r'\bsnr\s+(\d+(?:\.\d+)?)\b',
        r'\bstd\.?\s+(\d+(?:\.\d+)?)\b'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text_lower)
        for match in matches:
            standard_ref = match.group(1)
            if standard_ref not in standards:
                standards.append(standard_ref)
    
    return standards[:5]  # Limit to top 5


def _auto_link_clauses(
    action: ImprovementAction,
    standard_refs: List[str],
    text_lower: str
) -> int:
    """
    Automatically create clause links based on standard references and keywords.
    
    Returns:
        Number of clause links created
    """
    linked_count = 0
    
    # Find relevant clauses
    clauses = ASQAClause.objects.filter(
        standard__standard_number__in=standard_refs
    ).select_related('standard')
    
    for clause in clauses:
        # Calculate confidence based on keyword matches
        clause_keywords = clause.keywords or []
        matches = sum(1 for kw in clause_keywords if kw.lower() in text_lower)
        
        if matches == 0:
            continue
        
        confidence = min(0.5 + (matches * 0.1), 0.95)
        
        # Create link if confidence threshold met
        if confidence >= 0.5:
            ClauseLink.objects.get_or_create(
                improvement_action=action,
                clause=clause,
                defaults={
                    'source': 'ai',
                    'confidence': confidence,
                    'rationale': f'Auto-linked based on {matches} keyword matches',
                    'created_by_id': None  # System-generated
                }
            )
            linked_count += 1
    
    return linked_count
