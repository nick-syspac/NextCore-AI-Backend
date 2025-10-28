#!/bin/bash
# Deploy infrastructure to AWS

set -e

ENVIRONMENT=${1:-production}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TERRAFORM_DIR="$(dirname "$SCRIPT_DIR")"

cd "$TERRAFORM_DIR"

echo "==> Deploying NextCore AI Cloud - Environment: $ENVIRONMENT"

# Check if backend is initialized
if [ ! -f ".terraform/terraform.tfstate" ]; then
  echo "==> Backend not initialized. Run init-backend.sh first."
  exit 1
fi

# Validate Terraform files
echo "==> Validating Terraform configuration..."
terraform validate

# Format check
echo "==> Checking Terraform formatting..."
terraform fmt -check=true || {
  echo "Warning: Some files need formatting. Run 'terraform fmt -recursive'"
}

# Plan
echo "==> Creating execution plan..."
terraform plan \
  -var-file="environments/${ENVIRONMENT}.tfvars" \
  -out=tfplan

# Show plan summary
echo ""
echo "==> Plan summary generated. Review above before applying."
echo ""
read -p "Do you want to apply this plan? (yes/no): " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
  echo "Deployment cancelled."
  exit 0
fi

# Apply
echo "==> Applying infrastructure changes..."
terraform apply tfplan

# Cleanup plan file
rm -f tfplan

echo ""
echo "==> Deployment complete!"
echo ""
echo "Outputs:"
terraform output

echo ""
echo "Next steps:"
echo "1. Build and push Docker images (see README.md)"
echo "2. Configure DNS records (if using custom domain)"
echo "3. Run database migrations"
echo "4. Access application at the ALB DNS name"
