# NextCore AI Cloud - AWS Deployment Guide

## Pre-Deployment Checklist

- [ ] AWS account with admin permissions
- [ ] AWS CLI configured (`aws configure`)
- [ ] Terraform >= 1.6.0 installed
- [ ] Docker installed (for building images)
- [ ] kubectl installed (optional, for debugging)

## Step-by-Step Deployment

### 1. Clone Repository

```bash
git clone https://github.com/your-org/NextCore-AI-Cloud.git
cd NextCore-AI-Cloud
```

### 2. Configure AWS Profile

```bash
export AWS_PROFILE=nextcore-production
export AWS_REGION=ap-southeast-2
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Verify credentials
aws sts get-caller-identity
```

### 3. Initialize Terraform Backend

```bash
cd infra/terraform

# Create S3 bucket and DynamoDB table for state
./scripts/init-backend.sh production
```

**Output:**
```
✓ S3 bucket configured: nextcore-terraform-state-production
✓ DynamoDB table configured: nextcore-terraform-locks-production
✓ Backend configuration written to: environments/production-backend.hcl
```

### 4. Review Configuration

Edit `environments/production.tfvars`:

```hcl
# Adjust for your needs
control_plane_count = 2  # Number of API instances
web_portal_count    = 2  # Number of web instances
worker_count        = 3  # Number of Celery workers

db_instance_class    = "db.t3.large"   # RDS instance size
redis_node_type      = "cache.t3.medium" # Redis instance size

# Optional: Custom domain
# domain_name         = "nextcore.ai"
# acm_certificate_arn = "arn:aws:acm:..."
```

### 5. Initialize Terraform

```bash
terraform init -backend-config="environments/production-backend.hcl"
```

**Expected output:**
```
Initializing modules...
Initializing the backend...
Terraform has been successfully initialized!
```

### 6. Validate Configuration

```bash
terraform validate
terraform fmt -check
```

### 7. Plan Deployment

```bash
terraform plan \
  -var-file="environments/production.tfvars" \
  -out=tfplan

# Review the plan carefully
# Expected: ~150 resources to be created
```

**Key resources:**
- VPC with 9 subnets (3 public, 3 private, 3 database)
- 3 NAT Gateways (one per AZ)
- RDS PostgreSQL (Multi-AZ)
- ElastiCache Redis (2 shards)
- ECS Fargate cluster with 3 services
- Application Load Balancer
- S3 buckets (documents, static, reports)
- IAM roles and policies
- KMS encryption keys
- Secrets Manager secrets

### 8. Apply Infrastructure

```bash
terraform apply tfplan
```

⏱️ **Duration**: 20-30 minutes

**Progress tracking:**
- Networking (VPC, subnets): 2-3 min
- Security (IAM, KMS, Secrets): 1-2 min
- Data layer (RDS, Redis, S3): 10-15 min
- Compute (ECS, ALB): 5-10 min
- CI/CD (ECR, CodeBuild): 2-3 min

### 9. Capture Outputs

```bash
# Save important outputs
terraform output > deployment-outputs.txt

# Get ALB DNS name
ALB_DNS=$(terraform output -raw alb_dns_name)
echo "Application URL: http://$ALB_DNS"

# Get ECR repositories
terraform output ecr_repositories
```

### 10. Build Docker Images

**Option A: Manual Build**

```bash
# Login to ECR
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build control-plane
docker build -t production-control-plane \
  -f apps/control-plane/Dockerfile .
docker tag production-control-plane:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/production-control-plane:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/production-control-plane:latest

# Build web-portal
docker build -t production-web-portal \
  -f apps/web-portal/Dockerfile .
docker tag production-web-portal:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/production-web-portal:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/production-web-portal:latest

# Build worker
docker build -t production-worker \
  -f apps/worker/Dockerfile .
docker tag production-worker:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/production-worker:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/production-worker:latest
```

**Option B: Use Helper Script**

```bash
./scripts/push-images.sh production
```

### 11. Run Database Migrations

```bash
# Get ECS cluster name
CLUSTER=$(terraform output -raw ecs_cluster_name)

# Get private subnet and security group
SUBNET=$(terraform output -json private_subnet_ids | jq -r '.[0]')
SG=$(terraform output -raw ecs_security_group_id)

# Run migration task
aws ecs run-task \
  --cluster $CLUSTER \
  --task-definition production-control-plane \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET],securityGroups=[$SG],assignPublicIp=DISABLED}" \
  --overrides '{
    "containerOverrides": [{
      "name": "control-plane",
      "command": ["python", "manage.py", "migrate"]
    }]
  }'

# Check migration logs
aws logs tail /ecs/production-nextcore/control-plane --follow
```

### 12. Verify Deployment

```bash
# Check ECS services
aws ecs describe-services \
  --cluster $CLUSTER \
  --services production-control-plane production-web-portal production-worker

# Check running tasks
aws ecs list-tasks --cluster $CLUSTER

# Test API endpoint
curl http://$ALB_DNS/api/health/

# Test web portal
curl http://$ALB_DNS/
```

### 13. Create Admin User

```bash
# Run Django createsuperuser in ECS task
TASK_ID=$(aws ecs list-tasks --cluster $CLUSTER --service-name production-control-plane --query 'taskArns[0]' --output text)

aws ecs execute-command \
  --cluster $CLUSTER \
  --task $TASK_ID \
  --container control-plane \
  --interactive \
  --command "python manage.py createsuperuser"
```

