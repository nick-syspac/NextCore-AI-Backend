# ASQA 2025 Standards - Quick Reference Guide

## Standards Overview

### Outcome Standards (Quality Areas 1-4)

#### Quality Area 1: Training and Assessment
| Code | Title | Key Focus |
|------|-------|-----------|
| QA1.1 | Training | Training delivery, industry currency, learner needs |
| QA1.2 | Assessment | Principles of assessment, rules of evidence, validation |
| QA1.3 | RPL & Credit Transfer | Recognition and credit for prior learning |
| QA1.4 | Facilities & Resources | Equipment, materials, learning environment |

#### Quality Area 2: VET Student Support
| Code | Title | Key Focus |
|------|-------|-----------|
| QA2.1 | Information | Pre-enrolment info, transparency, accessibility |
| QA2.2 | Training Support | LLN support, learning assistance, success support |
| QA2.3 | Diversity & Inclusion | Equity, reasonable adjustments, cultural safety |
| QA2.4 | Wellbeing | Health & safety, duty of care, safe environment |
| QA2.5 | Feedback & Complaints | Complaints process, appeals, feedback mechanisms |

#### Quality Area 3: VET Workforce
| Code | Title | Key Focus |
|------|-------|-----------|
| QA3.1 | Workforce Management | Induction, professional development, workforce planning |
| QA3.2 | Trainer & Assessor Competencies | Credentials, vocational competence, industry currency |

#### Quality Area 4: Governance
| Code | Title | Key Focus |
|------|-------|-----------|
| QA4.1 | Leadership & Accountability | Governance structures, decision-making, commitment |
| QA4.2 | Risk Management | Risk identification, mitigation, third-party management |
| QA4.3 | Continuous Improvement | Monitoring, evaluation, improvement actions |

### Compliance Requirements

| Code | Title | Key Focus |
|------|-------|-----------|
| C1 | Information & Transparency | Marketing accuracy, website info, notifications |
| C2 | Integrity of NRT Products | Training product integrity, correct certification |
| C3 | Accountability | Record keeping, AVETMISS, USI, reporting |
| C4 | Fit & Proper Person | Key personnel requirements, background checks |

### Credential Policy

| Code | Title | Key Focus |
|------|-------|-----------|
| CP1 | Trainer & Assessor Credentials | TAE qualifications, vocational competence |
| CP2 | Validation Credentials | Validation personnel requirements |

## Database Fields

### ASQAStandard Model

```python
standard_number = "QA1.1"          # Standard identifier
version = "2025"                   # 2015 or 2025
standard_category = "outcome"      # outcome, compliance, credential, legacy_2015
quality_area = 1                   # 1-4 for Outcome Standards, null for others
standard_type = "qa1_training_assessment"
asqa_url = "https://..."          # Link to ASQA Practice Guide
```

### Filtering Examples

```python
# Get all 2025 Outcome Standards
ASQAStandard.objects.filter(version='2025', standard_category='outcome')

# Get Quality Area 1 standards
ASQAStandard.objects.filter(quality_area=1, is_active=True)

# Get all Compliance Requirements
ASQAStandard.objects.filter(standard_category='compliance')

# Get both 2015 and 2025 versions of similar standards
ASQAStandard.objects.filter(standard_number__in=['1.1', 'QA1.1'])
```

## Code Migration Patterns

### Before (2015)
```python
target_clauses = ["1.1", "1.2", "1.3", "1.8"]
```

### After (2025)
```python
target_clauses = ["QA1.1", "QA1.2", "QA1.3", "QA3.2"]
```

### Version-aware Loading
```python
def get_standards(version='2025'):
    return ASQAStandard.objects.filter(
        version=version,
        is_active=True
    ).order_by('quality_area', 'standard_number')
```

## Common Mappings (2015 → 2025)

| 2015 Standard | 2025 Standard | Notes |
|---------------|---------------|-------|
| 1.1 | QA1.1, QA1.2 | Split into Training and Assessment |
| 1.2 | QA1.1, QA1.2 | Training and assessment strategies |
| 1.3 | C2 | Certification integrity |
| 1.4 | QA2.2 | LLN support |
| 1.8 | QA1.2 | Assessment including validation |
| 1.13-1.16 | QA1.4 | Resources and facilities |
| 2.1 | QA2.1 | Student information |
| 2.2 | QA2.2, QA2.4 | Support and wellbeing |
| 3.1-3.5 | C4 | Fit and proper person |
| 4.1-4.3 | C3 | Accountability and records |
| 5.1-5.3 | C2 | Certification |
| 7.1-7.5 | QA4.1, QA4.2 | Governance and risk |
| 8.1-8.6 | QA4.3, C1 | Continuous improvement, transparency |

## API Response Format

### 2025 Standards
```json
{
  "standard_number": "QA1.1",
  "version": "2025",
  "title": "Training",
  "standard_category": "outcome",
  "quality_area": 1,
  "standard_type": "qa1_training_assessment",
  "keywords": ["training delivery", "industry currency", "learner needs"],
  "asqa_url": "https://www.asqa.gov.au/rtos/2025-standards-rtos/practice-guides/practice-guide-training"
}
```

## Testing Checklist

- [ ] Verify 2025 standards seed data loads correctly (20 standards total)
- [ ] Test filtering by version (2025 vs 2015)
- [ ] Test filtering by standard_category (outcome, compliance, credential)
- [ ] Test filtering by quality_area (1, 2, 3, 4)
- [ ] Verify unique constraint works: same standard_number allowed across versions
- [ ] Test Policy Comparator with 2025 standards
- [ ] Test TAS Generator compliance checking with QA1.x codes
- [ ] Verify HTML documentation displays correctly
- [ ] Test backward compatibility with existing 2015 data

## Important Dates

- **July 1, 2025:** 2025 Standards came into effect
- **From July 1, 2025:** RTOs must demonstrate compliance against 2025 Standards for all regulatory activity
- **Transition:** Any audits continuing after July 1 may require additional evidence against 2025 Standards

## Resources

- **Main Page:** https://www.asqa.gov.au/rtos/2025-standards-rtos
- **Practice Guides:** https://www.asqa.gov.au/rtos/2025-standards-rtos/practice-guides
- **Legislation:** https://www.legislation.gov.au/F2025L00354/asmade/text
- **Policy Guidance:** https://www.dewr.gov.au/revisions-standards-registered-training-organisations

---

**Quick Links:**
- [Full Migration Summary](./ASQA_2025_MIGRATION_SUMMARY.md)
- [2025 Standards Seed Data](./db/seeds/asqa_standards_2025.json)
- [Database Migration Script](./db/migrations/2025_standards_migration.sql)
