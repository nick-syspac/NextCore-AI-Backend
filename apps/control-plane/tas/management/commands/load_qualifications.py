"""
Management command to load qualification and units data into cache
Usage: python manage.py load_qualifications
"""
from django.core.management.base import BaseCommand
from tas.models import QualificationCache
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Load qualification and units data into database cache'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing cache before loading',
        )
        parser.add_argument(
            '--source',
            type=str,
            default='curated',
            help='Data source identifier',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('🗑️  Clearing existing cache...')
            count = QualificationCache.objects.all().count()
            QualificationCache.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} cached qualifications'))

        self.stdout.write('📚 Loading qualification data...')
        
        # Load curated qualification data
        qualifications_data = self.get_qualifications_data()
        
        created_count = 0
        updated_count = 0
        
        for qual_data in qualifications_data:
            qual_code = qual_data['qualification_code']
            
            try:
                # Create or update
                obj, created = QualificationCache.objects.update_or_create(
                    qualification_code=qual_code,
                    defaults={
                        'qualification_title': qual_data['qualification_title'],
                        'training_package': qual_data.get('training_package', ''),
                        'aqf_level': qual_data.get('aqf_level', ''),
                        'packaging_rules': qual_data.get('packaging_rules', ''),
                        'has_groupings': qual_data.get('has_groupings', False),
                        'groupings': qual_data.get('groupings', []),
                        'source': options['source'],
                        'is_active': True,
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'  ✅ Created: {qual_code} - {qual_data["qualification_title"]}')
                else:
                    updated_count += 1
                    self.stdout.write(f'  🔄 Updated: {qual_code} - {qual_data["qualification_title"]}')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Error loading {qual_code}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✨ Complete! Created: {created_count}, Updated: {updated_count}'
            )
        )

    def get_qualifications_data(self):
        """Return all curated qualification data"""
        return [
            # ICT Qualifications
            {
                'qualification_code': 'ICT40120',
                'qualification_title': 'Certificate IV in Information Technology',
                'training_package': 'ICT',
                'aqf_level': 'certificate_iv',
                'packaging_rules': 'Total of 20 units: 9 core units + 11 elective units. Electives organized into specialization groupings.',
                'has_groupings': True,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 9,
                        'units': [
                            {'code': 'BSBCRT401', 'title': 'Articulate, present and debate ideas', 'type': 'core'},
                            {'code': 'BSBXCS404', 'title': 'Contribute to cyber security risk management', 'type': 'core'},
                            {'code': 'ICTICT401', 'title': 'Determine and confirm client business requirements', 'type': 'core'},
                            {'code': 'ICTICT418', 'title': 'Contribute to copyright, ethics and privacy in an ICT environment', 'type': 'core'},
                            {'code': 'ICTSAS432', 'title': 'Identify and resolve client ICT problems', 'type': 'core'},
                            {'code': 'ICTSAS527', 'title': 'Manage client problems', 'type': 'core'},
                            {'code': 'BSBXTW401', 'title': 'Lead and facilitate a team', 'type': 'core'},
                            {'code': 'BSBXCS303', 'title': 'Securely manage personally identifiable information and workplace information', 'type': 'core'},
                            {'code': 'ICTICT426', 'title': 'Identify and evaluate emerging technologies', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Cloud Computing',
                        'type': 'elective',
                        'required': 0,
                        'description': 'Specialization in cloud technologies and services',
                        'units': [
                            {'code': 'ICTCLD401', 'title': 'Configure and manage virtual computing environments', 'type': 'elective'},
                            {'code': 'ICTCLD501', 'title': 'Identify and implement cloud services', 'type': 'elective'},
                            {'code': 'ICTCLD503', 'title': 'Deploy and manage infrastructure as code', 'type': 'elective'},
                            {'code': 'ICTCLD504', 'title': 'Deploy and manage containerized applications', 'type': 'elective'},
                        ]
                    },
                    {
                        'name': 'Programming',
                        'type': 'elective',
                        'required': 0,
                        'description': 'Software development and programming specialization',
                        'units': [
                            {'code': 'ICTPRG302', 'title': 'Apply introductory programming techniques', 'type': 'elective'},
                            {'code': 'ICTPRG410', 'title': 'Build a web application', 'type': 'elective'},
                            {'code': 'ICTPRG418', 'title': 'Apply intermediate programming skills in another language', 'type': 'elective'},
                            {'code': 'ICTPRG430', 'title': 'Apply introductory object-oriented language skills', 'type': 'elective'},
                        ]
                    },
                    {
                        'name': 'Networking',
                        'type': 'elective',
                        'required': 0,
                        'description': 'Network infrastructure and administration',
                        'units': [
                            {'code': 'ICTNWK401', 'title': 'Install and manage network protocols', 'type': 'elective'},
                            {'code': 'ICTNWK404', 'title': 'Install, operate and troubleshoot a small enterprise branch network', 'type': 'elective'},
                            {'code': 'ICTNWK411', 'title': 'Deploy software to networked computers', 'type': 'elective'},
                            {'code': 'ICTNWK529', 'title': 'Install and manage complex ICT networks', 'type': 'elective'},
                        ]
                    },
                    {
                        'name': 'Cyber Security',
                        'type': 'elective',
                        'required': 0,
                        'description': 'Security and risk management specialization',
                        'units': [
                            {'code': 'ICTCYS401', 'title': 'Implement and monitor cyber security practices', 'type': 'elective'},
                            {'code': 'ICTCYS402', 'title': 'Identify and report security incidents', 'type': 'elective'},
                            {'code': 'ICTCYS501', 'title': 'Protect critical infrastructure from cyber threats', 'type': 'elective'},
                            {'code': 'ICTCYS503', 'title': 'Respond to cyber security incidents', 'type': 'elective'},
                        ]
                    },
                    {
                        'name': 'General Electives',
                        'type': 'elective',
                        'required': 0,
                        'description': 'Additional ICT electives from any grouping',
                        'units': [
                            {'code': 'BSBTEC404', 'title': 'Use digital technologies to collaborate in a work environment', 'type': 'elective'},
                            {'code': 'ICTICT443', 'title': 'Work collaboratively in the ICT industry', 'type': 'elective'},
                            {'code': 'ICTSAS425', 'title': 'Implement and support software tools for the workplace', 'type': 'elective'},
                            {'code': 'ICTICT424', 'title': 'Manage and use software and hardware', 'type': 'elective'},
                            {'code': 'ICTTEN423', 'title': 'Manage technical documentation', 'type': 'elective'},
                        ]
                    }
                ]
            },
            # Business Qualifications
            {
                'qualification_code': 'BSB50120',
                'qualification_title': 'Diploma of Business',
                'training_package': 'BSB',
                'aqf_level': 'diploma',
                'packaging_rules': 'Total of 12 units: 5 core units + 7 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 5,
                        'units': [
                            {'code': 'BSBCRT511', 'title': 'Develop critical thinking in others', 'type': 'core'},
                            {'code': 'BSBFIN501', 'title': 'Manage budgets and financial plans', 'type': 'core'},
                            {'code': 'BSBOPS502', 'title': 'Manage business operational plans', 'type': 'core'},
                            {'code': 'BSBTWK502', 'title': 'Manage team effectiveness', 'type': 'core'},
                            {'code': 'BSBXCS402', 'title': 'Promote workplace cyber security awareness and best practices', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 7,
                        'description': 'Select 7 elective units',
                        'units': [
                            {'code': 'BSBHRM522', 'title': 'Manage employee and industrial relations', 'type': 'elective'},
                            {'code': 'BSBMGT517', 'title': 'Manage operational plan', 'type': 'elective'},
                            {'code': 'BSBPMG430', 'title': 'Undertake project work', 'type': 'elective'},
                            {'code': 'BSBSTR501', 'title': 'Establish innovative work environments', 'type': 'elective'},
                            {'code': 'BSBMKT541', 'title': 'Identify and evaluate marketing opportunities', 'type': 'elective'},
                            {'code': 'BSBOPS504', 'title': 'Manage business risk', 'type': 'elective'},
                            {'code': 'BSBPEF502', 'title': 'Develop and use emotional intelligence', 'type': 'elective'},
                            {'code': 'BSBLDR523', 'title': 'Lead and manage effective workplace relationships', 'type': 'elective'},
                            {'code': 'BSBCMM511', 'title': 'Communicate with influence', 'type': 'elective'},
                            {'code': 'BSBINS503', 'title': 'Develop and implement strategic plans', 'type': 'elective'},
                        ]
                    }
                ]
            },
            # Community Services
            {
                'qualification_code': 'CHC50113',
                'qualification_title': 'Diploma of Early Childhood Education and Care',
                'training_package': 'CHC',
                'aqf_level': 'diploma',
                'packaging_rules': 'Total of 29 units: 15 core units + 14 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 15,
                        'units': [
                            {'code': 'CHCECE001', 'title': 'Develop cultural competence', 'type': 'core'},
                            {'code': 'CHCECE002', 'title': 'Ensure the health and safety of children', 'type': 'core'},
                            {'code': 'CHCECE003', 'title': 'Provide care for children', 'type': 'core'},
                            {'code': 'CHCECE004', 'title': 'Promote and provide healthy food and drinks', 'type': 'core'},
                            {'code': 'CHCECE005', 'title': 'Provide care for babies and toddlers', 'type': 'core'},
                            {'code': 'CHCECE007', 'title': 'Develop positive and respectful relationships with children', 'type': 'core'},
                            {'code': 'CHCECE009', 'title': 'Use an approved learning framework to guide practice', 'type': 'core'},
                            {'code': 'CHCECE010', 'title': 'Support the holistic development of children in early childhood', 'type': 'core'},
                            {'code': 'CHCECE011', 'title': 'Provide experiences to support children\'s play and learning', 'type': 'core'},
                            {'code': 'CHCECE013', 'title': 'Use information about children to inform practice', 'type': 'core'},
                            {'code': 'CHCECE016', 'title': 'Establish and maintain a safe and healthy environment for children', 'type': 'core'},
                            {'code': 'CHCECE017', 'title': 'Foster the holistic development and wellbeing of the child in early childhood', 'type': 'core'},
                            {'code': 'CHCECE018', 'title': 'Nurture creativity in children', 'type': 'core'},
                            {'code': 'CHCECE019', 'title': 'Facilitate compliance in an education and care service', 'type': 'core'},
                            {'code': 'CHCECE020', 'title': 'Establish and implement plans for developing cooperative behaviour', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 14,
                        'description': 'Select 14 elective units',
                        'units': [
                            {'code': 'CHCECE021', 'title': 'Implement strategies for the inclusion of all children', 'type': 'elective'},
                            {'code': 'CHCECE022', 'title': 'Promote children\'s agency', 'type': 'elective'},
                            {'code': 'CHCECE023', 'title': 'Analyse information to inform learning', 'type': 'elective'},
                            {'code': 'CHCECE024', 'title': 'Design and implement the curriculum to foster children\'s learning and development', 'type': 'elective'},
                            {'code': 'CHCECE025', 'title': 'Embed sustainable practices in service operations', 'type': 'elective'},
                            {'code': 'CHCECE026', 'title': 'Work in partnership with families to provide appropriate education and care for children', 'type': 'elective'},
                            {'code': 'CHCPRT001', 'title': 'Identify and respond to children and young people at risk', 'type': 'elective'},
                            {'code': 'HLTAID012', 'title': 'Provide First Aid in an education and care setting', 'type': 'elective'},
                            {'code': 'CHCDIV001', 'title': 'Work with diverse people', 'type': 'elective'},
                            {'code': 'CHCLEG001', 'title': 'Work legally and ethically', 'type': 'elective'},
                            {'code': 'CHCMGT003', 'title': 'Lead the work team', 'type': 'elective'},
                            {'code': 'CHCPRP003', 'title': 'Reflect on and improve own professional practice', 'type': 'elective'},
                            {'code': 'BSBSUS411', 'title': 'Implement and monitor environmentally sustainable work practices', 'type': 'elective'},
                            {'code': 'CHCECE054', 'title': 'Encourage understanding of Aboriginal and/or Torres Strait Islander peoples\' cultures', 'type': 'elective'},
                        ]
                    }
                ]
            },
            # Hospitality
            {
                'qualification_code': 'SIT50416',
                'qualification_title': 'Diploma of Hospitality Management',
                'training_package': 'SIT',
                'aqf_level': 'diploma',
                'packaging_rules': 'Total of 27 units comprising: 13 core units + 14 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 13,
                        'units': [
                            {'code': 'BSBDIV501', 'title': 'Manage diversity in the workplace', 'type': 'core'},
                            {'code': 'BSBFIN501', 'title': 'Manage budgets and financial plans', 'type': 'core'},
                            {'code': 'BSBMGT517', 'title': 'Manage operational plan', 'type': 'core'},
                            {'code': 'SITXCCS007', 'title': 'Enhance customer service experiences', 'type': 'core'},
                            {'code': 'SITXCCS008', 'title': 'Develop and manage quality customer service practices', 'type': 'core'},
                            {'code': 'SITXCOM005', 'title': 'Manage conflict', 'type': 'core'},
                            {'code': 'SITXFIN003', 'title': 'Manage finances within a budget', 'type': 'core'},
                            {'code': 'SITXFIN004', 'title': 'Prepare and monitor budgets', 'type': 'core'},
                            {'code': 'SITXGLC001', 'title': 'Research and comply with regulatory requirements', 'type': 'core'},
                            {'code': 'SITXHRM002', 'title': 'Roster staff', 'type': 'core'},
                            {'code': 'SITXHRM003', 'title': 'Lead and manage people', 'type': 'core'},
                            {'code': 'SITXMGT001', 'title': 'Monitor work operations', 'type': 'core'},
                            {'code': 'SITXMGT002', 'title': 'Establish and conduct business relationships', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 14,
                        'description': 'Select 14 elective units',
                        'units': [
                            {'code': 'SITXFSA001', 'title': 'Use hygienic practices for food safety', 'type': 'elective'},
                            {'code': 'SITXFSA002', 'title': 'Participate in safe food handling practices', 'type': 'elective'},
                            {'code': 'SITXHRM001', 'title': 'Coach others in job skills', 'type': 'elective'},
                            {'code': 'SITXHRM004', 'title': 'Recruit, select and induct staff', 'type': 'elective'},
                            {'code': 'SITXMGT003', 'title': 'Manage projects', 'type': 'elective'},
                            {'code': 'SITXMGT004', 'title': 'Monitor work operations', 'type': 'elective'},
                            {'code': 'SITXWHS003', 'title': 'Implement and monitor work health and safety practices', 'type': 'elective'},
                            {'code': 'SITHCCC001', 'title': 'Use food preparation equipment', 'type': 'elective'},
                            {'code': 'SITHCCC005', 'title': 'Prepare dishes using basic methods of cookery', 'type': 'elective'},
                            {'code': 'SITHKOP002', 'title': 'Plan and cost basic menus', 'type': 'elective'},
                            {'code': 'SITHKOP005', 'title': 'Coordinate cooking operations', 'type': 'elective'},
                            {'code': 'SITTTSL003', 'title': 'Provide advice on Australian destinations', 'type': 'elective'},
                            {'code': 'SITTTSL004', 'title': 'Provide advice on international destinations', 'type': 'elective'},
                            {'code': 'SITTTVL001', 'title': 'Access and interpret product information', 'type': 'elective'},
                        ]
                    }
                ]
            },
            {
                'qualification_code': 'BSB40120',
                'qualification_title': 'Certificate IV in Business',
                'training_package': 'BSB',
                'aqf_level': 'certificate_iv',
                'packaging_rules': 'Total of 6 units comprising: 2 core units + 4 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 2,
                        'units': [
                            {'code': 'BSBCRT411', 'title': 'Apply critical thinking to work practices', 'type': 'core'},
                            {'code': 'BSBXCS303', 'title': 'Securely manage personally identifiable information and workplace information', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 4,
                        'description': 'Select 4 elective units',
                        'units': [
                            {'code': 'BSBCMM411', 'title': 'Make presentations', 'type': 'elective'},
                            {'code': 'BSBCOM412', 'title': 'Negotiate to achieve desired outcomes', 'type': 'elective'},
                            {'code': 'BSBFIN401', 'title': 'Report on financial activity', 'type': 'elective'},
                            {'code': 'BSBINS402', 'title': 'Coordinate workplace information systems', 'type': 'elective'},
                            {'code': 'BSBLEG414', 'title': 'Apply legal principles in contract law matters', 'type': 'elective'},
                            {'code': 'BSBMGT412', 'title': 'Lead and facilitate a team', 'type': 'elective'},
                            {'code': 'BSBOPS402', 'title': 'Coordinate business operational plans', 'type': 'elective'},
                            {'code': 'BSBPEF402', 'title': 'Develop personal work priorities', 'type': 'elective'},
                            {'code': 'BSBPMG430', 'title': 'Undertake project work', 'type': 'elective'},
                            {'code': 'BSBSTR402', 'title': 'Implement continuous improvement', 'type': 'elective'},
                            {'code': 'BSBTEC402', 'title': 'Design and produce complex spreadsheets', 'type': 'elective'},
                            {'code': 'BSBWHS411', 'title': 'Implement and monitor WHS policies, procedures and programs', 'type': 'elective'},
                        ]
                    }
                ]
            },
            {
                'qualification_code': 'BSB50420',
                'qualification_title': 'Diploma of Leadership and Management',
                'training_package': 'BSB',
                'aqf_level': 'diploma',
                'packaging_rules': 'Total of 12 units comprising: 6 core units + 6 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 6,
                        'units': [
                            {'code': 'BSBCRT511', 'title': 'Develop critical thinking in others', 'type': 'core'},
                            {'code': 'BSBLDR523', 'title': 'Lead and manage effective workplace relationships', 'type': 'core'},
                            {'code': 'BSBOPS502', 'title': 'Manage business operational plans', 'type': 'core'},
                            {'code': 'BSBPEF502', 'title': 'Develop and use emotional intelligence', 'type': 'core'},
                            {'code': 'BSBTWK502', 'title': 'Manage team effectiveness', 'type': 'core'},
                            {'code': 'BSBXCS402', 'title': 'Promote workplace cyber security awareness and best practices', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 6,
                        'description': 'Select 6 elective units',
                        'units': [
                            {'code': 'BSBCOM511', 'title': 'Communicate with influence', 'type': 'elective'},
                            {'code': 'BSBFIN501', 'title': 'Manage budgets and financial plans', 'type': 'elective'},
                            {'code': 'BSBHRM522', 'title': 'Manage employee and industrial relations', 'type': 'elective'},
                            {'code': 'BSBINS503', 'title': 'Develop and implement strategic plans', 'type': 'elective'},
                            {'code': 'BSBLDR522', 'title': 'Manage people performance', 'type': 'elective'},
                            {'code': 'BSBMGT516', 'title': 'Facilitate continuous improvement', 'type': 'elective'},
                            {'code': 'BSBMGT517', 'title': 'Manage operational plan', 'type': 'elective'},
                            {'code': 'BSBPMG530', 'title': 'Manage project scope', 'type': 'elective'},
                            {'code': 'BSBSTR501', 'title': 'Establish innovative work environments', 'type': 'elective'},
                            {'code': 'BSBTEC501', 'title': 'Develop and implement organisational digital strategy', 'type': 'elective'},
                            {'code': 'BSBWHS516', 'title': 'Contribute to developing, implementing and maintaining an organisation\'s WHS management system', 'type': 'elective'},
                        ]
                    }
                ]
            },
            {
                'qualification_code': 'FNS40217',
                'qualification_title': 'Certificate IV in Bookkeeping',
                'training_package': 'FNS',
                'aqf_level': 'certificate_iv',
                'packaging_rules': 'Total of 10 units comprising: 6 core units + 4 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 6,
                        'units': [
                            {'code': 'FNSACC311', 'title': 'Process financial transactions and extract interim reports', 'type': 'core'},
                            {'code': 'FNSACC321', 'title': 'Process financial transactions and extract interim reports (with MYOB)', 'type': 'core'},
                            {'code': 'FNSACC416', 'title': 'Set up and operate computerised accounting systems', 'type': 'core'},
                            {'code': 'FNSACC418', 'title': 'Work effectively in the accounting and bookkeeping industry', 'type': 'core'},
                            {'code': 'FNSTPB411', 'title': 'Complete business activity and instalment activity statements', 'type': 'core'},
                            {'code': 'FNSTPB412', 'title': 'Establish and maintain payroll systems', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 4,
                        'description': 'Select 4 elective units',
                        'units': [
                            {'code': 'BSBCMM411', 'title': 'Make presentations', 'type': 'elective'},
                            {'code': 'BSBFIN401', 'title': 'Report on financial activity', 'type': 'elective'},
                            {'code': 'BSBINS402', 'title': 'Coordinate workplace information systems', 'type': 'elective'},
                            {'code': 'BSBPEF402', 'title': 'Develop personal work priorities', 'type': 'elective'},
                            {'code': 'BSBTEC401', 'title': 'Design and develop complex text documents', 'type': 'elective'},
                            {'code': 'BSBTEC402', 'title': 'Design and produce complex spreadsheets', 'type': 'elective'},
                            {'code': 'FNSACC415', 'title': 'Make decisions in a legal context', 'type': 'elective'},
                            {'code': 'FNSTPB413', 'title': 'Establish and maintain cash controls', 'type': 'elective'},
                        ]
                    }
                ]
            },
            {
                'qualification_code': 'TAE40116',
                'qualification_title': 'Certificate IV in Training and Assessment',
                'training_package': 'TAE',
                'aqf_level': 'certificate_iv',
                'packaging_rules': 'Total of 10 units comprising: 4 core units + 6 elective units',
                'has_groupings': False,
                'groupings': [
                    {
                        'name': 'Core Units',
                        'type': 'core',
                        'required': 4,
                        'units': [
                            {'code': 'TAEDES401', 'title': 'Design and develop learning programs', 'type': 'core'},
                            {'code': 'TAEDES402', 'title': 'Use training packages and accredited courses to meet client needs', 'type': 'core'},
                            {'code': 'TAEDEL401', 'title': 'Plan, organise and deliver group-based learning', 'type': 'core'},
                            {'code': 'TAEASS401', 'title': 'Plan assessment activities and processes', 'type': 'core'},
                        ]
                    },
                    {
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': 6,
                        'description': 'Must include TAEDEL402, TAEASS402, TAEASS403',
                        'units': [
                            {'code': 'TAEDEL402', 'title': 'Plan, organise and facilitate learning in the workplace', 'type': 'elective'},
                            {'code': 'TAEASS402', 'title': 'Assess competence', 'type': 'elective'},
                            {'code': 'TAEASS403', 'title': 'Participate in assessment validation', 'type': 'elective'},
                            {'code': 'TAEDEL301', 'title': 'Provide work skill instruction', 'type': 'elective'},
                            {'code': 'BSBCMM411', 'title': 'Make presentations', 'type': 'elective'},
                            {'code': 'TAELLN411', 'title': 'Address adult language, literacy and numeracy skills', 'type': 'elective'},
                            {'code': 'TAEPDD401', 'title': 'Work effectively in vocational education and training', 'type': 'elective'},
                            {'code': 'TAEASS404', 'title': 'Assess competence in an online environment', 'type': 'elective'},
                            {'code': 'TAEDES403', 'title': 'Design and develop print-based learning resources', 'type': 'elective'},
                        ]
                    }
                ]
            },
        ]
