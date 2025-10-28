# Organization Module Outputs

output "kms_key_id" {
  description = "ID of KMS key"
  value       = aws_kms_key.main.id
}

output "kms_key_arn" {
  description = "ARN of KMS key"
  value       = aws_kms_key.main.arn
}

output "ecs_task_execution_role_arn" {
  description = "ARN of ECS task execution role"
  value       = aws_iam_role.ecs_task_execution.arn
}

output "ecs_task_role_arn" {
  description = "ARN of ECS task role"
  value       = aws_iam_role.ecs_task.arn
}

output "db_secret_arn" {
  description = "ARN of database credentials secret"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "django_secret_arn" {
  description = "ARN of Django secret key"
  value       = aws_secretsmanager_secret.django_secret_key.arn
}

output "redis_secret_arn" {
  description = "ARN of Redis auth token secret"
  value       = aws_secretsmanager_secret.redis_auth_token.arn
}

output "github_token_secret_arn" {
  description = "ARN of GitHub token secret"
  value       = aws_secretsmanager_secret.github_token.arn
}

output "db_password" {
  description = "Database password (sensitive)"
  value       = random_password.db_password.result
  sensitive   = true
}

output "redis_auth_token" {
  description = "Redis auth token (sensitive)"
  value       = random_password.redis_auth.result
  sensitive   = true
}
