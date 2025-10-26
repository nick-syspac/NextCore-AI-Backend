# TAS Module - Documentation Index

Complete documentation for the Training and Assessment Strategy (TAS) module's dynamic qualification management system and AI integration.

## 📚 Documentation Structure

### 1. Getting Started

**[TAS Module README](../apps/control-plane/tas/README.md)**  
Main module overview, architecture, setup instructions, and feature summary.
- Best for: Understanding the overall TAS system
- Audience: Developers, system administrators, project managers

### 2. Detailed Guides

**[TAS Qualification Management Guide](TAS_QUALIFICATION_MANAGEMENT.md)**  
Comprehensive documentation for the qualification cache system.
- Database model details
- API endpoint specifications
- Adding new qualifications (3 methods)
- Maintenance procedures
- Troubleshooting guide
- Future enhancements
- Best for: Detailed implementation and maintenance
- Audience: Developers, database administrators

**[TAS AI Integration Guide](TAS_AI_INTEGRATION.md)** ⭐ NEW  
Complete AI capabilities documentation across 9 feature areas.
- AI service architecture
- 20+ AI-powered API endpoints
- Feature area guides (Intake, Packaging, Drafting, Compliance, Evidence, Analytics, Co-pilot)
- Implementation notes and best practices
- Quick wins to implement first
- Cost estimates and optimization
- Best for: Understanding and implementing AI features
- Audience: Developers, AI engineers, RTO managers

### 3. Quick Reference

**[TAS Quick Reference](TAS_QUICK_REFERENCE.md)**  
Fast lookup guide with common commands and code snippets.
- Common commands (copy-paste ready)
- Quick add qualification examples
- Query examples
- Troubleshooting shortcuts
- Currently loaded qualifications table
- Best for: Daily operations and quick lookups
- Audience: All technical staff

**[TAS AI Quick Reference](TAS_AI_QUICK_REFERENCE.md)** ⭐ NEW  
Fast lookup for AI features and API calls.
- Available AI services table
- Common API curl commands
- Python usage examples
- Common workflows
- Cost estimates
- Quick troubleshooting
- Best for: Using AI features in daily work
- Audience: All technical staff, RTO content developers

### 4. Management Commands

**[Management Commands README](../apps/control-plane/tas/management/commands/README.md)**  
Detailed documentation for Django management commands.
- `load_qualifications` command reference
- Command options and examples
- Data structure specifications
- Development guide for custom commands
- Best for: Understanding and using management commands
- Audience: Developers, system administrators

## 🎯 Quick Navigation

### I want to...

#### **Understand the system**
→ Start with [TAS Module README](../apps/control-plane/tas/README.md)

#### **Learn about AI features**
→ See [TAS AI Integration Guide](TAS_AI_INTEGRATION.md)  
→ Or [TAS AI Quick Reference](TAS_AI_QUICK_REFERENCE.md) for quick examples

