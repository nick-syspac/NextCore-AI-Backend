# PD Tracker

**TrainAI Suite Tool #1**

## Purpose
Professional Development (PD) Tracker automates trainer administration with comprehensive PD tracking, LLM-powered activity suggestions, compliance rule mapping, and RTO trainer currency maintenance.

## Features

### 1. PD Activity Logging
- **12 Activity Types**: Formal courses, workshops, conferences, webinars, industry placements, networking, research, mentoring, self-study, certifications, teaching observations, curriculum development
- **Compliance Mapping**: Track which activities maintain vocational, industry, and teaching currency
- **Evidence Management**: Document evidence types and verification status
- **Learning Outcomes**: Record learning outcomes, application to practice, and reflection notes
- **ASQA Compliance**: Flag activities that meet ASQA requirements

### 2. LLM-Powered PD Suggestions
- **Intelligent Recommendations**: Generate personalized PD suggestions based on trainer profile and currency gaps
- **Priority Levels**: Critical, high, medium, low priority recommendations
- **Currency Gap Analysis**: Identifies vocational, industry, or teaching currency deficiencies
- **Contextual Rationale**: Explains why each PD activity is recommended
- **Actionable Suggestions**: Includes estimated hours, costs, providers, and timeframes
- **Acceptance Workflow**: Trainers can accept, plan, or dismiss suggestions

### 3. Trainer Currency Tracking
- **Vocational Currency**: Track vocational competency with 1-year expiry (365 days)
- **Industry Currency**: Monitor industry engagement with 2-year expiry (730 days)
- **Teaching Currency**: Track teaching and assessment skills maintenance
- **Status Indicators**: Current, expiring soon (30-day warning), expired, or not applicable
- **Hours Tracking**: Total PD hours, vocational hours, industry hours, teaching hours
- **Annual Goals**: Set and track annual PD hour goals with progress percentage

### 4. Compliance Rule Mapping
- **Regulatory Sources**: ASQA Standards, VET Quality Framework, state regulations, RTO policies, industry requirements
- **Rule Types**: Minimum hours, activity types, frequency requirements, industry engagement, qualification maintenance
- **Applicability Filters**: Rules can be specific to roles, sectors, or qualification levels
- **Active/Inactive Rules**: Enable/disable rules with effective and expiry dates
- **Reference Codes**: Link rules to specific standards (e.g., "Standard 1.14")

### 5. Compliance Checking
- **Automated Checks**: Run compliance checks against all active rules
- **Compliance Scoring**: 0-100% compliance score based on requirements met
- **Hours Analysis**: Calculate hours required vs completed vs shortfall
- **Findings & Recommendations**: Detailed compliance findings with actionable recommendations
- **Risk Identification**: Flag non-compliant and at-risk trainers
- **Action Tracking**: Set deadlines and track remediation actions

### 6. Reporting & Analytics
- **Dashboard Statistics**: Total activities, hours, recent activity (30 days)
- **Currency Overview**: Count of trainers current, expiring soon, expired
- **Activity Breakdown**: Activities by type with counts
- **Monthly Trends**: Visual representation of PD hours over time
- **Top Performers**: Identify trainers meeting or exceeding goals
- **Export Reports**: Generate audit-ready compliance reports

## Data Models

### PDActivity (PD Activity Records)
- Activity number (auto-generated: PD-YYYYMMDD-XXXX)
- Trainer information (ID, name, role, department)
- Activity details (type, title, description, provider)
- Dates and hours (start, end, hours completed)
- Compliance areas (vocational, industry, teaching)
- Evidence and verification (files, status, verified by/date)
- Learning outcomes and reflection
- Status (planned, in_progress, completed, cancelled)

### TrainerProfile (Trainer PD Profile)
- Profile number (auto-generated: PROF-YYYYMMDD-XXX)
- Trainer details (ID, name, email, role, department)
- Qualifications (highest, teaching, industry)
- Teaching areas (subjects, qualification levels, sectors)
- Currency requirements (vocational, industry, teaching)
- Hours tracking (total, vocational, industry, teaching, current year)
- Currency status (current, expiring soon, expired, not applicable)
- Compliance status (meets ASQA requirements)
- Annual goals (goal hours, current hours, progress percentage)

### PDSuggestion (LLM-Generated Suggestions)
- Suggestion number (auto-generated: SUG-YYYYMMDD-XXX)
- Trainer profile (foreign key)
- Activity recommendation (type, title, description, rationale)
- Currency gap addressed (vocational, industry, teaching, compliance, skill development)
- Priority level (critical, high, medium, low)
- Suggested providers and resources
- Estimated hours and cost
- Timeline (suggested timeframe, deadline)
- LLM metadata (model, generation date, prompt, confidence score)
- Action tracking (status, trainer feedback, linked activity)

