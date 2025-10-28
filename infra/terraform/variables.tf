# Global Configuration
variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
}

variable "project" {
  description = "Project name"
  type        = string
  default     = "nextcore-ai-cloud"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-southeast-2"
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}

# Networking
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["ap-southeast-2a", "ap-southeast-2b", "ap-southeast-2c"]
}

# Database (RDS PostgreSQL)
variable "db_name" {
  description = "Database name"
  type        = string
  default     = "rto"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "postgres"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.large"
}

variable "db_allocated_storage" {
  description = "RDS allocated storage in GB"
  type        = number
  default     = 100
}

variable "db_multi_az" {
  description = "Enable Multi-AZ for RDS"
  type        = bool
  default     = true
}

# Redis (ElastiCache)
variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t3.medium"
}

variable "redis_num_shards" {
  description = "Number of Redis shards"
  type        = number
  default     = 2
}

# ECS Fargate - Control Plane (Django API)
variable "control_plane_cpu" {
  description = "CPU units for control plane tasks (1024 = 1 vCPU)"
  type        = number
  default     = 1024
}

variable "control_plane_memory" {
  description = "Memory for control plane tasks in MB"
  type        = number
  default     = 2048
}

variable "control_plane_count" {
  description = "Desired number of control plane tasks"
  type        = number
  default     = 2
}

variable "control_plane_image" {
  description = "Docker image for control plane"
  type        = string
  default     = ""
}

# ECS Fargate - Web Portal (Next.js)
variable "web_portal_cpu" {
  description = "CPU units for web portal tasks"
  type        = number
  default     = 512
}

variable "web_portal_memory" {
  description = "Memory for web portal tasks in MB"
  type        = number
  default     = 1024
}

variable "web_portal_count" {
  description = "Desired number of web portal tasks"
  type        = number
  default     = 2
}

variable "web_portal_image" {
  description = "Docker image for web portal"
  type        = string
  default     = ""
}

# ECS Fargate - Workers (Celery)
variable "worker_cpu" {
  description = "CPU units for worker tasks"
  type        = number
  default     = 1024
}

variable "worker_memory" {
  description = "Memory for worker tasks in MB"
  type        = number
  default     = 2048
}

variable "worker_count" {
  description = "Desired number of worker tasks"
  type        = number
  default     = 3
}

variable "worker_image" {
  description = "Docker image for workers"
  type        = string
  default     = ""
}

# Domain & SSL
variable "domain_name" {
  description = "Primary domain name for the application"
  type        = string
  default     = ""
}

variable "acm_certificate_arn" {
  description = "ACM certificate ARN for HTTPS"
  type        = string
  default     = ""
}

# CI/CD
variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
  default     = ""
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
  default     = "NextCore-AI-Cloud"
}

variable "github_branch" {
  description = "GitHub branch for deployments"
  type        = string
  default     = "main"
}
