# CI/CD Module Outputs

output "ecr_repositories" {
  description = "Map of ECR repository URLs"
  value = {
    control_plane = aws_ecr_repository.control_plane.repository_url
    web_portal    = aws_ecr_repository.web_portal.repository_url
    worker        = aws_ecr_repository.worker.repository_url
  }
}

output "ecr_repository_arns" {
  description = "Map of ECR repository ARNs"
  value = {
    control_plane = aws_ecr_repository.control_plane.arn
    web_portal    = aws_ecr_repository.web_portal.arn
    worker        = aws_ecr_repository.worker.arn
  }
}

output "codebuild_projects" {
  description = "Map of CodeBuild project names"
  value = {
    control_plane = aws_codebuild_project.control_plane.name
    web_portal    = aws_codebuild_project.web_portal.name
    worker        = aws_codebuild_project.worker.name
  }
}

# output "codepipeline_name" {
#   description = "Name of CodePipeline"
#   value       = aws_codepipeline.main.name
# }

# output "codepipeline_arn" {
#   description = "ARN of CodePipeline"
#   value       = aws_codepipeline.main.arn
# }

output "artifacts_bucket" {
  description = "S3 bucket for CodePipeline artifacts"
  value       = aws_s3_bucket.codepipeline.id
}