### ComplianceRule (RTO Compliance Rules)
- Rule number (auto-generated: RULE-YYYYMMDD-XXX)
- Rule metadata (name, description, regulatory source, reference code)
- Regulatory source (ASQA, VET Quality, state regulation, RTO policy, industry)
- Applicability (roles, sectors, qualifications)
- Requirement type (minimum hours, activity type, frequency, industry engagement)
- Requirement details (JSON: hours, period, activity types)
- Validation (active status, effective date, expiry date)

### ComplianceCheck (Compliance Verification Records)
- Check number (auto-generated: CHK-YYYYMMDD-XXX)
- Trainer profile (foreign key)
- Check details (date, period start/end, checked by)
- Results (overall status: compliant, at_risk, non_compliant)
- Rules (checked, met, not met)
- Findings (compliance score, hours required/completed/shortfall)
- Recommendations (actionable suggestions)
- Follow-up (requires action, deadline, actions taken)

## API Endpoints

### PDActivity Endpoints
- `GET /activities/` - List all activities (filterable by tenant, trainer_id, activity_type, status, date range)
- `POST /activities/` - Create new activity
- `GET /activities/{id}/` - Retrieve activity details
- `PUT /activities/{id}/` - Update activity
- `DELETE /activities/{id}/` - Delete activity
- `POST /activities/log_activity/` - Log activity and update trainer profile
- `POST /activities/{id}/verify_activity/` - Verify an activity

### TrainerProfile Endpoints
- `GET /profiles/` - List all profiles (filterable by tenant)
- `POST /profiles/` - Create new profile
- `GET /profiles/{id}/` - Retrieve profile details
- `PUT /profiles/{id}/` - Update profile
- `DELETE /profiles/{id}/` - Delete profile
- `POST /profiles/check_currency/` - Check trainer currency status

### PDSuggestion Endpoints
- `GET /suggestions/` - List all suggestions (filterable by trainer_id, priority, status)
- `POST /suggestions/` - Create new suggestion
- `GET /suggestions/{id}/` - Retrieve suggestion details
- `PUT /suggestions/{id}/` - Update suggestion
- `DELETE /suggestions/{id}/` - Delete suggestion
- `POST /suggestions/generate_suggestions/` - Generate LLM-powered suggestions
- `POST /suggestions/{id}/accept_suggestion/` - Accept a suggestion

### ComplianceRule Endpoints
- `GET /rules/` - List all rules (filterable by tenant, regulatory_source)
- `POST /rules/` - Create new rule
- `GET /rules/{id}/` - Retrieve rule details
- `PUT /rules/{id}/` - Update rule
- `DELETE /rules/{id}/` - Delete rule

### ComplianceCheck Endpoints
- `GET /checks/` - List all checks (filterable by trainer_id, overall_status)
- `POST /checks/` - Create new check
- `GET /checks/{id}/` - Retrieve check details
- `PUT /checks/{id}/` - Update check
- `DELETE /checks/{id}/` - Delete check
- `GET /checks/dashboard/` - Get dashboard statistics
- `POST /checks/compliance_report/` - Generate compliance report

## Frontend Features

### 1. Log Activity Tab
- Comprehensive activity logging form
- Activity type selection (12 types)
- Date and hours input
- Currency maintenance checkboxes
- Provider and description fields
- Automatic profile updates on submission

### 2. Activities Tab
- Complete activity history
- Status badges (completed, in progress, planned, cancelled)
- Verification status indicators
- Currency flags (vocational, industry, teaching)
- Compliance areas display
- Activity details with provider and dates

### 3. Suggestions Tab
- LLM-powered recommendation cards
- Priority-based color coding (critical=red, high=orange, medium=yellow, low=blue)
- Rationale explanations
- Estimated hours and timeframes
- Accept/dismiss actions
- Generate suggestions button

### 4. Currency Tab
- Vocational currency status with days remaining
- Industry currency status with expiry tracking
- Annual goal progress bar
- Last activity dates
- Visual status indicators (current=green, expiring=yellow, expired=red)

### 5. Compliance Tab
- Run compliance check button
- Compliance score visualization (0-100%)
- Hours analysis (required vs completed vs shortfall)
- Findings with alert icons
- Recommendations with checkmarks
- Overall status badges