### 14. Configure DNS (Optional)

If using custom domain:

```bash
# Get ALB zone ID
ALB_ZONE=$(terraform output -raw alb_zone_id)
ALB_DNS=$(terraform output -raw alb_dns_name)

# Create Route53 records
aws route53 change-resource-record-sets \
  --hosted-zone-id ZXXXXX \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "nextcore.ai",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "'$ALB_ZONE'",
          "DNSName": "'$ALB_DNS'",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'
```

## Post-Deployment

### 1. Monitor CloudWatch

```bash
# View logs
aws logs tail /ecs/production-nextcore --follow

# Check alarms
aws cloudwatch describe-alarms --state-value ALARM
```

### 2. Test Auto-Scaling

```bash
# Trigger scale-up by increasing load
# Services will auto-scale based on CPU/memory

# Check current task count
aws ecs describe-services \
  --cluster $CLUSTER \
  --services production-control-plane \
  --query 'services[0].{desired:desiredCount,running:runningCount}'
```

### 3. Backup Configuration

```bash
# Export current state
terraform state pull > terraform-state-backup-$(date +%Y%m%d).json

# Export secrets ARNs (for documentation)
terraform output -json | jq '.db_secret_arn.value' > secrets-arns.txt
```

### 4. Set Up Monitoring Alerts

```bash
# Subscribe to SNS topic for alarms
SNS_TOPIC=$(aws sns list-topics --query 'Topics[?contains(TopicArn, `nextcore-production-alerts`)].TopicArn' --output text)

aws sns subscribe \
  --topic-arn $SNS_TOPIC \
  --protocol email \
  --notification-endpoint ops@nextcore.ai
```

## Troubleshooting

### Issue: ECS Tasks Failing to Start

**Symptoms:**
- Tasks show "PENDING" or repeatedly fail
- CloudWatch logs show connection errors

**Solutions:**

1. Check task definition:
```bash
aws ecs describe-task-definition --task-definition production-control-plane
```

2. Verify secrets exist:
```bash
aws secretsmanager list-secrets --query 'SecretList[?contains(Name, `production`)].Name'
```

3. Check security group rules:
```bash
aws ec2 describe-security-groups --group-ids $SG
```

### Issue: Database Connection Timeout

**Symptoms:**
- Tasks start but can't connect to RDS
- Logs show "connection refused"

**Solutions:**

1. Verify RDS endpoint:
```bash
terraform output db_endpoint
```

2. Check RDS security group allows ECS tasks:
```bash
aws ec2 describe-security-groups --group-ids $(terraform output -raw db_security_group_id)
```

3. Test connection from ECS task:
```bash
aws ecs execute-command --cluster $CLUSTER --task $TASK_ID --interactive --command "/bin/bash"
# Inside container:
psql -h <db-endpoint> -U postgres -d rto
```

### Issue: High Costs

**Solutions:**

1. Check current costs:
```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE
```

2. Optimize:
   - Use single NAT Gateway in non-prod
   - Enable RDS Reserved Instances
   - Use ECS Savings Plans
   - Reduce worker count during off-hours

## Rollback Procedures

### Rollback Infrastructure

```bash
# Restore previous state
terraform state pull > current-state-backup.json
terraform state push <previous-state-file>

# Apply previous configuration
terraform apply -var-file="environments/production.tfvars"
```

### Rollback Application

```bash
# Revert to previous image
aws ecs update-service \
  --cluster $CLUSTER \
  --service production-control-plane \
  --task-definition production-control-plane:42  # Previous revision
```

## Maintenance

### Update Infrastructure

```bash
# Make changes to .tf files or .tfvars
terraform plan -var-file="environments/production.tfvars" -out=tfplan
terraform apply tfplan
```

### Update Application

```bash
# Build new images
./scripts/push-images.sh production

# Force new deployment (zero-downtime)
aws ecs update-service --cluster $CLUSTER --service production-control-plane --force-new-deployment
aws ecs update-service --cluster $CLUSTER --service production-web-portal --force-new-deployment
aws ecs update-service --cluster $CLUSTER --service production-worker --force-new-deployment
```

### Rotate Secrets

```bash
# Rotate database password
aws secretsmanager rotate-secret \
  --secret-id production/db/credentials \
  --rotation-lambda-arn <lambda-arn>

# Update ECS services to pick up new secret
aws ecs update-service --cluster $CLUSTER --service production-control-plane --force-new-deployment
```

## Cost Breakdown

### Production Environment (Monthly)

| Service | Configuration | Cost |
|---------|--------------|------|
| ECS Fargate | 2 API + 2 Web + 3 Workers | $240 |
| RDS PostgreSQL | db.t3.large Multi-AZ | $250 |
| ElastiCache Redis | cache.t3.medium × 2 | $120 |
| NAT Gateways | 3 AZs | $120 |
| ALB | Standard | $25 |
| S3 | 100GB | $3 |
| CloudWatch | Logs + Metrics | $30 |
| Data Transfer | 100GB/month | $10 |
| **Total** | | **~$850/month** |

**Cost Optimization:**
- Use RDS Reserved Instances: -$150/month
- Use ECS Savings Plans: -$120/month
- Single NAT Gateway (non-prod): -$80/month

**Optimized Production**: ~$500/month

---

**Support**: ops@nextcore.ai
**Documentation**: https://docs.nextcore.ai/deployment
