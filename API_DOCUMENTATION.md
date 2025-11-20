# API Documentation

> [!IMPORTANT]
> **Full API Reference**: For a complete list of all available endpoints, parameters, and schemas, please refer to [API_REFERENCE.md](API_REFERENCE.md).


## Base URLs

- **Control Plane**: `http://localhost:8000` (dev) / `https://api.yourcompany.com` (prod)
- **AI Gateway**: `http://localhost:8080` (dev) / `https://ai.yourcompany.com` (prod)

## Authentication

All API endpoints (except health checks) require authentication using Token Authentication.

### Get Token

```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

**Response:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Using the Token

Include the token in the `Authorization` header:

```http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Control Plane API

### Tenants

#### List Tenants
```http
GET /api/tenants/
Authorization: Token {your-token}
```

**Query Parameters:**
- `page` - Page number
- `page_size` - Results per page (default: 50)

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Acme Corporation",
      "slug": "acme-corp",
      "domain": "",
      "status": "active",
      "subscription_tier": "professional",
      "contact_email": "admin@acme.com",
      "contact_name": "John Doe",
      "contact_phone": "+61400000000",
      "billing_email": "billing@acme.com",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "activated_at": "2024-01-01T00:00:00Z",
      "suspended_at": null,
      "suspension_reason": "",
      "settings": {},
      "quota": {
        "api_calls_limit": 100000,
        "api_calls_used": 1234,
        "api_calls_percentage": 1.23,
        "ai_tokens_limit": 1000000,
        "ai_tokens_used": 50000,
        "ai_tokens_percentage": 5.0,
        "storage_limit_gb": 100.0,
        "storage_used_gb": 12.5,
        "storage_percentage": 12.5,
        "max_users": 50,
        "current_users": 15,
        "quota_reset_at": "2024-02-01T00:00:00Z",
        "last_reset_at": "2024-01-01T00:00:00Z"
      },
      "user_count": 15
    }
  ]
}
```

#### Create Tenant
```http
POST /api/tenants/
Authorization: Token {your-token}
Content-Type: application/json

{
  "name": "New Company",
  "slug": "new-company",
  "contact_email": "admin@newcompany.com",
  "contact_name": "Jane Smith",
  "subscription_tier": "basic"
}
```

**Response:** `201 Created` with tenant object

#### Get Tenant
```http
GET /api/tenants/{slug}/
Authorization: Token {your-token}
```

#### Update Tenant
```http
PATCH /api/tenants/{slug}/
Authorization: Token {your-token}
Content-Type: application/json

{
  "contact_name": "Updated Name",
  "subscription_tier": "professional"
}
```

#### Activate Tenant
```http
POST /api/tenants/{slug}/activate/
Authorization: Token {your-token}
```

Requires admin permissions.

#### Suspend Tenant
```http
POST /api/tenants/{slug}/suspend/
Authorization: Token {your-token}
Content-Type: application/json

{
  "reason": "Payment overdue"
}
```

Requires admin permissions.

#### Restore Tenant
```http
POST /api/tenants/{slug}/restore/
Authorization: Token {your-token}
```

Requires admin permissions.

#### Get Tenant Quota
```http
GET /api/tenants/{slug}/quota/
Authorization: Token {your-token}
```

#### Reset Tenant Quota
```http
POST /api/tenants/{slug}/reset_quota/
Authorization: Token {your-token}
```

Requires admin permissions.

### Audit Logs

#### List Audit Events
```http
GET /api/audit/events/
Authorization: Token {your-token}
```

**Query Parameters:**
- `tenant_id` - Filter by tenant
- `event_type` - Filter by event type
- `since` - ISO timestamp, events after this date
- `page` - Page number
- `page_size` - Results per page

**Response:**
```json
[
  {
    "id": 1,
    "tenant_id": "tenant-123",
    "event_type": "user.created",
    "payload": {
      "user_id": "456",
      "email": "user@example.com"
    },
    "timestamp": "2024-01-01T00:00:00Z",
    "prev_hash": null,
    "hash": "a1b2c3d4..."
  }
]
```

#### Verify Audit Chain
```http
GET /api/audit/verify/
Authorization: Token {your-token}
```

**Query Parameters:**
- `tenant_id` - Verify chain for specific tenant (optional)

**Response:**
```json
{
  "chain_valid": true,
  "verified_count": 1500,
  "total_events": 1500,
  "chain_head": "9a8b7c6d5e4f3a2b1c0d..."
}
```

If chain is broken:
```json
{
  "chain_valid": false,
  "verified_count": 1498,
  "total_events": 1500,
  "chain_head": "9a8b7c6d5e4f3a2b1c0d...",
  "broken_links": [
    {
      "event_id": 150,
      "event_type": "user.updated",
      "timestamp": "2024-01-15T10:30:00Z",
      "reason": "Hash mismatch - potential tampering detected",
      "computed_hash": "abc123...",
      "stored_hash": "def456..."
    }
  ]
}
```

### Tenant Users

#### List Tenant Users
```http
GET /api/tenant-users/
Authorization: Token {your-token}
```

#### Create Tenant User
```http
POST /api/tenant-users/
Authorization: Token {your-token}
Content-Type: application/json

