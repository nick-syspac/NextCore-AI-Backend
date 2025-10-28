# Application Module - ECS Fargate, ALB, Task Definitions, Services
# Deploys containerized applications on Fargate

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.environment}-nextcore-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = var.tags
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.environment}-nextcore"
  retention_in_days = 30

  tags = var.tags
}

# Application Load Balancer
resource "aws_lb" "main" {
  name_prefix        = "${substr(var.environment, 0, 6)}-"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.alb_security_group_id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = var.environment == "production" ? true : false
  enable_http2              = true
  enable_cross_zone_load_balancing = true

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-alb"
    }
  )
}

# ALB Target Group - Control Plane (Django API)
resource "aws_lb_target_group" "control_plane" {
  name_prefix = "cp-"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/api/health/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }

  deregistration_delay = 30

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-control-plane-tg"
    }
  )

  lifecycle {
    create_before_destroy = true
  }
}

# ALB Target Group - Web Portal (Next.js)
resource "aws_lb_target_group" "web_portal" {
  name_prefix = "wp-"
  port        = 3000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }

  deregistration_delay = 30

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-web-portal-tg"
    }
  )

  lifecycle {
    create_before_destroy = true
  }
}

# ALB Listener - HTTP (redirect to HTTPS if certificate provided)
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = var.acm_certificate_arn != "" ? "redirect" : "forward"

    dynamic "redirect" {
      for_each = var.acm_certificate_arn != "" ? [1] : []
      content {
        port        = "443"
        protocol    = "HTTPS"
        status_code = "HTTP_301"
      }
    }

    target_group_arn = var.acm_certificate_arn == "" ? aws_lb_target_group.web_portal.arn : null
  }

  tags = var.tags
}

# ALB Listener - HTTPS (if certificate provided)
resource "aws_lb_listener" "https" {
  count = var.acm_certificate_arn != "" ? 1 : 0

  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.acm_certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_portal.arn
  }

  tags = var.tags
}

# ALB Listener Rule - API path routing
resource "aws_lb_listener_rule" "api" {
  listener_arn = var.acm_certificate_arn != "" ? aws_lb_listener.https[0].arn : aws_lb_listener.http.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.control_plane.arn
  }

  condition {
    path_pattern {
      values = ["/api/*", "/admin/*"]
    }
  }

  tags = var.tags
}

# ECS Task Definition - Control Plane (Django)
resource "aws_ecs_task_definition" "control_plane" {
  family                   = "${var.environment}-control-plane"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.control_plane_cpu
  memory                   = var.control_plane_memory
  execution_role_arn       = var.ecs_task_execution_role_arn
  task_role_arn            = var.ecs_task_role_arn

  container_definitions = jsonencode([
    {
      name      = "control-plane"
      image     = var.control_plane_image != "" ? var.control_plane_image : "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${var.environment}-control-plane:latest"
      essential = true

      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "ENVIRONMENT"
          value = var.environment
        },
        {
          name  = "DEBUG"
          value = var.environment == "production" ? "False" : "True"
        },
        {
          name  = "DATABASE_HOST"
          value = split(":", var.db_endpoint)[0]
        },
        {
          name  = "DATABASE_PORT"
          value = "5432"
        },
        {
          name  = "DATABASE_NAME"
          value = var.db_name
        },
        {
          name  = "REDIS_HOST"
          value = var.redis_endpoint
        },
        {
          name  = "REDIS_PORT"
          value = "6379"
        },
        {
          name  = "AWS_STORAGE_BUCKET_NAME"
          value = var.documents_bucket
        },
        {
          name  = "AWS_S3_REGION_NAME"
          value = data.aws_region.current.name
        }
      ]

      secrets = [
        {
          name      = "DATABASE_PASSWORD"
          valueFrom = "${var.db_secret_arn}:password::"
        },
        {
          name      = "SECRET_KEY"
          valueFrom = var.django_secret_arn
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "control-plane"
        }
      }

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:8000/api/health/ || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])

  tags = var.tags
}

