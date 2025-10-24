# NextCore AI Cloud - Third-Party Integrations

This document provides implementation details for all supported third-party integrations.

## Overview

NextCore AI Cloud supports 14 third-party integrations across 4 categories:
- **SMS/RTO Systems** (4): ReadyTech JR Plus, VETtrak, eSkilled, plus legacy Axcelerate
- **LMS/Assessment** (5): CloudAssess, Coursebox, Moodle, D2L Brightspace, plus legacy Canvas
- **Accounting** (3): QuickBooks Online, Sage Intacct, plus existing Xero/MYOB
- **Payment Gateways** (1): Stripe (AU)

## Integration Priority Matrix

| Priority | Integration | Type | API Maturity | Implementation Status |
|----------|-------------|------|--------------|----------------------|
| **HIGH** | ReadyTech JR Plus | SMS/RTO | Stable REST, long-running docs | ✅ Connector ready |
| **HIGH** | VETtrak | SMS/RTO | Published API + change logs | ✅ Connector ready |
| **MEDIUM** | eSkilled | SMS+LMS | Confirm API surface | ✅ Connector ready |
| **MEDIUM** | CloudAssess | LMS/Assessment | Integrations common | ✅ Connector ready |
| **LOW-MED** | Coursebox | AI-LMS | Emerging API | ✅ Connector ready |
| **MEDIUM** | Moodle | LMS | Mature web services | ✅ Connector ready |
| **MEDIUM** | D2L Brightspace | LMS | Robust APIs/LTI | ✅ Connector ready |
| **LOW-MED** | QuickBooks Online | Accounting | REST + webhooks + sandbox | ✅ Connector ready |
| **MEDIUM** | Sage Intacct | Accounting | Modern REST (XML legacy) | ✅ Connector ready |
| **LOW** | Stripe (AU) | Payments | Industry standard | ✅ Connector ready |

## SMS/RTO Systems

### 1. ReadyTech JR Plus / Ready Student

**Target Market**: Major AU VET footprint (TAFEs & enterprise RTOs)  
**Value Proposition**: Win these = unlock big providers  
**API Priority**: **HIGH** - Stable REST, long-running platform docs

**Authentication**: OAuth 2.0 Bearer Token

**Key Endpoints**:
```python
GET  /api/v1/health           # Health check
GET  /api/v1/students         # Sync students
GET  /api/v1/units            # Units of competency
GET  /api/v1/enrolments       # Student enrolments
```

**Configuration Requirements**:
- `api_base_url`: ReadyTech instance URL
- `access_token`: OAuth bearer token
- `refresh_token`: For token renewal

**Data Sync Capabilities**:
- Students (bidirectional)
- Units of Competency (pull)
- Enrolments (bidirectional)
- Assessment outcomes (push)

### 2. VETtrak (ReadyTech)

**Target Market**: Longstanding AU RTO SMS; many private RTOs  
**API Priority**: **HIGH** - Published API + change logs

**Authentication**: API Key

**Key Endpoints**:
```python
GET  /api/v1/ping             # Connection test
GET  /api/v1/clients          # Student/client data
GET  /api/v1/programs         # Training programs
GET  /api/v1/enrolments       # Enrolment data
```

**Configuration Requirements**:
- `api_base_url`: VETtrak instance URL
- `api_key`: VETtrak API key

**Data Sync Capabilities**:
- Clients/Students
- Programs/Qualifications
- Enrolments
- Unit completions

### 3. eSkilled SMS+LMS

**Target Market**: AU-focused SMS+LMS targeting 2025 Standards  
**API Priority**: **MEDIUM** - Confirm API surface

**Authentication**: OAuth 2.0 Bearer Token

**Configuration Requirements**:
- `api_base_url`: eSkilled instance URL
- `access_token`: OAuth token

**Data Sync Capabilities**:
- Student records
- Course data
- LMS activity
- Compliance reports

### 4. Axcelerate (Legacy)

**Status**: Existing integration  
**Authentication**: WS Token

## LMS/Assessment Systems

### 5. CloudAssess

**Target Market**: Compliance-first assessment platform  
**Value Proposition**: Strong alignment with compliance AI  
**API Priority**: **MEDIUM** - Integrations common

**Authentication**: API Key (X-API-Key header)

**Key Endpoints**:
```python
GET  /api/v1/assessments              # Assessment list
GET  /api/v1/students/{id}/results    # Student results
POST /api/v1/assessments/{id}/submit  # Submit assessment
```

