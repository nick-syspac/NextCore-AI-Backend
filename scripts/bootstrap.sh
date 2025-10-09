#!/usr/bin/env bash
set -euo pipefail

echo ">> Creating local .env file if missing"
cp -n .env.example .env 2>/dev/null || true

echo ">> Starting local services (Postgres + MinIO + LocalStack)"
docker compose up -d

echo ">> Seeding demo tenant"
python apps/control-plane/manage.py seed_demo_tenant || true

echo "Done."
