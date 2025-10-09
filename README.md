# NextCore AI Cloud - RTO SaaS Platform

[![CI Status](https://github.com/nick-syspac/NextCore-AI-Cloud/workflows/CI%20(Python)/badge.svg)](https://github.com/nick-syspac/NextCore-AI-Cloud/actions)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This is a production-ready **monorepo** for an RTO-focused SaaS platform. It's designed for:

- 🏢 **Django/DRF Control Plane** - Tenant provisioning, lifecycle, RBAC, billing, audit logging
- 🤖 **FastAPI AI Gateway** - Model routing, usage metering, rate limiting, multi-provider support
- 🌐 **Next.js Web Portal** - Modern tenant web interface (coming soon)
- ⚙️ **Celery Workers** - Background jobs, emails, ETL, scheduled tasks
- 🏗️ **Infrastructure as Code** - Terraform-managed AWS infra with GitHub OIDC
- ☸️ **Kubernetes Ready** - Helm charts for containerized deployments
- 📋 **Compliance Built-in** - Audit hooks for ASQA/RTO Standards

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Make (optional but recommended)

### Setup

1. **Clone and configure:**

```bash
git clone https://github.com/nick-syspac/NextCore-AI-Cloud.git
cd NextCore-AI-Cloud
cp .env.example .env
# Edit .env with your configuration
```

2. **Start services:**

```bash
make up
```

3. **Run migrations:**

```bash
make migrate
```

4. **Create superuser:**

```bash
make createsuperuser
```

5. **Access services:**

- Control Plane: http://localhost:8000
- Control Plane Admin: http://localhost:8000/admin
- AI Gateway: http://localhost:8080
- MinIO Console: http://localhost:9001

## 📁 Project Structure

```
NextCore-AI-Cloud/
├── apps/
│   ├── control-plane/      # Django REST API for tenant & user management
│   ├── ai-gateway/          # FastAPI gateway for AI model routing
│   ├── worker/              # Celery background workers
│   └── web-portal/          # Next.js frontend (planned)
├── libs/
│   ├── common-py/           # Shared Python utilities
│   └── observability/       # Logging, metrics, tracing
├── infra/
│   └── terraform/           # Infrastructure as Code
├── kubernetes/
│   ├── base/                # Base Kubernetes configs
│   └── charts/              # Helm charts
├── docs/
│   ├── architecture/        # Architecture Decision Records
│   ├── compliance/          # Compliance documentation
│   └── runbooks/            # Operational runbooks
└── db/
    ├── migrations/          # Database migration scripts
    └── seeds/               # Seed data
```

## 🛠️ Development

### Available Commands

```bash
make help              # Show all available commands
make install           # Install dependencies
make up                # Start all services
make down              # Stop all services
make logs              # View all logs
make test              # Run tests with coverage
make lint              # Run linters
make format            # Format code
make migrate           # Run database migrations
make shell             # Open Django shell
make clean             # Clean temporary files
```

### Running Tests

```bash
# Run all tests with coverage
make test

# Run fast tests (no coverage)
make test-fast

# Run specific test file
cd apps/control-plane
pytest audit/tests.py -v
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Fix linting issues
make lint-fix

# Type checking
make typecheck

# Security checks
make security
```

## 🏗️ Architecture

### Control Plane (Django)

**Key Features:**
- Multi-tenant architecture with tenant isolation
- Role-based access control (RBAC)
- Audit logging with blockchain-inspired chain verification
- RESTful API with token authentication
- PostgreSQL database with connection pooling
- Redis caching and session management

**API Endpoints:**
- `/api/auth/token/` - Get authentication token
- `/api/tenants/` - Tenant management
- `/api/tenant-users/` - User-tenant relationships
- `/api/api-keys/` - API key management
- `/api/audit/events/` - Audit log access
- `/api/audit/verify/` - Audit chain verification

### AI Gateway (FastAPI)

**Key Features:**
- Multi-provider AI model routing (OpenAI, Anthropic)
- Real-time usage metering and token counting
- Rate limiting per tenant
- Request/response logging
- Async/await for high performance
- Redis-based caching and metrics

**API Endpoints:**
- `/v1/chat/completions` - Chat completion proxy
- `/metrics/{tenant_id}` - Usage metrics
- `/health` - Health check

### Worker (Celery)

**Background Tasks:**
- Audit event processing (outbox pattern)
- Email notifications
- Data exports
- Monthly quota resets
- Scheduled cleanups

## 🔒 Security

### Implemented Features

- ✅ Environment-based configuration (no hardcoded secrets)
- ✅ Strong password validation
- ✅ HTTPS/TLS in production (via settings)
- ✅ Security headers (XSS, CSRF, Clickjacking protection)
- ✅ Token-based authentication
- ✅ Rate limiting
- ✅ SQL injection protection (ORM)
- ✅ Input validation with Pydantic
- ✅ Non-root Docker containers
- ✅ Multi-stage Docker builds

### Best Practices

1. **Never commit secrets** - Use environment variables
2. **Rotate credentials regularly** - Especially API keys
3. **Enable 2FA** - For admin accounts
4. **Monitor audit logs** - Regular chain verification
5. **Keep dependencies updated** - Use Dependabot
6. **Run security scans** - `make security`

## 📊 Monitoring & Observability

### Logging

- Structured JSON logging in production
- Contextual logging with tenant IDs
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Metrics (Planned)

- Prometheus for metrics collection
- Grafana for visualization
- Custom metrics for business KPIs

### Tracing (Planned)

- Distributed tracing with OpenTelemetry
- Jaeger for trace visualization

## 🚢 Deployment

### Docker Compose (Development)

```bash
make up
```

### Kubernetes (Production)

```bash
# Install Helm charts
helm install control-plane ./kubernetes/charts/control-plane
helm install ai-gateway ./kubernetes/charts/ai-gateway
helm install worker ./kubernetes/charts/worker
```

### Terraform (Infrastructure)

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

## 🧪 Testing

### Test Coverage

Current coverage: Run `make test` to see latest

### Test Structure

```
apps/control-plane/
├── audit/tests.py           # Audit functionality tests
├── tenants/tests.py         # Tenant management tests
└── conftest.py              # Pytest fixtures
```

## 📚 Documentation

- [Architecture Decisions](docs/architecture/)
- [Compliance Controls](docs/compliance/controls-map.md)
- [Operational Runbooks](docs/runbooks/)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@nextcollege.edu.au
- 🔒 Security: security@nextcollege.edu.au
- 📖 Docs: [Coming soon]

## 🗺️ Roadmap

### Phase 1 (Current)
- [x] Django control plane setup
- [x] AI Gateway implementation
- [x] Tenant management
- [x] Audit logging with chain verification
- [x] Docker containerization
- [x] CI/CD pipeline

### Phase 2 (Q1 2026)
- [ ] Next.js web portal
- [ ] Stripe billing integration
- [ ] Advanced RBAC with permissions
- [ ] Email notification system
- [ ] Data export functionality
- [ ] Comprehensive Helm charts

### Phase 3 (Q2 2026)
- [ ] Terraform AWS deployment
- [ ] Production Kubernetes setup
- [ ] Monitoring & alerting
- [ ] Advanced AI features
- [ ] Multi-region support
- [ ] Compliance certifications

---

**Built with ❤️ for RTO organizations**onorepo (Starter)

This is a production-ready **monorepo skeleton** for an RTO-focused SaaS platform. It’s designed for:
- Django/DRF control plane (tenant provisioning, lifecycle, RBAC, billing)
- FastAPI AI Gateway (model routing, usage metering)
- Next.js tenant web portal
- Worker processes (emails, ETL, background jobs)
- Terraform-managed AWS infra with GitHub OIDC
- Kubernetes manifests/Helm charts
- Compliance & audit hooks for ASQA/RTO Standards

> You can clone this repo and incrementally fill in the services. CI/CD and guardrails are pre-wired.
