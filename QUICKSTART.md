# Quick Start Guide - RTOComply AI Cloud

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Docker & Docker Compose installed
- Git
- (Optional) Make utility

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/nick-syspac/RTOComply-AI-Backend.git
cd RTOComply-AI-Backend

# Copy environment file
cp .env.example .env

# Edit .env file with your settings (at minimum, set DJANGO_SECRET_KEY)
nano .env  # or use your favorite editor
```

### Step 2: Start Services

```bash
# Using Make (recommended)
make up

# Or using Docker Compose directly
docker compose up -d
```

Wait about 30 seconds for services to start.

### Step 3: Initialize Database

```bash
# Run migrations
make migrate

# Create a superuser
make createsuperuser
# Follow the prompts to create your admin account
```

### Step 4: Access the Application

- **Control Plane API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **AI Gateway**: http://localhost:8080
- **MinIO Console**: http://localhost:9001 (user: minio, pass: minio123)

### Step 5: Test the API

#### Get Authentication Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your-username","password":"your-password"}'
```

#### Create a Tenant
```bash
curl -X POST http://localhost:8000/api/tenants/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "name": "Test Organization",
    "slug": "test-org",
    "contact_email": "test@example.com",
    "contact_name": "John Doe",
    "subscription_tier": "free"
  }'
```

#### Test AI Gateway
```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "tenant_id": "test-tenant",
    "max_tokens": 100
  }'
```

Note: AI Gateway requires API keys. Set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in your `.env` file.

## 📖 Common Tasks

### View Logs
```bash
# All services
make logs

# Specific service
make logs-control-plane
make logs-ai-gateway
make logs-worker
```

### Run Tests
```bash
make test
```

### Access Database
```bash
# Django shell
make shell

# PostgreSQL shell
make shell-db
```

### Stop Services
```bash
make down
```

### Reset Everything (⚠️ Destroys all data!)
```bash
make reset-db
```

## 🔧 Development Workflow

### 1. Install Dependencies Locally (Optional)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
make install
```

### 2. Make Changes
Edit files in `apps/control-plane/`, `apps/ai-gateway/`, etc.

### 3. Run Linters
```bash
make lint
```

### 4. Format Code
```bash
make format
```

### 5. Run Tests
```bash
make test
```

### 6. Create Migrations (if models changed)
```bash
make makemigrations
make migrate
```

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check service status
make status

# View logs for errors
make logs

# Rebuild containers
make build
make up
```

### Database Connection Errors
```bash
# Ensure database is healthy
docker compose ps

# Restart database
docker compose restart db

# Check database logs
docker compose logs db
```

### Port Already in Use
Edit `docker-compose.yml` to change port mappings:
```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

### Migration Errors
```bash
# Reset database (⚠️ destroys data)
make reset-db

# Or manually
docker compose down -v
docker compose up -d db
sleep 5
make migrate
```

## 📚 Next Steps

1. **Read the full README**: See [README.md](README.md)
2. **Explore the API**: Visit http://localhost:8000/admin
3. **Check the architecture**: See [docs/architecture/](docs/architecture/)
4. **Run the test suite**: `make test`
5. **Deploy to production**: See [README.md#deployment](README.md#deployment)

## 💡 Tips

- Use `make help` to see all available commands
- Set `DJANGO_DEBUG=True` in `.env` for development
- Check logs frequently: `make logs`
- Run tests before committing: `make test`
- Use `make format` before committing code

## 🆘 Get Help

- 📖 Full Documentation: [README.md](README.md)
- 🐛 Issues: https://github.com/nick-syspac/NextCore-AI-Cloud/issues
- 📧 Email: support@nextcollege.edu.au

---

**Happy coding! 🎉**
