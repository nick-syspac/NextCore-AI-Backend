# TAS Template Sections Management

## Overview

The TAS Template Sections feature allows you to manage individual sections within TAS (Training and Assessment Strategy) templates. Each section can be configured with specific content types, help text, default content, and AI generation prompts.

## Model: TASTemplateSection

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `section_name` | CharField(200) | Display name for the section (e.g., "Cohort Profile") |
| `section_code` | CharField(50) | Unique code identifier (e.g., "cohort_profile") |
| `description` | TextField | Help text/context for content creators |
| `content_type` | CharField | Type of content: text, rich_text, table, list, json |
| `default_content` | TextField | Default/placeholder content for the section |
| `is_editable` | BooleanField | Whether users can edit this section (default: True) |
| `is_required` | BooleanField | Whether section is required in TAS document (default: True) |
| `section_order` | IntegerField | Display order within template (default: 0) |
| `parent_section` | ForeignKey | Parent section for nested structure (optional) |
| `gpt_prompt` | TextField | GPT-4 prompt for auto-generating this section |
| `template` | ForeignKey | Parent TASTemplate |

### Content Types

- **text**: Plain text content
- **rich_text**: HTML/rich text editor content
- **table**: Tabular data
- **list**: Bulleted or numbered lists
- **json**: Structured JSON data

## API Endpoints

### Base URL
```
/api/tenants/{tenant_slug}/tas/template-sections/
```

### 1. List Sections
```http
GET /api/tenants/{tenant_slug}/tas/template-sections/
```

**Query Parameters:**
- `template_id`: Filter by template ID
- `content_type`: Filter by content type
- `is_editable`: Filter editable sections
- `is_required`: Filter required sections
- `top_level_only=true`: Only return top-level sections (no parents)

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "template": 3,
      "section_name": "Cohort Profile",
      "section_code": "cohort_profile",
      "description": "Describe the target learner cohort",
      "content_type": "rich_text",
      "content_type_display": "Rich Text / HTML",
      "default_content": "<p>Enter cohort description...</p>",
      "is_editable": true,
      "is_required": true,
      "section_order": 1,
      "parent_section": null,
      "gpt_prompt": "Generate a cohort profile for...",
      "has_subsections": false,
      "created_at": "2025-11-02T10:00:00Z",
      "updated_at": "2025-11-02T10:00:00Z"
    }
  ]
}
```

### 2. Get Section by ID
```http
GET /api/tenants/{tenant_slug}/tas/template-sections/{id}/
```

### 3. Create Section
```http
POST /api/tenants/{tenant_slug}/tas/template-sections/
Content-Type: application/json

{
  "template": 3,
  "section_name": "Assessment Overview",
  "section_code": "assessment_overview",
  "description": "Provide a high-level overview of assessment strategy",
  "content_type": "rich_text",
  "default_content": "<p>Assessment will be conducted through...</p>",
  "is_editable": true,
  "is_required": true,
  "section_order": 5,
  "gpt_prompt": "Generate an assessment overview that includes..."
}
```

### 4. Update Section
```http
PATCH /api/tenants/{tenant_slug}/tas/template-sections/{id}/
Content-Type: application/json

{
  "section_name": "Updated Section Name",
  "section_order": 10
}
```

### 5. Delete Section
```http
DELETE /api/tenants/{tenant_slug}/tas/template-sections/{id}/
```

### 6. Get Sections by Template (Hierarchical)
```http
GET /api/tenants/{tenant_slug}/tas/template-sections/by_template/?template_id=3
```

Returns sections organized hierarchically with subsections:

```json
{
  "template": {
    "id": 3,
    "name": "Business Diploma Template",
    "aqf_level": "diploma"
  },
  "sections": [
    {
      "id": 1,
      "section_name": "Cohort Profile",
      "section_code": "cohort_profile",
      "section_order": 1,
      "subsections": [
        {
          "id": 2,
          "section_name": "Demographics",
          "section_code": "demographics",
          "parent_section": 1
        }
      ]
    }
  ]
}
```

### 7. Reorder Sections
```http
POST /api/tenants/{tenant_slug}/tas/template-sections/reorder/
Content-Type: application/json

{
  "section_orders": [
    {"id": 1, "section_order": 5},
    {"id": 2, "section_order": 1},
    {"id": 3, "section_order": 3}
  ]
}
```

**Response:**
```json
{
  "message": "Sections reordered successfully"
}
```

### 8. Duplicate Section
```http
POST /api/tenants/{tenant_slug}/tas/template-sections/{id}/duplicate/
Content-Type: application/json

{
  "target_template_id": 4  // Optional: duplicate to another template
}
```

**Response:** Returns the newly created section with "(Copy)" appended to name.

## Usage Examples

### Python/Requests

```python
import requests

base_url = "http://localhost:8000/api/tenants/acme-college/tas"
headers = {"Authorization": "Token your-token-here"}

# Create a new section
section_data = {
    "template": 3,
    "section_name": "Industry Engagement",
    "section_code": "industry_engagement",
    "description": "Document industry consultation and validation",
    "content_type": "table",
    "default_content": "",
    "is_editable": True,
    "is_required": True,
    "section_order": 8,
    "gpt_prompt": "Generate a table showing industry engagement activities..."
}

response = requests.post(
    f"{base_url}/template-sections/",
    json=section_data,
    headers=headers
)
section = response.json()

# Get all sections for a template
response = requests.get(
    f"{base_url}/template-sections/by_template/",
    params={"template_id": 3},
    headers=headers
)
sections = response.json()

