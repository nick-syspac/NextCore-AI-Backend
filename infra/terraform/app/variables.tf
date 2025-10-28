# Application Module Variables

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "public_subnet_ids" {
  description = "List of public subnet IDs"
  type        = list(string)
}

# Database
variable "db_endpoint" {
  description = "RDS endpoint"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_secret_arn" {
  description = "ARN of DB secret in Secrets Manager"
  type        = string
}

variable "django_secret_arn" {
  description = "ARN of Django secret in Secrets Manager"
  type        = string
}

# Redis
variable "redis_endpoint" {
  description = "ElastiCache Redis endpoint"
  type        = string
}

# S3
variable "documents_bucket" {
  description = "Documents S3 bucket name"
  type        = string
}

variable "static_bucket" {
  description = "Static assets S3 bucket name"
  type        = string
}

# ECS Configuration - Control Plane
variable "control_plane_cpu" {
  description = "CPU units for control plane"
  type        = number
}

variable "control_plane_memory" {
  description = "Memory for control plane in MB"
  type        = number
}

variable "control_plane_count" {
  description = "Desired count of control plane tasks"
  type        = number
}

variable "control_plane_image" {
  description = "Docker image for control plane"
  type        = string
  default     = ""
}

# ECS Configuration - Web Portal
variable "web_portal_cpu" {
  description = "CPU units for web portal"
  type        = number
}

variable "web_portal_memory" {
  description = "Memory for web portal in MB"
  type        = number
}

variable "web_portal_count" {
  description = "Desired count of web portal tasks"
  type        = number
}

variable "web_portal_image" {
  description = "Docker image for web portal"
  type        = string
  default     = ""
}

# ECS Configuration - Worker
variable "worker_cpu" {
  description = "CPU units for worker"
  type        = number
}

variable "worker_memory" {
  description = "Memory for worker in MB"
  type        = number
}

variable "worker_count" {
  description = "Desired count of worker tasks"
  type        = number
}

variable "worker_image" {
  description = "Docker image for worker"
  type        = string
  default     = ""
}

# Security
variable "ecs_task_execution_role_arn" {
  description = "ARN of ECS task execution role"
  type        = string
}

variable "ecs_task_role_arn" {
  description = "ARN of ECS task role"
  type        = string
}

variable "alb_security_group_id" {
  description = "Security group ID for ALB"
  type        = string
}

variable "ecs_security_group_id" {
  description = "Security group ID for ECS tasks"
  type        = string
}

# Domain
variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = ""
}

variable "acm_certificate_arn" {
  description = "ACM certificate ARN for HTTPS"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}
