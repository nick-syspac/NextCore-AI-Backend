# Policy Comparator Implementation Plan

## Status: **IN PROGRESS**

Based on the High-Level Design, this document tracks the implementation of the Policy Comparator feature.

## Phase 1: Data Models ✅ (Partial - Existing Structure)

### Existing Models
- ✅ `ASQAStandard` - ASQA standards repository
- ✅ `ASQAClause` - Individual clauses with compliance levels
- ✅ `Policy` - Organization policies
- ✅ `ComparisonResult` - NLP comparison results
- ✅ `ComparisonSession` - Batch comparison tracking

### New Models Required
- ⏳ `Document` - Multi-format document uploads with S3 storage
- ⏳ `DocumentVersion` - Version history
- ⏳ `DocumentChunk` - Text chunks for embedding
- ⏳ `AsqaClausePack` - Versioned clause collections
- ⏳ `Embedding` - Vector embeddings (pgvector)
- ⏳ `ComparisonJob` - Async job tracking
- ⏳ `ComparisonScore` - Per-clause scores
- ⏳ `Finding` - Gap/coverage findings
- ⏳ `Report` - Generated reports

## Phase 2: NLP & Embeddings Infrastructure

### Dependencies to Install
```bash
# Vector database
pgvector>=0.2.0

# Text extraction
PyPDF2>=3.0.0
pdfminer.six>=20221105
python-docx>=0.8.11
beautifulsoup4>=4.12.0
html2text>=2020.1.16

# NLP & Embeddings
sentence-transformers>=2.2.2
transformers>=4.30.0
torch>=2.0.0

# OCR (optional)
pytesseract>=0.3.10

# Celery for async tasks
celery>=5.3.0
redis>=4.5.0
```

### NLP Utilities
- Text extraction pipeline (PDF/DOCX/HTML)
- Chunking strategy (300-800 tokens with overlap)
- Embedding generation (E5-large or Instructor)
- Similarity search (cosine + re-ranking)
- Keyword extraction

## Phase 3: API Endpoints

### Document Management
- `POST /v1/policies/upload` - File upload to S3
- `GET /v1/policies` - List documents
- `GET /v1/policies/{id}` - Document details
- `GET /v1/policies/{id}/versions` - Version history

### Comparison Operations
- `POST /v1/comparisons` - Start comparison job
- `GET /v1/comparisons/{job_id}` - Job status
- `GET /v1/comparisons/{job_id}/scores` - Clause scores
- `GET /v1/comparisons/{job_id}/findings` - Gaps & coverage
- `POST /v1/comparisons/{job_id}/report` - Generate report

### Clause Management
- `GET /v1/clause-packs` - List packs
- `GET /v1/clause-packs/{id}/clauses` - Clause list

## Phase 4: Celery Tasks

### Task Queue Structure
```
ingest_queue:
  - extract_document_text
  - chunk_document
  
embed_queue:
  - generate_document_embeddings
  - generate_clause_embeddings (one-time/on-update)
  
compare_queue:
  - run_similarity_search
  - compute_scores
  - detect_gaps
  
report_queue:
  - generate_pdf_report
  - generate_csv_export
```

### Job Flow
```
Upload → Extract → Chunk → Embed → Store
                                 ↓
Comparison Job → Retrieve Clauses → Search Similar Chunks → Re-rank → Score → Findings → Report
```

## Phase 5: Frontend Components

### Pages
- `/dashboard/{tenant}/policies` - Upload & list
- `/dashboard/{tenant}/policies/{id}` - Document viewer
- `/dashboard/{tenant}/compare` - Comparison wizard
- `/dashboard/{tenant}/comparisons/{id}` - Results dashboard
- `/dashboard/{tenant}/clause-packs` - Browse ASQA clauses

### Key Components
- `UploadDropzone` - Drag & drop with validations
- `CoverageHeatmap` - Visual clause coverage matrix
- `GapCard` - Individual gap with evidence
- `EvidenceViewer` - Side-by-side clause vs chunk
- `ThresholdControls` - Adjust thresholds dynamically
- `ReportExporter` - PDF/CSV generation

## Phase 6: Security & Multi-Tenancy

### Implemented
- ✅ Tenant isolation via `tenant_id` on Policy model
- ✅ Row-level filtering in existing views

### Required
- ⏳ Extend tenancy to all new models
- ⏳ S3 path scoping per tenant
- ⏳ Embedding isolation (prevent cross-tenant leaks)
- ⏳ RBAC permissions for comparison operations
- ⏳ Audit logging for all comparisons

## Phase 7: Observability

### Metrics
- Job completion time (p50, p95, p99)
- Embedding throughput (chunks/sec)
- Similarity search latency
- Coverage distribution per tenant
- Failure rates by stage

### Tracing
- End-to-end job traces
- Document processing pipeline
- NLP model inference timing

## Implementation Priority

### Sprint 1 (Current)
1. ✅ Review existing models
2. ⏳ Add Document/DocumentVersion/DocumentChunk models
3. ⏳ Add Embedding model with pgvector
4. ⏳ Install dependencies (pgvector, transformers, etc.)
5. ⏳ Create migrations

### Sprint 2
1. Build text extraction utilities
2. Implement chunking strategy
3. Set up embedding generation
4. Create basic upload API

### Sprint 3
1. Implement similarity search
2. Build comparison job orchestration
3. Create scoring & gap detection logic
4. Basic frontend upload page

### Sprint 4
1. Coverage heatmap UI
2. Gap cards & evidence viewer
3. Report generation (PDF/CSV)
4. Polish & testing

## Technical Decisions

### Embedding Model
**Chosen**: `intfloat/e5-large-v2` (1024 dimensions)
- Good multilingual support
- Proven accuracy on semantic search
- Reasonable inference speed
- Can run on CPU if needed

**Alternative**: `BAAI/bge-large-en-v1.5` for English-only

### Vector Storage
**Chosen**: pgvector with HNSW index
- Integrated with PostgreSQL (no separate service)
- Sufficient performance for RTO document volumes
- Transactional consistency with relational data

### Re-Ranking
**Chosen**: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Fast inference
- Good precision improvements
- Low memory footprint

## Current Blockers

1. Need to install pgvector PostgreSQL extension
2. Need to install Python dependencies
3. Need to provision S3-compatible storage for documents
4. Need to configure Celery workers

## Next Steps

1. Complete model definitions with embeddings
2. Install pgvector extension: `CREATE EXTENSION vector;`
3. Add dependencies to requirements.txt
4. Create and run migrations
5. Build text extraction pipeline
6. Implement first API endpoint (upload)

---

**Last Updated**: October 28, 2025
**Status**: Models in progress, infrastructure setup pending
