#!/bin/bash
# Initialize Terraform backend (S3 + DynamoDB) for state management

set -e

ENVIRONMENT=${1:-production}
REGION=${AWS_REGION:-ap-southeast-2}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "==> Initializing Terraform backend for environment: $ENVIRONMENT"
echo "==> Region: $REGION"
echo "==> AWS Account: $AWS_ACCOUNT_ID"

# S3 Bucket for Terraform state
BUCKET_NAME="nextcore-terraform-state-${ENVIRONMENT}"
echo "==> Creating S3 bucket: $BUCKET_NAME"

aws s3api create-bucket \
  --bucket "$BUCKET_NAME" \
  --region "$REGION" \
  --create-bucket-configuration LocationConstraint="$REGION" \
  2>/dev/null || echo "Bucket already exists"

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket "$BUCKET_NAME" \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket "$BUCKET_NAME" \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'

# Block public access
aws s3api put-public-access-block \
  --bucket "$BUCKET_NAME" \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

echo "✓ S3 bucket configured: $BUCKET_NAME"

# DynamoDB table for state locking
TABLE_NAME="nextcore-terraform-locks-${ENVIRONMENT}"
echo "==> Creating DynamoDB table: $TABLE_NAME"

aws dynamodb create-table \
  --table-name "$TABLE_NAME" \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region "$REGION" \
  2>/dev/null || echo "Table already exists"

echo "✓ DynamoDB table configured: $TABLE_NAME"

# Update backend config file
BACKEND_FILE="environments/${ENVIRONMENT}-backend.hcl"
cat > "$BACKEND_FILE" <<EOF
# Backend configuration for ${ENVIRONMENT} environment
bucket         = "${BUCKET_NAME}"
key            = "nextcore-ai-cloud/terraform.tfstate"
region         = "${REGION}"
encrypt        = true
dynamodb_table = "${TABLE_NAME}"
EOF

echo "✓ Backend configuration written to: $BACKEND_FILE"

echo ""
echo "==> Backend initialization complete!"
echo ""
echo "Next steps:"
echo "1. Initialize Terraform:"
echo "   terraform init -backend-config=\"${BACKEND_FILE}\""
echo ""
echo "2. Plan deployment:"
echo "   terraform plan -var-file=\"environments/${ENVIRONMENT}.tfvars\" -out=tfplan"
echo ""
echo "3. Apply infrastructure:"
echo "   terraform apply tfplan"
