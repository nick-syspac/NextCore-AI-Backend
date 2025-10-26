# TAS Qualification Management System

## Overview

The TAS (Training and Assessment Strategy) system uses a **database-backed qualification cache** to dynamically load qualification codes and their associated units of competency. This approach provides flexibility, scalability, and maintainability for managing Australian vocational qualifications from training.gov.au.

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                        │
│  User selects qualification → API request for units         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Django REST API                             │
│  GET /api/tenants/{slug}/tas/units/?qualification_code=X   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              QualificationCache Model                        │
│  • qualification_code (indexed)                              │
│  • qualification_title                                       │
│  • training_package (BSB, ICT, CHC, etc.)                   │
│  • groupings (JSON: core/elective units)                    │
│  • last_updated, source                                      │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│           Management Command (Optional)                      │
│  python manage.py load_qualifications                        │
│  • Populates/updates cache from curated data                │
│  • Can be extended to scrape training.gov.au                │
└─────────────────────────────────────────────────────────────┘
```

## Database Model

### QualificationCache

Located in: `apps/control-plane/tas/models.py`

```python
class QualificationCache(models.Model):
    """Cached qualification and units data from training.gov.au"""
    
    # Identification
    qualification_code = models.CharField(max_length=20, unique=True, db_index=True)
    qualification_title = models.CharField(max_length=500)
    training_package = models.CharField(max_length=20, blank=True)
    aqf_level = models.CharField(max_length=50, blank=True)
    
    # Packaging information
    packaging_rules = models.TextField(blank=True)
    has_groupings = models.BooleanField(default=False)
    
    # Units structure (JSON)
    groupings = models.JSONField(default=list)
    
    # Metadata
    source = models.CharField(max_length=50, default='training.gov.au')
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    release_date = models.DateField(null=True, blank=True)
```

### Groupings JSON Structure

```json
{
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
      "units": [
        {
          "code": "ICTCLD401",
          "title": "Configure and manage virtual computing environments",
          "type": "elective"
        }
      ]
    }
  ]
}
```

## API Endpoints

### Get Units for Qualification

**Endpoint:** `GET /api/tenants/{tenant_slug}/tas/units/`

**Query Parameters:**
- `qualification_code` (required): The qualification code (e.g., "ICT40120")

**Response:**
```json
{
  "qualification_code": "ICT40120",
  "qualification_title": "Certificate IV in Information Technology",
  "packaging_rules": "Total of 20 units: 9 core units + 11 elective units...",
  "has_groupings": true,
  "groupings": [
    {
      "name": "Core Units",
      "type": "core",
      "required": 9,
      "units": [...]
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

**Error Responses:**
- `400 Bad Request`: Missing qualification_code parameter
- `404 Not Found`: Qualification code not in cache
- `500 Internal Server Error`: Server error

### Example Request

```bash
curl -X GET "http://localhost:8000/api/tenants/acme-college/tas/units/?qualification_code=ICT40120"
```

## Management Commands

### load_qualifications

Populates or updates the qualification cache with curated data.

**Location:** `apps/control-plane/tas/management/commands/load_qualifications.py`

#### Usage

**Basic load (creates or updates):**
```bash
python manage.py load_qualifications
```

**Clear existing cache and reload:**
```bash
python manage.py load_qualifications --clear
```

**Specify custom source identifier:**
```bash
python manage.py load_qualifications --source "manual_entry_2025"
```

#### Output Example

```
📚 Loading qualification data...
  ✅ Created: ICT40120 - Certificate IV in Information Technology
  ✅ Created: BSB50120 - Diploma of Business
  ✅ Created: CHC50113 - Diploma of Early Childhood Education and Care
  🔄 Updated: SIT50416 - Diploma of Hospitality Management
  
✨ Complete! Created: 7, Updated: 1
```

## Adding New Qualifications

### Method 1: Update Management Command (Recommended)

1. **Edit the command file:**
   ```bash
   vim apps/control-plane/tas/management/commands/load_qualifications.py
   ```

2. **Add qualification to `get_qualifications_data()` method:**
   ```python
   def get_qualifications_data(self):
       return [
           # ... existing qualifications ...
           {
               'qualification_code': 'SIT30616',
               'qualification_title': 'Certificate III in Hospitality',
               'training_package': 'SIT',
               'aqf_level': 'certificate_iii',
               'packaging_rules': 'Total of 15 units: 8 core + 7 elective',
               'has_groupings': False,
               'groupings': [
                   {
                       'name': 'Core Units',
                       'type': 'core',
                       'required': 8,
                       'units': [
                           {'code': 'SITXFSA001', 'title': 'Use hygienic practices...', 'type': 'core'},
                           # ... more units ...
                       ]
                   },
                   {
                       'name': 'Elective Units',
                       'type': 'elective',
                       'required': 7,
                       'description': 'Select 7 elective units',
                       'units': [
                           {'code': 'SITHCCC001', 'title': 'Use food preparation...', 'type': 'elective'},
                           # ... more units ...
                       ]
                   }
               ]
           }
       ]
   ```

3. **Run the command:**
   ```bash
   python manage.py load_qualifications
   ```

### Method 2: Django Admin Interface

1. Navigate to: `http://localhost:8000/admin/tas/qualificationcache/`
2. Click "Add Qualification Cache"
3. Fill in the form:
   - Qualification code
   - Qualification title
   - Training package
   - Groupings (JSON format)
4. Save

### Method 3: Django Shell

```python
python manage.py shell

from tas.models import QualificationCache

QualificationCache.objects.create(
    qualification_code='HLT33015',
    qualification_title='Certificate III in Allied Health Assistance',
    training_package='HLT',
    aqf_level='certificate_iii',
    packaging_rules='Total of 13 units: 6 core + 7 elective',
    has_groupings=False,
    groupings=[
        {
            'name': 'Core Units',
            'type': 'core',
            'required': 6,
            'units': [
                {'code': 'CHCDIV001', 'title': 'Work with diverse people', 'type': 'core'},
                {'code': 'CHCCOM005', 'title': 'Communicate and work in health...', 'type': 'core'},
                # ... more units
            ]
        },
        {
            'name': 'Elective Units',
            'type': 'elective',
            'required': 7,
            'description': 'Select 7 elective units',
            'units': [
                {'code': 'HLTAAP001', 'title': 'Recognise healthy body systems', 'type': 'elective'},
                # ... more units
            ]
        }
    ],
    source='manual',
    is_active=True
)
```

## Querying the Cache

### Python/Django Examples

```python
from tas.models import QualificationCache

# Get single qualification
qual = QualificationCache.objects.get(qualification_code='ICT40120')
print(qual.qualification_title)
print(f"Has {len(qual.groupings)} groupings")

# Get all active qualifications in a training package
ict_quals = QualificationCache.objects.filter(
    training_package='ICT',
    is_active=True
)

# Get all active qualifications
all_quals = QualificationCache.objects.filter(is_active=True)

# Get units data for API response
units_data = qual.get_units_data()
```

### SQL Examples

```sql
-- List all cached qualifications
SELECT qualification_code, qualification_title, training_package, last_updated
FROM tas_qualification_cache
WHERE is_active = true
ORDER BY qualification_code;

-- Count units per qualification
SELECT 
    qualification_code,
    qualification_title,
    jsonb_array_length(groupings) as num_groupings
FROM tas_qualification_cache;

-- Find qualifications with groupings/majors
SELECT qualification_code, qualification_title
FROM tas_qualification_cache
WHERE has_groupings = true;

-- Recently updated qualifications
SELECT qualification_code, qualification_title, last_updated
FROM tas_qualification_cache
ORDER BY last_updated DESC
LIMIT 10;
```

## Frontend Integration

### React/Next.js Implementation

The frontend automatically loads units when a user selects a qualification:

```typescript
// When qualification is selected
const loadUnitsForQualification = async (qualCode: string) => {
  setLoadingUnits(true);
  
  try {
    const response = await fetch(
      `/api/tenants/${tenantSlug}/tas/units/?qualification_code=${qualCode}`
    );
    
    if (!response.ok) {
      if (response.status === 404) {
        setUnitsData({ groupings: [] });
        return;
      }
      throw new Error('Failed to load units');
    }
    
    const data = await response.json();
    setUnitsData(data);
    
    // Auto-select core units (disabled checkboxes)
    const coreUnits = data.groupings
      .find(g => g.type === 'core')?.units || [];
    setSelectedUnits(coreUnits.map(u => u.code));
    
  } catch (error) {
    console.error('Error loading units:', error);
  } finally {
    setLoadingUnits(false);
  }
};
```

## Maintenance Tasks

### Update Existing Qualifications

When training.gov.au releases new packaging rules or units:

```bash
# Clear and reload all
python manage.py load_qualifications --clear

# Or update specific qualification via Django shell
python manage.py shell
>>> from tas.models import QualificationCache
>>> qual = QualificationCache.objects.get(qualification_code='ICT40120')
>>> qual.groupings = [...]  # Updated structure
>>> qual.save()
```

### Deactivate Superseded Qualifications

```python
from tas.models import QualificationCache

# Deactivate old qualification
old_qual = QualificationCache.objects.get(qualification_code='ICT40118')
old_qual.is_active = False
old_qual.save()
```

### Bulk Import from CSV

Create a script for bulk imports:

```python
import csv
import json
from tas.models import QualificationCache

with open('qualifications.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        QualificationCache.objects.update_or_create(
            qualification_code=row['code'],
            defaults={
                'qualification_title': row['title'],
                'training_package': row['package'],
                'aqf_level': row['aqf_level'],
                'packaging_rules': row['packaging_rules'],
                'groupings': json.loads(row['groupings_json']),
                'is_active': True,
                'source': 'bulk_import'
            }
        )
```

## Future Enhancements

### 1. Training.gov.au API Integration

```python
# Future scraper service
class TrainingGovAuAPI:
    def fetch_qualification(self, code):
        # Call training.gov.au API
        # Parse response
        # Return structured data
        pass
    
    def sync_all_qualifications(self):
        # Periodic sync job
        pass
```

### 2. Automated Scheduled Updates

```python
# Celery task for periodic updates
@shared_task
def sync_qualifications():
    api = TrainingGovAuAPI()
    updated_count = api.sync_all_qualifications()
    return f"Updated {updated_count} qualifications"
```

### 3. Version History

Track changes to qualifications over time:

```python
class QualificationVersion(models.Model):
    qualification = models.ForeignKey(QualificationCache, on_delete=models.CASCADE)
    version_number = models.IntegerField()
    groupings_snapshot = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### 4. Unit Details Cache

Cache individual unit details:

```python
class UnitCache(models.Model):
    unit_code = models.CharField(max_length=20, unique=True)
    unit_title = models.CharField(max_length=500)
    elements = models.JSONField()  # Performance criteria, knowledge evidence
    prerequisites = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)
```

## Troubleshooting

### Issue: Units not loading for a qualification

**Check 1: Is qualification in cache?**
```bash
python manage.py shell
>>> from tas.models import QualificationCache
>>> QualificationCache.objects.filter(qualification_code='ICT40120').exists()
```

**Check 2: Is qualification active?**
```python
>>> qual = QualificationCache.objects.get(qualification_code='ICT40120')
>>> qual.is_active
```

**Check 3: Check API logs**
```bash
# View Django logs
tail -f /path/to/django.log | grep "units"
```

### Issue: Duplicate qualifications

```python
# Find duplicates
from django.db.models import Count
from tas.models import QualificationCache

dupes = QualificationCache.objects.values('qualification_code').annotate(
    count=Count('id')
).filter(count__gt=1)

print(dupes)

# Remove duplicates (keep newest)
for dupe in dupes:
    quals = QualificationCache.objects.filter(
        qualification_code=dupe['qualification_code']
    ).order_by('-last_updated')
    # Keep first, delete rest
    quals.exclude(id=quals.first().id).delete()
```

### Issue: JSON structure errors

Validate JSON structure:

```python
from tas.models import QualificationCache
import json

for qual in QualificationCache.objects.all():
    try:
        # Validate structure
        assert isinstance(qual.groupings, list)
        for group in qual.groupings:
            assert 'name' in group
            assert 'type' in group
            assert 'units' in group
            assert isinstance(group['units'], list)
    except AssertionError as e:
        print(f"Invalid structure for {qual.qualification_code}: {e}")
```

## Best Practices

1. **Always test in development first** before loading to production
2. **Backup database** before running `--clear` option
3. **Use source parameter** to track data origin
4. **Set is_active=False** instead of deleting superseded qualifications
5. **Document packaging rule changes** in packaging_rules field
6. **Keep groupings structure consistent** across all qualifications
7. **Use management commands** rather than direct database manipulation
8. **Monitor last_updated** field to track stale data

## Support

For issues or questions:
- Check the troubleshooting section above
- Review Django logs: `/path/to/django.log`
- Inspect database directly: `python manage.py dbshell`
- Contact: RTO systems team

---

**Last Updated:** October 26, 2025  
**Version:** 1.0  
**Maintained by:** NextCore AI Cloud Team
