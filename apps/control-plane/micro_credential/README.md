# Micro-Credential Builder

**TrainAI Suite Tool #6**

## Overview

The Micro-Credential Builder automates the creation of short courses from training package units using AI-powered curriculum compression and intelligent metadata tagging.

## Features

### Core Capabilities
- **Curriculum Compression**: Automatically compress full training package units into focused short courses
- **Metadata Tagging**: Intelligent extraction and tagging of skills, industry sectors, and competencies
- **Rapid Course Creation**: Generate new micro-credentials in minutes, not hours
- **AI-Powered Generation**: Leverage LLMs to create learning outcomes, assessment tasks, and course structure

### Course Management
- Create micro-credentials from 1 or more training package units
- Customize duration, delivery mode, and target audience
- Track drafts, published courses, and enrollments
- Version control for course iterations
- Duplicate and modify existing courses

### Key Components

#### 1. Course Generation
- **Input**: Select training package unit codes (e.g., ICTICT418, BSBXCS404)
- **Compression**: AI analyzes unit elements and compresses to essential competencies
- **Output**: Complete micro-credential with:
  - Course title and description
  - Learning outcomes (derived from unit elements)
  - Compressed curriculum structure (modules and topics)
  - Assessment strategy and tasks
  - Skills covered and industry mapping
  - Metadata tags for searchability

#### 2. Curriculum Compression
Transforms full training package units into focused learning experiences:
- **Foundation Skills** (30% of duration): Industry context, safety, basic procedures
- **Core Competencies** (50% of duration): Practical application, skills development
- **Advanced Application** (20% of duration): Complex scenarios, integration

#### 3. Assessment Mapping
Auto-generates assessment strategy:
- **Knowledge Assessment** (40%): Written questions covering key concepts
- **Practical Demonstration** (60%): Workplace or simulated environment tasks
- Maps assessment tasks back to source unit elements

#### 4. Metadata & Tagging
Intelligent extraction of:
- **Skills Covered**: Extracted from unit elements (e.g., "Plan and prepare for work")
- **Industry Sectors**: Auto-detected from unit prefixes (ICT → Information Technology)
- **Tags**: Searchable keywords for categorization
- **AQF Level**: Equivalent Australian Qualifications Framework level

## Technical Implementation

### Backend (Django)

**Models** (`micro_credential/models.py`):
```python
MicroCredential          # Main course model
MicroCredentialVersion   # Version history
MicroCredentialEnrollment # Student tracking
```

**API Endpoints** (`/api/tenants/{slug}/micro-credentials/`):
- `GET /` - List all micro-credentials
- `POST /` - Create new micro-credential
- `GET /{id}/` - Get micro-credential details
- `PUT /{id}/` - Update micro-credential
- `DELETE /{id}/` - Delete micro-credential
- `POST /generate_from_units/` - AI-generate from unit codes
- `POST /{id}/publish/` - Publish a course
- `POST /{id}/duplicate/` - Duplicate a course
- `GET /{id}/versions/` - View version history
- `GET /enrollments/` - List enrollments

**Key Fields**:
- `source_units`: Array of training package units used
- `compressed_content`: Structured curriculum data
- `learning_outcomes`: List of specific learning outcomes
- `assessment_tasks`: Assessment strategy with element mapping
- `tags`, `skills_covered`, `industry_sectors`: Metadata
- `duration_hours`: Target course length
- `delivery_mode`: online, face_to_face, blended, workplace

### Frontend (Next.js)

**Page**: `/dashboard/[tenantSlug]/micro-credential/page.tsx`

**Features**:
- 📊 Dashboard with statistics (total courses, published, drafts, enrollments)
- 🎨 Card-based course listing with status indicators
- ✨ AI generation modal for creating new courses
- 📖 Detailed course view modal
- 🏷️ Visual tags for skills, industries, and metadata

**User Flow**:
1. Click "Generate New Course"
2. Enter unit codes (e.g., ICTICT418, BSBXCS404)
3. Optional: Customize title, duration, delivery mode, audience
4. AI generates complete micro-credential structure
5. Review, edit, and publish

## Use Cases

### 1. Targeted Upskilling
Create focused courses for specific skill gaps:
- **Example**: Cybersecurity fundamentals from BSB and ICT units
- **Duration**: 40 hours instead of 200+ hours for full qualification
- **Outcome**: Faster time-to-competency

### 2. Modular Learning Pathways
Break down full qualifications into bite-sized courses:
- **Example**: Certificate IV split into 6 micro-credentials
- **Benefit**: Flexible, stackable learning options
- **Market**: Appeals to time-poor professionals

### 3. Industry-Specific Training
Combine units from multiple training packages:
- **Example**: Project management + IT + business units
- **Outcome**: Hybrid courses matching industry needs
- **Differentiation**: Unique course offerings

