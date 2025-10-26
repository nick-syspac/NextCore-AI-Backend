# TAS AI Integration Documentation

## Overview

The TAS (Training and Assessment Strategy) module now includes comprehensive AI integration across 9 major feature areas. This document provides a complete reference for all AI-powered capabilities.

## Architecture

### AI Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      TAS ViewSet (API)                      │
│                  20+ AI-powered endpoints                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI Service Factory                        │
│              Service instantiation & routing                │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴──────────────┐
                │                            │
      ┌─────────▼─────────┐     ┌───────────▼──────────┐
      │  Small LLM        │     │   Large LLM          │
      │  (Classification) │     │   (Content Draft)    │
      └───────────────────┘     └──────────────────────┘
                │                            │
      ┌─────────▼─────────┐     ┌───────────▼──────────┐
      │  Embeddings       │     │   RAG Engine         │
      │  (Vector Search)  │     │   (Compliance)       │
      └───────────────────┘     └──────────────────────┘
```

### AI Service Classes

1. **IntakePrefillService** - Entity extraction, TGA enrichment, cohort suggestions
2. **PackagingClusteringService** - Elective recommendations, unit clustering, timetabling
3. **TASContentDrafter** - Contextual copy, assessment blueprinting, resource mapping
4. **ComplianceRAGService** - ASQA clause coverage, trainer scoring, policy drift
5. **EvidenceService** - Minutes summarization, validation planning, version diffs
6. **QualityAnalyticsService** - LLN prediction, risk analysis, consistency checking
7. **ConversationalCopilot** - Inline Q&A, guided prompts

## Feature Areas

### 1. Intake & Prefill

**Purpose**: Automate data extraction and TAS field population

#### API Endpoints

##### Enrich TGA Snapshot
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/enrich-tga/
Content-Type: application/json

{
  "unit_code": "BSBWHS411",
  "tga_data": {
    "title": "Implement and monitor WHS policies...",
    "elements": [...],
    "knowledge_evidence": "..."
  }
}
```

**Response**:
```json
{
  "unit_code": "BSBWHS411",
  "learning_outcomes": [
    "Implement WHS consultation processes",
    "Monitor WHS performance indicators",
    "Maintain WHS records and documentation"
  ],
  "assessment_hints": [
    "Practical demonstration of consultation processes",
    "Case study analysis of WHS incident management"
  ],
  "industry_contexts": [
    "Construction sites",
    "Manufacturing facilities",
    "Office environments"
  ],
  "evidence_types": [
    "WHS policy implementation records",
    "Meeting minutes from consultation",
    "Incident investigation reports"
  ],
  "delivery_notes": "Focus on practical application in real workplace contexts",
  "enriched_at": "2024-01-15T10:30:00Z"
}
```

##### Suggest Cohort Archetype
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/suggest-cohort/
Content-Type: application/json

