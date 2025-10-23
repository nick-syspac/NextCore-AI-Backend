# 🚀 Getting Started with NextCore AI Cloud on Ubuntu WSL

This guide will walk you through setting up and running NextCore AI Cloud locally on Ubuntu WSL.

## Prerequisites Installation

First, ensure you have the required tools installed:

```bash
# Update package list
sudo apt update

# Install Docker if not already installed
sudo apt install -y docker.io docker-compose

# Add your user to docker group (to run docker without sudo)
sudo usermod -aG docker $USER

# Start Docker service
sudo service docker start

# Install Make (if not installed)
sudo apt install -y make

# Install Python 3.11+ (if not installed)
sudo apt install -y python3.11 python3.11-venv python3-pip

# Verify installations
docker --version
docker-compose --version
python3 --version
make --version
```

**Important for WSL:** After adding yourself to the docker group, you may need to restart your WSL session:
```bash
exit
# Then reopen your WSL terminal
```

## Step-by-Step Setup

### 1. Navigate to Your Project
```bash
cd /path/to/NextCore-AI-Cloud
```

### 2. Create Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your settings
nano .env
```

**Minimum required changes in `.env`:**
```bash
# Generate a secure secret key
DJANGO_SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# For development, you can leave most defaults
DJANGO_DEBUG=True
ALLOWED_HOSTS=*

# If you want to test AI Gateway, add your API key:
OPENAI_API_KEY=sk-your-actual-openai-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

### 3. Start Docker Services
```bash
# Make sure Docker is running
sudo service docker start

# IMPORTANT: Stop system Redis/PostgreSQL if running (WSL often has these)
sudo service redis-server stop 2>/dev/null || true
sudo service postgresql stop 2>/dev/null || true

# Start all services (this will download images and start containers)
make up

# This is equivalent to: docker-compose up -d
```

Wait about 30-60 seconds for all services to initialize. You can monitor progress:
```bash
# Check service status
make status

# Or watch the logs
make logs
```

### 4. Run Database Migrations
```bash
# Run migrations to set up the database schema
make migrate
```

### 5. Create Your Admin User
```bash
# Create a superuser account
make createsuperuser
```

Follow the prompts to enter:
- Username
- Email
- Password (enter twice)

### 6. Verify Everything is Running
```bash
# Check all services are healthy
docker-compose ps

# You should see all services as "running" or "healthy"
```

## 🎉 Access Your Application

Once everything is running, you can access:

- **Control Plane API**: http://localhost:8000
- **Django Admin Panel**: http://localhost:8000/admin
- **AI Gateway**: http://localhost:8080
- **MinIO Console**: http://localhost:9001 (user: `minio`, pass: `minio123`)

## Quick Test

### Test the Django Admin
1. Go to http://localhost:8000/admin
2. Log in with your superuser credentials
3. You should see the admin dashboard

### Test the API
```bash
# Get an authentication token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your-username","password":"your-password"}'

# Save the token and create a tenant
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

## Common Commands

```bash
# View all logs
make logs

# View specific service logs
make logs-control-plane
make logs-ai-gateway
make logs-worker

# Stop all services
make down

# Restart services
make restart

# Access Django shell
make shell

# Access PostgreSQL database
make shell-db

# Run tests
make test

# See all available commands
make help
```

## Troubleshooting

### Initial Setup: System Services Conflict (Common in WSL)
**Problem**: Ports 6379 (Redis) and 5432 (PostgreSQL) already in use  
**Solution**:
```bash
# Stop system services before starting Docker containers
sudo service redis-server stop
sudo service postgresql stop

# Prevent them from auto-starting (optional)
sudo systemctl disable redis-server
sudo systemctl disable postgresql

# Then start your containers
make up
```

### Docker Permission Issues
```bash
# If you get permission denied errors
sudo service docker start
sudo chmod 666 /var/run/docker.sock
```

### Port Already in Use
If ports are already in use (common with Redis on 6379 or PostgreSQL on 5432):

**For system services (Redis/PostgreSQL):**
```bash
# Check what's using the ports
sudo lsof -i :6379 -i :5432

# Stop system Redis and PostgreSQL services
sudo service redis-server stop
sudo service postgresql stop

# Prevent them from auto-starting (optional)
sudo systemctl disable redis-server
sudo systemctl disable postgresql

