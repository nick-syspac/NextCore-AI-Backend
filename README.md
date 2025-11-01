# NextCore AI Backend

Production-ready backend services for the NextCore AI RTO SaaS platform.

[![CI Status](https://github.com/nick-syspac/NextCore-AI-Backend/workflows/CI%20(Python)/badge.svg)](https://github.com/nick-syspac/NextCore-AI-Backend/actions)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🏗️ Architecture

This repository contains three main services:

- 🏢 **Control Plane** (Django/DRF) - Multi-tenant API, RBAC, audit logging, 20+ feature modules
- 🤖 **AI Gateway** (FastAPI) - AI model routing, usage metering, rate limiting
- ⚙️ **Worker** (Celery) - Background jobs, emails, ETL, scheduled tasks

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- PostgreSQL 16 with pgvector extension
- Redis 7

### Setup

```bash
# Clone repository
git clone https://github.com/nick-syspac/NextCore-AI-Backend.git
cd NextCore-AI-Backend

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Start all services
make up

# Run migrations
make migrate

# Create superuser
make createsuperuser
```

### Access Services

- **Control Plane API**: http://localhost:8000
- **Control Plane Admin**: http://localhost:8000/admin
- **AI Gateway**: http://localhost:8080
- **API Documentation**: http://localhost:8000/api/schema/swagger-ui/

## 📁 Project Structure

```
NextCore-AI-Backend/
├── apps/
│   ├── control-plane/          # Django REST API
│   │   ├── adaptive_pathway/   # Adaptive learning pathways
│   │   ├── assessment_builder/ # Assessment creation tools
│   │   ├── audit/              # Audit logging with blockchain
│   │   ├── audit_assistant/    # AI-powered audit assistance
│   │   ├── authenticity_check/ # Student work verification
│   │   ├── auto_marker/        # Automated marking
│   │   ├── competency_gap/     # Gap analysis
│   │   ├── continuous_improvement/ # CIR system
│   │   ├── email_assistant/    # Email automation
│   │   ├── engagement_heatmap/ # Student engagement tracking
│   │   ├── evidence_mapper/    # Evidence mapping
│   │   ├── feedback_assistant/ # Feedback generation
│   │   ├── funding_eligibility/# Eligibility checking with rules engine
│   │   ├── industry_currency/  # Industry currency tracking
│   │   ├── integrations/       # External system integrations
│   │   ├── intervention_tracker/ # Student interventions
│   │   ├── message_assistant/  # Messaging automation
│   │   ├── moderation_tool/    # Content moderation
│   │   ├── pd_tracker/         # Professional development
│   │   ├── policy_comparator/  # Policy comparison with vector search
│   │   ├── risk_engine/        # Risk assessment
│   │   ├── rubric_generator/   # Rubric creation
│   │   ├── study_coach/        # Student coaching
│   │   ├── tas/                # Training & Assessment System
│   │   ├── tenants/            # Multi-tenancy
│   │   ├── trainer_diary/      # Trainer activity logs
│   │   └── users/              # User management
│   ├── ai-gateway/             # FastAPI AI routing
│   └── worker/                 # Celery workers
├── libs/
│   ├── common-py/              # Shared Python utilities
│   └── observability/          # Logging, metrics, tracing
├── infra/
│   └── terraform/              # Infrastructure as Code
├── kubernetes/
│   ├── base/                   # Base Kubernetes configs
│   └── charts/                 # Helm charts
├── docs/
│   ├── architecture/           # Architecture Decision Records
│   ├── compliance/             # Compliance documentation
│   └── runbooks/               # Operational runbooks
├── db/
│   ├── migrations/             # Database migrations
│   └── seeds/                  # Seed data
├── docker-compose.yml
├── Makefile
└── pytest.ini
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

# Run specific app tests
cd apps/control-plane
pytest funding_eligibility/tests.py -v

# Run with coverage report
pytest --cov=. --cov-report=html
```

### Code Quality

```bash
make format      # Format with black
make lint        # Run flake8 and mypy
make typecheck   # Type checking only
make security    # Security checks with bandit
```

## 🎯 Key Features

### Control Plane (Django)

- ✅ Multi-tenant architecture with tenant isolation
- ✅ 20+ feature modules for RTO compliance
- ✅ Funding eligibility with JSONLogic rules engine
- ✅ Audit logging with blockchain-inspired chain verification
- ✅ Training & Assessment System (TAS)
- ✅ AI-powered assistants (email, feedback, messages)
- ✅ Assessment builder and auto-marker
- ✅ Policy comparison with pgvector semantic search
- ✅ RESTful API with token authentication
- ✅ PostgreSQL with pgvector extension
- ✅ Redis caching and session management

**API Endpoints**: `/api/schema/swagger-ui/` for full documentation

### AI Gateway (FastAPI)

- ✅ Multi-provider AI model routing (OpenAI, Anthropic)
- ✅ Real-time usage metering and token counting
- ✅ Per-tenant rate limiting
- ✅ Request/response logging
- ✅ Async/await for high performance
- ✅ Redis-based caching

### Worker (Celery)

- ✅ Audit event processing (outbox pattern)
- ✅ Email notifications
- ✅ Data exports
- ✅ Monthly quota resets
- ✅ Scheduled cleanups

## 🔒 Security

- ✅ Environment-based configuration (no hardcoded secrets)
- ✅ Strong password validation
- ✅ Security headers (XSS, CSRF, Clickjacking protection)
- ✅ Token-based authentication
- ✅ Rate limiting
- ✅ SQL injection protection (ORM)
- ✅ Input validation with Pydantic
- ✅ Non-root Docker containers
- ✅ Multi-stage Docker builds
- ✅ pgvector for secure vector storage

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

## 📊 Monitoring

- Structured JSON logging in production
- Contextual logging with tenant IDs
- Audit chain verification
- Health check endpoints
- (Planned) Prometheus metrics
- (Planned) OpenTelemetry tracing

## 🔗 Related Repositories

- **Frontend**: [NextCore-AI-Portal](https://github.com/nick-syspac/NextCore-AI-Portal) - Next.js web portal

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Architecture Decisions](docs/architecture/)
- [Compliance Controls](docs/compliance/controls-map.md)
- [Operational Runbooks](docs/runbooks/)
- [Getting Started Guide](GETTING-STARTED.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow conventional commits:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `refactor:` for refactoring
   - `test:` for tests
   - `chore:` for maintenance
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@nextcollege.edu.au
- 🔒 Security: security@nextcollege.edu.au

---

**Built with ❤️ for RTO organizations**