### 4. Rapid Market Response
Create new courses quickly as industry demands shift:
- **Traditional**: Weeks to design a short course
- **With AI**: Minutes to generate, hours to refine
- **Advantage**: First-to-market with emerging skill areas

## AI Generation Process

### Input Processing
1. Accept unit codes from user
2. Fetch unit details from training.gov.au (or database)
3. Extract elements, performance criteria, knowledge, and skills

### Curriculum Compression
1. **Identify Core Competencies**: LLM analyzes unit elements for key skills
2. **Remove Duplication**: Merge overlapping content from multiple units
3. **Prioritize**: Focus on most critical competencies for target duration
4. **Structure**: Create logical learning modules (foundation → core → advanced)

### Learning Outcomes Generation
1. Transform unit elements into learner-facing outcomes
2. Example: "Plan and prepare for work" → "Apply planning and preparation techniques in workplace contexts"
3. Ensure SMART (Specific, Measurable, Achievable, Relevant, Time-bound)

### Assessment Design
1. Map learning outcomes to assessment tasks
2. Create knowledge assessment (written) and practical demonstration
3. Ensure coverage of all source unit elements
4. Weight assessments appropriately (40/60 split)

### Metadata Extraction
1. **Skills**: Extract from unit elements
2. **Industries**: Map from unit code prefixes (ICT, BSB, FNS, etc.)
3. **Tags**: Generate from title, units, and content analysis
4. **AQF Level**: Infer from source unit levels

## Status Management

Micro-credentials progress through lifecycle stages:
- **Draft**: Initial creation, editable
- **In Review**: Under review by subject matter experts
- **Approved**: Quality assured, ready to publish
- **Published**: Active and available for enrollment
- **Archived**: No longer offered, historical record

## Integration Points

### Training.gov.au API
- Fetch current unit of competency details
- Ensure compliance with latest training package versions
- Auto-update when units are superseded

### LMS/SMS Systems
- Export micro-credentials as SCORM packages
- Sync enrollment data
- Track completion and competency attainment

### Assessment Builder
- Link to full assessment tools and instruments
- Generate detailed marking rubrics
- Evidence collection and validation

## Compliance & Quality

### ASQA Alignment
- Courses maintain links to source training package units
- Evidence requirements preserved through compression
- Assessment maintains coverage of all elements
- Version control ensures audit trail

### Validation Rules
- Minimum duration requirements per unit
- Assessment coverage validation
- Competency outcome mapping
- Quality assurance checkpoints

## Future Enhancements

### Planned Features
1. **AI Refinement**: Allow users to regenerate specific sections
2. **Template Library**: Save and reuse compression patterns
3. **Collaboration**: Multi-user course development workflow
4. **Analytics**: Track success rates and learner feedback
5. **Marketplace**: Share micro-credentials with other RTOs
6. **Badging**: Issue digital credentials upon completion
7. **Prerequisite Mapping**: Auto-detect and recommend pathways
8. **Cost Calculator**: Estimate pricing based on duration and resources

### Integration Roadmap
- Integration with Evidence Mapper for assessment validation
- Connection to Trainer Diary for delivery tracking
- Link to PD Tracker for trainer qualification verification
- Sync with Competency Gap Finder for curriculum coverage

## Analytics & Insights

### Course Performance Metrics
- Enrollment trends over time
- Completion rates by delivery mode
- Student satisfaction scores
- Time-to-competency averages

### Portfolio Analytics
- Most popular skills/industries
- Revenue by course type
- Conversion rates (draft → published → enrolled)
- ROI on AI generation vs manual development

## Getting Started

### For Administrators
1. Navigate to TrainAI Suite → Micro-Credential Builder
2. Click "Generate New Course"
3. Enter 1-5 unit codes from training packages
4. Customize settings or use AI defaults
5. Review generated course structure
6. Publish when ready

### For Learners
1. Browse published micro-credentials
2. Enroll in courses aligned to career goals
3. Complete learning modules
4. Submit assessments
5. Receive digital credential upon completion

## Technical Requirements

### Backend
- Django 4.x
- PostgreSQL with JSONField support
- OpenAI API access (for generation)
- Training.gov.au API credentials

### Frontend
- Next.js 14.x
- React 18.x
- TailwindCSS for styling

### Infrastructure
- Minimum 2GB RAM for AI generation
- Adequate API rate limits for OpenAI
- Database backup for version control

## Support & Documentation

- **User Guide**: See `/docs/user-guides/micro-credential-builder.md`
- **API Docs**: See `/docs/api/micro-credentials.md`
- **Video Tutorial**: Coming soon
- **Support**: Contact TrainAI Suite support team

---

**Micro-Credential Builder** is part of the TrainAI Suite - automating trainer admin, PD tracking, and curriculum development for RTOs.

**Status**: ✅ Released (v1.0)  
**Last Updated**: October 27, 2025  
**Maintained By**: NextCore AI Cloud Platform Team
