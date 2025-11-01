## [1.0.1](https://github.com/nick-syspac/NextCore-AI-Backend/compare/v1.0.0...v1.0.1) (2025-11-01)


### Bug Fixes

* update image reference in Trivy scan workflow to use lowercase repository name ([5d55fb7](https://github.com/nick-syspac/NextCore-AI-Backend/commit/5d55fb779b06f209ad10101620efca3ba3ab32e2))

# 1.0.0 (2025-11-01)


### Bug Fixes

* Update requests to 2.32.3 and add urllib3 2.2.3 in requirements ([eb557ca](https://github.com/nick-syspac/NextCore-AI-Backend/commit/eb557ca6f8c1d0b1fc30c80eabafd7bca8b25504))


### Features

* Add Adaptive Learning Pathway feature with personalized recommendations ([ec2de76](https://github.com/nick-syspac/NextCore-AI-Backend/commit/ec2de76341bdea273198f047eec3bac883a9ae9f))
* add competency gap finder module to control plane and web portal ([b85a105](https://github.com/nick-syspac/NextCore-AI-Backend/commit/b85a105cdbadb9778eb1a15b94415c0cf3a77138))
* Add Continuous Improvement module to control plane and web portal ([b31419d](https://github.com/nick-syspac/NextCore-AI-Backend/commit/b31419ddef0b93dc2857f54cca87a569779073e4))
* Add Continuous Improvement Register (CIR) functionality ([651c55f](https://github.com/nick-syspac/NextCore-AI-Backend/commit/651c55fbad83aed7e44ec3139f9c795ff36f6562))
* Add Document management models and implementation plan ([1ebb3a1](https://github.com/nick-syspac/NextCore-AI-Backend/commit/1ebb3a170ab67ec006e32ba0650859cf9000f867))
* Add Email/Message Assistant module with dashboard integration and UI components ([3783b0f](https://github.com/nick-syspac/NextCore-AI-Backend/commit/3783b0f90b1006a39254dcb7c01defcd673e5925))
* add engagement heatmap feature to tenant dashboard ([ad03c3b](https://github.com/nick-syspac/NextCore-AI-Backend/commit/ad03c3b44083f343b41e3e787633f6ea177c9339))
* add funding eligibility checker to tenant dashboard and implement eligibility check page ([f7ad02f](https://github.com/nick-syspac/NextCore-AI-Backend/commit/f7ad02f2b30550175aa57776b1e94e8901f6f737))
* Add Integrations and TAS Generator sections to Tenant Dashboard ([a4871dc](https://github.com/nick-syspac/NextCore-AI-Backend/commit/a4871dc607b012919f4405406a797a319514f7ec))
* Add Micro-Credential management functionality ([f12f767](https://github.com/nick-syspac/NextCore-AI-Backend/commit/f12f76701d77babcfe7b28b347483101b24e0bd7))
* Add Moderation Tool with session management, outlier detection, and bias scoring ([0f7e887](https://github.com/nick-syspac/NextCore-AI-Backend/commit/0f7e887ad9ece40294e741cf67a5f9380eb3ca4c))
* Add qualification selection and unit loading functionality ([bc00984](https://github.com/nick-syspac/NextCore-AI-Backend/commit/bc00984b28f27881861014a2ad0fd074165c572a))
* Add Rubric Generator functionality with NLP summarization and taxonomy tagging ([b73d338](https://github.com/nick-syspac/NextCore-AI-Backend/commit/b73d338dce531eb89f69d5825ac02b1b3b04c4ff))
* add semantic release configuration for automated versioning and changelog generation ([bb4f759](https://github.com/nick-syspac/NextCore-AI-Backend/commit/bb4f75966b22442ab184e1c51f3d0fc8ba230784))
* Add usage statistics components for tenant dashboard ([df31b11](https://github.com/nick-syspac/NextCore-AI-Backend/commit/df31b116236bc0c3f280a8f2da93d7c947bcbc54))
* **audit-assistant:** integrate audit assistant module into control plane and web portal ([dcfc168](https://github.com/nick-syspac/NextCore-AI-Backend/commit/dcfc16869a122f20d2bf6f2a72605b5f3ce2d6be))
* **audit:** refactor Audit model to control timestamp and hash calculation ([58b56ed](https://github.com/nick-syspac/NextCore-AI-Backend/commit/58b56ed1f94838434981cac58919303139418164))
* **authenticity-check:** add authenticity check functionality with views, serializers, and URLs ([56ed3a4](https://github.com/nick-syspac/NextCore-AI-Backend/commit/56ed3a4bfaa0c117f79c9913574cb62cbac9fab4))
* **evidence-mapper:** add Evidence Mapper functionality with CRUD operations, text extraction, tagging, and embedding search ([9818551](https://github.com/nick-syspac/NextCore-AI-Backend/commit/9818551e232f4fb0410a504e337d0d5685bbc90b))
* Implement audit logging with Celery integration and API endpoints ([78f59d9](https://github.com/nick-syspac/NextCore-AI-Backend/commit/78f59d92ce5d854a34e6d73a97004116ee4b916a))
* Implement Auto-Marker feature with API endpoints and frontend integration ([78376e3](https://github.com/nick-syspac/NextCore-AI-Backend/commit/78376e3cb9a3f97e177265ca5639fbcfba8c4ece))
* Implement Evidence and Snapshot Service for Course TAS management ([d40826f](https://github.com/nick-syspac/NextCore-AI-Backend/commit/d40826f01ae5b0524984d7ccfc41c07451e0d0fc))
* Implement funding eligibility system with Celery tasks and extended API endpoints ([0a961e5](https://github.com/nick-syspac/NextCore-AI-Backend/commit/0a961e5df0fb3138d5421bfbdeb0cbb08626e44d))
* Implement networking module with VPC, subnets, NAT gateways, and security groups ([d1bc9a5](https://github.com/nick-syspac/NextCore-AI-Backend/commit/d1bc9a5f7aaa3ad9e6ab7006aaccb93d6d7e2ce7))
* Implement TAS document management features including loading, editing, and deleting documents ([5436d61](https://github.com/nick-syspac/NextCore-AI-Backend/commit/5436d61086764002c1a62dfc7e4c0e4dda97c048))
* Initial commit of NextCore AI Cloud web portal ([490bead](https://github.com/nick-syspac/NextCore-AI-Backend/commit/490bead1a1cca2296fddae92ebd571c366312534))
* Initialize RTO SaaS Monorepo with Django, FastAPI, and Next.js ([6af6a59](https://github.com/nick-syspac/NextCore-AI-Backend/commit/6af6a59256d7b96a08804618b7770d22e90d32e9))
* integrate Rich Text Editor and enhance TAS page ([a1bb400](https://github.com/nick-syspac/NextCore-AI-Backend/commit/a1bb400dff0daf9b285be9b2756800a6d31d3946))
* **integrations:** add new connectors for ReadyTech JR, VETtrak, eSkilled, CloudAssess, Coursebox, Moodle, D2L Brightspace, QuickBooks, Sage Intacct, and Stripe ([025d537](https://github.com/nick-syspac/NextCore-AI-Backend/commit/025d5373dd148d65f21ea0fa7c5cbf36924df73d))
* **tenants:** Implement tenant management serializers, views, and tests ([f014beb](https://github.com/nick-syspac/NextCore-AI-Backend/commit/f014beb6a6f8576dd448170d26f6491d293bd9f3))
* Update funding eligibility views and API integration ([bfb312e](https://github.com/nick-syspac/NextCore-AI-Backend/commit/bfb312ea2d147c976f36fa067614c6231ce2068f))
* update TAS template management with new modals and API integration ([077cb8e](https://github.com/nick-syspac/NextCore-AI-Backend/commit/077cb8ec95c5366783d64d79fdfd526d3fad5c48))

# Changelog

All notable changes to the NextCore AI Cloud project.

## [2.0.0] - 2025-10-09

### 🎉 Major Release - Production Ready

This release represents a complete overhaul of the system with production-ready features, security hardening, and comprehensive functionality.

### ✨ Added

#### Security
- Enforced environment-based configuration with required SECRET_KEY
- Added comprehensive security headers (XSS, CSRF, Clickjacking protection)
- Implemented HSTS with preload support
- Added secure cookie configurations
- Configured rate limiting (100/hour anonymous, 1000/hour authenticated)
- Created custom exception handling with standardized error responses
- Added token-based authentication
- Implemented non-root Docker containers

#### Features - Control Plane
- Complete tenant management system with lifecycle (pending, active, suspended, deactivated)
- Multi-tier subscriptions (Free, Basic, Professional, Enterprise)
- Tenant quota management with usage tracking
- API key management per tenant with scopes and expiration
- User-tenant relationships with RBAC (Owner, Admin, Member, Viewer)
- Tenant activation, suspension, and restoration workflows
- Monthly quota reset functionality
- Comprehensive tenant API with ViewSets and custom actions

#### Features - AI Gateway
- Multi-provider AI routing (OpenAI, Anthropic)
- Intelligent model routing based on model identifiers
- Usage metering and token counting
- Real-time metrics collection in Redis
- Per-tenant rate limiting
- Request/response logging
- Health check and metrics endpoints
- Async/await for high performance
- Pydantic-based configuration and validation

#### Features - Worker
- Celery worker implementation with Django integration
- Outbox pattern for reliable audit event processing
- Comprehensive error handling and logging
- Scheduled tasks via Celery Beat
- Background job processing infrastructure

#### Features - Audit System
- Complete audit chain verification algorithm
- Detects tampering and broken links
- Reports detailed verification results
- Blockchain-inspired hash chaining
- Tenant-isolated audit logs

#### Infrastructure
- Multi-stage Docker builds for all services
- Health checks in all Dockerfiles
- Docker Compose with all services integrated
- Redis service with persistence
- Service dependency management and health checks
- Complete Kubernetes Helm charts with:
  - Deployments with init containers
  - Services and Ingress with TLS
  - ConfigMaps and Secrets
  - Horizontal Pod Autoscaler
  - Resource limits and requests
  - Security contexts
  - Liveness and readiness probes

#### Testing
- Comprehensive test suite for audit functionality
- Tenant management tests (models, API, quotas)
- API integration tests
- pytest configuration with coverage reporting
- Test fixtures and factories
- CI pipeline with PostgreSQL and Redis services

#### Development Tools
- Enhanced Makefile with 25+ commands
- Development environment bootstrap
- Automated testing, linting, and formatting
- Database management commands
- Log viewing shortcuts
- Security scanning commands

#### Documentation
- Comprehensive README with architecture overview
- Quick Start Guide for developers
- Production Deployment Checklist
- Implementation Summary
- API endpoint documentation
- Security features documentation
- Contributing guidelines
- Runbooks and compliance docs

#### Configuration
- .env.example with all required variables
- Pinned dependencies with exact versions
- pytest.ini configuration
- CI/CD enhancements with proper testing
- Structured logging configuration

### 🔄 Changed

- **Database**: Switched from SQLite to PostgreSQL
- **Settings**: Environment-based configuration throughout
- **Docker**: Updated to production-ready multi-stage builds
- **CI**: Fixed Python version matrix (removed 3.14, added 3.11-3.12)
- **Requirements**: Pinned all dependencies to specific versions
- **Logging**: Structured JSON logging for production
- **Authentication**: Enhanced with proper DRF configuration

### 🐛 Fixed

- Missing `timezone` import in audit tasks
- Database configuration mismatch between Docker Compose and Django
- Incomplete audit chain verification
- Missing Redis configuration in docker-compose
- Security vulnerabilities in Django settings
- Docker containers running as root
- Missing health checks
- Incomplete error handling
- Missing Celery dependencies

### 🔒 Security

- All secrets now required via environment variables
- No hardcoded credentials anywhere
- Security headers enabled
- HTTPS/TLS configuration for production
- Rate limiting implemented
- SQL injection protection via ORM
- XSS and CSRF protection enabled
- Secure session management
- Non-root Docker users
- Input validation with Pydantic

### 📦 Dependencies

Updated to latest stable versions:
- Django 5.1.2
- djangorestframework 3.15.2
- FastAPI 0.115.4
- Celery 5.4.0
- Redis 5.1.1
- psycopg 3.2.3
- pydantic 2.9.2

### 🗑️ Removed

- SQLite database configuration
- Hardcoded DEBUG=True
- Weak secret key fallback
- ALLOWED_HOSTS="*"
- Development server in production Dockerfile
- Root user in containers

---

## [1.0.0] - 2024-10-08

### Initial Release

- Basic Django control plane structure
- Minimal FastAPI AI gateway
- Audit model with basic chain
- Docker Compose setup
- Basic CI/CD pipeline
- Project structure and monorepo setup

---

## Legend

- 🎉 Major Release
- ✨ Added - New features
- 🔄 Changed - Changes to existing functionality
- 🐛 Fixed - Bug fixes
- 🔒 Security - Security improvements
- 📦 Dependencies - Dependency updates
- 🗑️ Removed - Removed features

---

**Format**: This changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
