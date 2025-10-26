# TAS Qualification Management - Quick Reference

## Common Commands

### Load Qualifications into Cache
```bash
# Initial load or update
python manage.py load_qualifications

# Clear and reload all
python manage.py load_qualifications --clear

# Load with custom source
python manage.py load_qualifications --source "training.gov.au-2025"
```

### Check Cache Status
```bash
python manage.py shell
>>> from tas.models import QualificationCache
>>> QualificationCache.objects.count()
8
>>> QualificationCache.objects.filter(training_package='ICT').count()
1
```

### API Testing
```bash
# Get units for qualification
curl "http://localhost:8000/api/tenants/acme-college/tas/units/?qualification_code=ICT40120"

# Pretty print JSON response
curl -s "http://localhost:8000/api/tenants/acme-college/tas/units/?qualification_code=BSB50120" | jq '.'
```

## Quick Add Qualification

### Via Python Shell (Fastest for single additions)
```python
python manage.py shell

from tas.models import QualificationCache

QualificationCache.objects.create(
    qualification_code='SIT30616',
    qualification_title='Certificate III in Hospitality',
    training_package='SIT',
    aqf_level='certificate_iii',
    packaging_rules='Total of 15 units: 8 core + 7 elective',
    has_groupings=False,
    groupings=[
        {
            'name': 'Core Units',
            'type': 'core',
            'required': 8,
            'units': [
                {'code': 'SITXFSA001', 'title': 'Use hygienic practices for food safety', 'type': 'core'},
                {'code': 'SITXFSA002', 'title': 'Participate in safe food handling practices', 'type': 'core'},
                {'code': 'SITXWHS001', 'title': 'Participate in safe work practices', 'type': 'core'},
                {'code': 'SITXCCS003', 'title': 'Interact with customers', 'type': 'core'},
                {'code': 'SITXCOM002', 'title': 'Show social and cultural sensitivity', 'type': 'core'},
                {'code': 'BSBSUS201', 'title': 'Participate in environmentally sustainable work practices', 'type': 'core'},
                {'code': 'BSBWOR203', 'title': 'Work effectively with others', 'type': 'core'},
                {'code': 'SITHIND002', 'title': 'Source and use information on the hospitality industry', 'type': 'core'},
            ]
        },
        {
            'name': 'Elective Units',
            'type': 'elective',
            'required': 7,
            'description': 'Select 7 elective units',
            'units': [
                {'code': 'SITHCCC001', 'title': 'Use food preparation equipment', 'type': 'elective'},
                {'code': 'SITHCCC002', 'title': 'Prepare and present simple dishes', 'type': 'elective'},
                {'code': 'SITHCCC003', 'title': 'Prepare and present sandwiches', 'type': 'elective'},
                {'code': 'SITXFIN001', 'title': 'Process financial transactions', 'type': 'elective'},
                {'code': 'SITXHRM001', 'title': 'Coach others in job skills', 'type': 'elective'},
                {'code': 'SITXINV002', 'title': 'Maintain the quality of perishable items', 'type': 'elective'},
            ]
        }
    ],
    is_active=True,
    source='manual'
)
```

## Groupings Structure Template

### Simple (Core + Electives)
```python
groupings=[
    {
        'name': 'Core Units',
        'type': 'core',
        'required': 6,
        'units': [
            {'code': 'ABC123', 'title': 'Unit Title', 'type': 'core'},
        ]
    },
    {
        'name': 'Elective Units',
        'type': 'elective',
        'required': 4,
        'description': 'Select 4 elective units',
        'units': [
            {'code': 'DEF456', 'title': 'Elective Unit', 'type': 'elective'},
        ]
    }
]
```

### With Specializations/Majors
```python
groupings=[
    {
        'name': 'Core Units',
        'type': 'core',
        'required': 9,
        'units': [...]
    },
    {
        'name': 'Cloud Computing Specialization',
        'type': 'elective',
        'required': 0,
        'description': 'Select units from this specialization',
        'units': [...]
    },
    {
        'name': 'Programming Specialization',
        'type': 'elective',
        'required': 0,
        'description': 'Select units from this specialization',
        'units': [...]
    },
    {
        'name': 'General Electives',
        'type': 'elective',
        'required': 0,
        'description': 'Additional elective units',
        'units': [...]
    }
]
```

