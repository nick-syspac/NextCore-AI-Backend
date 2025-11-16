# ASQA Standards 2025 Migration Summary

**Date:** November 7, 2025  
**Effective Date:** July 1, 2025  
**Status:** Documentation and Code Updates Complete

## Overview

The Standards for Registered Training Organisations (RTOs) 2025 came into effect on July 1, 2025, replacing the 2015 standards with an outcome-focused framework. This document summarizes all updates made to the RTOComply AI Backend system to support the new standards structure.

## Key Changes in 2025 Standards

### Structure Transformation

**2015 Standards (Legacy):**
- 8 Standards with numbered clauses (1.1, 1.2, etc.)
- Prescriptive, process-focused requirements
- Clause-based compliance checking

**2025 Standards (Current):**
- **Outcome Standards:** 4 Quality Areas with 14 total standards
  - Quality Area 1: Training and Assessment (4 standards)
  - Quality Area 2: VET Student Support (5 standards)
  - Quality Area 3: VET Workforce (2 standards)
  - Quality Area 4: Governance (3 standards)
- **Compliance Requirements:** 4 administrative standards (C1-C4)
- **Credential Policy:** 2 standards for trainer/assessor credentials (CP1-CP2)
- Outcome-focused, quality-driven approach

## Files Updated

### 1. Documentation (HTML)

#### Policy Comparator (`/html_help/EduAI_Compliance_Suite/Policy_Comparator/`)

**index.html:**
- Updated ASQA Standards Coverage section with 2025 structure
- Added Quality Areas 1-4 breakdown with all standards
- Included official ASQA resource links
- Added transition notice for July 1, 2025 effective date
- Replaced 2015 standards table with comprehensive 2025 standards table

**getting-started.html:**
- Updated setup instructions with 2025 Standards information
- Added alert about July 1, 2025 transition requirement

#### TAS Generator (`/html_help/EduAI_Compliance_Suite/TAS_Generator/`)

**index.html:**
- Updated compliance description from "2015" to "2025"
- Revised ASQA Standards Coverage table with QA1-QA4 structure
- Added 8 key standards relevant to TAS (QA1.1-QA4.3)
- Included link to official 2025 Standards website
- Added informational alert about July 1, 2025 effective date

### 2. Database Models

**File:** `/apps/control-plane/policy_comparator/models.py`

**ASQAStandard Model Updates:**
- Added support for both 2015 and 2025 standards versions
- New field: `standard_category` (outcome/compliance/credential/legacy_2015)
- New field: `quality_area` (1-4 for Outcome Standards)
- New field: `asqa_url` (links to official documentation)
- Updated `STANDARD_TYPES` to include 2025 categories
- Changed default `version` from "2015" to "2025"
- Modified unique constraint to allow same standard_number across versions
- Updated `__str__` method to display Quality Area for 2025 standards
- Added new indexes for performance (version, category, quality_area)

### 3. Database Migration

**File:** `/db/migrations/2025_standards_migration.sql`

SQL migration script created to:
- Add new columns: `standard_category`, `quality_area`, `asqa_url`
- Update version field default to "2025"
- Drop old unique constraint on `standard_number`
- Add new composite unique constraint: `(standard_number, version)`
- Create performance indexes
- Update existing 2015 records with proper category
- Add column comments for documentation

### 4. Seed Data

**File:** `/db/seeds/asqa_standards_2025.json`

Comprehensive JSON seed data file containing:
- **Metadata:** Effective date, legislation links, source URLs
- **14 Outcome Standards** across 4 Quality Areas:
  - QA1: Training (QA1.1), Assessment (QA1.2), RPL & Credit (QA1.3), Facilities (QA1.4)
  - QA2: Information (QA2.1), Training Support (QA2.2), Diversity (QA2.3), Wellbeing (QA2.4), Complaints (QA2.5)
  - QA3: Workforce Management (QA3.1), Trainer Credentials (QA3.2)
  - QA4: Leadership (QA4.1), Risk Management (QA4.2), Continuous Improvement (QA4.3)
- **4 Compliance Requirements:** C1-C4
- **2 Credential Policy Standards:** CP1-CP2
- Full requirements breakdown for each standard
- Keywords for NLP matching
- Official ASQA Practice Guide URLs

### 5. Backend Code

**File:** `/apps/control-plane/tas/ai_services.py`

**ComplianceValidator Class Updates:**
- `_load_asqa_standards()`: Updated to load 2025 standards (QA1.1-QA4.3)
- Added comprehensive docstring explaining 2025 structure
- `evaluate_clause_coverage()`: Updated default clauses to 2025 standards
  - Changed from ["1.1", "1.2", ...] to ["QA1.1", "QA1.2", ...]
  - Updated to check 8 key 2025 Outcome Standards
- Added TODO notes to load from database ASQAStandard model

**File:** `/apps/control-plane/tas/README.md`

**Compliance Section Updates:**
- Replaced "ASQA Standards for RTOs 2015" header
- Added "ASQA Standards for RTOs 2025 (effective 1 July 2025)" header
- Reorganized standards by Quality Areas 1-4
- Listed relevant standards for TAS module (QA1.1-QA4.3)
- Added note about outcome-focused framework
- Updated External Resources section:
  - Changed link from "Standards for RTOs 2015" to "Standards for RTOs 2025"
  - Added Practice Guides link

**File:** `/docs/TAS_AI_INTEGRATION.md`

