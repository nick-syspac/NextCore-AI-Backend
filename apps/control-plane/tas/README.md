# Training and Assessment Strategy (TAS) Module

The TAS module provides comprehensive tools for Australian Registered Training Organisations (RTOs) to create, manage, and maintain compliant Training and Assessment Strategies.

## Overview

The TAS system supports:
- **Course-level TAS** documents for qualifications
- **Unit-level TAS** documents for individual units of competency
- **Dynamic qualification data** from cached training.gov.au information
- **Compliance checking** against ASQA Standards
- **Assessment mapping** to performance criteria and knowledge evidence
- **Evidence packs** with immutable audit trails
- **Multi-format exports** (PDF, DOCX, JSON)

## Architecture

```
TAS Module
├── Models (tas/models.py)
│   ├── CourseTAS - Qualification-level strategies
│   ├── UnitTAS - Unit of competency strategies
│   ├── QualificationCache - Cached qualification data ⭐
│   ├── Trainer - Trainer profiles and credentials
│   ├── Facility - Training facility information
│   ├── ComplianceCheck - RAG compliance engine
│   ├── AssessmentTask - Assessment mapping
│   └── EvidencePack - Audit evidence bundles
│
├── Views (tas/views.py)
│   ├── TASViewSet - Main CRUD operations
│   ├── qualifications() - List all qualifications
│   └── units_of_competency() - Get units for qualification ⭐
│
├── Management Commands
│   └── load_qualifications - Populate qualification cache ⭐
│
└── Services (future)
    ├── Orchestrator - Workflow management
    ├── Prefill - Auto-population from integrations
    ├── ComplianceRAG - Compliance checking
    ├── AssessmentMapper - PC/KE mapping
    └── Exporter - Document generation
```

## Key Features

### 1. Dynamic Qualification Loading ⭐ NEW

Qualifications and units are loaded dynamically from a database cache rather than hardcoded.

**Benefits:**
- Add qualifications without code changes
- Update units as training.gov.au releases changes
- Scale to hundreds of qualifications
- Track data freshness with timestamps

**Quick Start:**
```bash
# Load initial qualification data
python manage.py load_qualifications

# Frontend automatically loads units when user selects qualification
# No hardcoded data needed!
```

**Documentation:**
- 📖 [Full Documentation](../../docs/TAS_QUALIFICATION_MANAGEMENT.md)
- ⚡ [Quick Reference](../../docs/TAS_QUICK_REFERENCE.md)
- 🛠️ [Management Commands](management/commands/README.md)

### 2. API Endpoints

#### Get All Qualifications
```http
GET /api/tenants/{tenant_slug}/tas/qualifications/
```

Returns list of available qualifications across all training packages.

#### Get Units for Qualification
```http
GET /api/tenants/{tenant_slug}/tas/units/?qualification_code=ICT40120
```

Returns units of competency organized by core/elective groupings.

**Response Structure:**
```json
{
  "qualification_code": "ICT40120",
  "qualification_title": "Certificate IV in Information Technology",
  "packaging_rules": "Total of 20 units: 9 core + 11 elective...",
  "has_groupings": true,
  "groupings": [
    {
      "name": "Core Units",
      "type": "core",
      "required": 9,
      "units": [
        {
          "code": "BSBCRT401",
          "title": "Articulate, present and debate ideas",
          "type": "core"
        }
      ]
    },
    {
      "name": "Cloud Computing",
      "type": "elective",
      "required": 0,
      "description": "Specialization in cloud technologies",
      "units": [...]
    }
  ]
}
```

#### Generate TAS Document
```http
POST /api/tenants/{tenant_slug}/tas/generate/
Content-Type: application/json

{
  "qualification_code": "ICT40120",
  "qualification_title": "Certificate IV in Information Technology",
  "delivery_mode": "classroom",
  "duration_weeks": 52,
  "selected_units": ["BSBCRT401", "ICTCLD401", ...]
}
```

Generates a new TAS document using GPT-4.

#### List TAS Documents
```http
GET /api/tenants/{tenant_slug}/tas/
```

Returns all TAS documents for the tenant.

