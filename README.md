# RTO SaaS Monorepo (Starter)

This is a production-ready **monorepo skeleton** for an RTO-focused SaaS platform. It’s designed for:
- Django/DRF control plane (tenant provisioning, lifecycle, RBAC, billing)
- FastAPI AI Gateway (model routing, usage metering)
- Next.js tenant web portal
- Worker processes (emails, ETL, background jobs)
- Terraform-managed AWS infra with GitHub OIDC
- Kubernetes manifests/Helm charts
- Compliance & audit hooks for ASQA/RTO Standards

> You can clone this repo and incrementally fill in the services. CI/CD and guardrails are pre-wired.
