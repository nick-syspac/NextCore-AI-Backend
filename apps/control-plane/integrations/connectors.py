"""
Integration connector classes for third-party systems.
Each connector handles authentication, API calls, and data synchronization.
"""
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class BaseConnector:
    """Base class for all integration connectors"""
    
    def __init__(self, integration):
        self.integration = integration
        self.config = integration.config or {}
        self.base_url = integration.api_base_url
        
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests"""
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'NextCore-AI-Cloud/1.0'
        }
    
    def test_connection(self) -> tuple[bool, str]:
        """Test if the integration connection is working"""
        raise NotImplementedError
    
    def sync_data(self, entity_type: str) -> Dict[str, Any]:
        """Sync data from external system"""
        raise NotImplementedError


# SMS/RTO Systems

class ReadyTechJRConnector(BaseConnector):
    """
    ReadyTech JR Plus / Ready Student Connector
    Major AU VET footprint (TAFEs & enterprise RTOs)
    API Priority: High - stable REST, long-running platform docs
    """
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        headers['Authorization'] = f"Bearer {self.integration.access_token}"
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/health",
                headers=self.get_headers(),
                timeout=10
            )
            if response.status_code == 200:
                return True, "Connection successful"
            return False, f"API returned status {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def sync_students(self) -> List[Dict]:
        """Sync student data from ReadyTech"""
        response = requests.get(
            f"{self.base_url}/api/v1/students",
            headers=self.get_headers(),
            params={'modified_since': self.integration.last_sync_at.isoformat() if self.integration.last_sync_at else None}
        )
        response.raise_for_status()
        return response.json()
    
    def sync_units(self) -> List[Dict]:
        """Sync units of competency"""
        response = requests.get(
            f"{self.base_url}/api/v1/units",
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def sync_enrolments(self) -> List[Dict]:
        """Sync student enrolments"""
        response = requests.get(
            f"{self.base_url}/api/v1/enrolments",
            headers=self.get_headers(),
            params={'modified_since': self.integration.last_sync_at.isoformat() if self.integration.last_sync_at else None}
        )
        response.raise_for_status()
        return response.json()


class VETtrakConnector(BaseConnector):
    """
    VETtrak (ReadyTech) Connector
    Longstanding AU RTO SMS; many private RTOs
    API Priority: High - published API + change logs
    """
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        headers['API-Key'] = self.integration.api_key
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/ping",
                headers=self.get_headers(),
                timeout=10
            )
            if response.status_code == 200:
                return True, "VETtrak connection successful"
            return False, f"API returned status {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def get_clients(self, modified_since: Optional[datetime] = None) -> List[Dict]:
        """Get student/client data"""
        params = {}
        if modified_since:
            params['modifiedSince'] = modified_since.isoformat()
        
        response = requests.get(
            f"{self.base_url}/api/v1/clients",
            headers=self.get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def get_programs(self) -> List[Dict]:
        """Get training programs/qualifications"""
        response = requests.get(
            f"{self.base_url}/api/v1/programs",
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()


class eSkilledConnector(BaseConnector):
    """
    eSkilled SMS+LMS Connector
    AU-focused SMS+LMS targeting 2025 Standards
    API Priority: Medium - confirm API surface
    """
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        headers['Authorization'] = f"Bearer {self.integration.access_token}"
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.base_url}/api/status",
                headers=self.get_headers(),
                timeout=10
            )
            return response.status_code == 200, "eSkilled connection test"
        except Exception as e:
            return False, str(e)


# LMS/Assessment Systems

class CloudAssessConnector(BaseConnector):
    """
    CloudAssess Connector
    Compliance-first assessment platform
    API Priority: Medium - integrations common
    """
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        headers['X-API-Key'] = self.integration.api_key
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/assessments",
                headers=self.get_headers(),
                params={'limit': 1},
                timeout=10
            )
            return response.status_code == 200, "CloudAssess connection successful"
        except Exception as e:
            return False, str(e)
    
    def get_assessments(self) -> List[Dict]:
        """Get assessment data"""
        response = requests.get(
            f"{self.base_url}/api/v1/assessments",
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_student_results(self, student_id: str) -> List[Dict]:
        """Get student assessment results"""
        response = requests.get(
            f"{self.base_url}/api/v1/students/{student_id}/results",
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()


class CourseboxConnector(BaseConnector):
    """
    Coursebox AI-LMS Connector
    AU AI-LMS popular with new RTOs
    API Priority: Emerging - API references exist
    """
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        headers['Authorization'] = f"Bearer {self.integration.access_token}"
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/courses",
                headers=self.get_headers(),
                params={'limit': 1},
                timeout=10
            )
            return response.status_code == 200, "Coursebox connection successful"
        except Exception as e:
            return False, str(e)


class MoodleConnector(BaseConnector):
    """
    Moodle Connector
    Huge AU adoption across VET/HE
    API Priority: High - mature web services/plugins
    """
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            # Moodle uses wstoken parameter
            response = requests.get(
                f"{self.base_url}/webservice/rest/server.php",
                params={
                    'wstoken': self.integration.api_key,
                    'wsfunction': 'core_webservice_get_site_info',
                    'moodlewsrestformat': 'json'
                },
                timeout=10
            )
            if response.status_code == 200 and not response.json().get('exception'):
                return True, "Moodle connection successful"
            return False, "Moodle API error"
        except Exception as e:
            return False, str(e)
    
    def get_courses(self) -> List[Dict]:
        """Get all courses"""
        response = requests.get(
            f"{self.base_url}/webservice/rest/server.php",
            params={
                'wstoken': self.integration.api_key,
                'wsfunction': 'core_course_get_courses',
                'moodlewsrestformat': 'json'
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_enrolled_users(self, course_id: int) -> List[Dict]:
        """Get users enrolled in a course"""
        response = requests.get(
            f"{self.base_url}/webservice/rest/server.php",
            params={
                'wstoken': self.integration.api_key,
                'wsfunction': 'core_enrol_get_enrolled_users',
                'moodlewsrestformat': 'json',
                'courseid': course_id
            }
        )
        response.raise_for_status()
        return response.json()


class D2LBrightspaceConnector(BaseConnector):
    """
    D2L Brightspace Connector
    Used across APAC in professional education
    API Priority: High - robust APIs/LTI
    """
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        headers['Authorization'] = f"Bearer {self.integration.access_token}"
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.base_url}/d2l/api/versions/",
                headers=self.get_headers(),
                timeout=10
            )
            return response.status_code == 200, "Brightspace connection successful"
        except Exception as e:
            return False, str(e)
    
    def get_org_units(self) -> List[Dict]:
        """Get organizational units (courses)"""
        response = requests.get(
            f"{self.base_url}/d2l/api/lp/1.0/orgstructure/",
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()


# Accounting Systems

class QuickBooksConnector(BaseConnector):
    """
    QuickBooks Online Connector
    Most common alternative to Xero/MYOB
    API Priority: High - REST + webhooks + sandbox
    """
    
    def __init__(self, integration):
        super().__init__(integration)
        self.realm_id = self.config.get('realm_id')  # Company ID
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        headers['Authorization'] = f"Bearer {self.integration.access_token}"
        headers['Accept'] = 'application/json'
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.base_url}/v3/company/{self.realm_id}/companyinfo/{self.realm_id}",
                headers=self.get_headers(),
                timeout=10
            )
            return response.status_code == 200, "QuickBooks connection successful"
        except Exception as e:
            return False, str(e)
    
    def create_invoice(self, invoice_data: Dict) -> Dict:
        """Create an invoice in QuickBooks"""
        response = requests.post(
            f"{self.base_url}/v3/company/{self.realm_id}/invoice",
            headers=self.get_headers(),
            json=invoice_data
        )
        response.raise_for_status()
        return response.json()
    
    def get_customers(self) -> List[Dict]:
        """Get customer list"""
        response = requests.get(
            f"{self.base_url}/v3/company/{self.realm_id}/query",
            headers=self.get_headers(),
            params={'query': 'SELECT * FROM Customer'}
        )
        response.raise_for_status()
        return response.json()['QueryResponse']['Customer']


class SageIntacctConnector(BaseConnector):
    """
    Sage Intacct Connector
    Larger education/training organizations
    API Priority: High - modern REST (XML legacy too)
    """
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        headers['Authorization'] = f"Bearer {self.integration.access_token}"
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            # Sage Intacct uses XML-based API
            response = requests.post(
                f"{self.base_url}/ia/xml/xmlgw.phtml",
                headers={'Content-Type': 'application/xml'},
                data=self._build_test_request(),
                timeout=10
            )
            return response.status_code == 200, "Sage Intacct connection successful"
        except Exception as e:
            return False, str(e)
    
    def _build_test_request(self) -> str:
        """Build XML request for API test"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <request>
            <control>
                <senderid>{self.config.get('sender_id')}</senderid>
                <password>{self.config.get('sender_password')}</password>
                <controlid>test</controlid>
                <uniqueid>false</uniqueid>
                <dtdversion>3.0</dtdversion>
            </control>
            <operation>
                <authentication>
                    <sessionid>{self.integration.access_token}</sessionid>
                </authentication>
                <content>
                    <function controlid="testfunction">
                        <getAPISession/>
                    </function>
                </content>
            </operation>
        </request>"""


# Payment Gateways

class StripeConnector(BaseConnector):
    """
    Stripe (AU) Connector
    Dominant online gateway; subscriptions/billing, PayTo/eftpos support
    API Priority: High
    """
    
    def get_headers(self) -> Dict[str, str]:
        headers = super().get_headers()
        headers['Authorization'] = f"Bearer {self.integration.access_token}"
        headers['Stripe-Version'] = '2023-10-16'
        return headers
    
    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.get(
                f"{self.base_url}/v1/balance",
                headers=self.get_headers(),
                timeout=10
            )
            return response.status_code == 200, "Stripe connection successful"
        except Exception as e:
            return False, str(e)
    
    def create_customer(self, email: str, name: str, metadata: Dict = None) -> Dict:
        """Create a Stripe customer"""
        data = {
            'email': email,
            'name': name,
            'metadata': metadata or {}
        }
        response = requests.post(
            f"{self.base_url}/v1/customers",
            headers=self.get_headers(),
            data=data
        )
        response.raise_for_status()
        return response.json()
    
    def create_payment_intent(self, amount: int, currency: str = 'aud', customer_id: str = None) -> Dict:
        """Create a payment intent"""
        data = {
            'amount': amount,  # Amount in cents
            'currency': currency,
            'automatic_payment_methods': {'enabled': True}
        }
        if customer_id:
            data['customer'] = customer_id
        
        response = requests.post(
            f"{self.base_url}/v1/payment_intents",
            headers=self.get_headers(),
            data=data
        )
        response.raise_for_status()
        return response.json()
    
    def create_subscription(self, customer_id: str, price_id: str) -> Dict:
        """Create a subscription"""
        data = {
            'customer': customer_id,
            'items': [{'price': price_id}]
        }
        response = requests.post(
            f"{self.base_url}/v1/subscriptions",
            headers=self.get_headers(),
            data=data
        )
        response.raise_for_status()
        return response.json()
    
    def list_webhooks(self) -> List[Dict]:
        """List configured webhooks"""
        response = requests.get(
            f"{self.base_url}/v1/webhook_endpoints",
            headers=self.get_headers()
        )
        response.raise_for_status()
        return response.json()['data']


# Connector Factory

def get_connector(integration) -> BaseConnector:
    """Factory function to get the appropriate connector for an integration"""
    connectors = {
        'readytech_jr': ReadyTechJRConnector,
        'vettrak': VETtrakConnector,
        'eskilled': eSkilledConnector,
        'cloudassess': CloudAssessConnector,
        'coursebox': CourseboxConnector,
        'moodle': MoodleConnector,
        'd2l_brightspace': D2LBrightspaceConnector,
        'quickbooks': QuickBooksConnector,
        'sage_intacct': SageIntacctConnector,
        'stripe': StripeConnector,
    }
    
    connector_class = connectors.get(integration.integration_type, BaseConnector)
    return connector_class(integration)
