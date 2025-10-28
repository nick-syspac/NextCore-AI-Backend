# Backend configuration for staging environment
bucket         = "nextcore-terraform-state-staging"
key            = "nextcore-ai-cloud/terraform.tfstate"
region         = "ap-southeast-2"
encrypt        = true
dynamodb_table = "nextcore-terraform-locks-staging"
