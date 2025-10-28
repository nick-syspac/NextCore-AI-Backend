# Staging Environment Configuration
environment = "staging"
project     = "nextcore-ai-cloud"
region      = "ap-southeast-2"

# VPC Configuration
vpc_cidr           = "10.1.0.0/16"
availability_zones = ["ap-southeast-2a", "ap-southeast-2b"]

# RDS PostgreSQL (smaller for staging)
db_name              = "rto"
db_username          = "postgres"
db_instance_class    = "db.t3.medium"
db_allocated_storage = 50
db_multi_az          = false  # Single-AZ for cost savings

# ElastiCache Redis (smaller for staging)
redis_node_type  = "cache.t3.small"
redis_num_shards = 1

# ECS Fargate - Control Plane
control_plane_cpu    = 512
control_plane_memory = 1024
control_plane_count  = 1

# ECS Fargate - Web Portal
web_portal_cpu    = 256
web_portal_memory = 512
web_portal_count  = 1

# ECS Fargate - Workers
worker_cpu    = 512
worker_memory = 1024
worker_count  = 1

# Resource Tags
tags = {
  Environment = "staging"
  Project     = "NextCore-AI-Cloud"
  ManagedBy   = "Terraform"
  CostCenter  = "Engineering"
}