#### **Use AI to check ASQA compliance**
→ See [AI Quick Reference - Check Compliance](TAS_AI_QUICK_REFERENCE.md#1-check-asqa-compliance-quick-win-1)

#### **Generate assessment blueprints with AI**
→ See [AI Integration - Assessment Blueprinting](TAS_AI_INTEGRATION.md#generate-assessment-blueprint)

#### **Get AI help with TAS drafting**
→ See [AI Integration - Content Drafting](TAS_AI_INTEGRATION.md#3-drafting-tas-content)

#### **Add a new qualification**
→ Go to [Quick Reference - Quick Add Qualification](TAS_QUICK_REFERENCE.md#quick-add-qualification)

#### **Learn about the database structure**
→ See [Qualification Management - Database Model](TAS_QUALIFICATION_MANAGEMENT.md#database-model)

#### **Use the API**
→ Check [Qualification Management - API Endpoints](TAS_QUALIFICATION_MANAGEMENT.md#api-endpoints)

#### **Troubleshoot issues**
→ See [Qualification Management - Troubleshooting](TAS_QUALIFICATION_MANAGEMENT.md#troubleshooting)  
→ Or [Quick Reference - Troubleshooting](TAS_QUICK_REFERENCE.md#troubleshooting)

#### **Run management commands**
→ See [Management Commands README](../apps/control-plane/tas/management/commands/README.md)

#### **Maintain the system**
→ See [Qualification Management - Maintenance Tasks](TAS_QUALIFICATION_MANAGEMENT.md#maintenance-tasks)

## 📖 Document Summaries

### TAS Module README
- **Location:** `apps/control-plane/tas/README.md`
- **Length:** ~400 lines
- **Topics:**
  - Overview and architecture diagram
  - Key features (dynamic loading ⭐)
  - API endpoints (6 endpoints)
  - Data models (8 models)
  - Setup instructions
  - Development workflow
  - Compliance standards
  - Future roadmap

### TAS Qualification Management Guide
- **Location:** `docs/TAS_QUALIFICATION_MANAGEMENT.md`
- **Length:** ~800 lines
- **Topics:**
  - Architecture diagram
  - QualificationCache model specification
  - Groupings JSON structure
  - API specifications with examples
  - Management command detailed usage
  - Three methods for adding qualifications
  - Python/SQL query examples

### TAS AI Integration Guide ⭐ NEW
- **Location:** `docs/TAS_AI_INTEGRATION.md`
- **Length:** ~2,500 lines
- **Topics:**
  - AI service architecture and design
  - 7 AI service classes with detailed specs
  - 20+ API endpoints with request/response examples
  - 9 feature areas:
    * Intake & Prefill (entity extraction, TGA enrichment, cohort suggestions)
    * Packaging & Clustering (elective recommendations, unit clustering, timetabling)
    * Content Drafting (TAS sections, assessment blueprints, resource mapping)
    * Compliance Guardrails (ASQA checks, trainer scoring, facility assessment, policy drift)
    * Evidence Pack (minutes summarization, validation planning, version diffs)
    * Quality & Risk Analytics (LLN prediction, completion risk, consistency checking)
    * Conversational Co-pilot (inline Q&A, guided prompts)
  - Implementation notes (model selection, embeddings, vector search)
  - Safety rails and privacy considerations
  - 5 quick wins to implement first
  - Cost estimates and optimization strategies
  - Testing and performance guidance
  - Roadmap (4 phases)

### TAS AI Quick Reference ⭐ NEW
- **Location:** `docs/TAS_AI_QUICK_REFERENCE.md`
- **Length:** ~500 lines
- **Topics:**
  - Quick start code examples
  - Available services table
  - 20+ common API curl commands
  - Python usage examples for all services
  - 3 complete workflows:
    * Complete TAS generation with AI
    * Compliance audit with AI
    * Evidence pack assembly
  - Troubleshooting common issues
  - Cost estimates by feature
  - Next steps checklist
  - Frontend integration code
  - Maintenance procedures
  - Future enhancements (4 planned features)
  - Comprehensive troubleshooting (3 common issues)
  - Best practices (8 recommendations)

### TAS Quick Reference
- **Location:** `docs/TAS_QUICK_REFERENCE.md`
- **Length:** ~350 lines
- **Topics:**
  - Common commands (ready to copy-paste)
  - Quick add qualification template
  - Groupings structure templates (2 patterns)
  - Query examples (7 common queries)
  - Currently loaded qualifications table (8 quals)
  - Training packages reference
  - Files reference table
  - Next steps checklist

### Management Commands README
- **Location:** `apps/control-plane/tas/management/commands/README.md`
- **Length:** ~250 lines
- **Topics:**
  - load_qualifications command detailed docs
  - Command options and examples
  - Data structure specifications
  - Adding new qualifications procedure
  - When to use the command
  - Cautions and warnings
  - Future commands (4 planned)
  - Development guide for custom commands

## 🔑 Key Concepts

### Qualification Cache
Database-backed storage for qualification codes, titles, and units of competency. Replaces hardcoded data with dynamic, maintainable records.

### Groupings
Organizational structure for units within a qualification. Can be simple (core/elective) or complex (specializations/majors).

### Management Command
Django command (`python manage.py load_qualifications`) that populates and updates the cache from curated data sources.

### Dynamic Loading
Units are fetched from the database when a user selects a qualification, rather than being hardcoded in the application.

## 📊 System Statistics

| Metric | Value |
|--------|-------|
| **Initial Qualifications** | 8 |
| **Total Units** | 166 |
| **Training Packages** | 7 (BSB, ICT, CHC, SIT, FNS, TAE) |
| **API Endpoints** | 6 |
| **Database Tables** | 9 |
| **Management Commands** | 1 (4 planned) |
| **Documentation Pages** | 4 |
| **Code Lines (Backend)** | ~3,000 |

## 🚀 Implementation Timeline

### Completed (October 26, 2025)
- ✅ QualificationCache model created
- ✅ Database migrations applied
- ✅ load_qualifications command implemented
- ✅ API endpoints updated to use cache
- ✅ 8 qualifications loaded
- ✅ Frontend integration working
- ✅ Complete documentation suite

### Next Steps
1. Add more qualifications (target: 50+)
2. Implement training.gov.au API integration
3. Add validation command
4. Create export/import commands
5. Set up periodic sync jobs

## 🛠️ Technical Details

### Technologies Used
- **Backend:** Django 5.1.2, Django REST Framework
- **Database:** PostgreSQL (JSONField for groupings)
- **Frontend:** Next.js 14, React, TypeScript
- **API:** RESTful JSON API
- **Data Source:** training.gov.au (cached)

### File Structure
```
NextCore-AI-Cloud/
├── apps/control-plane/tas/
│   ├── models.py              # QualificationCache model
│   ├── views.py               # API endpoints
│   ├── serializers.py         # DRF serializers
│   ├── README.md              # Module documentation
│   └── management/commands/
│       ├── load_qualifications.py  # Management command
│       └── README.md          # Commands documentation
├── apps/web-portal/src/app/dashboard/[tenantSlug]/tas/
│   └── page.tsx               # Frontend implementation
└── docs/
    ├── TAS_QUALIFICATION_MANAGEMENT.md  # Full guide
    ├── TAS_QUICK_REFERENCE.md           # Quick reference
    └── TAS_DOCUMENTATION_INDEX.md       # This file
```

### Database Schema
```sql
CREATE TABLE tas_qualification_cache (
    id SERIAL PRIMARY KEY,
    qualification_code VARCHAR(20) UNIQUE NOT NULL,
    qualification_title VARCHAR(500) NOT NULL,
    training_package VARCHAR(20),
    aqf_level VARCHAR(50),
    packaging_rules TEXT,
    has_groupings BOOLEAN DEFAULT false,
    groupings JSONB DEFAULT '[]',
    source VARCHAR(50) DEFAULT 'training.gov.au',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    release_date DATE
);

CREATE INDEX idx_qual_code_active ON tas_qualification_cache(qualification_code, is_active);
CREATE INDEX idx_training_package ON tas_qualification_cache(training_package);
```

## 📞 Support

### Getting Help

1. **Check documentation** - Start with this index
2. **Review examples** - Quick Reference has many examples
3. **Search issues** - Check GitHub issues for similar problems
4. **Ask the team** - Slack #tas-module or email support@nextcore.ai

### Reporting Issues

When reporting issues, include:
- Qualification code (if relevant)
- Error messages (full stack trace)
- Steps to reproduce
- Expected vs actual behavior
- Django/database logs

### Contributing

To improve documentation:
1. Fork the repository
2. Update relevant markdown files
3. Test commands and examples
4. Submit pull request with clear description

## 🎓 Learning Path

### For New Developers
1. Read [TAS Module README](../apps/control-plane/tas/README.md) - Overview
2. Review [Quick Reference](TAS_QUICK_REFERENCE.md) - Common patterns
3. Try adding a qualification using shell method
4. Explore [Full Guide](TAS_QUALIFICATION_MANAGEMENT.md) - Deep dive

### For System Administrators
1. Read [TAS Module README](../apps/control-plane/tas/README.md) - Setup
2. Review [Management Commands](../apps/control-plane/tas/management/commands/README.md)
3. Practice with `load_qualifications --clear`
4. Bookmark [Quick Reference](TAS_QUICK_REFERENCE.md) for daily use

### For Database Administrators
1. Review [Database Model](TAS_QUALIFICATION_MANAGEMENT.md#database-model)
2. Study [SQL Examples](TAS_QUALIFICATION_MANAGEMENT.md#sql-examples)
3. Understand [Maintenance Tasks](TAS_QUALIFICATION_MANAGEMENT.md#maintenance-tasks)
4. Review backup and recovery procedures

## 🔄 Version History

### Version 2.0 (October 26, 2025) - Current
- ✨ Dynamic qualification loading system
- 📊 Database-backed cache
- 🛠️ Management command implementation
- 📚 Complete documentation suite
- 🎯 8 initial qualifications loaded

### Version 1.0 (Prior)
- Static hardcoded qualification data
- Limited to 3 qualifications
- Required code changes for updates

## 📝 Change Log

See `CHANGELOG.md` for detailed change history.

---

**Documentation Version:** 1.0  
**Last Updated:** October 26, 2025  
**Maintained by:** NextCore AI Cloud Team  
**Status:** Production Ready ✅
