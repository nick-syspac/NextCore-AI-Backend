# Development Environment Configuration
environment = "dev"
project     = "nextcore-ai-cloud"
region      = "ap-southeast-2"

# VPC Configuration
vpc_cidr           = "10.2.0.0/16"
availability_zones = ["ap-southeast-2a", "ap-southeast-2b"]

# RDS PostgreSQL (minimal for dev)
db_name              = "rto"
db_username          = "postgres"
db_instance_class    = "db.t3.small"
db_allocated_storage = 20
db_multi_az          = false

# ElastiCache Redis (minimal for dev)
redis_node_type  = "cache.t3.micro"
redis_num_shards = 1

# ECS Fargate - Control Plane
control_plane_cpu    = 256
control_plane_memory = 512
control_plane_count  = 1

# ECS Fargate - Web Portal
web_portal_cpu    = 256
web_portal_memory = 512
web_portal_count  = 1

# ECS Fargate - Workers
worker_cpu    = 256
worker_memory = 512
worker_count  = 1

# Resource Tags
tags = {
  Environment = "dev"
  Project     = "NextCore-AI-Cloud"
  ManagedBy   = "Terraform"
  CostCenter  = "Engineering"
}