## Query Examples

### List All Qualifications
```python
from tas.models import QualificationCache

for qual in QualificationCache.objects.filter(is_active=True):
    print(f"{qual.qualification_code}: {qual.qualification_title}")
```

### Count Units per Qualification
```python
from tas.models import QualificationCache

for qual in QualificationCache.objects.all():
    total_units = sum(len(g['units']) for g in qual.groupings)
    print(f"{qual.qualification_code}: {total_units} units")
```

### Find Qualifications by Training Package
```python
from tas.models import QualificationCache

# All BSB qualifications
bsb_quals = QualificationCache.objects.filter(
    training_package='BSB',
    is_active=True
)
for qual in bsb_quals:
    print(qual.qualification_title)
```

### Update Existing Qualification
```python
from tas.models import QualificationCache

qual = QualificationCache.objects.get(qualification_code='ICT40120')
qual.packaging_rules = "Updated rules..."
qual.save()
```

### Deactivate Qualification
```python
from tas.models import QualificationCache

qual = QualificationCache.objects.get(qualification_code='OLD123')
qual.is_active = False
qual.save()
```

## Troubleshooting

### Check if qualification exists
```python
from tas.models import QualificationCache
QualificationCache.objects.filter(qualification_code='ICT40120').exists()
# True or False
```

### View qualification details
```python
from tas.models import QualificationCache
qual = QualificationCache.objects.get(qualification_code='ICT40120')
print(f"Title: {qual.qualification_title}")
print(f"Groupings: {len(qual.groupings)}")
print(f"Active: {qual.is_active}")
print(f"Last updated: {qual.last_updated}")
```

### List all training packages
```python
from tas.models import QualificationCache
packages = QualificationCache.objects.values_list('training_package', flat=True).distinct()
print(list(packages))
```

### Clear all cached data
```python
from tas.models import QualificationCache
QualificationCache.objects.all().delete()
# Then reload with: python manage.py load_qualifications
```

## Currently Loaded Qualifications (as of setup)

| Code | Title | Package | Level | Units |
|------|-------|---------|-------|-------|
| ICT40120 | Certificate IV in Information Technology | ICT | Cert IV | 37 |
| BSB50120 | Diploma of Business | BSB | Diploma | 15 |
| CHC50113 | Diploma of Early Childhood Education and Care | CHC | Diploma | 29 |
| SIT50416 | Diploma of Hospitality Management | SIT | Diploma | 27 |
| BSB40120 | Certificate IV in Business | BSB | Cert IV | 14 |
| BSB50420 | Diploma of Leadership and Management | BSB | Diploma | 17 |
| FNS40217 | Certificate IV in Bookkeeping | FNS | Cert IV | 14 |
| TAE40116 | Certificate IV in Training and Assessment | TAE | Cert IV | 13 |

## Files Reference

| File | Purpose |
|------|---------|
| `tas/models.py` | QualificationCache model definition |
| `tas/views.py` | API endpoint for fetching units |
| `tas/management/commands/load_qualifications.py` | Management command to load data |
| `tas/migrations/0003_*.py` | Database migration creating cache table |

## Training Packages

Common training packages in Australian VET:

- **BSB** - Business Services
- **ICT** - Information and Communications Technology
- **CHC** - Community Services
- **SIT** - Tourism, Travel and Hospitality
- **SIR** - Retail Services
- **TAE** - Training and Education
- **HLT** - Health
- **FNS** - Financial Services
- **AHC** - Agriculture, Horticulture and Conservation
- **AUR** - Automotive Retail, Service and Repair

## Next Steps

1. **Add more qualifications** - Edit `load_qualifications.py` or use shell
2. **Test frontend** - Select qualifications in UI to verify units load
3. **Set up periodic updates** - Consider Celery task for regular syncing
4. **Monitor performance** - Add logging to track cache hit rates

---

**Need help?** See full documentation in `docs/TAS_QUALIFICATION_MANAGEMENT.md`
