# NextCore AI Cloud - AWS Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INTERNET / USERS                                │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    │ HTTPS/HTTP
                                    │
┌───────────────────────────────────▼─────────────────────────────────────────┐
│                          AWS CLOUD (ap-southeast-2)                          │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Route53 (Optional)                              │   │
│  │                   nextcore.ai → ALB Alias                            │   │
│  └────────────────────────────────┬────────────────────────────────────┘   │
│                                    │                                          │
│  ┌─────────────────────────────────▼────────────────────────────────────┐  │
│  │                    CloudFront CDN (Optional)                          │  │
│  │                Static Assets & Media Distribution                     │  │
│  └────────────────────────────────┬────────────────────────────────────┘  │
│                                    │                                          │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        VPC (10.0.0.0/16)                               │ │
│  │                                                                         │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │              PUBLIC SUBNETS (3 AZs)                               │ │ │
│  │  │              10.0.1.0/24, 10.0.2.0/24, 10.0.3.0/24                │ │ │
│  │  │                                                                    │ │ │
│  │  │  ┌────────────────────────────────────────────────────────────┐  │ │ │
│  │  │  │   Application Load Balancer (ALB)                          │  │ │ │
│  │  │  │   - Listener: HTTP (80) → Redirect HTTPS                   │  │ │ │
│  │  │  │   - Listener: HTTPS (443) → Target Groups                  │  │ │ │
│  │  │  │   - Path Routing:                                          │  │ │ │
│  │  │  │     • /api/* → Control Plane TG (port 8000)               │  │ │ │
│  │  │  │     • / → Web Portal TG (port 3000)                       │  │ │ │
│  │  │  │   - Health Checks: /api/health/, /health                  │  │ │ │
│  │  │  └─────────────┬──────────────────────────────────────────────┘  │ │ │
│  │  │                │                                                    │ │ │
│  │  │  ┌─────────────┴─────────────┬────────────────────────────────┐  │ │ │
│  │  │  │  NAT Gateway (AZ-a)        │  NAT Gateway (AZ-b/c)         │  │ │ │
│  │  │  │  Elastic IP                │  Elastic IPs                  │  │ │ │
│  │  │  └────────────────────────────┴────────────────────────────────┘  │ │ │
│  │  │                                                                    │ │ │
│  │  │  ┌──────────────────────────────────────────────────────────┐    │ │ │
│  │  │  │  Internet Gateway                                         │    │ │ │
│  │  │  └──────────────────────────────────────────────────────────┘    │ │ │
│  │  └────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                         │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │              PRIVATE SUBNETS (3 AZs)                              │ │ │
│  │  │              10.0.11.0/24, 10.0.12.0/24, 10.0.13.0/24             │ │ │
│  │  │                                                                    │ │ │
│  │  │  ┌─────────────────────────────────────────────────────────────┐ │ │ │
│  │  │  │         ECS Fargate Cluster                                  │ │ │ │
│  │  │  │                                                              │ │ │ │
│  │  │  │  ┌────────────────────┐  ┌────────────────────┐            │ │ │ │
│  │  │  │  │ Control Plane (x2) │  │  Web Portal (x2)   │            │ │ │ │
│  │  │  │  │  Django + DRF      │  │   Next.js          │            │ │ │ │
│  │  │  │  │  Port 8000         │  │   Port 3000        │            │ │ │ │
│  │  │  │  │  1 vCPU / 2GB      │  │   0.5 vCPU / 1GB   │            │ │ │ │
│  │  │  │  │  Auto-scale: 2-6   │  │   Auto-scale: 2-6  │            │ │ │ │
│  │  │  │  └────────────────────┘  └────────────────────┘            │ │ │ │
│  │  │  │                                                              │ │ │ │
│  │  │  │  ┌────────────────────────────────────────────┐            │ │ │ │
│  │  │  │  │        Celery Workers (x3)                 │            │ │ │ │
│  │  │  │  │        Background Tasks                    │            │ │ │ │
│  │  │  │  │        1 vCPU / 2GB each                   │            │ │ │ │
│  │  │  │  │        Auto-scale: 3-9                     │            │ │ │ │
│  │  │  │  └────────────────────────────────────────────┘            │ │ │ │
│  │  │  │                                                              │ │ │ │
│  │  │  │  ┌────────────────────────────────────────────┐            │ │ │ │
│  │  │  │  │     ElastiCache Redis Cluster               │            │ │ │ │
│  │  │  │  │     Redis 7.0 (2 shards)                   │            │ │ │ │
│  │  │  │  │     cache.t3.medium                        │            │ │ │ │
│  │  │  │  │     Auth token enabled                     │            │ │ │ │
│  │  │  │  │     Multi-AZ, automatic failover           │            │ │ │ │
│  │  │  │  └────────────────────────────────────────────┘            │ │ │ │
│  │  │  └─────────────────────────────────────────────────────────────┘ │ │ │
│  │  └────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                         │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │              DATABASE SUBNETS (3 AZs)                             │ │ │
│  │  │              10.0.21.0/24, 10.0.22.0/24, 10.0.23.0/24             │ │ │
│  │  │                                                                    │ │ │
│  │  │  ┌─────────────────────────────────────────────────────────────┐ │ │ │
│  │  │  │         RDS PostgreSQL 15                                    │ │ │ │
│  │  │  │         Primary: AZ-a, Standby: AZ-b (Multi-AZ)             │ │ │ │
│  │  │  │         db.t3.large                                          │ │ │ │
│  │  │  │         100 GB gp3 storage                                   │ │ │ │
│  │  │  │         Extensions: pgvector                                 │ │ │ │
│  │  │  │         Encrypted with KMS                                   │ │ │ │
│  │  │  │         Automated backups (7-day retention)                  │ │ │ │
│  │  │  │         Enhanced Monitoring + Performance Insights          │ │ │ │
│  │  │  └─────────────────────────────────────────────────────────────┘ │ │ │
│  │  └────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                         │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          S3 Storage                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │  Documents   │  │    Static    │  │   Reports    │              │   │
│  │  │  Bucket      │  │    Assets    │  │   Bucket     │              │   │
│  │  │  (Policies,  │  │   Bucket     │  │  (Generated  │              │   │
│  │  │   PDFs)      │  │  (Media)     │  │   PDFs)      │              │   │
│  │  │  Versioned   │  │  Versioned   │  │  Versioned   │              │   │
│  │  │  Lifecycle   │  │  CORS        │  │  365d exp    │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Security & Identity                               │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │     IAM      │  │     KMS      │  │   Secrets    │              │   │
│  │  │    Roles     │  │   Keys for   │  │   Manager    │              │   │
│  │  │  - ECS Task  │  │  Encryption  │  │  - DB creds  │              │   │
│  │  │  - ECS Exec  │  │  (RDS, S3,   │  │  - Django    │              │   │
│  │  │  - CodeBuild │  │   Secrets)   │  │  - Redis     │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      CI/CD Pipeline                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │     ECR      │  │  CodeBuild   │  │ CodePipeline │              │   │
│  │  │ Repositories │  │   Projects   │  │  (Optional)  │              │   │
│  │  │  - control   │  │  - Build &   │  │  - GitHub    │              │   │
│  │  │  - web       │  │    Push      │  │  - Build     │              │   │
│  │  │  - worker    │  │  - Image     │  │  - Deploy    │              │   │
│  │  │              │  │    Scan      │  │              │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Monitoring & Logging                            │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │                    CloudWatch                                 │   │   │
│  │  │  - Logs: /ecs/production-nextcore                            │   │   │
│  │  │  - Metrics: CPU, Memory, Requests, Latency                   │   │   │
│  │  │  - Alarms: High CPU, High Memory, 5xx Errors                 │   │   │
│  │  │  - Dashboards: Service health, Database performance          │   │   │
│  │  │  - Container Insights: ECS cluster metrics                   │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### User Request Flow

```
User Browser
    │
    │ HTTPS
    ▼
[CloudFront] (Optional)
    │
    │
    ▼
[ALB - HTTPS Listener]
    │
    ├─── /api/* ──────────────────┐
    │                              │
    │                              ▼
    │                      [Control Plane ECS]
    │                          (Django API)
    │                              │
    │                              ├──→ [RDS PostgreSQL]
    │                              │
    │                              ├──→ [Redis Cache]
    │                              │
    │                              └──→ [S3 Documents]
    │
    └─── / ───────────────────────┐
                                   │
                                   ▼
                           [Web Portal ECS]
                             (Next.js)
                                   │
                                   └──→ [S3 Static Assets]
```

### Background Job Flow

```
[Control Plane API]
    │
    │ Queue Job
    ▼
[Redis - Celery Broker]
    │
    │ Consume
    ▼
[Celery Workers ECS]
    │
    ├──→ [RDS PostgreSQL] (read/write)
    │
    ├──→ [S3 Documents] (upload/process)
    │
    └──→ [Redis Cache] (results)
```

### CI/CD Flow

```
[GitHub Repository]
    │
    │ git push
    ▼
[CodePipeline]
    │
    │ Trigger
    ▼
[CodeBuild]
    │
    ├──→ Build Docker Image
    │
    ├──→ Run Tests
    │
    ├──→ Security Scan (ECR)
    │
    └──→ Push to ECR
         │
         │ Image Available
         ▼
    [ECS Service Update]
         │
         └──→ Rolling Deployment (Blue/Green)
              - Health Check
              - Circuit Breaker
              - Automatic Rollback
```

## Network Security

### Security Group Rules

```
[ALB Security Group]
  Inbound:
    - 0.0.0.0/0 → 80 (HTTP)
    - 0.0.0.0/0 → 443 (HTTPS)
  Outbound:
    - [ECS SG] → 8000, 3000

[ECS Tasks Security Group]
  Inbound:
    - [ALB SG] → 8000, 3000
    - [Self] → All (inter-task)
  Outbound:
    - [RDS SG] → 5432
    - [Redis SG] → 6379
    - 0.0.0.0/0 → 443 (AWS APIs, ECR)

[RDS Security Group]
  Inbound:
    - [ECS SG] → 5432
  Outbound:
    - None (no outbound needed)

[Redis Security Group]
  Inbound:
    - [ECS SG] → 6379
  Outbound:
    - None
```

## High Availability Design

```
┌─────────────────────────────────────────────────────────┐
│                   Availability Zone A                    │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────┐   │
│  │ Public     │  │ Private    │  │ Database        │   │
│  │ Subnet     │  │ Subnet     │  │ Subnet          │   │
│  │ - ALB (1)  │  │ - ECS (2+) │  │ - RDS Primary   │   │
│  │ - NAT GW   │  │ - Redis(1) │  │                 │   │
│  └────────────┘  └────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   Availability Zone B                    │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────┐   │
│  │ Public     │  │ Private    │  │ Database        │   │
│  │ Subnet     │  │ Subnet     │  │ Subnet          │   │
│  │ - ALB (1)  │  │ - ECS (2+) │  │ - RDS Standby   │   │
│  │ - NAT GW   │  │ - Redis(1) │  │ (Failover)      │   │
│  └────────────┘  └────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   Availability Zone C                    │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────┐   │
│  │ Public     │  │ Private    │  │ Database        │   │
│  │ Subnet     │  │ Subnet     │  │ Subnet          │   │
│  │ - ALB (1)  │  │ - ECS (2+) │  │ (Reserved)      │   │
│  │ - NAT GW   │  │            │  │                 │   │
│  └────────────┘  └────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Failure Scenarios:**

1. **Single AZ Failure**: ECS tasks redistribute to other AZs, ALB routes to healthy targets
2. **RDS Primary Failure**: Automatic failover to standby in different AZ (~30s)
3. **Redis Node Failure**: Automatic failover to replica
4. **NAT Gateway Failure**: Traffic routes through other AZ NAT gateways
5. **Task Failure**: ECS launches replacement, ALB health check removes failed task

---

**Total Resources**: ~150 AWS resources  
**Deployment Time**: 20-30 minutes  
**RPO**: 5 minutes (RDS PITR)  
**RTO**: 2-4 hours (complete region failover)
