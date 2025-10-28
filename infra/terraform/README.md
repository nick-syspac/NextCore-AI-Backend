Terraform root. Configure AWS OIDC roles and backend before apply.

# NextCore AI Cloud - AWS Infrastructure (ECS Fargate)

Complete Terraform infrastructure-as-code for deploying NextCore AI Cloud on AWS using ECS Fargate.

## Quick Start

```bash
# 1. Initialize backend
cd infra/terraform
./scripts/init-backend.sh production

# 2. Initialize Terraform
terraform init -backend-config="environments/production-backend.hcl"

# 3. Deploy infrastructure
terraform plan -var-file="environments/production.tfvars" -out=tfplan
terraform apply tfplan

# 4. Build and push Docker images
./scripts/push-images.sh production

# 5. Access application
terraform output alb_dns_name
```

## Architecture

**AWS Services:**
- **Compute**: ECS Fargate (serverless containers)
- **Load Balancer**: Application Load Balancer with HTTPS
- **Database**: RDS PostgreSQL 15 (Multi-AZ) with pgvector
- **Cache**: ElastiCache Redis 7 (cluster mode)
- **Storage**: S3 (documents, static assets, reports)
- **Networking**: VPC with public/private subnets across 3 AZs
- **Security**: IAM roles, KMS encryption, Secrets Manager, Security Groups
- **CI/CD**: ECR, CodeBuild, CodePipeline
- **Monitoring**: CloudWatch Logs, Metrics, Alarms

## Module Structure

```
infra/terraform/
├── main.tf                    # Root orchestration
├── variables.tf               # Global variables
├── outputs.tf                 # Stack outputs
├── backend.tf                 # S3 backend config
├── versions.tf                # Provider versions
│
├── environments/              # Environment configs
│   ├── dev.tfvars
│   ├── staging.tfvars
│   └── production.tfvars
│
├── modules/
│   ├── org/                   # IAM, KMS, Secrets Manager
│   ├── networking/            # VPC, subnets, NAT, security groups
│   ├── data/                  # RDS, ElastiCache, S3
│   ├── app/                   # ECS Fargate, ALB, services
│   └── ci/                    # ECR, CodeBuild
│
└── scripts/                   # Helper scripts
    ├── init-backend.sh
    ├── deploy.sh
    ├── push-images.sh
    └── destroy.sh
```

## Prerequisites

- Terraform >= 1.6.0
- AWS CLI >= 2.0
- Docker (for building images)
- AWS account with admin permissions

## Deployment Steps

### 1. Configure AWS Credentials

```bash
export AWS_PROFILE=nextcore-prod
export AWS_REGION=ap-southeast-2
```

### 2. Initialize Backend (First Time Only)

```bash
./scripts/init-backend.sh production
```

Creates S3 bucket and DynamoDB table for Terraform state.

### 3. Initialize Terraform

```bash
terraform init -backend-config="environments/production-backend.hcl"
```

### 4. Review Configuration

Edit `environments/production.tfvars`:
- Adjust instance sizes for your needs
- Configure domain name (optional)
- Review resource tags

### 5. Deploy Infrastructure

```bash
terraform plan -var-file="environments/production.tfvars" -out=tfplan
terraform apply tfplan
```

⏱️ **Initial deployment**: ~20-30 minutes

### 6. Build and Push Docker Images

```bash
./scripts/push-images.sh production
```

This builds:
- `control-plane`: Django API (port 8000)
- `web-portal`: Next.js frontend (port 3000)
- `worker`: Celery workers

### 7. Run Database Migrations

```bash
# Get cluster name
CLUSTER=$(terraform output -raw ecs_cluster_name)

# Run migration task
aws ecs run-task \
  --cluster $CLUSTER \
  --task-definition production-control-plane \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}" \
  --overrides '{"containerOverrides":[{"name":"control-plane","command":["python","manage.py","migrate"]}]}'
```

### 8. Access Application

```bash
# Get ALB DNS name
terraform output alb_dns_name

# API: http://<alb-dns>/api/
# Web: http://<alb-dns>/
```

## Environment-Specific Deployments

### Development
```bash
terraform apply -var-file="environments/dev.tfvars"
```
- Single AZ
- Smaller instance sizes
- No Multi-AZ RDS
- Cost: ~$200/month

### Staging
```bash
terraform apply -var-file="environments/staging.tfvars"
```
- 2 AZs
- Medium instance sizes
- Single-AZ RDS
- Cost: ~$400/month

### Production
```bash
terraform apply -var-file="environments/production.tfvars"
```
- 3 AZs
- Large instance sizes
- Multi-AZ RDS
- Cost: ~$850/month

## Configuration

### Custom Domain

1. Create ACM certificate:
```bash
aws acm request-certificate \
  --domain-name nextcore.ai \
  --subject-alternative-names *.nextcore.ai \
  --validation-method DNS
```

2. Update `production.tfvars`:
```hcl
domain_name         = "nextcore.ai"
acm_certificate_arn = "arn:aws:acm:..."
```