#### Get TAS Document
```http
GET /api/tenants/{tenant_slug}/tas/{id}/
```

Returns a specific TAS document with all sections.

#### Regenerate Section
```http
POST /api/tenants/{tenant_slug}/tas/{id}/regenerate_section/
Content-Type: application/json

{
  "section_key": "learning_resources"
}
```

Regenerates a specific section of the TAS document.

### 3. Frontend Integration

The Next.js frontend (`/apps/web-portal/src/app/dashboard/[tenantSlug]/tas/page.tsx`) provides:

- Qualification search and selection
- Dynamic unit loading based on selected qualification
- Core units (auto-selected, disabled checkboxes)
- Elective units (user-selectable checkboxes)
- Groupings/majors/specializations display
- TAS document generation with GPT-4
- Document viewing and editing
- Section regeneration

### 4. Data Models

#### CourseTAS
Qualification-level TAS with:
- Qualification details
- Delivery strategy
- Assessment overview
- Resources
- Entry requirements
- Pathways

#### UnitTAS
Unit-level TAS with:
- Unit details
- Learning outcomes
- Assessment tasks
- Resources per unit
- Delivery approach

#### QualificationCache ⭐
Cached qualification data:
- Qualification code and title
- Training package
- AQF level
- Packaging rules
- Units organized by groupings
- Last updated timestamp

#### Trainer
Trainer profiles:
- Qualifications
- Industry experience
- Scope of registration
- Currency maintenance

#### Facility
Training facilities:
- Location and capacity
- Equipment and resources
- Compliance status
- Adequacy documentation

#### ComplianceCheck
RAG (Red/Amber/Green) compliance:
- Packaging rule validation
- Trainer scope verification
- Facility adequacy
- Hours validation
- Clustering checks

#### AssessmentTask
Assessment mapping:
- Links to performance criteria
- Links to knowledge evidence
- Assessment instruments
- Mapping matrix generation

#### EvidencePack
Audit evidence:
- Industry engagement records
- Validation evidence
- Policy documents
- Trainer credentials
- Change logs
- SHA-256 checksums for immutability

## Setup and Installation

### 1. Run Migrations
```bash
cd apps/control-plane
python manage.py migrate tas
```

### 2. Load Qualification Data
```bash
python manage.py load_qualifications
```

This loads 8 initial qualifications:
- ICT40120 - Certificate IV in Information Technology (37 units)
- BSB50120 - Diploma of Business (15 units)
- CHC50113 - Diploma of Early Childhood Education and Care (29 units)
- SIT50416 - Diploma of Hospitality Management (27 units)
- BSB40120 - Certificate IV in Business (14 units)
- BSB50420 - Diploma of Leadership and Management (17 units)
- FNS40217 - Certificate IV in Bookkeeping (14 units)
- TAE40116 - Certificate IV in Training and Assessment (13 units)

### 3. Start Services
```bash
# Django backend
python manage.py runserver

# Next.js frontend (separate terminal)
cd apps/web-portal
npm run dev
```

### 4. Access TAS Module
Navigate to: `http://localhost:3000/dashboard/{tenant-slug}/tas`

## Adding New Qualifications

### Method 1: Management Command (Recommended)

1. Edit `management/commands/load_qualifications.py`
2. Add qualification to `get_qualifications_data()` list
3. Run command:
```bash
python manage.py load_qualifications
```

### Method 2: Django Shell

```python
python manage.py shell

from tas.models import QualificationCache

QualificationCache.objects.create(
    qualification_code='SIT30616',
    qualification_title='Certificate III in Hospitality',
    training_package='SIT',
    aqf_level='certificate_iii',
    groupings=[...]
)
```

### Method 3: Django Admin

1. Navigate to `/admin/tas/qualificationcache/`
2. Click "Add Qualification Cache"
3. Fill in form and save

## Development Workflow

### Adding a New Feature

1. **Update Models** (`tas/models.py`)
2. **Create Migration** 
   ```bash
   python manage.py makemigrations tas
   python manage.py migrate tas
   ```
