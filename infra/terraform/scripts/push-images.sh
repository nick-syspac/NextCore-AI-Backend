#!/bin/bash
# Build and push Docker images to ECR

set -e

ENVIRONMENT=${1:-production}
REGION=${AWS_REGION:-ap-southeast-2}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "==> Building and pushing Docker images"
echo "==> Environment: $ENVIRONMENT"
echo "==> Region: $REGION"
echo "==> Account: $AWS_ACCOUNT_ID"

# Login to ECR
echo "==> Logging in to ECR..."
aws ecr get-login-password --region "$REGION" | \
  docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"

# Build and push control-plane
echo "==> Building control-plane image..."
docker build -t "${ENVIRONMENT}-control-plane" \
  -f apps/control-plane/Dockerfile \
  .

docker tag "${ENVIRONMENT}-control-plane:latest" \
  "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ENVIRONMENT}-control-plane:latest"

echo "==> Pushing control-plane image..."
docker push "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ENVIRONMENT}-control-plane:latest"

# Build and push web-portal
echo "==> Building web-portal image..."
docker build -t "${ENVIRONMENT}-web-portal" \
  -f apps/web-portal/Dockerfile \
  .

docker tag "${ENVIRONMENT}-web-portal:latest" \
  "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ENVIRONMENT}-web-portal:latest"

echo "==> Pushing web-portal image..."
docker push "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ENVIRONMENT}-web-portal:latest"

# Build and push worker
echo "==> Building worker image..."
docker build -t "${ENVIRONMENT}-worker" \
  -f apps/worker/Dockerfile \
  .

docker tag "${ENVIRONMENT}-worker:latest" \
  "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ENVIRONMENT}-worker:latest"

echo "==> Pushing worker image..."
docker push "${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ENVIRONMENT}-worker:latest"

echo ""
echo "==> All images pushed successfully!"
echo ""
echo "Next steps:"
echo "1. Update ECS services to use new images:"
echo "   aws ecs update-service --cluster ${ENVIRONMENT}-nextcore-cluster --service ${ENVIRONMENT}-control-plane --force-new-deployment"
echo "   aws ecs update-service --cluster ${ENVIRONMENT}-nextcore-cluster --service ${ENVIRONMENT}-web-portal --force-new-deployment"
echo "   aws ecs update-service --cluster ${ENVIRONMENT}-nextcore-cluster --service ${ENVIRONMENT}-worker --force-new-deployment"
