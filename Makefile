# CHAOS Makefile
# ==============
# Developer commands for building, testing, and maintaining CHAOS.

.PHONY: help dev install test lint format clean build docs fuzz coverage check validate all

# Default target
help:
	@echo "CHAOS Development Commands"
	@echo "=========================="
	@echo ""
	@echo "Setup:"
	@echo "  make dev         Install development dependencies"
	@echo "  make install     Install package in editable mode"
	@echo ""
	@echo "Quality:"
	@echo "  make test        Run test suite"
	@echo "  make coverage    Run tests with coverage report"
	@echo "  make lint        Run pylint"
	@echo "  make format      Check code formatting"
	@echo "  make check       Run all checks (lint + test)"
	@echo ""
	@echo "Validation:"
	@echo "  make validate    Validate example CHAOS files"
	@echo "  make fuzz        Run corpus validation"
	@echo ""
	@echo "Build:"
	@echo "  make build       Build distribution packages"
	@echo "  make clean       Remove build artifacts"
	@echo ""
	@echo "Docker:"
	@echo "  make docker      Build Docker image"
	@echo "  make docker-run  Run in Docker container"
	@echo ""
	@echo "Utilities:"
	@echo "  make all         Run check + build"

# Setup targets
dev:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"
	@echo ""
	@echo "✓ Development environment ready!"

install:
	pip install -e .

# Quality targets
test:
	python -m pytest -v

coverage:
	python -m pytest --cov=chaos_language --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "✓ Coverage report generated in htmlcov/"

lint:
	pylint src/chaos_language tests tools/cli_shims --ignore-patterns='__pycache__'

format:
	@echo "Checking code formatting..."
	python -m py_compile src/chaos_language/*.py tests/*.py tools/cli_shims/*.py
	pylint src/chaos_language tests scripts tools/cli_shims --ignore-patterns='__pycache__'

format:
	@echo "Checking code formatting..."
	python -m py_compile src/chaos_language/*.py tests/*.py scripts/*.py $(shell find tools/cli_shims -name "*.py")
	@echo "✓ All files compile successfully"

check: lint test
	@echo ""
	@echo "✓ All checks passed!"

# Validation targets
validate:
	chaos-validate artifacts/examples/*.chaos -v
	chaos-validate artifacts/templates/*.chaos -v
	@echo ""
	@echo "✓ Example and template files validated"

fuzz:
	python tools/cli_shims/chaos_fuzz.py
	@echo ""
	@echo "✓ Corpus validation complete"

# Build targets
build: clean
	python -m pip install --upgrade build
	python -m build
	@echo ""
	@echo "✓ Built packages in dist/"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned build artifacts"

# Docker targets
docker:
	docker build -t chaos-language:latest .
	@echo ""
	@echo "✓ Docker image built: chaos-language:latest"

docker-run:
	docker run -it --rm chaos-language:latest

# Combined targets
all: check build
	@echo ""
	@echo "✓ All tasks complete!"
