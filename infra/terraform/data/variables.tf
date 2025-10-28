# Data Module Variables

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "database_subnets" {
  description = "List of database subnet IDs"
  type        = list(string)
}

variable "cache_subnets" {
  description = "List of cache subnet IDs"
  type        = list(string)
}

# RDS
variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
}

variable "db_allocated_storage" {
  description = "RDS allocated storage in GB"
  type        = number
}

variable "db_multi_az" {
  description = "Enable Multi-AZ for RDS"
  type        = bool
}

variable "db_secret_arn" {
  description = "ARN of DB secret in Secrets Manager"
  type        = string
}

# Redis
variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
}

variable "redis_num_shards" {
  description = "Number of Redis cache clusters"
  type        = number
}

variable "redis_auth_token" {
  description = "Redis auth token"
  type        = string
  sensitive   = true
}

# Security
variable "kms_key_arn" {
  description = "KMS key ARN for encryption"
  type        = string
}

variable "db_security_group_id" {
  description = "Security group ID for RDS"
  type        = string
}

variable "redis_security_group_id" {
  description = "Security group ID for Redis"
  type        = string
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}

