# TAS AI Features - Quick Reference

## Quick Start

```python
from tas.ai_services import AIServiceFactory

# Get a service
service = AIServiceFactory.get_service('compliance_rag')

# Use it
result = service.evaluate_clause_coverage(tas_content, ['1.1', '1.2'])
```

## Available Services

| Service Name | Purpose | Key Methods |
|--------------|---------|-------------|
| `intake_prefill` | Data extraction & enrichment | `extract_trainer_details()`, `enrich_tga_snapshot()`, `suggest_cohort_archetype()` |
| `packaging_clustering` | Unit selection & scheduling | `recommend_electives()`, `suggest_unit_clusters()`, `optimize_timetable()` |
| `content_drafter` | TAS content generation | `draft_cohort_needs_section()`, `generate_assessment_blueprint()`, `map_resources()` |
| `compliance_rag` | Compliance checking | `evaluate_clause_coverage()`, `score_trainer_suitability()`, `detect_policy_drift()` |
| `evidence` | Evidence & audit prep | `summarize_industry_minutes()`, `generate_validation_plan()`, `explain_version_differences()` |
| `quality_analytics` | Risk analysis | `predict_lln_risk()`, `analyze_completion_risk()`, `check_system_consistency()` |
| `copilot` | Inline assistance | `answer_inline_question()`, `generate_guided_content()` |

## Common API Calls

### 1. Check ASQA Compliance (Quick Win #1)
```bash
curl -X POST http://localhost:8000/api/tenants/acme-college/tas/1/ai/check-compliance/ \
  -H "Content-Type: application/json" \
  -d '{
    "tas_content": {
      "trainer_qualifications": "All trainers hold TAE40116",
      "assessment_strategy": "Competency-based..."
    },
    "target_clauses": ["1.1", "1.2", "1.3"]
  }'
```

### 2. Generate Assessment Blueprint (Quick Win #2)
```bash
curl -X POST http://localhost:8000/api/tenants/acme-college/tas/1/ai/assessment-blueprint/ \
  -H "Content-Type: application/json" \
  -d '{
    "unit_code": "BSBWHS411",
    "elements": [...],
    "delivery_mode": "workplace",
    "industry_context": "construction"
  }'
```

### 3. Summarize Industry Minutes (Quick Win #3)
```bash
curl -X POST http://localhost:8000/api/tenants/acme-college/tas/1/ai/summarize-minutes/ \
  -H "Content-Type: application/json" \
  -d '{
    "minutes_text": "Meeting held with industry partners...",
    "meeting_date": "2024-01-15",
    "attendees": ["John Smith", "Jane Doe"]
  }'
```

### 4. Score Trainer Suitability (Quick Win #4)
```bash
curl -X POST http://localhost:8000/api/tenants/acme-college/tas/1/ai/score-trainer/ \
  -H "Content-Type: application/json" \
  -d '{
    "trainer_profile": {
      "qualifications": ["Bachelor of Business", "TAE40116"],
      "industry_experience": [...]
    },
    "unit_requirements": {
      "unit_code": "BSBOPS502"
    }
  }'
```

### 5. Detect Policy Changes (Quick Win #5)
```bash
curl -X POST http://localhost:8000/api/tenants/acme-college/tas/1/ai/detect-policy-drift/ \
  -H "Content-Type: application/json" \
  -d '{
    "tas_policy_references": [
      {"name": "Assessment Policy", "version": "2.0"}
    ],
    "current_policies": [
      {"name": "Assessment Policy", "version": "3.0"}
    ]
  }'
```

## Feature Area Endpoints

### Intake & Prefill
- `/ai/enrich-tga/` - Enrich TGA unit data
- `/ai/suggest-cohort/` - Suggest cohort archetype

### Packaging & Clustering
- `/ai/recommend-electives/` - Recommend electives for job outcomes
- `/ai/cluster-units/` - Suggest unit clusters
- `/ai/optimize-timetable/` - Optimize delivery schedule

### Content Drafting
- `/ai/draft-section/` - Draft TAS sections
- `/ai/assessment-blueprint/` - Generate assessment blueprint
- `/ai/map-resources/` - Map resources to requirements

### Compliance
- `/ai/check-compliance/` - Check ASQA clause coverage
- `/ai/score-trainer/` - Score trainer suitability
- `/ai/assess-facility/` - Assess facility adequacy
- `/ai/detect-policy-drift/` - Detect policy changes

### Evidence & Audit
- `/ai/summarize-minutes/` - Summarize industry minutes
- `/ai/validation-plan/` - Generate validation plan
- `/ai/explain-changes/` - Explain version differences