{
  "tenant": "tenant-id-here",
  "user": "user-id-here",
  "role": "member"
}
```

**Roles:** `owner`, `admin`, `member`, `viewer`

### API Keys

#### List API Keys
```http
GET /api/api-keys/
Authorization: Token {your-token}
```

#### Create API Key
```http
POST /api/api-keys/
Authorization: Token {your-token}
Content-Type: application/json

{
  "tenant": "tenant-id-here",
  "name": "Production API Key",
  "scopes": ["read", "write"],
  "expires_at": "2025-12-31T23:59:59Z"
}
```

#### Revoke API Key
```http
POST /api/api-keys/{id}/revoke/
Authorization: Token {your-token}
```

## AI Gateway API

### Chat Completions

```http
POST /v1/chat/completions
Content-Type: application/json

{
  "model": "gpt-4",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000,
  "tenant_id": "your-tenant-id"
}
```

**Supported Models:**
- OpenAI: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, `o1-preview`, `o1-mini`
- Anthropic: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`

**Response:**
```json
{
  "id": "chatcmpl-123",
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 10,
    "total_tokens": 30
  },
  "created": 1704067200
}
```

### Get Metrics

```http
GET /metrics/{tenant_id}
```

**Response:**
```json
{
  "tenant_id": "tenant-123",
  "daily": {
    "gpt-4": "1500",
    "claude-3-sonnet": "800"
  },
  "monthly": {
    "total": "50000"
  }
}
```

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "ai-gateway",
  "redis": "connected"
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "error_code",
    "message": "Human readable error message",
    "details": {
      "field": ["Field-specific error"]
    }
  }
}
```

### Common Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests (Rate Limited)
- `500` - Internal Server Error
- `502` - Bad Gateway (Provider error)
- `503` - Service Unavailable

### Example Error Response

```json
{
  "error": {
    "code": "tenant_required",
    "message": "Tenant context is required for this operation.",
    "details": {}
  }
}
```

## Rate Limits

### Control Plane
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour

### AI Gateway
- Default: 60 requests/minute per tenant
- Configurable via `RATE_LIMIT_PER_MINUTE` environment variable

Rate limit headers:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1704067260
```

## Pagination

List endpoints support pagination:

**Request:**
```http
GET /api/tenants/?page=2&page_size=25
```

**Response:**
```json
{
  "count": 100,
  "next": "http://api.example.com/api/tenants/?page=3",
  "previous": "http://api.example.com/api/tenants/?page=1",
  "results": [...]
}
```

## Filtering and Search

Many endpoints support filtering:

```http
GET /api/audit/events/?tenant_id=tenant-123&event_type=user.created&since=2024-01-01T00:00:00Z
```

## Best Practices

1. **Always use HTTPS in production**
2. **Store tokens securely** - Never log or expose them
3. **Handle rate limits gracefully** - Implement exponential backoff
4. **Set appropriate timeouts** - Default is 60 seconds
5. **Log API errors** - For debugging and monitoring
6. **Validate input** - Before sending to API
7. **Use pagination** - For large result sets
8. **Monitor usage** - Check metrics endpoint regularly

## SDKs and Libraries

Coming soon! We're working on official SDKs for:
- Python
- JavaScript/TypeScript
- Go
- Ruby

## Support

- 📖 Documentation: [README.md](README.md)
- 🐛 Report Issues: GitHub Issues
- 📧 Email: support@nextcollege.edu.au
- 💬 Chat: Coming soon

---

**Last Updated:** October 9, 2025
**API Version:** 2.0.0