# Reorder sections
reorder_data = {
    "section_orders": [
        {"id": section["id"], "section_order": 1}
    ]
}
response = requests.post(
    f"{base_url}/template-sections/reorder/",
    json=reorder_data,
    headers=headers
)
```

### JavaScript/Fetch

```javascript
const baseUrl = 'http://localhost:8000/api/tenants/acme-college/tas';
const token = 'your-token-here';

// Create section
const createSection = async () => {
  const response = await fetch(`${baseUrl}/template-sections/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`
    },
    body: JSON.stringify({
      template: 3,
      section_name: 'Resources Required',
      section_code: 'resources_required',
      description: 'List all required resources',
      content_type: 'list',
      is_editable: true,
      is_required: true,
      section_order: 6
    })
  });
  return await response.json();
};

// Get hierarchical sections
const getSections = async (templateId) => {
  const response = await fetch(
    `${baseUrl}/template-sections/by_template/?template_id=${templateId}`,
    {
      headers: { 'Authorization': `Token ${token}` }
    }
  );
  return await response.json();
};

// Duplicate section
const duplicateSection = async (sectionId, targetTemplateId) => {
  const response = await fetch(
    `${baseUrl}/template-sections/${sectionId}/duplicate/`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`
      },
      body: JSON.stringify({ target_template_id: targetTemplateId })
    }
  );
  return await response.json();
};
```

## Django Admin Interface

Sections can be managed through the Django admin at:
```
/admin/tas/tastemplatesection/
```

**Features:**
- List view with filtering by template, content type, editability
- Search by section name, code, description
- Ordered by template and section_order
- Related lookups for template and parent section

## Common Workflows

### 1. Create a New Template with Sections

```python
# 1. Create template
template = TASTemplate.objects.create(
    name="Certificate III Template",
    template_type="trade",
    aqf_level="certificate_iii",
    description="Template for trade qualifications"
)

# 2. Create sections
sections = [
    {
        "section_name": "Qualification Details",
        "section_code": "qualification_details",
        "content_type": "rich_text",
        "section_order": 1
    },
    {
        "section_name": "Cohort Profile",
        "section_code": "cohort_profile",
        "content_type": "rich_text",
        "section_order": 2
    },
    {
        "section_name": "Delivery Strategy",
        "section_code": "delivery_strategy",
        "content_type": "rich_text",
        "section_order": 3
    }
]

for section_data in sections:
    TASTemplateSection.objects.create(
        template=template,
        **section_data
    )
```

### 2. Create Nested Sections

```python
# Create parent section
parent = TASTemplateSection.objects.create(
    template=template,
    section_name="Assessment Strategy",
    section_code="assessment_strategy",
    section_order=4
)

# Create subsections
TASTemplateSection.objects.create(
    template=template,
    parent_section=parent,
    section_name="Assessment Methods",
    section_code="assessment_methods",
    section_order=1
)

TASTemplateSection.objects.create(
    template=template,
    parent_section=parent,
    section_name="Assessment Tools",
    section_code="assessment_tools",
    section_order=2
)
```

### 3. Clone Template with Sections

```python
# Clone template
new_template = TASTemplate.objects.create(
    name=f"{original_template.name} (Copy)",
    template_type=original_template.template_type,
    aqf_level=original_template.aqf_level,
    description=original_template.description
)

# Clone sections
for section in original_template.sections.all():
    TASTemplateSection.objects.create(
        template=new_template,
        section_name=section.section_name,
        section_code=section.section_code,
        description=section.description,
        content_type=section.content_type,
        default_content=section.default_content,
        is_editable=section.is_editable,
        is_required=section.is_required,
        section_order=section.section_order,
        gpt_prompt=section.gpt_prompt
    )
```

## Best Practices

1. **Use clear section codes**: Use snake_case identifiers that match the section purpose
2. **Provide helpful descriptions**: These guide content creators on what to include
3. **Set appropriate content types**: Match the content type to the expected data format
4. **Use section_order strategically**: Leave gaps (10, 20, 30) for easy insertion
5. **Leverage nested sections**: Use parent_section for logical grouping
6. **Write effective GPT prompts**: Include context, tone, and specific requirements
7. **Mark system sections as non-editable**: Protect critical compliance sections
8. **Provide good defaults**: Include example content to guide users

## Database Schema

```sql
CREATE TABLE tas_template_sections (
    id SERIAL PRIMARY KEY,
    template_id INTEGER NOT NULL REFERENCES tas_templates(id),
    section_name VARCHAR(200) NOT NULL,
    section_code VARCHAR(50) NOT NULL,
    description TEXT,
    content_type VARCHAR(20) NOT NULL DEFAULT 'rich_text',
    default_content TEXT,
    is_editable BOOLEAN NOT NULL DEFAULT TRUE,
    is_required BOOLEAN NOT NULL DEFAULT TRUE,
    section_order INTEGER NOT NULL DEFAULT 0,
    parent_section_id INTEGER REFERENCES tas_template_sections(id),
    gpt_prompt TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (template_id, section_code)
);

CREATE INDEX idx_template_sections_template_order 
    ON tas_template_sections(template_id, section_order);
CREATE INDEX idx_template_sections_code 
    ON tas_template_sections(section_code);
```

## Future Enhancements

- Section templates library (reusable across templates)
- Version control for sections
- Section-level permissions
- Content validation rules
- Section dependencies (require X before Y)
- Bulk import/export of sections
- Section usage analytics
- AI-powered section recommendations

---

**Version:** 1.0  
**Last Updated:** November 2, 2025  
**Status:** Production Ready ✅
