# CI/CD Module Variables

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "ecs_cluster_name" {
  description = "Name of ECS cluster"
  type        = string
}

variable "services" {
  description = "Map of service names"
  type = object({
    control_plane = string
    web_portal    = string
    worker        = string
  })
}

variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
  default     = ""
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
  default     = ""
}

variable "github_branch" {
  description = "GitHub branch"
  type        = string
  default     = "main"
}

variable "github_token_secret_arn" {
  description = "ARN of GitHub token in Secrets Manager"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}