3. **Update Serializers** (`tas/serializers.py`)
4. **Add API Endpoints** (`tas/views.py`)
5. **Update Frontend** (`apps/web-portal/src/app/dashboard/[tenantSlug]/tas/`)
6. **Write Tests** (`tas/tests.py`)

### Testing

```bash
# Run TAS tests
python manage.py test tas

# Run with coverage
coverage run --source='tas' manage.py test tas
coverage report
```

## Configuration

### Settings

Located in `control_plane/settings.py`:

```python
# TAS Configuration
TAS_GPT_MODEL = 'gpt-4o'  # Model for document generation
TAS_MAX_RETRIES = 3        # API retry attempts
TAS_TIMEOUT = 60           # API timeout in seconds
```

### Environment Variables

```bash
OPENAI_API_KEY=sk-...  # Required for GPT-4 generation
```

## Compliance Standards

The TAS module helps RTOs comply with:

- **ASQA Standards for RTOs 2025** (effective 1 July 2025)
  - **Quality Area 1 - Training and Assessment**
    - QA1.1: Training delivery aligned with training products
    - QA1.2: Assessment meets principles and rules of evidence
    - QA1.3: Recognition of Prior Learning and Credit Transfer
    - QA1.4: Facilities, resources and equipment
  - **Quality Area 2 - VET Student Support**
    - QA2.1: Accurate and accessible information
    - QA2.2: Training support for learner success
  - **Quality Area 3 - VET Workforce**
    - QA3.2: Trainer and assessor credentials and competence
  - **Quality Area 4 - Governance**
    - QA4.3: Continuous improvement systems

> **Note:** The 2025 Standards introduced an outcome-focused framework replacing the 2015 clause-based structure.

## Troubleshooting

### Issue: Units not loading for qualification

```bash
# Check if qualification exists in cache
python manage.py shell
>>> from tas.models import QualificationCache
>>> QualificationCache.objects.filter(qualification_code='ICT40120').exists()
True
```

If False, run:
```bash
python manage.py load_qualifications
```

### Issue: API returns 404 for units

1. Check qualification_code spelling
2. Verify qualification is active:
   ```python
   >>> qual = QualificationCache.objects.get(qualification_code='ICT40120')
   >>> qual.is_active
   True
   ```
3. Check API logs for errors

### Issue: GPT-4 generation fails

1. Verify OPENAI_API_KEY is set
2. Check API quota/limits
3. Review error logs in `/var/log/django/`

## API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Future Enhancements

### Phase 1 (Current)
- ✅ Dynamic qualification loading
- ✅ Basic TAS generation
- ✅ Section regeneration
- ✅ Qualification and units APIs

### Phase 2 (In Progress)
- ⏳ Compliance RAG engine
- ⏳ Assessment mapping
- ⏳ Evidence pack generation
- ⏳ Multi-format exports

### Phase 3 (Planned)
- 📋 Training.gov.au API integration
- 📋 Automated validation
- 📋 Version history
- 📋 Collaboration features
- 📋 LMS/SMS sync

## Support and Resources

### Documentation
- 📖 [TAS Qualification Management](../../docs/TAS_QUALIFICATION_MANAGEMENT.md) - Full documentation
- ⚡ [Quick Reference Guide](../../docs/TAS_QUICK_REFERENCE.md) - Common tasks and examples
- 🛠️ [Management Commands](management/commands/README.md) - Command reference

### External Resources
- [training.gov.au](https://training.gov.au) - Official TGA website
- [ASQA](https://www.asqa.gov.au) - Australian Skills Quality Authority
- [Standards for RTOs 2025](https://www.asqa.gov.au/rtos/2025-standards-rtos) - Current compliance standards (effective 1 July 2025)
- [Practice Guides](https://www.asqa.gov.au/rtos/2025-standards-rtos/practice-guides) - ASQA guidance on 2025 Standards

### Contact
For questions or support:
- RTO Systems Team
- Email: support@nextcore.ai
- Slack: #tas-module

---

**Last Updated:** October 26, 2025  
**Version:** 2.0 (Dynamic Loading Release)  
**Maintained by:** NextCore AI Cloud Team
