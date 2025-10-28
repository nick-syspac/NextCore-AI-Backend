# NextCore AI Cloud - AWS Infrastructure
# Root orchestration for ECS Fargate deployment

# Organization setup (IAM roles, KMS keys, Secrets Manager)
module "org" {
  source = "./org"

  environment = var.environment
  project     = var.project
  tags        = var.tags
}

# VPC, subnets, NAT gateways, security groups
module "networking" {
  source = "./networking"

  environment        = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  tags               = var.tags
}

# RDS PostgreSQL, ElastiCache Redis, S3 buckets
module "data" {
  source = "./data"

  environment       = var.environment
  vpc_id            = module.networking.vpc_id
  database_subnets  = module.networking.database_subnet_ids
  cache_subnets     = module.networking.private_subnet_ids
  
  # Database configuration
  db_name              = var.db_name
  db_username          = var.db_username
  db_password          = module.org.db_password
  db_instance_class    = var.db_instance_class
  db_allocated_storage = var.db_allocated_storage
  db_multi_az          = var.db_multi_az
  db_secret_arn        = module.org.db_secret_arn
  
  # Redis configuration
  redis_node_type  = var.redis_node_type
  redis_num_shards = var.redis_num_shards
  redis_auth_token = module.org.redis_auth_token
  
  # Security
  kms_key_arn         = module.org.kms_key_arn
  db_security_group_id = module.networking.db_security_group_id
  redis_security_group_id = module.networking.redis_security_group_id
  
  tags = var.tags
}

# ECS Fargate cluster, services, ALB, CloudWatch
module "app" {
  source = "./app"

  environment         = var.environment
  vpc_id              = module.networking.vpc_id
  private_subnet_ids  = module.networking.private_subnet_ids
  public_subnet_ids   = module.networking.public_subnet_ids
  
  # Database connection
  db_endpoint = module.data.db_endpoint
  db_name     = var.db_name
  db_secret_arn = module.org.db_secret_arn
  django_secret_arn = module.org.django_secret_arn
  
  # Redis connection
  redis_endpoint = module.data.redis_endpoint
  
  # S3 buckets
  documents_bucket = module.data.documents_bucket
  static_bucket    = module.data.static_bucket
  
  # ECS task configuration
  control_plane_cpu    = var.control_plane_cpu
  control_plane_memory = var.control_plane_memory
  control_plane_count  = var.control_plane_count
  
  web_portal_cpu       = var.web_portal_cpu
  web_portal_memory    = var.web_portal_memory
  web_portal_count     = var.web_portal_count
  
  worker_cpu           = var.worker_cpu
  worker_memory        = var.worker_memory
  worker_count         = var.worker_count
  
  # Security
  ecs_task_execution_role_arn = module.org.ecs_task_execution_role_arn
  ecs_task_role_arn           = module.org.ecs_task_role_arn
  alb_security_group_id       = module.networking.alb_security_group_id
  ecs_security_group_id       = module.networking.ecs_security_group_id
  
  # Domain & SSL
  domain_name        = var.domain_name
  acm_certificate_arn = var.acm_certificate_arn
  
  tags = var.tags
}

# CI/CD module for ECR and CodePipeline
module "ci" {
  source = "./ci"

  environment    = var.environment
  ecs_cluster_name = module.app.ecs_cluster_name
  
  # Service names for deployment
  services = {
    control_plane = module.app.control_plane_service_name
    web_portal    = module.app.web_portal_service_name
    worker        = module.app.worker_service_name
  }
  
  # GitHub integration
  github_owner      = var.github_owner
  github_repo       = var.github_repo
  github_branch     = var.github_branch
  github_token_secret_arn = module.org.github_token_secret_arn
  
  tags = var.tags
}