{
  "cohort_history": [
    {
      "completion_rate": 78,
      "avg_lln_level": 3,
      "withdrawal_reasons": ["work conflicts", "childcare issues"]
    }
  ],
  "demographics": {
    "size": 25,
    "age_range": "25-45",
    "background": "mixed employment status"
  }
}
```

**Response**:
```json
{
  "archetype": "Working Adults with Caring Responsibilities",
  "lln_support_level": "medium",
  "reasonable_adjustments": [
    "Flexible attendance options",
    "Online resource library",
    "Extended assessment deadlines"
  ],
  "risk_indicators": [
    "Irregular attendance patterns",
    "Assessment submission delays",
    "Limited engagement with online materials"
  ],
  "support_hours_per_week": 2,
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### 2. Packaging, Clustering & Timetabling

**Purpose**: Optimize unit selection and delivery scheduling

#### API Endpoints

##### Recommend Electives
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/recommend-electives/
Content-Type: application/json

{
  "qualification_code": "BSB50120",
  "job_outcomes": ["Business Manager", "Operations Coordinator"],
  "available_electives": [
    {
      "code": "BSBOPS502",
      "title": "Manage business operational plans"
    },
    {
      "code": "BSBFIN501",
      "title": "Manage budgets and financial plans"
    }
  ],
  "packaging_rules": "Select 6 electives from Group A or B"
}
```

**Response**:
```json
[
  {
    "unit_code": "BSBOPS502",
    "title": "Manage business operational plans",
    "relevance_score": 0.95,
    "rationale": "Critical for Business Manager role - directly maps to strategic planning responsibilities",
    "skills_developed": [
      "Operational planning",
      "Resource allocation",
      "Performance monitoring"
    ],
    "industry_demand": "high"
  },
  {
    "unit_code": "BSBFIN501",
    "title": "Manage budgets and financial plans",
    "relevance_score": 0.90,
    "rationale": "Essential financial management skills for both target roles",
    "skills_developed": [
      "Budget preparation",
      "Financial reporting",
      "Variance analysis"
    ],
    "industry_demand": "high"
  }
]
```

##### Cluster Units
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/cluster-units/
Content-Type: application/json

{
  "units": [
    {
      "code": "BSBWHS411",
      "title": "Implement and monitor WHS policies",
      "application": "Workplace health and safety contexts"
    },
    {
      "code": "BSBLDR411",
      "title": "Demonstrate leadership in the workplace",
      "application": "Leadership and team management"
    }
  ],
  "max_cluster_size": 4
}
```

**Response**:
```json
[
  {
    "cluster_name": "Workplace Management Essentials",
    "units": ["BSBWHS411", "BSBLDR411", "BSBOPS401"],
    "shared_elements": [
      "Communication with stakeholders",
      "Policy implementation",
      "Performance monitoring"
    ],
    "contexts": [
      "Workplace supervision",
      "Team coordination",
      "Compliance management"
    ],
    "assessment_opportunities": [
      "Integrated workplace project",
      "Case study analysis",
      "Portfolio of evidence"
    ],
    "sequence": "parallel",
    "rationale": "Common workplace management themes allow integrated delivery"
  }
]
```

##### Optimize Timetable
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/optimize-timetable/
Content-Type: application/json

{
  "clusters": [
    {
      "name": "Foundation Skills",
      "units": ["BSBCMM411", "BSBTEC404"],
      "total_hours": 80
    }
  ],
  "total_weeks": 52,
  "resources": {
    "rooms": ["Room A", "Room B", "Computer Lab"],
    "trainer_count": 3
  },
  "constraints": {
    "max_hours_per_week": 20,
    "trainer_availability": {...}
  }
}
```

**Response**:
```json
{
  "weeks": [
    {
      "week_number": 1,
      "clusters": [
        {
          "name": "Foundation Skills",
          "hours": 8,
          "room": "Computer Lab",
          "trainer": "Trainer 1"
        }
      ]
    }
  ],
  "resource_utilization": {
    "Computer Lab": 0.75,
    "Room A": 0.60
  },
  "conflicts": [],
  "recommendations": [
    "Week 12 has high assessment load - consider spreading",
    "Trainer 2 underutilized in weeks 5-8"
  ],
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### 3. Drafting TAS Content

**Purpose**: Generate audit-ready TAS sections with justifications

#### API Endpoints

##### Draft Section
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/draft-section/
Content-Type: application/json

{
  "section_type": "cohort_needs",
  "cohort_data": {
    "size": 25,
    "demographics": {...},
    "lln_assessment": "Average Level 3",
    "education_background": "Year 10-12 completion",
    "employment_status": "60% employed, 40% seeking work"
  },
  "qualification": "BSB50120 Diploma of Business",
  "delivery_context": "Blended - weekly face-to-face with online resources"
}
```

**Response**:
```json
{
  "content": "The cohort comprises 25 learners aged 25-45, primarily working adults balancing employment and study commitments. This demographic profile necessitates flexible delivery modes to accommodate diverse work schedules and family responsibilities...",
  "justifications": [
    {
      "statement": "Flexible delivery modes",
      "reason": "60% of cohort currently employed requiring evening/weekend access",
      "evidence": "Cohort survey data, enrolment forms"
    }
  ],
  "asqa_clauses_addressed": ["1.1", "1.2"],
  "word_count": 450,
  "citations": [
    {
      "source": "Cohort LLN Assessment Report",
      "reference": "Average ACSF Level 3"
    }
  ],
  "generated_at": "2024-01-15T10:30:00Z"
}
```

##### Generate Assessment Blueprint
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/assessment-blueprint/
Content-Type: application/json

{
  "unit_code": "BSBWHS411",
  "elements": [
    {
      "element": "1. Implement WHS consultation and participation processes",
      "performance_criteria": [
        "1.1 Consult with relevant parties...",
        "1.2 Facilitate effective consultation..."
      ]
    }
  ],
  "delivery_mode": "workplace",
  "industry_context": "construction industry"
}
```

**Response**:
```json
{
  "unit_code": "BSBWHS411",
  "assessment_tasks": [
    {
      "task_number": 1,
      "name": "WHS Consultation Implementation Project",
      "description": "Plan and implement a WHS consultation process in actual workplace",
      "elements_assessed": ["Element 1", "Element 2"],
      "pc_coverage": ["1.1", "1.2", "1.3", "2.1", "2.2"]
    }
  ],
  "instruments": [
    {
      "type": "practical_demonstration",
      "description": "Facilitation of WHS meeting with observation",
      "duration": "2 hours"
    },
    {
      "type": "portfolio",
      "description": "Collection of consultation records and meeting minutes",
      "duration": "ongoing"
    }
  ],
  "rubric_skeletons": [
    {
      "criterion": "Consultation Process Design",
      "performance_levels": {
        "competent": "Consultation process meets legislative requirements...",
        "not_yet_competent": "Consultation process has gaps in..."
      }
    }
  ],
  "observation_checklists": [
    {
      "element": "Element 1",
      "checklist_items": [
        "Identifies relevant parties for consultation",
        "Facilitates inclusive discussion",
        "Records consultation outcomes"
      ]
    }
  ],
  "coverage_matrix": {
    "Element 1": ["Task 1", "Task 2"],
    "Element 2": ["Task 1", "Task 3"]
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

##### Map Resources
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/map-resources/
Content-Type: application/json

{
  "unit_requirements": {
    "equipment": ["PPE", "First aid kits", "WHS signage"],
    "software": ["WHS management system"],
    "facilities": ["Training room", "Simulated workplace"]
  },
  "available_inventory": [
    {
      "item": "PPE - hard hats, safety glasses",
      "quantity": 30,
      "condition": "good"
    }
  ],
  "budget_constraints": {
    "max_per_unit": 2000
  }
}
```

**Response**:
```json
{
  "direct_matches": [
    {
      "requirement": "PPE",
      "inventory_item": "PPE - hard hats, safety glasses",
      "adequacy": "sufficient"
    }
  ],
  "substitutes": [
    {
      "requirement": "WHS management system",
      "substitute": "Excel-based tracking system",
      "adequacy_justification": "Meets learning outcomes for basic WHS record-keeping"
    }
  ],
  "gaps": [
    {
      "requirement": "Simulated workplace",
      "severity": "medium",
      "cost_estimate": 1500
    }
  ],
  "mitigation_strategies": [
    "Partner with local construction company for workplace access",
    "Use VR simulation software for hazard identification"
  ],
  "mitigation_text": "Where direct workplace access is not available, simulated environments using VR technology and case study scenarios will be utilized to ensure learners can demonstrate competency in realistic contexts.",
  "estimated_cost": 1500,
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### 4. Compliance Guardrails (RAG Engine)

**Purpose**: Ensure ASQA compliance and identify gaps

#### API Endpoints

##### Check Compliance
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/check-compliance/
Content-Type: application/json

{
  "tas_content": {
    "trainer_qualifications": "All trainers hold TAE40116...",
    "assessment_strategy": "Competency-based assessment using...",
    "industry_engagement": "Industry advisory committee meets quarterly..."
  },
  "target_clauses": ["1.1", "1.2", "1.3", "1.8"]
}
```

**Response**:
```json
{
  "overall_status": "partial",
  "clause_results": {
    "1.1": {
      "status": "compliant",
      "addressed": [
        "TAE qualification requirement",
        "Vocational competency evidence",
        "Currency mechanisms"
      ],
      "missing": [],
      "evidence_gaps": [],
      "suggested_fixes": [],
      "risk_level": "low"
    },
    "1.2": {
      "status": "partial",
      "addressed": [
        "Training strategy exists",
        "Assessment methods described"
      ],
      "missing": [
        "Volume of learning justification",
        "Modes of delivery rationale"
      ],
      "evidence_gaps": [
        "No mention of RPL/CT processes",
        "LLN support strategies not detailed"
      ],
      "suggested_fixes": [
        "Add section explaining volume of learning calculation",
        "Include RPL/CT policy reference and procedures"
      ],
      "risk_level": "medium"
    }
  },
  "priority_fixes": [
    {
      "clause": "1.2",
      "fix": "Add volume of learning justification",
      "priority": "high"
    }
  ],
  "evaluated_at": "2024-01-15T10:30:00Z"
}
```

##### Score Trainer
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/score-trainer/
Content-Type: application/json

{
  "trainer_profile": {
    "qualifications": [
      "Bachelor of Business",
      "TAE40116 Certificate IV in Training and Assessment"
    ],
    "tae_status": "current",
    "industry_experience": [
      {
        "role": "Business Operations Manager",
        "years": 8,
        "sector": "Retail"
      }
    ],
    "currency_evidence": [
      "Current employment in business operations",
      "Recent PD: Business Management Conference 2024"
    ]
  },
  "unit_requirements": {
    "unit_code": "BSBOPS502",
    "vocational_competency": "Recent business operations experience",
    "tae_requirement": "TAE40116 or TAE40110"
  }
}
```

**Response**:
```json
{
  "suitability_score": 85,
  "tae_compliant": true,
  "vocational_competency": "adequate",
  "currency_status": "current",
  "gaps": [],
  "pd_recommendations": [
    {
      "area": "Digital transformation",
      "priority": "medium",
      "rationale": "Emerging trend in business operations",
      "resources": [
        "Industry workshop: Digital Operations",
        "Online course: Agile Project Management"
      ]
    }
  ],
  "risk_level": "low",
  "generated_at": "2024-01-15T10:30:00Z"
}
```

##### Assess Facility
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/assess-facility/
Content-Type: application/json

{
  "facility_inventory": [
    {
      "name": "Training Room A",
      "capacity": 25,
      "equipment": ["Projector", "Whiteboard", "Tables/Chairs"]
    },
    {
      "name": "Computer Lab",
      "capacity": 20,
      "equipment": ["20x Windows PCs", "MS Office Suite"]
    }
  ],
  "unit_requirements": {
    "unit_code": "BSBTEC404",
    "space_requirements": "Computer lab with internet access",
    "equipment": ["Computers with MS Office", "Projector"],
    "software": ["MS Word, Excel, PowerPoint"]
  }
}
```

**Response**:
```json
{
  "adequacy_status": "adequate",
  "requirements_met": [
    "Computer lab available with 20 workstations",
    "MS Office suite installed",
    "Projection facilities available"
  ],
  "gaps": [],
  "safety_issues": [],
  "mitigation_options": [],
  "mitigation_text": "",
  "capex_needed": 0,
  "generated_at": "2024-01-15T10:30:00Z"
}
```

##### Detect Policy Drift
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/detect-policy-drift/
Content-Type: application/json

{
  "tas_policy_references": [
    {
      "name": "Assessment Validation Policy",
      "version": "2.0",
      "tas_text": "Annual validation conducted as per Policy 2.0..."
    }
  ],
  "current_policies": [
    {
      "name": "Assessment Validation Policy",
      "version": "3.0",
      "change_summary": "Updated to require 6-monthly validation for high-risk qualifications"
    }
  ]
}
```

**Response**:
```json
{
  "drifts_detected": 1,
  "drifts": [
    {
      "policy_name": "Assessment Validation Policy",
      "old_version": "2.0",
      "new_version": "3.0",
      "impact": "high",
      "affected_sections": [
        "Section 5: Validation and Moderation"
      ],
      "proposed_updates": "Update validation schedule from annual to 6-monthly for this qualification. Add text: 'As this qualification is identified as high-risk, validation activities are conducted 6-monthly as per Assessment Validation Policy v3.0, ensuring ongoing assessment quality and consistency.'",
      "risk": "high"
    }
  ],
  "high_priority_count": 1,
  "checked_at": "2024-01-15T10:30:00Z"
}
```

### 5. Evidence Pack & Audit Readiness

**Purpose**: Automate evidence collection and audit preparation

#### API Endpoints

##### Summarize Minutes
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/summarize-minutes/
Content-Type: application/json

{
  "minutes_text": "Meeting held with industry partners to discuss curriculum relevance...",
  "meeting_date": "2024-01-15",
  "attendees": [
    "John Smith - ABC Construction",
    "Jane Doe - Training Manager",
    "Bob Wilson - Industry Rep"
  ]
}
```

**Response**:
```json
{
  "meeting_date": "2024-01-15",
  "summary": "Industry partners confirmed qualification packaging remains relevant to current industry needs. Feedback provided on emerging technologies requiring integration into delivery.",
  "key_points": [
    "Digital tools integration recommended for BSBOPS units",
    "Industry requests more workplace assessment opportunities",
    "Skills shortage identified in project management"
  ],
  "tas_implications": [
    {
      "point": "Digital tools integration",
      "section": "Delivery Strategy",
      "action": "Update delivery methods to include cloud-based collaboration tools"
    }
  ],
  "actions": [
    "Update TAS delivery section with digital tools",
    "Arrange workplace assessment partnerships",
    "Add project management elective"
  ],
  "evidence_quality": "high",
  "tas_sections_to_update": [
    "Delivery Strategy",
    "Assessment Methods",
    "Industry Engagement"
  ],
  "generated_at": "2024-01-15T10:30:00Z"
}
```

##### Generate Validation Plan
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/validation-plan/
Content-Type: application/json

{
  "assessment_tasks": [
    {
      "unit_code": "BSBWHS411",
      "name": "WHS Implementation Project",
      "instrument_type": "project"
    },
    {
      "unit_code": "BSBLDR411",
      "name": "Leadership Portfolio",
      "instrument_type": "portfolio"
    }
  ],
  "cohort_size": 25,
  "last_validation_date": "2023-06-01"
}
```

**Response**:
```json
{
  "schedule": [
    {
      "month": "March 2024",
      "tasks": ["BSBWHS411 - WHS Implementation Project"],
      "validator": "External - Industry WHS Expert",
      "sample_size": 3
    },
    {
      "month": "September 2024",
      "tasks": ["BSBLDR411 - Leadership Portfolio"],
      "validator": "Internal - Senior Trainer",
      "sample_size": 3
    }
  ],
  "sample_requirements": {
    "BSBWHS411": {
      "sample_size": 3,
      "selection_method": "random from completed assessments"
    }
  },
  "validator_assignments": [
    {
      "name": "External WHS Expert",
      "tasks": ["BSBWHS411"],
      "type": "external"
    }
  ],
  "meeting_dates": [
    "2024-04-15 - Post-validation moderation meeting",
    "2024-10-15 - Annual validation review"
  ],
  "documentation_requirements": [
    "Validation report template",
    "Sample assessment marking",
    "Validator feedback forms",
    "Action items register"
  ],
  "email_templates": {
    "validator_invitation": "Dear [Validator Name], You are invited to participate in assessment validation for [Unit Code]..."
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

##### Explain Version Changes
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/explain-changes/
Content-Type: application/json

{
  "old_version": {
    "delivery_mode": "Face-to-face only",
    "assessment_methods": ["Projects", "Written tests"]
  },
  "new_version": {
    "delivery_mode": "Blended - face-to-face and online",
    "assessment_methods": ["Projects", "Written tests", "Online quizzes"]
  }
}
```

**Response**:
```json
{
  "summary": "Version 2.0 introduces blended delivery model and online assessment methods in response to cohort feedback and industry best practice.",
  "changes": [
    {
      "field": "delivery_mode",
      "description": "Delivery mode expanded from face-to-face only to blended approach",
      "reason": "compliance",
      "rationale": "Cohort feedback indicated 60% preferred flexible online access; blended model increases accessibility while maintaining quality",
      "impact_delivery": "Requires development of online learning resources and LMS setup",
      "impact_assessment": "Minimal - core assessments remain workplace-based"
    },
    {
      "field": "assessment_methods",
      "description": "Added online quizzes as formative assessment tool",
      "reason": "quality",
      "rationale": "Provides timely feedback on knowledge acquisition; supports learner progress monitoring",
      "impact_delivery": "Trainers require PD on online quiz design",
      "impact_assessment": "Formative only - does not replace summative assessments"
    }
  ],
  "rationale_draft": "This TAS update responds to learner feedback and incorporates contemporary delivery practices. The blended delivery model addresses the needs of working learners while maintaining rigorous workplace-based assessment. Online quizzes provide formative feedback without compromising assessment validity.",
  "impact_analysis": {
    "delivery": "medium - requires resource development",
    "assessment": "low - maintains existing rigor",
    "compliance": "positive - enhances accessibility"
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### 6. Quality & Risk Analytics

**Purpose**: Predict risks and maintain quality

#### API Endpoints

##### Predict LLN Risk
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/predict-lln-risk/
Content-Type: application/json

{
  "cohort_data": {
    "avg_lln_score": 2.5,
    "demographics": {
      "age_range": "18-25",
      "education_background": "Year 10-11"
    },
    "background": "School leavers, limited work experience"
  },
  "historical_cohorts": [
    {
      "avg_lln_score": 2.8,
      "completion_rate": 65,
      "support_hours": 3
    }
  ]
}
```

**Response**:
```json
{
  "risk_level": "high",
  "support_hours_per_week": 4,
  "interventions": [
    "Weekly LLN workshops on workplace communication",
    "One-on-one tutoring for learners scoring below Level 2",
    "Scaffolded reading resources with glossaries",
    "Extended time for written assessments"
  ],
  "at_risk_count": 8,
  "budget_estimate": 12000,
  "success_probability": {
    "with_support": 0.75,
    "without_support": 0.55
  },
  "generated_at": "2024-01-15T10:30:00Z"
}
```

##### Analyze Completion Risk
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/completion-risk/
Content-Type: application/json

{
  "clusters": [
    {
      "name": "Core Business Skills",
      "units": ["BSBCMM411", "BSBWRT411"],
      "total_hours": 120
    }
  ],
  "delivery_schedule": {
    "week_12": {
      "clusters": ["Core Business Skills", "WHS Cluster"],
      "total_hours": 16,
      "assessments_due": 4
    }
  }
}
```

**Response**:
```json
{
  "overall_risk": "medium",
  "high_risk_periods": [
    {
      "week": 12,
      "issue": "Assessment overload - 4 major assessments due",
      "risk_score": 0.75,
      "impact": "High withdrawal risk"
    }
  ],
  "prerequisite_issues": [],
  "pacing_analysis": {
    "weeks_1_to_10": "appropriate",
    "weeks_11_to_15": "too dense",
    "weeks_16_to_20": "too sparse"
  },
  "recommendations": [
    "Spread week 12 assessments across weeks 10-14",
    "Move WHS assessment to week 15",
    "Add formative checkpoints in weeks 16-20"
  ],
  "alternative_schedules": [
    {
      "description": "Balanced load distribution",
      "changes": [
        "Move BSBWHS assessment from week 12 to week 15",
        "Introduce mid-cluster reviews in sparse weeks"
      ],
      "expected_risk_reduction": 0.35
    }
  ],
  "generated_at": "2024-01-15T10:30:00Z"
}
```

##### Check System Consistency
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/check-consistency/
Content-Type: application/json

{
  "tas_data": {
    "units": ["BSBWHS411", "BSBLDR411"],
    "total_hours": 200
  },
  "lms_data": {
    "units": ["BSBWHS411", "BSBLDR412"],
    "total_hours": 200
  },
  "assessment_tools": [
    {
      "unit": "BSBWHS411",
      "tool_name": "WHS Implementation Project"
    }
  ]
}
```

**Response**:
```json
{
  "consistent": false,
  "discrepancies": [
    {
      "type": "unit_mismatch",
      "severity": "high",
      "tas_value": ["BSBWHS411", "BSBLDR411"],
      "lms_value": ["BSBWHS411", "BSBLDR412"],
      "recommendation": "LMS has BSBLDR412 but TAS specifies BSBLDR411 - update LMS to match TAS"
    }
  ],
  "high_priority_count": 1,
  "checked_at": "2024-01-15T10:30:00Z"
}
```

### 7. Conversational Co-pilot

**Purpose**: Provide inline AI assistance

#### API Endpoints

##### Ask AI
```http
POST /api/tenants/{tenant_slug}/tas/{id}/ai/ask/
Content-Type: application/json

{
  "question": "Why is this cluster non-compliant?",
  "context": {
    "section": "unit_clustering",
    "unit": "BSBWHS411",
    "qualification": "BSB50120",
    "current_text": "Units clustered: BSBWHS411, BSBFIN501, BSBOPS502"
  }
}
```

**Response**:
```json
{
  "answer": "This cluster may have compliance concerns because it combines units from very different contexts (WHS, Finance, Operations) without clear pedagogical justification. ASQA Standard 1.2 requires that training and assessment strategies demonstrate how units will be delivered in a coherent, integrated manner. These units have limited shared knowledge or skills, making integrated assessment challenging.",
  "asqa_clauses": ["1.2"],
  "best_practices": [
    "Cluster units with shared industry contexts",
    "Identify common knowledge/skills for integrated assessment",
    "Justify clustering with clear pedagogical rationale"
  ],
  "example_text": "These units are clustered because they share common workplace contexts in business operations management. The cluster enables integrated assessment through a workplace project where learners demonstrate WHS compliance while managing operational plans.",
  "resources": [
    "TAS_CLUSTERING_GUIDE.md",
    "ASQA_Standard_1.2_Guidance.pdf"
  ],
  "generated_at": "2024-01-15T10:30:00Z"
}
```

## Implementation Notes

### Model Selection

- **Small LLM (Fast)**: Use for classification, checklists, scoring
  - Examples: GPT-3.5-turbo, Claude-instant
  - Typical use: Risk scoring, compliance checks, entity extraction
  
- **Large LLM (High Quality)**: Use for content drafting, explanations
  - Examples: GPT-4o, Claude-3-opus
  - Typical use: TAS section drafting, assessment blueprints, rationale generation

### Embeddings & Vector Search

- **Embedding Model**: text-embedding-3-small or text-embedding-3-large
- **Vector Database**: Recommended options:
  - PostgreSQL with pgvector extension
  - Pinecone
  - Weaviate
  - Qdrant

### Data to Index

1. **ASQA Standards**: All Standards for RTOs 2015 clauses
2. **RTO Policies**: Current policy documents and procedures
3. **Industry Minutes**: Meeting notes and engagement records
4. **Unit Snapshots**: TGA unit descriptors, elements, PC, KS, FS
5. **Historical TAS**: Previous approved TAS documents for reference

### Safety Rails

1. **Citation Tracking**: Always include source references in responses
2. **Human-in-the-Loop**: AI suggestions require human approval before publication
3. **Hallucination Prevention**: Use RAG (Retrieval-Augmented Generation) to ground responses in actual documents
4. **Audit Trail**: Log all AI operations with timestamps and inputs
5. **Version Control**: Maintain snapshots before AI-suggested changes

### Privacy & Security

- **Data Residency**: Process AI requests in-region (Australia)
- **PII Redaction**: Automatically redact personal information from evidence summaries
- **Immutable Logs**: Store all AI interactions for audit purposes
- **Access Controls**: Restrict AI features to authorized staff only

## Quick Wins to Implement First

### Priority 1: Compliance RAG Engine
```python
# Quick implementation for clause coverage
from tas.ai_services import AIServiceFactory

service = AIServiceFactory.get_service('compliance_rag')
result = service.evaluate_clause_coverage(
    tas_content={'trainer_qualifications': '...'},
    target_clauses=['1.1', '1.2']
)
```

### Priority 2: Assessment Mapper
```python
# Generate assessment blueprint
service = AIServiceFactory.get_service('content_drafter')
blueprint = service.generate_assessment_blueprint(
    unit_code='BSBWHS411',
    elements=[...],
    delivery_mode='workplace',
    industry_context='construction'
)
```

### Priority 3: Minutes Summarizer
```python
# Automate evidence pack creation
service = AIServiceFactory.get_service('evidence')
summary = service.summarize_industry_minutes(
    minutes_text='...',
    meeting_date='2024-01-15',
    attendees=[...]
)
```

### Priority 4: Trainer Suitability Checker
```python
# Score trainer against unit requirements
service = AIServiceFactory.get_service('compliance_rag')
score = service.score_trainer_suitability(
    trainer_profile={...},
    unit_requirements={...}
)
```

### Priority 5: Policy Drift Detector
```python
# Detect when policies change
service = AIServiceFactory.get_service('compliance_rag')
drifts = service.detect_policy_drift(
    tas_policy_references=[...],
    current_policies=[...]
)
```

## Testing AI Features

### Unit Testing
```python
# test_ai_services.py
from tas.ai_services import IntakePrefillService

def test_enrich_tga_snapshot():
    service = IntakePrefillService()
    result = service.enrich_tga_snapshot(
        'BSBWHS411',
        {'title': '...', 'elements': [...]}
    )
    assert 'learning_outcomes' in result
    assert len(result['learning_outcomes']) >= 3
```

### Integration Testing
```bash
# Test API endpoints
curl -X POST http://localhost:8000/api/tenants/acme-college/tas/1/ai/enrich-tga/ \
  -H "Content-Type: application/json" \
  -d '{"unit_code": "BSBWHS411", "tga_data": {...}}'
```

## Performance Optimization

### Caching Strategy
- Cache embeddings for frequently accessed documents
- Store AI responses for common queries
- Implement Redis cache for session data

### Rate Limiting
```python
# Implement rate limiting to control AI API costs
from django.core.cache import cache

def rate_limited_ai_call(user_id, limit=10, window=3600):
    key = f'ai_calls:{user_id}'
    calls = cache.get(key, 0)
    if calls >= limit:
        raise RateLimitExceeded()
    cache.set(key, calls + 1, window)
```

### Batch Processing
- Process multiple units in single API call where possible
- Use async processing for long-running operations
- Queue AI tasks using Celery for background processing

## Cost Management

### Estimated API Costs (OpenAI GPT-4)

| Operation | Tokens | Cost/Call | Monthly Estimate (100 users) |
|-----------|--------|-----------|------------------------------|
| TGA Enrichment | 2000 | $0.06 | $600 |
| Assessment Blueprint | 3000 | $0.09 | $900 |
| Compliance Check | 4000 | $0.12 | $1,200 |
| Cohort Suggestion | 1500 | $0.045 | $450 |
| Content Drafting | 2500 | $0.075 | $750 |

**Total Monthly Estimate**: ~$3,900 for 100 active users

### Cost Reduction Strategies
1. Use GPT-3.5-turbo for non-critical operations (90% cheaper)
2. Implement aggressive caching
3. Batch similar requests
4. Use smaller context windows where possible
5. Consider open-source LLMs for internal deployment

## Roadmap

### Phase 1 (Current) - Foundation
- ✅ AI service architecture
- ✅ 20+ API endpoints
- ✅ Basic RAG engine
- ✅ Documentation

### Phase 2 (Next 3 months) - OpenAI Integration
- Implement actual OpenAI API calls
- Build vector database for policies/standards
- Add embeddings for semantic search
- Production rate limiting and caching

### Phase 3 (3-6 months) - Advanced Features
- ML models for risk prediction
- Advanced timetable optimization algorithms
- Trainer-unit recommendation system
- LMS/SMS integration for consistency checks

### Phase 4 (6-12 months) - Enterprise Scale
- Multi-model support (Anthropic, Cohere, etc.)
- On-premise LLM deployment option
- Advanced analytics dashboard
- Automated workflow orchestration

## Support & Resources

### Documentation
- `/docs/TAS_AI_INTEGRATION.md` (this file)
- `/docs/TAS_DOCUMENTATION_INDEX.md` - Complete documentation index
- `/apps/control-plane/tas/README.md` - Module overview

### Code Examples
- `/apps/control-plane/tas/ai_services.py` - AI service implementations
- `/apps/control-plane/tas/views.py` - API endpoint implementations

### Getting Help
- Check logs: `/logs/tas_ai.log`
- Review API documentation: `/docs/API_DOCUMENTATION.md`
- Contact: RTO support team

---

**Version**: 1.0  
**Last Updated**: January 2025  
**Author**: NextCore AI Cloud Team