**Configuration Requirements**:
- `api_base_url`: CloudAssess instance URL
- `api_key`: CloudAssess API key

**Data Sync Capabilities**:
- Assessment templates
- Student submissions
- Marking/results
- Competency outcomes

### 6. Coursebox AI-LMS

**Target Market**: AU AI-LMS popular with new RTOs  
**Value Proposition**: Pairs well with AI modules  
**API Priority**: **LOW-MED** - Emerging API

**Authentication**: Bearer Token

**Configuration Requirements**:
- `api_base_url`: Coursebox instance URL
- `access_token`: API token

**Data Sync Capabilities**:
- Courses
- AI-generated content
- Student progress
- Analytics

### 7. Moodle

**Target Market**: Huge AU adoption across VET/HE  
**API Priority**: **MEDIUM** - Mature web services/plugins

**Authentication**: WS Token (Web Service Token)

**Key Endpoints**:
```python
# All via /webservice/rest/server.php with wsfunction parameter
core_webservice_get_site_info     # Site info/test
core_course_get_courses           # Course list
core_enrol_get_enrolled_users     # Course enrollments
core_grades_get_grades            # Student grades
```

**Configuration Requirements**:
- `api_base_url`: Moodle instance URL (e.g., https://moodle.example.edu.au)
- `api_key`: Web services token

**Data Sync Capabilities**:
- Courses
- Users/Students
- Enrolments
- Grades
- Activities

### 8. D2L Brightspace

**Target Market**: APAC professional education  
**API Priority**: **MEDIUM** - Robust APIs/LTI

**Authentication**: OAuth 2.0

**Key Endpoints**:
```python
GET  /d2l/api/versions/                    # API versions
GET  /d2l/api/lp/1.0/orgstructure/         # Org units
GET  /d2l/api/le/1.0/{orgUnitId}/content/  # Course content
```

**Configuration Requirements**:
- `api_base_url`: Brightspace instance URL
- `access_token`: OAuth token
- `client_id`, `client_secret`: OAuth credentials

**Data Sync Capabilities**:
- Organizational units
- Course content
- Grades
- User enrollments

### 9. Canvas LMS (Legacy)

**Status**: Existing integration  
**Authentication**: API Key

## Accounting Systems

### 10. QuickBooks Online

**Target Market**: Most common alternative to Xero/MYOB  
**API Priority**: **LOW-MED** - REST + webhooks + sandbox

**Authentication**: OAuth 2.0

**Key Endpoints**:
```python
GET  /v3/company/{realmId}/companyinfo/{realmId}  # Company info
POST /v3/company/{realmId}/invoice                # Create invoice
GET  /v3/company/{realmId}/query                  # SQL-like queries
```

**Configuration Requirements**:
- `api_base_url`: https://quickbooks.api.intuit.com
- `realm_id`: Company ID
- `access_token`: OAuth token
- `refresh_token`: For renewal

**Data Sync Capabilities**:
- Customers (students/organizations)
- Invoices
- Payments
- Chart of accounts

### 11. Sage Intacct

**Target Market**: Larger education/training organizations  
**API Priority**: **MEDIUM** - Modern REST (XML legacy)

**Authentication**: Session-based + Sender credentials

**Key Endpoints**:
```python
POST /ia/xml/xmlgw.phtml  # XML gateway (all operations)
```

**Configuration Requirements**:
- `api_base_url`: https://api.intacct.com
- `sender_id`: Company sender ID
- `sender_password`: Sender password
- `access_token`: Session token

**Data Sync Capabilities**:
- Customers
- Invoices
- Journal entries
- Financial reporting

### 12-13. Xero / MYOB (Legacy)

**Status**: Existing integrations  
**Authentication**: OAuth 2.0

## Payment Gateways

### 14. Stripe (AU)

**Target Market**: Online payments, subscriptions  
**Value Proposition**: Dominant gateway, PayTo/eftpos support  
**API Priority**: **LOW** (easy integration)

**Authentication**: Bearer Token (Secret Key)

**Key Endpoints**:
```python
GET  /v1/balance                  # Account balance
POST /v1/customers                # Create customer
POST /v1/payment_intents          # Create payment
POST /v1/subscriptions            # Create subscription
GET  /v1/webhook_endpoints        # List webhooks
```

**Configuration Requirements**:
- `api_base_url`: https://api.stripe.com
- `access_token`: Secret key (sk_live_... or sk_test_...)
- `webhook_secret`: For webhook signature verification

**Data Sync Capabilities**:
- Customer records
- Payment processing
- Subscription management
- Webhook events (payment success, subscription updates, etc.)

**Webhook Events**:
- `payment_intent.succeeded`
- `customer.created`
- `customer.updated`
- `invoice.paid`
- `subscription.created`
- `subscription.updated`

## API Usage

### Creating an Integration

```python
POST /api/tenants/{tenant_slug}/integrations/

{
    "integration_type": "readytech_jr",
    "name": "ReadyTech Production",
    "description": "Main SMS integration",
    "config": {
        "organization_id": "12345"
    },
    "api_base_url": "https://api.readytech.io",
    "access_token": "your-oauth-token"
}
```

### Testing Connection

```python
POST /api/tenants/{tenant_slug}/integrations/{id}/test_connection/

Response:
{
    "success": true,
    "message": "Connection successful",
    "details": {
        "integration_type": "readytech_jr",
        "integration_name": "ReadyTech JR Plus / Ready Student",
        "tested_at": "2025-10-24T10:30:00Z"
    }
}
```

### Syncing Data

```python
POST /api/tenants/{tenant_slug}/integrations/{id}/sync/

Response:
{
    "id": "abc123",
    "status": "active",
    "last_sync_at": "2025-10-24T10:35:00Z",
    "last_sync_status": "success"
}
```

### Viewing Logs

```python
GET /api/tenants/{tenant_slug}/integrations/{id}/logs/

Response:
[
    {
        "id": "log123",
        "action": "sync",
        "status": "success",
        "message": "Synced 150 student records",
        "created_at": "2025-10-24T10:35:00Z"
    }
]
```

## Implementation Roadmap

### Phase 1: High Priority (Weeks 1-2)
- ✅ ReadyTech JR Plus connector
- ✅ VETtrak connector
- 🔄 Production API credentials setup
- 🔄 OAuth flow implementation

### Phase 2: Medium Priority (Weeks 3-4)
- ✅ CloudAssess connector
- ✅ Moodle connector
- ✅ D2L Brightspace connector
- 🔄 LMS data sync workflows

### Phase 3: Accounting & Payments (Weeks 5-6)
- ✅ QuickBooks connector
- ✅ Sage Intacct connector
- ✅ Stripe connector
- 🔄 Payment webhooks
- 🔄 Invoice generation workflows

### Phase 4: Emerging Platforms (Week 7)
- ✅ Coursebox connector
- ✅ eSkilled connector
- 🔄 API surface validation

### Phase 5: Testing & Documentation (Week 8)
- 🔄 Integration test suite
- 🔄 Sandbox environment setup
- 🔄 Customer documentation
- 🔄 Migration guides

## Security Considerations

1. **Credential Storage**: All API keys and tokens encrypted at rest
2. **OAuth Refresh**: Automatic token refresh before expiration
3. **Rate Limiting**: Respect API rate limits per integration
4. **Webhook Verification**: Verify webhook signatures (Stripe, etc.)
5. **Audit Logging**: All API calls logged for compliance
6. **Data Privacy**: PHI/PII handling per integration requirements

## Support & Resources

### ReadyTech
- Developer Portal: https://developer.readytech.io
- API Docs: Check partner portal
- Support: Dedicated account manager

### VETtrak
- API Docs: Available in customer portal
- Support: support@vettrak.com.au

### CloudAssess
- Partner API: Check integrations page
- Support: Via partner program

### Moodle
- Web Services: https://docs.moodle.org/dev/Web_services
- Plugins: https://moodle.org/plugins

### D2L Brightspace
- Developer Portal: https://developers.brightspace.com
- API Reference: Valence Learning Framework

### QuickBooks
- Developer Site: https://developer.intuit.com
- Sandbox: Available via developer account

### Sage Intacct
- Developer Portal: https://developer.sage.com/intacct
- API Docs: XML and REST APIs

### Stripe
- API Docs: https://stripe.com/docs/api
- Test Mode: Full test environment available
- Webhooks: https://stripe.com/docs/webhooks

## Contact

For integration support or partnership inquiries:
- Email: integrations@nextcore.ai
- Slack: #integrations channel
- Documentation: https://docs.nextcore.ai/integrations
