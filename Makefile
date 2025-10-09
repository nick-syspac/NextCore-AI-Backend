.PHONY: bootstrap up test format

bootstrap:
	pre-commit install || true
	python -m venv .venv || true

up:
	docker compose up -d

test:
	pytest -q || true

format:
	ruff . --fix || true
	black . || true