### 6. Reports Tab
- Activity overview (total activities, total hours)
- Last 30 days statistics
- Currency status summary (current, expiring, expired counts)
- Activities by type breakdown
- Monthly hours trend visualization
- Export report functionality

## Currency Rules

### Vocational Currency
- **Duration**: 12 months (365 days)
- **Warning**: 30 days before expiry (335 days)
- **Status**: Current → Expiring Soon (30 days) → Expired
- **Requirements**: Regular PD activities maintaining vocational competency

### Industry Currency
- **Duration**: 24 months (730 days)
- **Warning**: 30 days before expiry (700 days)
- **Status**: Current → Expiring Soon (30 days) → Expired
- **Requirements**: Industry engagement activities (placements, networking, research)

### Teaching Currency
- **Requirements**: Ongoing professional development in teaching and assessment practices
- **Recommended**: Regular teaching observations, pedagogical training

## LLM Suggestion Algorithm

The PD Tracker uses a rule-based LLM approach to generate suggestions:

1. **Currency Gap Detection**: Check vocational and industry currency status
2. **Critical Suggestions**: Generate for expired currency (vocational, industry)
3. **High Priority**: Generate for expiring soon status
4. **Annual Goal Check**: Suggest activities if below annual PD goal
5. **Teaching Development**: Recommend teaching observations for ongoing improvement
6. **Prioritization**: Critical → High → Medium → Low
7. **Contextual Rationale**: Explain why each suggestion addresses trainer needs
8. **Actionable Details**: Include providers, hours, costs, timeframes

## Compliance Mapping

### ASQA Standards
- Standard 1.13: Trainers and assessors
- Standard 1.14: Industry engagement
- Standard 1.15: Training and assessment strategies

### RTO Requirements
- Vocational competency maintenance
- Industry currency requirements
- Teaching and assessment qualifications
- Continuous professional development

## Use Cases

1. **Log Workshop Attendance**: Trainer completes workshop, logs activity, updates vocational currency
2. **Currency Alert**: System detects expiring vocational currency, generates critical suggestion
3. **LLM Recommendations**: Generate 5 personalized PD suggestions based on profile gaps
4. **Compliance Audit**: Run compliance check for all trainers, generate audit report
5. **Annual Goal Tracking**: Monitor progress towards 20-hour annual PD goal
6. **Industry Placement**: Record industry placement, extend industry currency by 2 years
7. **Evidence Verification**: Upload certificates, verify PD activity completion
8. **Team Dashboard**: View currency status across all trainers, identify at-risk staff

## Integration Points

- **Trainer Management**: Links to trainer profiles and employment records
- **LMS Integration**: Import PD activities from learning management system
- **Evidence Storage**: Document management for certificates and evidence
- **Notification System**: Alerts for expiring currency and compliance deadlines
- **Reporting Tools**: Export compliance reports for ASQA audits

## Technical Details

- **Backend**: Django 5.1.2, Django REST Framework
- **Database**: PostgreSQL with JSON fields for flexible data
- **Models**: 5 models (PDActivity, TrainerProfile, PDSuggestion, ComplianceRule, ComplianceCheck)
- **API**: RESTful API with custom actions for specialized operations
- **Frontend**: Next.js 14 with TypeScript, 6-tab interface
- **Authentication**: Tenant-based authentication with trainer ID
- **Scalability**: Designed for multi-tenant RTO deployments

## Future Enhancements

1. **Enhanced LLM Integration**: Connect to GPT-4 or Claude for natural language suggestions
2. **Automated Reminders**: Email/SMS notifications for expiring currency
3. **Evidence OCR**: Automatic extraction of hours and dates from certificates
4. **Industry Provider Database**: Searchable database of PD providers
5. **Team Analytics**: Manager dashboard for team PD overview
6. **Mobile App**: iOS/Android apps for logging PD on-the-go
7. **Calendar Integration**: Sync planned PD activities with calendars
8. **Budget Tracking**: Track PD expenses and budget allocation

## Deployment

PD Tracker is deployed as part of the TrainAI Suite within the NextCore AI Cloud platform:

1. **Django App**: Installed in `control_plane.settings.INSTALLED_APPS`
2. **URL Routing**: Configured in `tenants.urls` with pattern `/tenants/<tenant_slug>/pd-tracker/`
3. **Migrations**: Applied with `python manage.py migrate pd_tracker`
4. **Admin Interface**: Registered in Django admin for data management
5. **Frontend**: Deployed at `/dashboard/<tenant_slug>/pd-tracker`
6. **Dashboard Card**: Added to main dashboard under "TrainAI Suite" section

## License

Part of the NextCore AI Cloud platform - see main LICENSE file.