**RAG Implementation Updates:**
- Updated example JSON response to reference QA1.1 and QA1.2 instead of "Standard 1.2"
- Changed `asqa_clauses` key to `asqa_standards`
- Added reference to "2025 Standards (QA1.1 Training)" in explanations
- Updated resource filename from "ASQA_Standard_1.2_Guidance.pdf" to "ASQA_2025_Standards_QA1_Practice_Guide.pdf"
- Updated "Data to Index" section:
  - Changed from "All Standards for RTOs 2015 clauses"
  - To "All Standards for RTOs 2025 (Outcome Standards, Compliance Requirements, Credential Policy)"
  - Added breakdown of QA1-4, C1-C4, and CP1-CP2
  - Added note about legacy 2015 standards for historical reference

## Official ASQA Resources

### Primary Sources
- **2025 Standards Homepage:** https://www.asqa.gov.au/rtos/2025-standards-rtos
- **Outcome Standards (Legislation):** https://www.legislation.gov.au/F2025L00354/asmade/text
- **Compliance Requirements (Legislation):** https://www.legislation.gov.au/F2025L00355/asmade/text
- **Practice Guides:** https://www.asqa.gov.au/rtos/2025-standards-rtos/practice-guides

### Key Practice Guides
- Training (QA1.1): https://www.asqa.gov.au/rtos/2025-standards-rtos/practice-guides/practice-guide-training
- Assessment (QA1.2): https://www.asqa.gov.au/how-we-regulate/revised-standards-rtos/practice-guides/practice-guide-assessment
- RPL & Credit Transfer (QA1.3): https://www.asqa.gov.au/how-we-regulate/revised-standards-rtos/practice-guides/practice-guide-recognition-prior-learning-and-credit-transfer
- Credential Policy: https://www.asqa.gov.au/how-we-regulate/revised-standards-rtos/practice-guides/practice-guide-credential-policy

## Implementation Status

### ✅ Completed
1. **Documentation Updates**
   - Policy Comparator HTML documentation (2 files)
   - TAS Generator HTML documentation (1 file)

2. **Database Schema**
   - ASQAStandard model updated with 2025 support
   - Migration SQL script created
   - Comprehensive seed data prepared

3. **Backend Code**
   - TAS AI services updated
   - TAS README documentation updated
   - TAS AI Integration documentation updated

### ⏳ Pending (Deployment Tasks)
1. **Database Migration**
   - Run migration script: `2025_standards_migration.sql`
   - Verify schema changes applied successfully

2. **Data Loading**
   - Load 2025 standards from seed data: `asqa_standards_2025.json`
   - Verify all 20 standards loaded (14 Outcome + 4 Compliance + 2 Credential)
   - Test database queries with new fields

3. **Code Deployment**
   - Deploy updated models.py
   - Deploy updated ai_services.py
   - Restart control-plane service

4. **Testing**
   - Test Policy Comparator with 2025 standards
   - Test TAS Generator compliance checking
   - Verify HTML documentation displays correctly
   - Test API endpoints with new standard_category filters

5. **User Communication**
   - Notify RTOs about 2025 Standards support
   - Update release notes
   - Provide migration guidance for existing data

## Migration Considerations

### Backward Compatibility
- System maintains support for 2015 standards (marked as `legacy_2015`)
- Existing data with 2015 standards remains accessible
- APIs should support filtering by version parameter
- Historical TAS documents referencing 2015 clauses remain valid

### Data Migration Strategy
1. **Keep 2015 Data:** Do not delete existing 2015 standard records
2. **Load 2025 Data:** Add new records with `version='2025'`
3. **Update Defaults:** Set new comparisons to use 2025 by default
4. **User Choice:** Allow users to select which version to compare against (for historical purposes)

### API Considerations
Endpoints should support version filtering:
```python
# Example API filter
GET /api/asqa-standards/?version=2025
GET /api/asqa-standards/?standard_category=outcome
GET /api/asqa-standards/?quality_area=1
```

## Benefits of 2025 Standards

### For RTOs
- **Outcome-focused:** Emphasis on quality outcomes rather than prescriptive processes
- **Flexibility:** More room for RTOs to demonstrate compliance in ways that suit their context
- **Clear Structure:** 4 Quality Areas provide logical organization
- **Practice Guides:** Comprehensive ASQA guidance for each standard

### For the System
- **Better Organization:** Quality Areas enable intuitive filtering and reporting
- **Enhanced Compliance:** Alignment with current regulatory framework
- **Future-proof:** System ready for ongoing 2025 standards implementation
- **Dual Support:** Maintains historical 2015 data while enabling 2025 compliance

## Next Steps

1. **Review Migration Script:** Validate SQL migration before production deployment
2. **Test Seed Data:** Load standards in development environment and test
3. **Update API Documentation:** Document new fields and filtering options
4. **User Training:** Prepare training materials on 2025 Standards differences
5. **Monitoring:** Track usage of 2025 vs 2015 standards in analytics

## References

- ASQA 2025 Standards Announcement: https://www.asqa.gov.au/rtos/2025-standards-rtos
- Department of Employment and Workplace Relations Policy Guidance: https://www.dewr.gov.au/revisions-standards-registered-training-organisations
- National Vocational Education and Training Regulator Act 2011: https://www.legislation.gov.au/C2011A00012/latest

---

**Document Version:** 1.0  
**Last Updated:** November 7, 2025  
**Author:** RTOComply AI Backend Team
