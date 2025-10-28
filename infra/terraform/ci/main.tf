# CI/CD Module - ECR Repositories, CodeBuild, CodePipeline
# Automates container builds and deployments

# ECR Repository - Control Plane
resource "aws_ecr_repository" "control_plane" {
  name                 = "${var.environment}-control-plane"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-control-plane-ecr"
    }
  )
}

resource "aws_ecr_lifecycle_policy" "control_plane" {
  repository = aws_ecr_repository.control_plane.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Delete untagged images after 7 days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 7
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# ECR Repository - Web Portal
resource "aws_ecr_repository" "web_portal" {
  name                 = "${var.environment}-web-portal"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-web-portal-ecr"
    }
  )
}

resource "aws_ecr_lifecycle_policy" "web_portal" {
  repository = aws_ecr_repository.web_portal.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Delete untagged images after 7 days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 7
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# ECR Repository - Worker
resource "aws_ecr_repository" "worker" {
  name                 = "${var.environment}-worker"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-worker-ecr"
    }
  )
}

resource "aws_ecr_lifecycle_policy" "worker" {
  repository = aws_ecr_repository.worker.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Delete untagged images after 7 days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 7
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# S3 Bucket for CodePipeline Artifacts
resource "aws_s3_bucket" "codepipeline" {
  bucket_prefix = "${var.environment}-codepipeline-"

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-codepipeline-artifacts"
    }
  )
}

