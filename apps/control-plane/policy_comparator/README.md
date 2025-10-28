# Policy Comparator - README

## Overview

The Policy Comparator is an NLP-powered tool that automatically compares RTO policies against ASQA standards to identify compliance coverage and gaps.

## Current Status: **FOUNDATION PHASE**

### What's Implemented

✅ **Core Data Models**
- ASQAStandard - ASQA standards repository  
- ASQAClause - Individual clauses with keywords
- Policy - Organization policy documents
- ComparisonResult - NLP similarity results
- ComparisonSession - Batch comparison tracking

✅ **Basic Functionality**
- Manual policy text entry
- Text similarity comparison (0-1 score)
- Gap detection based on thresholds
- Compliance scoring

### Architecture (Current)

```
User Upload Policy Text
         ↓
Store in Database
         ↓
Compare vs ASQA Clauses
         ↓
Compute Similarity Scores
         ↓
Generate Gap Reports
```

## Roadmap to Full HLD Implementation

### Phase 1: Enhanced Models (Next)
- [ ] Document model with file upload support
- [ ] DocumentVersion for version tracking
- [ ] DocumentChunk for text segmentation
- [ ] Embedding storage with pgvector
- [ ] ComparisonJob for async processing

### Phase 2: File Processing
- [ ] PDF text extraction (PyPDF2/pdfminer)
- [ ] DOCX parsing (python-docx)
- [ ] HTML processing
- [ ] Text chunking strategy
- [ ] S3 file storage integration

### Phase 3: NLP Enhancement  
- [ ] Sentence transformers for embeddings
- [ ] Vector similarity search (pgvector)
- [ ] Cross-encoder re-ranking
- [ ] Keyword extraction
- [ ] Evidence linking

### Phase 4: Async Processing
- [ ] Celery task queues
- [ ] Background job processing
- [ ] Progress tracking
- [ ] Email notifications

### Phase 5: Advanced UI
- [ ] Coverage heatmap visualization
- [ ] Interactive gap cards
- [ ] Evidence viewer (side-by-side)
- [ ] PDF report generation
- [ ] Threshold controls

## Quick Start (Current Version)

### 1. Seed ASQA Standards

```python
python manage.py shell
from policy_comparator.models import ASQAStandard, ASQAClause

# Create a standard
standard = ASQAStandard.objects.create(
    standard_number="1.1",
    title="Training and Assessment",
    description="The RTO's training and assessment strategies...",
    standard_type="training_assessment",
    full_text="[Full standard text]",
    requirements=["Requirement 1", "Requirement 2"]
)

# Create clauses
ASQAClause.objects.create(
    standard=standard,
    clause_number="1",
    title="Training and assessment",
    clause_text="Training and assessment is delivered by trainers and assessors who...",
    keywords=["trainers", "assessors", "qualifications", "competency"],
    compliance_level="critical"
)
```

### 2. Create a Policy

```python
from policy_comparator.models import Policy
from tenants.models import Tenant

tenant = Tenant.objects.first()
policy = Policy.objects.create(
    tenant=tenant,
    policy_number="POL-001",
    title="Trainer and Assessor Policy",
    policy_type="training_delivery",
    content="[Full policy text]",
    status="approved"
)
```

### 3. Run Comparison (via API or admin)

The comparison will compute similarity scores and flag gaps automatically.

## API Endpoints (Current)

- `GET /api/policy-comparator/standards/` - List ASQA standards
- `GET /api/policy-comparator/policies/` - List policies
- `POST /api/policy-comparator/compare/` - Run comparison
- `GET /api/policy-comparator/results/` - View results

## Database Schema

### Core Tables
- `asqa_standards` - ASQA standard library
- `asqa_clauses` - Individual compliance clauses
- `policies` - RTO policy documents
- `comparison_results` - Clause-by-clause scores
- `comparison_sessions` - Batch comparison metadata

## Configuration

### Similarity Thresholds (in settings.py)

```python
POLICY_COMPARATOR = {
    'THRESHOLD_FULL_MATCH': 0.8,      # 80%+ = compliant
    'THRESHOLD_PARTIAL_MATCH': 0.6,    # 60-80% = partial
    'THRESHOLD_WEAK_MATCH': 0.4,       # 40-60% = weak
    # Below 40% = gap
}
```

## Future Enhancements

### High Priority
1. **File Upload** - PDF/DOCX support instead of text paste
2. **Embeddings** - Semantic search with transformers
3. **Async Jobs** - Celery for background processing
4. **Rich UI** - Heatmaps and interactive dashboards

### Medium Priority
5. **Versioning** - Track policy changes over time
6. **Evidence Linking** - Show exact text matches
7. **Custom Clause Packs** - Tenant-specific standards
8. **Scheduled Scans** - Automatic periodic checks

### Low Priority  
9. **LLM Summarization** - AI-generated gap explanations
10. **Multi-language** - Support non-English policies
11. **Integration** - Webhooks for policy updates
12. **Advanced Analytics** - Compliance trends over time

## Contributing

When enhancing the Policy Comparator:

1. Start with model changes and migrations
2. Add business logic in `services/` directory
3. Create DRF serializers and views
4. Build frontend components in Next.js
5. Add tests for each layer

## Support

For questions or issues with Policy Comparator:
- Check `/docs/policy-comparator/` for detailed guides
- Review IMPLEMENTATION_PLAN.md for roadmap
- Contact: platform-team@nextcore.ai

---

**Version**: 0.1.0 (Foundation)  
**Last Updated**: October 28, 2025
