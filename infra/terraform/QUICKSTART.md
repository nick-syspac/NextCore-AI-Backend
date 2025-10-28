# NextCore AI Cloud - AWS Infrastructure Quick Reference

## 🚀 Quick Deployment Commands

```bash
# 1. Initialize backend
cd infra/terraform && ./scripts/init-backend.sh production

# 2. Deploy infrastructure (20-30 min)
terraform init -backend-config="environments/production-backend.hcl"
terraform apply -var-file="environments/production.tfvars"

# 3. Push Docker images
./scripts/push-images.sh production

# 4. Get application URL
terraform output alb_dns_name
```

## 📁 Repository Structure

```
NextCore-AI-Cloud/
├── apps/
│   ├── control-plane/     # Django API (port 8000)
│   ├── web-portal/        # Next.js UI (port 3000)
│   └── worker/            # Celery workers
├── infra/terraform/
│   ├── modules/
│   │   ├── org/           # IAM, KMS, Secrets
│   │   ├── networking/    # VPC, subnets, NAT
│   │   ├── data/          # RDS, Redis, S3
│   │   ├── app/           # ECS Fargate, ALB
│   │   └── ci/            # ECR, CodeBuild
│   ├── environments/      # dev/staging/production.tfvars
│   └── scripts/           # Helper scripts
```

## 🏗️ Infrastructure Components

| Component | Service | Configuration |
|-----------|---------|---------------|
| **Compute** | ECS Fargate | 2 API + 2 Web + 3 Workers |
| **Load Balancer** | ALB | HTTP/HTTPS with path routing |
| **Database** | RDS PostgreSQL 15 | Multi-AZ, pgvector, 100GB |
| **Cache** | ElastiCache Redis 7 | 2 shards, cluster mode |
| **Storage** | S3 | 3 buckets (encrypted, versioned) |
| **Network** | VPC | 9 subnets across 3 AZs |
| **Security** | IAM/KMS | Least-privilege roles, encryption |
| **Monitoring** | CloudWatch | Logs, metrics, alarms |

## 💰 Cost Estimates (Monthly)

| Environment | Configuration | Cost |
|-------------|--------------|------|
| **Development** | 1 AZ, small instances | ~$200 |
| **Staging** | 2 AZ, medium instances | ~$400 |
| **Production** | 3 AZ, large instances | ~$850 |

**Production Optimized** (with Reserved Instances + Savings Plans): ~$500

## 🔧 Common Operations

### View Application

```bash
# Get URL
ALB=$(terraform output -raw alb_dns_name)

# API health check
curl http://$ALB/api/health/

# Web portal
open http://$ALB
```

### View Logs

```bash
# Tail all logs
aws logs tail /ecs/production-nextcore --follow

# Filter by service
aws logs tail /ecs/production-nextcore --follow --filter-pattern control-plane
```

### Update Application

```bash
# Build new images
./scripts/push-images.sh production

# Force deployment (zero-downtime)
CLUSTER=$(terraform output -raw ecs_cluster_name)
aws ecs update-service --cluster $CLUSTER --service production-control-plane --force-new-deployment
```

### Scale Services

```bash
# Update tfvars
control_plane_count = 4  # Scale from 2 to 4

# Apply changes
terraform apply -var-file="environments/production.tfvars"
```

### Run Database Migration

```bash
CLUSTER=$(terraform output -raw ecs_cluster_name)
SUBNET=$(terraform output -json private_subnet_ids | jq -r '.[0]')
SG=$(terraform output -raw ecs_security_group_id)

aws ecs run-task \
  --cluster $CLUSTER \
  --task-definition production-control-plane \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET],securityGroups=[$SG]}" \
  --overrides '{"containerOverrides":[{"name":"control-plane","command":["python","manage.py","migrate"]}]}'
```

### Access Database

```bash
# Get credentials
DB_ENDPOINT=$(terraform output -raw db_endpoint)
DB_SECRET=$(terraform output -raw db_secret_arn)
DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id $DB_SECRET --query SecretString --output text | jq -r .password)

# Connect
psql -h $(echo $DB_ENDPOINT | cut -d: -f1) -U postgres -d rto
```

