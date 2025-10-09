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