resource "aws_s3_bucket_public_access_block" "codepipeline" {
  bucket = aws_s3_bucket.codepipeline.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "codepipeline" {
  bucket = aws_s3_bucket.codepipeline.id

  versioning_configuration {
    status = "Enabled"
  }
}

# IAM Role for CodeBuild
resource "aws_iam_role" "codebuild" {
  name_prefix = "${var.environment}-codebuild-"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "codebuild.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "codebuild" {
  name_prefix = "codebuild-policy-"
  role        = aws_iam_role.codebuild.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:GetRepositoryPolicy",
          "ecr:DescribeRepositories",
          "ecr:ListImages",
          "ecr:DescribeImages",
          "ecr:BatchGetImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:PutImage"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.codepipeline.arn}/*"
      }
    ]
  })
}

# CodeBuild Project - Control Plane
resource "aws_codebuild_project" "control_plane" {
  name          = "${var.environment}-control-plane-build"
  service_role  = aws_iam_role.codebuild.arn
  build_timeout = 30

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:7.0"
    type                        = "LINUX_CONTAINER"
    privileged_mode             = true
    image_pull_credentials_type = "CODEBUILD"

    environment_variable {
      name  = "AWS_ACCOUNT_ID"
      value = data.aws_caller_identity.current.account_id
    }

    environment_variable {
      name  = "AWS_REGION"
      value = data.aws_region.current.name
    }

    environment_variable {
      name  = "IMAGE_REPO_NAME"
      value = aws_ecr_repository.control_plane.name
    }

    environment_variable {
      name  = "IMAGE_TAG"
      value = "latest"
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "apps/control-plane/buildspec.yml"
  }

  tags = var.tags
}

# CodeBuild Project - Web Portal
resource "aws_codebuild_project" "web_portal" {
  name          = "${var.environment}-web-portal-build"
  service_role  = aws_iam_role.codebuild.arn
  build_timeout = 30

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:7.0"
    type                        = "LINUX_CONTAINER"
    privileged_mode             = true
    image_pull_credentials_type = "CODEBUILD"

    environment_variable {
      name  = "AWS_ACCOUNT_ID"
      value = data.aws_caller_identity.current.account_id
    }

    environment_variable {
      name  = "AWS_REGION"
      value = data.aws_region.current.name
    }

    environment_variable {
      name  = "IMAGE_REPO_NAME"
      value = aws_ecr_repository.web_portal.name
    }

    environment_variable {
      name  = "IMAGE_TAG"
      value = "latest"
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "apps/web-portal/buildspec.yml"
  }

  tags = var.tags
}

# CodeBuild Project - Worker
resource "aws_codebuild_project" "worker" {
  name          = "${var.environment}-worker-build"
  service_role  = aws_iam_role.codebuild.arn
  build_timeout = 30

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:7.0"
    type                        = "LINUX_CONTAINER"
    privileged_mode             = true
    image_pull_credentials_type = "CODEBUILD"

    environment_variable {
      name  = "AWS_ACCOUNT_ID"
      value = data.aws_caller_identity.current.account_id
    }

    environment_variable {
      name  = "AWS_REGION"
      value = data.aws_region.current.name
    }

    environment_variable {
      name  = "IMAGE_REPO_NAME"
      value = aws_ecr_repository.worker.name
    }

    environment_variable {
      name  = "IMAGE_TAG"
      value = "latest"
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = "apps/worker/buildspec.yml"
  }

  tags = var.tags
}

# IAM Role for CodePipeline
resource "aws_iam_role" "codepipeline" {
  name_prefix = "${var.environment}-codepipeline-"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "codepipeline.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "codepipeline" {
  name_prefix = "codepipeline-policy-"
  role        = aws_iam_role.codepipeline.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.codepipeline.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "codebuild:BatchGetBuilds",
          "codebuild:StartBuild"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecs:DescribeServices",
          "ecs:DescribeTaskDefinition",
          "ecs:DescribeTasks",
          "ecs:ListTasks",
          "ecs:RegisterTaskDefinition",
          "ecs:UpdateService"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "iam:PassRole"
        ]
        Resource = "*"
      }
    ]
  })
}

# CodePipeline (optional - requires GitHub token)
# Uncomment when GitHub integration is configured
# resource "aws_codepipeline" "main" {
#   name     = "${var.environment}-nextcore-pipeline"
#   role_arn = aws_iam_role.codepipeline.arn
#
#   artifact_store {
#     location = aws_s3_bucket.codepipeline.bucket
#     type     = "S3"
#   }
#
#   stage {
#     name = "Source"
#
#     action {
#       name             = "Source"
#       category         = "Source"
#       owner            = "ThirdParty"
#       provider         = "GitHub"
#       version          = "1"
#       output_artifacts = ["source_output"]
#
#       configuration = {
#         Owner  = var.github_owner
#         Repo   = var.github_repo
#         Branch = var.github_branch
#         OAuthToken = var.github_token
#       }
#     }
#   }
#
#   stage {
#     name = "Build"
#
#     action {
#       name             = "Build-ControlPlane"
#       category         = "Build"
#       owner            = "AWS"
#       provider         = "CodeBuild"
#       version          = "1"
#       input_artifacts  = ["source_output"]
#       output_artifacts = ["control_plane_output"]
#
#       configuration = {
#         ProjectName = aws_codebuild_project.control_plane.name
#       }
#     }
#
#     action {
#       name             = "Build-WebPortal"
#       category         = "Build"
#       owner            = "AWS"
#       provider         = "CodeBuild"
#       version          = "1"
#       input_artifacts  = ["source_output"]
#       output_artifacts = ["web_portal_output"]
#
#       configuration = {
#         ProjectName = aws_codebuild_project.web_portal.name
#       }
#     }
#
#     action {
#       name             = "Build-Worker"
#       category         = "Build"
#       owner            = "AWS"
#       provider         = "CodeBuild"
#       version          = "1"
#       input_artifacts  = ["source_output"]
#       output_artifacts = ["worker_output"]
#
#       configuration = {
#         ProjectName = aws_codebuild_project.worker.name
#       }
#     }
#   }
#
#   stage {
#     name = "Deploy"
#
#     action {
#       name            = "Deploy-ControlPlane"
#       category        = "Deploy"
#       owner           = "AWS"
#       provider        = "ECS"
#       version         = "1"
#       input_artifacts = ["control_plane_output"]
#
#       configuration = {
#         ClusterName = var.ecs_cluster_name
#         ServiceName = var.services.control_plane
#         FileName    = "imagedefinitions.json"
#       }
#     }
#
#     action {
#       name            = "Deploy-WebPortal"
#       category        = "Deploy"
#       owner           = "AWS"
#       provider        = "ECS"
#       version         = "1"
#       input_artifacts = ["web_portal_output"]
#
#       configuration = {
#         ClusterName = var.ecs_cluster_name
#         ServiceName = var.services.web_portal
#         FileName    = "imagedefinitions.json"
#       }
#     }
#
#     action {
#       name            = "Deploy-Worker"
#       category        = "Deploy"
#       owner           = "AWS"
#       provider        = "ECS"
#       version          = "1"
#       input_artifacts = ["worker_output"]
#
#       configuration = {
#         ClusterName = var.ecs_cluster_name
#         ServiceName = var.services.worker
#         FileName    = "imagedefinitions.json"
#       }
#     }
#   }
#
#   tags = var.tags
# }

# Data sources
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