# Then restart your containers
make up
```

**For other ports (8000, 8080, etc):**
```bash
# Find what's using the port
sudo lsof -i :8000

# Kill the process or edit docker-compose.yml to change ports
```

### Services Won't Start
```bash
# Check Docker is running
sudo service docker status
sudo service docker start

# Rebuild containers
docker-compose build
docker-compose up -d

# Or use make
make build
make up

# Check logs for errors
make logs
```

### Database Connection Errors
```bash
# Restart database and wait for it to be ready
docker-compose restart db
sleep 10
make migrate
```

### Reset Everything (Nuclear Option)
```bash
# This will delete all data and start fresh
make reset-db
```

## WSL-Specific Tips

### 1. Docker Service
WSL doesn't start services automatically. Always run:
```bash
sudo service docker start
```

You can add this to your `~/.bashrc` or `~/.zshrc` to auto-start Docker:
```bash
# Start Docker service if not running
if ! service docker status > /dev/null 2>&1; then
    sudo service docker start
fi
```

### 2. Memory Issues
If containers are slow, increase WSL memory in `.wslconfig`:
```bash
# Create/edit ~/.wslconfig on Windows side
# (This file goes in your Windows user directory: C:\Users\YourName\.wslconfig)
[wsl2]
memory=8GB
processors=4
```

After editing, restart WSL:
```powershell
# In Windows PowerShell
wsl --shutdown
# Then reopen your WSL terminal
```

### 3. File Permissions
If you encounter permission issues with mounted volumes:
```bash
# Fix permissions on project directory
sudo chmod -R 755 /path/to/NextCore-AI-Cloud

# Or if you need write access to all files
sudo chown -R $USER:$USER /path/to/NextCore-AI-Cloud
```

### 4. DNS Issues
If you experience network connectivity issues in WSL:
```bash
# Add to /etc/wsl.conf
[network]
generateResolvConf = false

# Then manually set DNS
sudo rm /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
sudo bash -c 'echo "nameserver 8.8.4.4" >> /etc/resolv.conf'
```

## Development Workflow

### 1. Making Code Changes
The docker-compose setup mounts your local code into the containers, so changes are reflected immediately:

```bash
# Edit files locally
code apps/control-plane/tenants/views.py

# Changes are automatically available in the container
# For Python changes, the dev server auto-reloads
```

### 2. Adding Python Dependencies
```bash
# Add to requirements.txt
echo "new-package==1.0.0" >> apps/control-plane/requirements.txt

# Rebuild the container
docker-compose build control-plane
docker-compose up -d control-plane
```

### 3. Database Migrations
```bash
# After modifying models.py files
make makemigrations

# Apply migrations
make migrate
```

### 4. Running Tests
```bash
# Run all tests with coverage
make test

# Run tests without coverage (faster)
make test-fast

# Run specific test file
docker-compose exec control-plane pytest audit/tests.py -v
```

### 5. Code Quality
```bash
# Format code
make format

# Check linting
make lint

# Auto-fix linting issues
make lint-fix

# Type checking
make typecheck
```

## Next Steps

1. **Explore the Admin Panel**: http://localhost:8000/admin
   - Create tenants, users, and manage the system

2. **Read API Documentation**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
   - Learn about all available endpoints

3. **Create Tenants**: Use the API or admin panel
   - Set up your first organization

4. **Test AI Gateway**: Add your OpenAI/Anthropic key to `.env` and restart
   ```bash
   # Edit .env
   nano .env
   # Add: OPENAI_API_KEY=sk-your-key
   
   # Restart services
   make restart
   ```

5. **Explore Architecture**: See [docs/architecture/](docs/architecture/)
   - Understand the system design

6. **Review Compliance**: See [docs/compliance/](docs/compliance/)
   - Learn about RTO compliance features

## Useful Resources

- **README.md** - Comprehensive project overview
- **QUICKSTART.md** - Quick reference guide
- **API_DOCUMENTATION.md** - Complete API reference
- **CONTRIBUTING.md** - Contribution guidelines
- **SECURITY.md** - Security policies and best practices

## Getting Help

- 📖 Documentation: Check the `docs/` directory
- 🐛 Issues: https://github.com/nick-syspac/NextCore-AI-Cloud/issues
- 📧 Email: support@nextcollege.edu.au

---

**Happy coding! 🎉**
