# Contributing

## Branching & Commits
- Trunk-based: feature branches → PR → `main`
- Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `perf:`, `test:`

## PR Checklist
- Risk/rollback plan documented
- DB impact noted (tenant-aware migrations if applicable)
- Security scopes/roles reviewed
- Observability: metrics/logs/traces added where applicable
- Compliance note updated in `docs/compliance/` when needed

## Local Dev (Quickstart)
```bash
make bootstrap
make up
```
