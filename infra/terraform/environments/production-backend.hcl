# Backend configuration for production environment
bucket         = "nextcore-terraform-state-production"
key            = "nextcore-ai-cloud/terraform.tfstate"
region         = "ap-southeast-2"
encrypt        = true
dynamodb_table = "nextcore-terraform-locks-production"
