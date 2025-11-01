"""Service helpers for processing audit evidence and auto-tagging."""

from __future__ import annotations

import logging
import os
from typing import Iterable, List, Tuple

from django.utils import timezone

from policy_comparator.models import ASQAClause

from .models import ClauseEvidence, Evidence

logger = logging.getLogger(__name__)


def extract_text_from_file(evidence: Evidence) -> str:
    """Attempt to extract raw text from the evidence file."""
    file_field = evidence.file
    if not file_field:
        logger.debug("Evidence %s has no file attached", evidence.id)
        return ""

    extension = os.path.splitext(file_field.name)[1].lower().lstrip(".")

    try:
        file_field.open("rb")
    except FileNotFoundError:
        logger.warning("File for evidence %s could not be opened", evidence.id)
        return ""

    try:
        if extension == "txt":
            buffer = file_field.read()
            try:
                return buffer.decode("utf-8")
            except UnicodeDecodeError:
                return buffer.decode("latin-1", errors="ignore")

        # Placeholder behaviour for binary formats until full extraction pipeline is wired in.
        return f"[TODO] Extracted text for {os.path.basename(file_field.name)}"
    finally:
        try:
            file_field.close()
        except Exception:  # pragma: no cover - defensive close only
            logger.debug("Failed to close file handle for evidence %s", evidence.id)


def detect_ner_entities(text: str) -> List[dict]:
    """Identify simple entity matches using lightweight regex heuristics."""
    import re

    entities: List[dict] = []

    # Standards (e.g. "Standard 1.8")
    standard_pattern = r"\b(?:Standard|SNR|Std\.?)\s+(\d+(?:\.\d+)?)\b"
    for match in re.finditer(standard_pattern, text, re.IGNORECASE):
        entities.append(
            {
                "entity": match.group(0),
                "type": "STANDARD",
                "start": match.start(),
                "end": match.end(),
                "value": match.group(1),
            }
        )

    # Clauses (e.g. "Clause 1.8.1")
    clause_pattern = r"\b(?:Clause\s+)?(\d+\.\d+(?:\.\d+)?)\b"
    for match in re.finditer(clause_pattern, text):
        entities.append(
            {
                "entity": match.group(0),
                "type": "CLAUSE",
                "start": match.start(),
                "end": match.end(),
                "value": match.group(1),
            }
        )

    # Dates (01/01/2024, January 2024 etc.)
    date_patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
    ]
    for pattern in date_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            entities.append(
                {
                    "entity": match.group(0),
                    "type": "DATE",
                    "start": match.start(),
                    "end": match.end(),
                }
            )

    # Qualifications (e.g. TAE40116)
    qual_pattern = r"\b[A-Z]{3}\d{5}\b"
    for match in re.finditer(qual_pattern, text):
        entities.append(
            {
                "entity": match.group(0),
                "type": "QUALIFICATION",
                "start": match.start(),
                "end": match.end(),
            }
        )

    # Common ORG keywords
    org_keywords = ["ASQA", "RTO", "Training Organisation", "VET", "AQF", "TGA"]
    for keyword in org_keywords:
        for match in re.finditer(
            r"\b" + re.escape(keyword) + r"\b", text, re.IGNORECASE
        ):
            entities.append(
                {
                    "entity": match.group(0),
                    "type": "ORG",
                    "start": match.start(),
                    "end": match.end(),
                }
            )

    # Policy references
    policy_pattern = r"\b(?:Policy|Procedure)\s+([A-Z0-9-]+)\b"
    for match in re.finditer(policy_pattern, text, re.IGNORECASE):
        entities.append(
            {
                "entity": match.group(0),
                "type": "POLICY",
                "start": match.start(),
                "end": match.end(),
                "value": match.group(1),
            }
        )

    # Remove duplicates while preserving order
    seen: set[Tuple[str, str, int]] = set()
    unique_entities: List[dict] = []
    for entity in entities:
        key = (entity["entity"], entity["type"], entity["start"])
        if key in seen:
            continue
        unique_entities.append(entity)
        seen.add(key)

    return unique_entities


