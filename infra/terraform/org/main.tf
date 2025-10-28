# Organization Module - IAM, KMS, Secrets Manager
# Creates security and identity resources

# KMS Key for encryption (RDS, S3, Secrets Manager)
resource "aws_kms_key" "main" {
  description             = "${var.environment} NextCore AI Cloud encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-kms-key"
    }
  )
}

resource "aws_kms_alias" "main" {
  name          = "alias/${var.environment}-nextcore"
  target_key_id = aws_kms_key.main.key_id
}

# ECS Task Execution Role (pulls images, writes logs)
resource "aws_iam_role" "ecs_task_execution" {
  name_prefix = "${var.environment}-ecs-exec-"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Additional policy for Secrets Manager and KMS
resource "aws_iam_role_policy" "ecs_task_execution_secrets" {
  name_prefix = "secrets-access-"
  role        = aws_iam_role.ecs_task_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = "arn:aws:secretsmanager:*:*:secret:${var.environment}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey"
        ]
        Resource = aws_kms_key.main.arn
      }
    ]
  })
}

# ECS Task Role (application permissions)
resource "aws_iam_role" "ecs_task" {
  name_prefix = "${var.environment}-ecs-task-"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# S3 access for tasks
resource "aws_iam_role_policy" "ecs_task_s3" {
  name_prefix = "s3-access-"
  role        = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${var.environment}-nextcore-*",
          "arn:aws:s3:::${var.environment}-nextcore-*/*"
        ]
      }
    ]
  })
}

# CloudWatch Logs access for tasks
resource "aws_iam_role_policy" "ecs_task_logs" {
  name_prefix = "logs-access-"
  role        = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:log-group:/ecs/${var.environment}/*"
      }
    ]
  })
}

# SES access for email functionality
resource "aws_iam_role_policy" "ecs_task_ses" {
  name_prefix = "ses-access-"
  role        = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Resource = "*"
      }
    ]
  })
}

# Secrets Manager - Database Credentials
resource "aws_secretsmanager_secret" "db_credentials" {
  name_prefix             = "${var.environment}/db/credentials-"
  description             = "RDS PostgreSQL credentials"
  recovery_window_in_days = 7
  kms_key_id              = aws_kms_key.main.id

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-db-credentials"
    }
  )
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = "postgres"
    password = random_password.db_password.result
    engine   = "postgres"
    port     = 5432
  })
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Secrets Manager - Django Secret Key
resource "aws_secretsmanager_secret" "django_secret_key" {
  name_prefix             = "${var.environment}/django/secret-key-"
  description             = "Django SECRET_KEY"
  recovery_window_in_days = 7
  kms_key_id              = aws_kms_key.main.id

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-django-secret"
    }
  )
}

resource "aws_secretsmanager_secret_version" "django_secret_key" {
  secret_id = aws_secretsmanager_secret.django_secret_key.id
  secret_string = jsonencode({
    secret_key = random_password.django_secret.result
  })
}

resource "random_password" "django_secret" {
  length  = 50
  special = true
}

# Secrets Manager - Redis Auth Token
resource "aws_secretsmanager_secret" "redis_auth_token" {
  name_prefix             = "${var.environment}/redis/auth-token-"
  description             = "ElastiCache Redis auth token"
  recovery_window_in_days = 7
  kms_key_id              = aws_kms_key.main.id

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-redis-auth"
    }
  )
}

resource "aws_secretsmanager_secret_version" "redis_auth_token" {
  secret_id = aws_secretsmanager_secret.redis_auth_token.id
  secret_string = jsonencode({
    auth_token = random_password.redis_auth.result
  })
}

resource "random_password" "redis_auth" {
  length  = 32
  special = false # Redis auth tokens can't have special chars
}

# Secrets Manager - GitHub Token (for CI/CD)
resource "aws_secretsmanager_secret" "github_token" {
  name_prefix             = "${var.environment}/github/token-"
  description             = "GitHub personal access token for CI/CD"
  recovery_window_in_days = 7
  kms_key_id              = aws_kms_key.main.id

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-github-token"
    }
  )
}

# Note: GitHub token must be manually added via AWS Console or CLI
# aws secretsmanager put-secret-value \
#   --secret-id <secret-arn> \
#   --secret-string '{"token":"ghp_xxxxx"}'

