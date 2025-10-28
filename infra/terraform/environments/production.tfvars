# Production Environment Configuration
environment = "production"
project     = "nextcore-ai-cloud"
region      = "ap-southeast-2"

# VPC Configuration
vpc_cidr           = "10.0.0.0/16"
availability_zones = ["ap-southeast-2a", "ap-southeast-2b", "ap-southeast-2c"]

# RDS PostgreSQL
db_name              = "rto"
db_username          = "postgres"
db_instance_class    = "db.t3.large"
db_allocated_storage = 100
db_multi_az          = true

# ElastiCache Redis
redis_node_type  = "cache.t3.medium"
redis_num_shards = 2

# ECS Fargate - Control Plane (Django API)
control_plane_cpu    = 1024  # 1 vCPU
control_plane_memory = 2048  # 2 GB
control_plane_count  = 2

# ECS Fargate - Web Portal (Next.js)
web_portal_cpu    = 512   # 0.5 vCPU
web_portal_memory = 1024  # 1 GB
web_portal_count  = 2

# ECS Fargate - Workers (Celery)
worker_cpu    = 1024  # 1 vCPU
worker_memory = 2048  # 2 GB
worker_count  = 3

# Domain & SSL (Optional - configure if using custom domain)
# domain_name         = "nextcore.ai"
# acm_certificate_arn = "arn:aws:acm:ap-southeast-2:ACCOUNT_ID:certificate/CERT_ID"

# CI/CD Configuration
# github_owner  = "your-github-org"
# github_repo   = "NextCore-AI-Cloud"
# github_branch = "main"

# Resource Tags
tags = {
  Environment = "production"
  Project     = "NextCore-AI-Cloud"
  ManagedBy   = "Terraform"
  CostCenter  = "Engineering"
}
