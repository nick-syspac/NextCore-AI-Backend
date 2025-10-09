# Security Policy

- Report vulnerabilities privately to security@nextcollege.edu.au
- Do not commit secrets. All credentials must be stored in AWS Secrets Manager / SSM.
- CI/CD uses GitHub OIDC to assume AWS roles with least privilege.
- Container images are scanned with Trivy; SBOM generated with Syft. Failing scans block release.