# ECS Service - Control Plane
resource "aws_ecs_service" "control_plane" {
  name            = "${var.environment}-control-plane"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.control_plane.arn
  desired_count   = var.control_plane_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [var.ecs_security_group_id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.control_plane.arn
    container_name   = "control-plane"
    container_port   = 8000
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  enable_execute_command = true

  tags = var.tags

  depends_on = [aws_lb_listener.http]
}

# Auto Scaling for Control Plane
resource "aws_appautoscaling_target" "control_plane" {
  max_capacity       = var.control_plane_count * 3
  min_capacity       = var.control_plane_count
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.control_plane.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "control_plane_cpu" {
  name               = "${var.environment}-control-plane-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.control_plane.resource_id
  scalable_dimension = aws_appautoscaling_target.control_plane.scalable_dimension
  service_namespace  = aws_appautoscaling_target.control_plane.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 70.0
  }
}

# ECS Task Definition - Web Portal (Next.js)
resource "aws_ecs_task_definition" "web_portal" {
  family                   = "${var.environment}-web-portal"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.web_portal_cpu
  memory                   = var.web_portal_memory
  execution_role_arn       = var.ecs_task_execution_role_arn
  task_role_arn            = var.ecs_task_role_arn

  container_definitions = jsonencode([
    {
      name      = "web-portal"
      image     = var.web_portal_image != "" ? var.web_portal_image : "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${var.environment}-web-portal:latest"
      essential = true

      portMappings = [
        {
          containerPort = 3000
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "NODE_ENV"
          value = var.environment == "production" ? "production" : "development"
        },
        {
          name  = "NEXT_PUBLIC_API_URL"
          value = "http://${aws_lb.main.dns_name}/api"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "web-portal"
        }
      }

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:3000/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])

  tags = var.tags
}

# ECS Service - Web Portal
resource "aws_ecs_service" "web_portal" {
  name            = "${var.environment}-web-portal"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.web_portal.arn
  desired_count   = var.web_portal_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [var.ecs_security_group_id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.web_portal.arn
    container_name   = "web-portal"
    container_port   = 3000
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  enable_execute_command = true

  tags = var.tags

  depends_on = [aws_lb_listener.http]
}

# Auto Scaling for Web Portal
resource "aws_appautoscaling_target" "web_portal" {
  max_capacity       = var.web_portal_count * 3
  min_capacity       = var.web_portal_count
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.web_portal.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "web_portal_cpu" {
  name               = "${var.environment}-web-portal-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.web_portal.resource_id
  scalable_dimension = aws_appautoscaling_target.web_portal.scalable_dimension
  service_namespace  = aws_appautoscaling_target.web_portal.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 70.0
  }
}

# ECS Task Definition - Worker (Celery)
resource "aws_ecs_task_definition" "worker" {
  family                   = "${var.environment}-worker"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.worker_cpu
  memory                   = var.worker_memory
  execution_role_arn       = var.ecs_task_execution_role_arn
  task_role_arn            = var.ecs_task_role_arn

  container_definitions = jsonencode([
    {
      name      = "worker"
      image     = var.worker_image != "" ? var.worker_image : "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${var.environment}-worker:latest"
      essential = true

      environment = [
        {
          name  = "ENVIRONMENT"
          value = var.environment
        },
        {
          name  = "DATABASE_HOST"
          value = split(":", var.db_endpoint)[0]
        },
        {
          name  = "DATABASE_PORT"
          value = "5432"
        },
        {
          name  = "DATABASE_NAME"
          value = var.db_name
        },
        {
          name  = "REDIS_HOST"
          value = var.redis_endpoint
        },
        {
          name  = "REDIS_PORT"
          value = "6379"
        },
        {
          name  = "AWS_STORAGE_BUCKET_NAME"
          value = var.documents_bucket
        }
      ]

      secrets = [
        {
          name      = "DATABASE_PASSWORD"
          valueFrom = "${var.db_secret_arn}:password::"
        },
        {
          name      = "SECRET_KEY"
          valueFrom = var.django_secret_arn
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = data.aws_region.current.name
          "awslogs-stream-prefix" = "worker"
        }
      }
    }
  ])

  tags = var.tags
}

# ECS Service - Worker
resource "aws_ecs_service" "worker" {
  name            = "${var.environment}-worker"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.worker.arn
  desired_count   = var.worker_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [var.ecs_security_group_id]
    assign_public_ip = false
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  enable_execute_command = true

  tags = var.tags
}

# Data sources
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