def _cleanup_previous_mappings(evidence: Evidence) -> None:
    """Remove stale auto-generated mappings before reprocessing."""
    ClauseEvidence.objects.filter(
        evidence=evidence,
        mapping_type__in=["auto_ner", "auto_rule", "suggested"],
    ).delete()


def auto_tag_clauses(
    evidence: Evidence, text: str, ner_entities: Iterable[dict]
) -> int:
    """Create clause evidence relationships using lightweight heuristics."""
    if not text:
        return 0

    entities_list = list(ner_entities)
    entities_count = len(entities_list)
    text_lower = text.lower()
    standard_refs = [
        e.get("value") for e in entities_list if e.get("type") == "STANDARD"
    ]
    clause_refs = [e.get("value") for e in entities_list if e.get("type") == "CLAUSE"]

    _cleanup_previous_mappings(evidence)

    all_clauses = ASQAClause.objects.select_related("standard").all()

    created = 0
    for clause in all_clauses:
        clause_num = clause.clause_number
        mapping_type = None
        confidence_score = 0.0
        matched_entities: List[dict] = []
        matched_keywords: List[str] = []
        rule_name = None

        if clause_num and (
            clause_num in clause_refs or f"clause {clause_num}" in text_lower
        ):
            mapping_type = "auto_rule"
            confidence_score = 0.95
            rule_name = "direct_clause_reference"
            matched_entities = [
                e for e in entities_list if e.get("value") == clause_num
            ]

        if not mapping_type:
            standard_num = clause.standard.standard_number if clause.standard else None
            if standard_num and (
                standard_num in standard_refs
                or f"standard {standard_num}" in text_lower
            ):
                clause_keywords = clause.keywords or []
                keywords_found = [
                    kw for kw in clause_keywords if kw.lower() in text_lower
                ]
                if len(keywords_found) >= 2:
                    mapping_type = "auto_ner"
                    confidence_score = min(0.7 + (len(keywords_found) * 0.05), 0.9)
                    rule_name = "standard_reference_with_keywords"
                    matched_keywords = keywords_found
                    matched_entities = [
                        e for e in entities_list if e.get("value") == standard_num
                    ]

        if not mapping_type:
            clause_keywords = clause.keywords or []
            if clause_keywords:
                keywords_found = [
                    kw for kw in clause_keywords if kw.lower() in text_lower
                ]
                keyword_ratio = len(keywords_found) / len(clause_keywords)
                if keyword_ratio >= 0.6:
                    mapping_type = "auto_rule"
                    confidence_score = min(0.5 + (keyword_ratio * 0.3), 0.8)
                    rule_name = "high_keyword_density"
                    matched_keywords = keywords_found

        if not mapping_type and clause.title:
            title_words = {w for w in clause.title.lower().split() if len(w) > 3}
            if title_words:
                title_matches = [w for w in title_words if w in text_lower]
                title_ratio = len(title_matches) / len(title_words)
                if title_ratio >= 0.5:
                    mapping_type = "suggested"
                    confidence_score = min(0.4 + (title_ratio * 0.2), 0.6)
                    rule_name = "title_similarity"
                    matched_keywords = title_matches

        if not mapping_type or confidence_score < 0.4:
            continue

        ClauseEvidence.objects.create(
            asqa_clause=clause,
            evidence=evidence,
            mapping_type=mapping_type,
            confidence_score=confidence_score,
            matched_entities=matched_entities,
            matched_keywords=matched_keywords,
            rule_name=rule_name or "auto_tag_pipeline",
            rule_metadata={
                "processed_at": timezone.now().isoformat(),
                "text_length": len(text),
                "entity_count": entities_count,
            },
        )
        created += 1

    logger.info(
        "Auto-tagging complete", extra={"evidence_id": evidence.id, "clauses": created}
    )
    return created
