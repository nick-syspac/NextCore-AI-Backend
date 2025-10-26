# TAS Management Commands

Django management commands for maintaining the TAS (Training and Assessment Strategy) system.

## Available Commands

### load_qualifications

Loads or updates qualification and units data into the `QualificationCache` database.

**Purpose:**  
Populates the database with Australian VET qualifications including their core and elective units of competency, packaging rules, and groupings.

**Usage:**
```bash
python manage.py load_qualifications [options]
```

**Options:**
- `--clear` - Delete all existing cached qualifications before loading
- `--source <string>` - Set custom source identifier (default: "curated")

**Examples:**
```bash
# Initial load
python manage.py load_qualifications

# Clear and reload all data
python manage.py load_qualifications --clear

# Load with custom source tracking
python manage.py load_qualifications --source "training.gov.au-2025-Q4"
```

**Output:**
```
📚 Loading qualification data...
  ✅ Created: ICT40120 - Certificate IV in Information Technology
  ✅ Created: BSB50120 - Diploma of Business
  🔄 Updated: CHC50113 - Diploma of Early Childhood Education and Care
  
✨ Complete! Created: 7, Updated: 1
```

**Data Structure:**

Each qualification includes:
- `qualification_code` - TGA code (e.g., "ICT40120")
- `qualification_title` - Full title
- `training_package` - Package code (BSB, ICT, CHC, etc.)
- `aqf_level` - AQF level (certificate_iii, diploma, etc.)
- `packaging_rules` - Requirements text
- `has_groupings` - Boolean indicating specializations/majors
- `groupings` - Array of unit groupings

**Groupings Structure:**
```python
{
    'name': 'Core Units',           # Grouping name
    'type': 'core',                 # 'core' or 'elective'
    'required': 9,                  # Number required
    'description': 'Optional text', # Additional info
    'units': [
        {
            'code': 'BSBCRT401',
            'title': 'Articulate, present and debate ideas',
            'type': 'core'
        }
    ]
}
```

**Adding New Qualifications:**

Edit `load_qualifications.py` and add to the `get_qualifications_data()` method:

```python
def get_qualifications_data(self):
    return [
        # Existing qualifications...
        {
            'qualification_code': 'NEW123',
            'qualification_title': 'New Qualification Title',
            'training_package': 'BSB',
            'aqf_level': 'diploma',
            'packaging_rules': 'Total of 12 units...',
            'has_groupings': False,
            'groupings': [
                {
                    'name': 'Core Units',
                    'type': 'core',
                    'required': 6,
                    'units': [
                        {'code': 'UNIT001', 'title': 'Unit title', 'type': 'core'},
                    ]
                },
                {
                    'name': 'Elective Units',
                    'type': 'elective',
                    'required': 6,
                    'description': 'Select 6 elective units',
                    'units': [
                        {'code': 'UNIT002', 'title': 'Elective unit', 'type': 'elective'},
                    ]
                }
            ]
        }
    ]
```

Then run:
```bash
python manage.py load_qualifications
```

**Database Changes:**

This command interacts with the `QualificationCache` model:
- Creates new records if qualification_code doesn't exist
- Updates existing records if qualification_code already exists
- Sets `last_updated` timestamp automatically
- Marks all loaded qualifications as `is_active=True`

**When to Use:**

- **Initial setup** - First time deploying the system
- **Adding qualifications** - When new courses are offered
- **Updating packaging rules** - When training.gov.au releases changes
- **Refreshing data** - Periodic maintenance (e.g., quarterly)
- **After code deployment** - If qualification data structure changes

**Caution:**

⚠️ Using `--clear` will delete ALL cached qualifications. Ensure you have:
1. Database backup
2. All desired qualifications in the command file
3. Tested in development environment first

**Related Models:**

- `QualificationCache` (`tas/models.py`)
- See: `docs/TAS_QUALIFICATION_MANAGEMENT.md` for full documentation

## Future Commands (Planned)

### sync_training_gov_au
Fetch qualifications directly from training.gov.au API/scraper.

### export_qualifications
Export cached qualifications to JSON/CSV for backup or migration.

### validate_qualifications
Check qualification data integrity and structure.

### import_qualifications
Bulk import from external file (CSV, JSON, Excel).

## Development

**Testing the Command:**

```python
# Create test database
python manage.py migrate --database=test

# Run command on test database
python manage.py load_qualifications --database=test

# Verify results
python manage.py shell
>>> from tas.models import QualificationCache
>>> QualificationCache.objects.using('test').count()
```

**Adding Custom Management Commands:**

1. Create new file in this directory: `command_name.py`
2. Implement `Command` class extending `BaseCommand`
3. Define `handle()` method
4. Use: `python manage.py command_name`

Example structure:
```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of what this command does'

    def add_arguments(self, parser):
        parser.add_argument('--option', type=str, help='Optional argument')

    def handle(self, *args, **options):
        self.stdout.write('Command executed!')
        self.stdout.write(self.style.SUCCESS('Done!'))
```

## Support

For issues or questions:
- Check `docs/TAS_QUALIFICATION_MANAGEMENT.md` for detailed documentation
- Review `docs/TAS_QUICK_REFERENCE.md` for quick examples
- Contact: RTO systems team

---

**Last Updated:** October 26, 2025  
**Maintained by:** NextCore AI Cloud Team