3. Create Route53 records:
```bash
# Point to ALB
aws route53 change-resource-record-sets ...
```

### Auto-Scaling

Services automatically scale based on:
- CPU > 70%
- Memory > 80%

Configure in tfvars:
```hcl
control_plane_count = 2  # Min: 2, Max: 6
web_portal_count    = 2  # Min: 2, Max: 6
worker_count        = 3  # Min: 3, Max: 9
```

## Monitoring

### CloudWatch Logs

```bash
# View logs
aws logs tail /ecs/production-nextcore --follow

# Filter by service
aws logs tail /ecs/production-nextcore --follow --filter-pattern control-plane
```

### CloudWatch Dashboard

Access via AWS Console:
- Metrics: CPU, Memory, Request Count, Latency
- Alarms: Configured for critical thresholds

### X-Ray Tracing

Enabled on all services for distributed tracing.

## Maintenance

### Update Images

```bash
# Build new images
./scripts/push-images.sh production

# Force new deployment
aws ecs update-service \
  --cluster production-nextcore-cluster \
  --service production-control-plane \
  --force-new-deployment
```

### Database Backup

Automated daily backups:
- Retention: 7 days
- Window: 03:00-04:00 UTC

Manual snapshot:
```bash
aws rds create-db-snapshot \
  --db-instance-identifier production-nextcore-db \
  --db-snapshot-identifier manual-backup-$(date +%Y%m%d)
```

### Secrets Rotation

```bash
# Rotate database password
aws secretsmanager rotate-secret \
  --secret-id production/db/credentials

# Update task definitions with new secret version
```

## Troubleshooting

### ECS Tasks Not Starting

```bash
# Check task logs
aws logs tail /ecs/production-nextcore/control-plane --follow

# Describe task
aws ecs describe-tasks --cluster production-nextcore-cluster --tasks <task-id>
```

### Database Connection Issues

```bash
# Test from ECS task
aws ecs execute-command \
  --cluster production-nextcore-cluster \
  --task <task-id> \
  --interactive \
  --command "/bin/bash"

# Inside container:
psql -h <db-endpoint> -U postgres -d rto
```

### High Costs

```bash
# Check Cost Explorer
aws ce get-cost-and-usage \
  --time-period Start=2025-01-01,End=2025-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE
```

Top cost drivers:
1. NAT Gateways: $120/month (3 AZs)
2. RDS: $250/month (db.t3.large Multi-AZ)
3. ECS Fargate: $240/month (compute)
4. ElastiCache: $120/month (cache.t3.medium × 2)

**Cost Optimization:**
- Use single NAT Gateway in non-prod (-$80/month)
- RDS Reserved Instances (-60%)
- Savings Plans for ECS (-50%)

## Security

### Implemented

✅ Encryption at rest (KMS)
✅ Encryption in transit (TLS 1.2+)
✅ VPC isolation (private subnets)
✅ Security groups (least privilege)
✅ IAM roles (no long-term credentials)
✅ Secrets Manager (no env var secrets)
✅ CloudWatch logging
✅ ECR image scanning

### Recommended Additions

- [ ] Enable AWS GuardDuty
- [ ] Enable AWS Security Hub
- [ ] Configure AWS Config rules
- [ ] Enable CloudTrail
- [ ] VPC Flow Logs analysis
- [ ] AWS WAF (if using custom domain)

## Disaster Recovery

### Backup Strategy

- **RDS**: Daily automated backups (7-day retention)
- **S3**: Versioning enabled
- **Terraform State**: Versioned in S3

### Recovery Procedures

**Database Restore:**
```bash
# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier production-nextcore-db-restored \
  --db-snapshot-identifier production-nextcore-final-20250128
```

**Complete Region Failover:**
1. Create RDS read replica in DR region
2. Promote replica to master
3. Deploy Terraform in DR region
4. Update DNS to DR ALB

**RPO**: 5 minutes (RDS point-in-time recovery)
**RTO**: 2-4 hours (complete failover)

## Cleanup

### Destroy Infrastructure

```bash
# ⚠️ WARNING: This deletes everything!
./scripts/destroy.sh production
```

### Manual Cleanup

```bash
# Delete S3 bucket contents
aws s3 rm s3://production-nextcore-documents-xxxxx --recursive
aws s3 rm s3://production-nextcore-static-xxxxx --recursive

# Delete backend resources
aws s3 rb s3://nextcore-terraform-state-production --force
aws dynamodb delete-table --table-name nextcore-terraform-locks-production
```

## Outputs

After deployment, view outputs:

```bash
terraform output

# Outputs:
# - vpc_id
# - alb_dns_name
# - ecr_repositories
# - db_endpoint (sensitive)
# - redis_endpoint (sensitive)
```

## Support

For issues:
1. Check CloudWatch Logs
2. Review ECS task status
3. Validate security group rules
4. Verify Secrets Manager values

---

**Last Updated**: 2025-01-28
**Terraform**: 1.6.0+
**AWS Provider**: 5.0.0+
