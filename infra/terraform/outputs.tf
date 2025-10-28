# NextCore AI Cloud - Terraform Outputs

# Networking Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.networking.vpc_id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = module.networking.public_subnet_ids
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = module.networking.private_subnet_ids
}

output "database_subnet_ids" {
  description = "List of database subnet IDs"
  value       = module.networking.database_subnet_ids
}

# Data Layer Outputs
output "db_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = module.data.db_endpoint
  sensitive   = true
}

output "db_secret_arn" {
  description = "ARN of RDS credentials secret in Secrets Manager"
  value       = module.data.db_secret_arn
}

output "redis_endpoint" {
  description = "ElastiCache Redis endpoint"
  value       = module.data.redis_endpoint
  sensitive   = true
}

output "documents_bucket" {
  description = "S3 bucket for documents"
  value       = module.data.documents_bucket
}

output "static_bucket" {
  description = "S3 bucket for static assets"
  value       = module.data.static_bucket
}

# Application Outputs
output "ecs_cluster_name" {
  description = "Name of ECS cluster"
  value       = module.app.ecs_cluster_name
}

output "alb_dns_name" {
  description = "DNS name of Application Load Balancer"
  value       = module.app.alb_dns_name
}

output "alb_zone_id" {
  description = "Zone ID of Application Load Balancer"
  value       = module.app.alb_zone_id
}

output "control_plane_service_name" {
  description = "Name of control plane ECS service"
  value       = module.app.control_plane_service_name
}

output "web_portal_service_name" {
  description = "Name of web portal ECS service"
  value       = module.app.web_portal_service_name
}

output "worker_service_name" {
  description = "Name of worker ECS service"
  value       = module.app.worker_service_name
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name"
  value       = module.app.cloudwatch_log_group
}

# CI/CD Outputs
output "ecr_repositories" {
  description = "Map of ECR repository URLs"
  value       = module.ci.ecr_repositories
}

# output "codepipeline_name" {
#   description = "Name of CodePipeline"
#   value       = module.ci.codepipeline_name
# }

# Security Outputs
output "kms_key_id" {
  description = "ID of KMS key for encryption"
  value       = module.org.kms_key_id
}

output "ecs_task_execution_role_arn" {
  description = "ARN of ECS task execution role"
  value       = module.org.ecs_task_execution_role_arn
}

output "ecs_task_role_arn" {
  description = "ARN of ECS task role"
  value       = module.org.ecs_task_role_arn
}

# Application URLs
output "api_url" {
  description = "API endpoint URL"
  value       = var.domain_name != "" ? "https://api.${var.domain_name}" : "http://${module.app.alb_dns_name}"
}

output "web_url" {
  description = "Web portal URL"
  value       = var.domain_name != "" ? "https://${var.domain_name}" : "http://${module.app.alb_dns_name}"
}

# Deployment Instructions
output "deployment_instructions" {
  description = "Quick start commands"
  value = <<-EOT
    NextCore AI Cloud - Deployment Complete!
    
    1. Configure DNS (if using custom domain):
       - Create CNAME record: api.${var.domain_name} -> ${module.app.alb_dns_name}
       - Create CNAME record: ${var.domain_name} -> ${module.app.alb_dns_name}
    
    2. Push Docker images to ECR:
       aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${module.ci.ecr_repositories["control_plane"]}
       docker build -t control-plane ./apps/control-plane
       docker tag control-plane:latest ${module.ci.ecr_repositories["control_plane"]}:latest
       docker push ${module.ci.ecr_repositories["control_plane"]}:latest
    
    3. Run database migrations:
       aws ecs run-task --cluster ${module.app.ecs_cluster_name} --task-definition ${module.app.control_plane_service_name}-migrate
    
    4. Access application:
       API: http://${module.app.alb_dns_name}/api/
       Web: http://${module.app.alb_dns_name}/
    
    5. View logs:
       aws logs tail ${module.app.cloudwatch_log_group} --follow
  EOT
}
