# Application Module Outputs

output "ecs_cluster_name" {
  description = "Name of ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecs_cluster_arn" {
  description = "ARN of ECS cluster"
  value       = aws_ecs_cluster.main.arn
}

output "alb_dns_name" {
  description = "DNS name of Application Load Balancer"
  value       = aws_lb.main.dns_name
}

output "alb_zone_id" {
  description = "Zone ID of Application Load Balancer"
  value       = aws_lb.main.zone_id
}

output "alb_arn" {
  description = "ARN of Application Load Balancer"
  value       = aws_lb.main.arn
}

output "control_plane_service_name" {
  description = "Name of control plane ECS service"
  value       = aws_ecs_service.control_plane.name
}

output "web_portal_service_name" {
  description = "Name of web portal ECS service"
  value       = aws_ecs_service.web_portal.name
}

output "worker_service_name" {
  description = "Name of worker ECS service"
  value       = aws_ecs_service.worker.name
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name"
  value       = aws_cloudwatch_log_group.ecs.name
}

output "control_plane_task_definition" {
  description = "Control plane task definition ARN"
  value       = aws_ecs_task_definition.control_plane.arn
}

output "web_portal_task_definition" {
  description = "Web portal task definition ARN"
  value       = aws_ecs_task_definition.web_portal.arn
}

output "worker_task_definition" {
  description = "Worker task definition ARN"
  value       = aws_ecs_task_definition.worker.arn
}
