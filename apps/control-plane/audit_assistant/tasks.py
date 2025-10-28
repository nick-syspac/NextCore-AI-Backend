"""Celery tasks for the Audit Assistant evidence pipeline."""
from __future__ import annotations

import logging
from typing import TypedDict

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import Evidence
from .services import auto_tag_clauses, detect_ner_entities, extract_text_from_file

logger = logging.getLogger(__name__)


class EvidenceProcessingResult(TypedDict):
    evidence_id: int
    status: str
    auto_tag_enabled: bool
    ner_entities_found: int
    auto_tagged_clauses: int
    message: str


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True, max_retries=3)
def process_evidence_document(self, evidence_id: int, auto_tag: bool = True) -> EvidenceProcessingResult:
    """Extract text, run NER, and optionally auto-tag clauses for an evidence document."""
    try:
        evidence = Evidence.objects.select_related("tenant").get(pk=evidence_id)
    except Evidence.DoesNotExist:
        logger.warning("Evidence %s no longer exists", evidence_id)
        return EvidenceProcessingResult(
            evidence_id=evidence_id,
            status="missing",
            auto_tag_enabled=auto_tag,
            ner_entities_found=0,
            auto_tagged_clauses=0,
            message="Evidence not found; skipping processing.",
        )

    logger.info(
        "Starting evidence processing",
        extra={"evidence_id": evidence_id, "auto_tag": auto_tag, "tenant_id": evidence.tenant_id},
    )

    with transaction.atomic():
        update_fields = ["status"]
        evidence.status = "processing"

        if evidence.file and not evidence.file_size:
            try:
                evidence.file_size = evidence.file.size
                update_fields.append("file_size")
            except Exception:  # pragma: no cover - storage backends may raise custom errors
                logger.debug("Unable to determine file size for evidence %s", evidence_id)

        evidence.save(update_fields=update_fields)

    extracted_text = extract_text_from_file(evidence)

    if not extracted_text:
        logger.warning("No extractable text for evidence %s", evidence_id)
        evidence.extracted_text = ""
        evidence.ner_entities = []
        evidence.ner_processed_at = None
        evidence.status = "uploaded"
        evidence.save(update_fields=["extracted_text", "ner_entities", "ner_processed_at", "status"])
        return EvidenceProcessingResult(
            evidence_id=evidence.id,
            status=evidence.status,
            auto_tag_enabled=auto_tag,
            ner_entities_found=0,
            auto_tagged_clauses=0,
            message="No text extracted; skipping NER and auto-tagging.",
        )

    ner_entities = detect_ner_entities(extracted_text)
    auto_tagged_count = auto_tag_clauses(evidence, extracted_text, ner_entities) if auto_tag else 0

    with transaction.atomic():
        evidence.refresh_from_db()
        evidence.extracted_text = extracted_text
        evidence.ner_entities = ner_entities
        evidence.ner_processed_at = timezone.now()
        evidence.status = "tagged" if auto_tag and auto_tagged_count > 0 else "uploaded"
        evidence.save(
            update_fields=[
                "extracted_text",
                "ner_entities",
                "ner_processed_at",
                "status",
            ]
        )

    logger.info(
        "Evidence processing finished",
        extra={
            "evidence_id": evidence_id,
            "entity_count": len(ner_entities),
            "auto_tagged": auto_tagged_count,
            "status": evidence.status,
        },
    )

    message = (
        f"Extracted text length: {len(extracted_text)} characters. "
        f"Detected {len(ner_entities)} entities."
    )
    if auto_tag:
        message += f" Auto-tagged {auto_tagged_count} clause mappings."

    return EvidenceProcessingResult(
        evidence_id=evidence.id,
        status=evidence.status,
        auto_tag_enabled=auto_tag,
        ner_entities_found=len(ner_entities),
        auto_tagged_clauses=auto_tagged_count,
        message=message,
    )
