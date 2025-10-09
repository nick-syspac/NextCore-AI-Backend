.PHONY: bootstrap up down test format lint clean migrate shell logs help

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

bootstrap: ## Set up development environment
	@echo "Setting up development environment..."
	cp -n .env.example .env || true
	python -m venv .venv || true
	@echo "Virtual environment created. Run 'source .venv/bin/activate' to activate"
	@echo "Then run 'make install' to install dependencies"

install: ## Install dependencies
	@echo "Installing Python dependencies..."
	pip install --upgrade pip
	pip install -r apps/control-plane/requirements.txt
	pip install -r apps/ai-gateway/requirements.txt
	pip install -r apps/worker/requirements.txt
	pip install pytest pytest-cov pytest-django pytest-asyncio mypy ruff black
	@echo "Dependencies installed"

up: ## Start all services with docker-compose
	@echo "Starting services..."
	docker compose up -d
	@echo "Services started. Run 'make logs' to view logs"

down: ## Stop all services
	@echo "Stopping services..."
	docker compose down

restart: ## Restart all services
	@echo "Restarting services..."
	docker compose restart

build: ## Build docker images
	@echo "Building images..."
	docker compose build

logs: ## View logs from all services
	docker compose logs -f

logs-control-plane: ## View control-plane logs
	docker compose logs -f control-plane

logs-ai-gateway: ## View ai-gateway logs
	docker compose logs -f ai-gateway

logs-worker: ## View worker logs
	docker compose logs -f worker

shell: ## Open Django shell in control-plane
	docker compose exec control-plane python manage.py shell

shell-db: ## Open PostgreSQL shell
	docker compose exec db psql -U postgres -d rto

migrate: ## Run Django migrations
	docker compose exec control-plane python manage.py migrate

makemigrations: ## Create new migrations
	docker compose exec control-plane python manage.py makemigrations

createsuperuser: ## Create Django superuser
	docker compose exec control-plane python manage.py createsuperuser

test: ## Run all tests
	@echo "Running tests..."
	cd apps/control-plane && pytest -v --cov
	@echo "Tests completed"

test-fast: ## Run tests without coverage
	@echo "Running fast tests..."
	cd apps/control-plane && pytest -v
	@echo "Tests completed"

test-watch: ## Run tests in watch mode
	cd apps/control-plane && pytest-watch

lint: ## Run linters
	@echo "Running linters..."
	ruff check apps/ libs/
	@echo "Linting completed"

lint-fix: ## Run linters and fix issues
	@echo "Running linters with auto-fix..."
	ruff check --fix apps/ libs/
	@echo "Linting completed"

format: ## Format code with black and ruff
	@echo "Formatting code..."
	black apps/ libs/
	ruff check --fix apps/ libs/
	@echo "Formatting completed"

format-check: ## Check code formatting
	@echo "Checking code formatting..."
	black --check apps/ libs/
	@echo "Format check completed"

typecheck: ## Run type checking with mypy
	@echo "Running type checker..."
	mypy apps/control-plane apps/ai-gateway libs/
	@echo "Type checking completed"

security: ## Run security checks
	@echo "Running security checks..."
	pip install bandit safety
	bandit -r apps/ libs/
	safety check
	@echo "Security checks completed"

clean: ## Clean up temporary files
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup completed"

reset-db: ## Reset database (WARNING: destroys all data)
	@echo "WARNING: This will destroy all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker compose down -v; \
		docker compose up -d db redis; \
		sleep 5; \
		docker compose up -d control-plane; \
		sleep 3; \
		docker compose exec control-plane python manage.py migrate; \
		echo "Database reset completed"; \
	fi

dev: ## Start development environment
	@echo "Starting development environment..."
	docker compose up

status: ## Show status of services
	docker compose ps

ps: status ## Alias for status
