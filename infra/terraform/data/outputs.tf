# Data Module Outputs

output "db_endpoint" {
  description = "RDS PostgreSQL endpoint"
  value       = aws_db_instance.main.endpoint
}

output "db_address" {
  description = "RDS PostgreSQL address (hostname)"
  value       = aws_db_instance.main.address
}

output "db_port" {
  description = "RDS PostgreSQL port"
  value       = aws_db_instance.main.port
}

output "db_name" {
  description = "Database name"
  value       = aws_db_instance.main.db_name
}

output "db_secret_arn" {
  description = "ARN of DB credentials in Secrets Manager"
  value       = var.db_secret_arn
}

output "redis_endpoint" {
  description = "ElastiCache Redis endpoint"
  value       = aws_elasticache_replication_group.main.configuration_endpoint_address
}

output "redis_port" {
  description = "ElastiCache Redis port"
  value       = aws_elasticache_replication_group.main.port
}

output "documents_bucket" {
  description = "Documents S3 bucket name"
  value       = aws_s3_bucket.documents.id
}

output "documents_bucket_arn" {
  description = "Documents S3 bucket ARN"
  value       = aws_s3_bucket.documents.arn
}

output "static_bucket" {
  description = "Static assets S3 bucket name"
  value       = aws_s3_bucket.static.id
}

output "static_bucket_arn" {
  description = "Static assets S3 bucket ARN"
  value       = aws_s3_bucket.static.arn
}

output "reports_bucket" {
  description = "Reports S3 bucket name"
  value       = aws_s3_bucket.reports.id
}

output "reports_bucket_arn" {
  description = "Reports S3 bucket ARN"
  value       = aws_s3_bucket.reports.arn
}
