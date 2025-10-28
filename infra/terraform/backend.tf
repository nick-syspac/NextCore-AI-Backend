# Terraform State Backend Configuration
# This stores Terraform state in S3 with DynamoDB locking

terraform {
  backend "s3" {
    # Configuration provided via backend config file or CLI
    # Example: terraform init -backend-config="environments/production-backend.hcl"
    
    # bucket         = "nextcore-terraform-state-production"
    # key            = "nextcore-ai-cloud/terraform.tfstate"
    # region         = "ap-southeast-2"
    # encrypt        = true
    # dynamodb_table = "nextcore-terraform-locks"
    # kms_key_id     = "arn:aws:kms:ap-southeast-2:ACCOUNT_ID:key/KEY_ID"
  }
}

# Note: To create backend resources, run:
# ./scripts/init-backend.sh <environment>