### Quality & Risk
- `/ai/predict-lln-risk/` - Predict LLN support needs
- `/ai/completion-risk/` - Analyze completion risk
- `/ai/check-consistency/` - Check system consistency

### Co-pilot
- `/ai/ask/` - Ask inline questions

## Python Examples

### Extract Trainer Details
```python
from tas.ai_services import IntakePrefillService

service = IntakePrefillService()
result = service.extract_trainer_details(
    cv_text="Professional Experience: 10 years in business...",
    pd_logs=[
        {"date": "2024-01-10", "activity": "Business Conference"}
    ]
)

print(result['qualifications'])
print(result['vocational_competency_score'])
```

### Recommend Electives
```python
from tas.ai_services import PackagingClusteringService

service = PackagingClusteringService()
electives = service.recommend_electives(
    qualification_code='BSB50120',
    job_outcomes=['Business Manager', 'Operations Coordinator'],
    available_electives=[
        {'code': 'BSBOPS502', 'title': 'Manage business operational plans'},
        {'code': 'BSBFIN501', 'title': 'Manage budgets and financial plans'}
    ],
    packaging_rules='Select 6 electives from Group A or B'
)

for e in electives:
    print(f"{e['unit_code']}: {e['rationale']} (Score: {e['relevance_score']})")
```

### Draft Cohort Needs
```python
from tas.ai_services import TASContentDrafter

service = TASContentDrafter()
draft = service.draft_cohort_needs_section(
    cohort_data={
        'size': 25,
        'demographics': {'age_range': '25-45'},
        'lln_assessment': 'Average Level 3'
    },
    qualification='BSB50120 Diploma of Business',
    delivery_context='Blended - weekly face-to-face with online'
)

print(draft['content'])
print(f"Addresses ASQA clauses: {draft['asqa_clauses_addressed']}")
```

### Check Compliance
```python
from tas.ai_services import ComplianceRAGService

service = ComplianceRAGService()
report = service.evaluate_clause_coverage(
    tas_content={
        'trainer_qualifications': 'All trainers hold TAE40116...',
        'assessment_strategy': 'Competency-based assessment...'
    },
    target_clauses=['1.1', '1.2', '1.3']
)

for clause, result in report['clause_results'].items():
    print(f"Clause {clause}: {result['status']}")
    if result['missing']:
        print(f"  Missing: {result['missing']}")
        print(f"  Fixes: {result['suggested_fixes']}")
```

### Summarize Minutes
```python
from tas.ai_services import EvidenceService

service = EvidenceService()
summary = service.summarize_industry_minutes(
    minutes_text="Discussion of current skills needs in retail sector...",
    meeting_date='2024-01-15',
    attendees=['John Smith', 'Jane Doe']
)

print(summary['summary'])
for point in summary['key_points']:
    print(f"- {point}")
```

### Predict LLN Risk
```python
from tas.ai_services import QualityAnalyticsService

service = QualityAnalyticsService()
prediction = service.predict_lln_risk(
    cohort_data={'avg_lln_score': 2.5},
    historical_cohorts=[
        {'avg_lln_score': 2.8, 'completion_rate': 65}
    ]
)

print(f"Risk Level: {prediction['risk_level']}")
print(f"Recommended Support Hours: {prediction['support_hours_per_week']}")
print(f"Interventions: {prediction['interventions']}")
```

### Ask AI Co-pilot
```python
from tas.ai_services import ConversationalCopilot

service = ConversationalCopilot()
answer = service.answer_inline_question(
    question="Why is this cluster non-compliant?",
    context={
        'section': 'unit_clustering',
        'current_text': 'Units: BSBWHS411, BSBFIN501, BSBOPS502'
    }
)

print(answer['answer'])
print(f"Related ASQA: {answer['asqa_clauses']}")
```

## Common Workflows

### Workflow 1: Complete TAS Generation with AI
```python
# 1. Extract trainer details
trainer_service = AIServiceFactory.get_service('intake_prefill')
trainer_data = trainer_service.extract_trainer_details(cv_text, pd_logs)

# 2. Suggest cohort archetype
cohort = trainer_service.suggest_cohort_archetype(history, demographics)

# 3. Recommend electives
packaging_service = AIServiceFactory.get_service('packaging_clustering')
electives = packaging_service.recommend_electives(qual, jobs, available, rules)

# 4. Cluster units
clusters = packaging_service.suggest_unit_clusters(selected_units, 4)

# 5. Generate assessment blueprints
drafter = AIServiceFactory.get_service('content_drafter')
for unit in units:
    blueprint = drafter.generate_assessment_blueprint(unit, elements, mode, context)

# 6. Draft TAS sections
cohort_section = drafter.draft_cohort_needs_section(cohort, qual, context)

# 7. Check compliance
compliance = AIServiceFactory.get_service('compliance_rag')
coverage = compliance.evaluate_clause_coverage(tas_content, asqa_clauses)

# 8. Generate validation plan
evidence = AIServiceFactory.get_service('evidence')
validation = evidence.generate_validation_plan(assessments, cohort_size, last_date)
```

