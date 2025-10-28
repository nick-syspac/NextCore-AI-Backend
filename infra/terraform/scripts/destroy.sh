#!/bin/bash
# Destroy infrastructure (USE WITH CAUTION!)

set -e

ENVIRONMENT=${1:-production}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TERRAFORM_DIR="$(dirname "$SCRIPT_DIR")"

cd "$TERRAFORM_DIR"

echo "==> WARNING: This will destroy ALL infrastructure for environment: $ENVIRONMENT"
echo "==> This action is IRREVERSIBLE!"
echo ""

read -p "Are you absolutely sure? Type 'destroy-$ENVIRONMENT' to confirm: " -r
if [[ ! $REPLY == "destroy-$ENVIRONMENT" ]]; then
  echo "Destruction cancelled."
  exit 0
fi

# Create final snapshot first
echo "==> Creating final RDS snapshot..."
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
SNAPSHOT_ID="${ENVIRONMENT}-nextcore-final-${TIMESTAMP}"

DB_INSTANCE=$(terraform output -raw db_endpoint 2>/dev/null | cut -d: -f1)
if [ -n "$DB_INSTANCE" ]; then
  aws rds create-db-snapshot \
    --db-instance-identifier "$DB_INSTANCE" \
    --db-snapshot-identifier "$SNAPSHOT_ID" || echo "Snapshot creation failed or already exists"
fi

# Destroy infrastructure
echo "==> Destroying infrastructure..."
terraform destroy \
  -var-file="environments/${ENVIRONMENT}.tfvars"

echo ""
echo "==> Infrastructure destroyed."
echo ""
echo "Manual cleanup required:"
echo "1. Delete ECR images if needed"
echo "2. Delete S3 bucket contents:"
echo "   aws s3 rm s3://${ENVIRONMENT}-nextcore-documents- --recursive"
echo "   aws s3 rm s3://${ENVIRONMENT}-nextcore-static- --recursive"
echo "   aws s3 rm s3://${ENVIRONMENT}-nextcore-reports- --recursive"
echo "3. Delete backend S3 bucket and DynamoDB table if no longer needed"