### Backup Database

```bash
# Manual snapshot
aws rds create-db-snapshot \
  --db-instance-identifier production-nextcore-db \
  --db-snapshot-identifier manual-backup-$(date +%Y%m%d)

# Export to S3
aws rds start-export-task \
  --export-task-identifier export-$(date +%Y%m%d) \
  --source-arn <snapshot-arn> \
  --s3-bucket-name backups-bucket \
  --iam-role-arn <role-arn>
```

## 🔐 Security Checklist

- [x] Encryption at rest (KMS)
- [x] Encryption in transit (TLS)
- [x] Secrets in Secrets Manager
- [x] IAM roles (no keys)
- [x] Private subnets for compute/data
- [x] Security groups (least privilege)
- [x] CloudWatch logging enabled
- [x] ECR image scanning enabled
- [ ] Enable GuardDuty
- [ ] Enable Security Hub
- [ ] Configure CloudTrail
- [ ] Enable WAF (if custom domain)

## 📊 Monitoring

### Key Metrics

```bash
# ECS service status
aws ecs describe-services --cluster $CLUSTER --services production-control-plane

# Task count
aws ecs list-tasks --cluster $CLUSTER

# Active alarms
aws cloudwatch describe-alarms --state-value ALARM
```

### CloudWatch Dashboard

Navigate to: CloudWatch → Dashboards → `production-nextcore`

**Metrics:**
- ECS CPU/Memory utilization
- ALB request count, latency, 5xx errors
- RDS connections, CPU, storage
- Redis CPU, evictions, connections

## 🚨 Troubleshooting

### ECS Tasks Not Starting

```bash
# Check task logs
aws logs tail /ecs/production-nextcore/control-plane --follow

# Describe failed task
aws ecs describe-tasks --cluster $CLUSTER --tasks <task-id>

# Common issues:
# 1. Missing secrets → Check Secrets Manager
# 2. Wrong IAM permissions → Review task role
# 3. Image not found → Verify ECR repository
```

### Database Connection Errors

```bash
# Verify RDS is running
aws rds describe-db-instances --db-instance-identifier production-nextcore-db

# Check security group allows ECS
aws ec2 describe-security-groups --group-ids $(terraform output -raw db_security_group_id)

# Test connection from ECS
aws ecs execute-command --cluster $CLUSTER --task <task-id> --interactive --command "/bin/bash"
```

### High Costs

```bash
# View cost breakdown
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE

# Top cost drivers:
# - NAT Gateways: Use 1 in non-prod
# - RDS: Use Reserved Instances
# - ECS: Use Savings Plans
```

## 🔄 CI/CD Integration

### Manual Build & Deploy

```bash
# Build images locally
docker build -t control-plane -f apps/control-plane/Dockerfile .

# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URL
docker tag control-plane:latest $ECR_URL/production-control-plane:latest
docker push $ECR_URL/production-control-plane:latest

# Update service
aws ecs update-service --cluster $CLUSTER --service production-control-plane --force-new-deployment
```

### GitHub Actions (Example)

```yaml
name: Deploy to AWS
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-region: ap-southeast-2
      - name: Build and push
        run: |
          ./infra/terraform/scripts/push-images.sh production
```

## 📞 Support Contacts

| Issue | Contact |
|-------|---------|
| Infrastructure | ops@nextcore.ai |
| Application | dev@nextcore.ai |
| Security | security@nextcore.ai |
| Billing | finance@nextcore.ai |

## 📚 Additional Resources

- [Full Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Architecture Documentation](./README.md)
- [Troubleshooting Guide](./README.md#troubleshooting)
- [Cost Optimization](./README.md#cost-estimation)

---

**Version**: 1.0.0  
**Last Updated**: 2025-01-28  
**Terraform**: 1.6.0+  
**AWS Provider**: 5.0.0+