### Workflow 2: Compliance Audit with AI
```python
# 1. Check ASQA clause coverage
compliance_service = AIServiceFactory.get_service('compliance_rag')
coverage = compliance_service.evaluate_clause_coverage(tas, asqa_clauses)

# 2. Score all trainers
for trainer in trainers:
    score = compliance_service.score_trainer_suitability(trainer, unit_reqs)
    if score['suitability_score'] < 70:
        print(f"Trainer {trainer['name']} needs PD: {score['pd_recommendations']}")

# 3. Assess facilities
for unit in units:
    adequacy = compliance_service.assess_facility_adequacy(inventory, unit['requirements'])
    if adequacy['adequacy_status'] != 'adequate':
        print(f"Unit {unit['code']} has gaps: {adequacy['gaps']}")

# 4. Detect policy drift
drift = compliance_service.detect_policy_drift(tas_policies, current_policies)
if drift['drifts_detected'] > 0:
    print(f"Policy updates required: {drift['high_priority_count']} high priority")
```

### Workflow 3: Evidence Pack Assembly
```python
# 1. Summarize all industry minutes
evidence_service = AIServiceFactory.get_service('evidence')
summaries = []
for minutes in industry_minutes:
    summary = evidence_service.summarize_industry_minutes(
        minutes['text'], minutes['date'], minutes['attendees']
    )
    summaries.append(summary)

# 2. Generate validation plan
validation_plan = evidence_service.generate_validation_plan(
    assessment_tasks, cohort_size, last_validation
)

# 3. Explain version changes
changes = evidence_service.explain_version_differences(old_version, new_version)

# 4. Compile evidence pack
evidence_pack = {
    'industry_engagement': summaries,
    'validation_schedule': validation_plan,
    'change_rationale': changes,
    'compliance_report': coverage_report
}
```

## Troubleshooting

### Issue: AI service returns error
```python
# Check service availability
try:
    service = AIServiceFactory.get_service('compliance_rag')
    result = service.evaluate_clause_coverage(data, clauses)
except ValueError as e:
    print(f"Service error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Issue: API call fails
```bash
# Check Django logs
tail -f /tmp/django-clean.log

# Test service directly
cd /home/nick/work/NextCore-AI-Cloud/apps/control-plane
python manage.py shell

>>> from tas.ai_services import ComplianceRAGService
>>> service = ComplianceRAGService()
>>> result = service.evaluate_clause_coverage({}, ['1.1'])
>>> print(result)
```

### Issue: Slow response times
- Check if LLM API is rate-limited
- Implement caching for common queries
- Reduce context window size
- Use smaller model for non-critical operations

## Cost Estimates

| Feature | API Calls/Month | Cost/Month (GPT-4) | Cost/Month (GPT-3.5) |
|---------|-----------------|---------------------|----------------------|
| TGA Enrichment | 500 | $30 | $3 |
| Compliance Checks | 1000 | $120 | $12 |
| Assessment Blueprints | 300 | $27 | $2.70 |
| Content Drafting | 400 | $30 | $3 |
| Trainer Scoring | 200 | $12 | $1.20 |
| **Total** | **2400** | **$219** | **$21.90** |

*Based on 100 active TAS documents per month*

## Next Steps

1. **Configure OpenAI API Key** (currently using placeholders)
   ```python
   # In settings.py
   OPENAI_API_KEY = 'sk-...'
   ```

2. **Set up Vector Database** for RAG
   ```bash
   # Install pgvector extension
   pip install pgvector
   ```

3. **Index Policy Documents**
   ```python
   # Create embeddings for policies
   from tas.ai_services import ComplianceRAGService
   service = ComplianceRAGService()
   # service._build_policies_index()  # Implement this
   ```

4. **Test Quick Wins**
   - Start with compliance checking
   - Move to assessment mapper
   - Add minutes summarizer
   - Implement trainer scorer
   - Deploy policy drift detector

## Resources

- Full Documentation: `/docs/TAS_AI_INTEGRATION.md`
- API Reference: `/docs/API_DOCUMENTATION.md`
- Code: `/apps/control-plane/tas/ai_services.py`
- Views: `/apps/control-plane/tas/views.py`

---

**Quick Tip**: Start with the 5 "Quick Win" features - they provide immediate value with minimal setup!
