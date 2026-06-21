SHELL := /bin/bash
PROJECT_NAME := hybrid-pki-lab
PACKAGE_NAME := hybrid_pki
PYTHON := python
PIP := pip
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Hybrid-PKI-Lab Makefile"
	@echo "  make install          Install dependencies"
	@echo "  make install-dev      Install development dependencies"
	@echo "  make run-api          Run FastAPI server"
	@echo "  make test             Run tests"
	@echo "  make coverage         Run tests with coverage"
	@echo "  make lint             Run Ruff"
	@echo "  make format           Format code"
	@echo "  make type-check       Run mypy"
	@echo "  make security         Run Bandit and pip-audit"
	@echo "  make benchmark        Run benchmarks"
	@echo "  make clean            Clean cache and build files"
	@echo "  make docker-build     Build Docker image"
	@echo "  make docker-up        Run API with Docker Compose"
	@echo "  make docker-down      Stop Docker Compose"
	@echo "  make init-dirs        Create cert/log directories"

.PHONY: install
install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

.PHONY: install-dev
install-dev:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev]"

.PHONY: run-api
run-api:
	uvicorn hybrid_pki.api.main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: test
test:
	pytest -v

.PHONY: coverage
coverage:
	pytest -v --cov=$(PACKAGE_NAME) --cov-report=term-missing --cov-report=html

.PHONY: lint
lint:
	ruff check src tests examples benchmarks

.PHONY: format
format:
	black src tests examples benchmarks
	ruff check src tests examples benchmarks --fix

.PHONY: type-check
type-check:
	mypy src

.PHONY: security
security:
	bandit -r src
	pip-audit

.PHONY: benchmark
benchmark:
	$(PYTHON) benchmarks/benchmark_keygen.py
	$(PYTHON) benchmarks/benchmark_signatures.py
	$(PYTHON) benchmarks/benchmark_handshake.py

.PHONY: clean
clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: init-dirs
init-dirs:
	mkdir -p certs/root certs/intermediate certs/issued certs/revoked certs/hybrid logs benchmarks/results

.PHONY: docker-build
docker-build:
	docker build -t $(PROJECT_NAME) .

.PHONY: docker-up
docker-up:
	docker compose up --build hybrid-pki-api

.PHONY: docker-down
docker-down:
	docker compose down

.PHONY: docker-test
docker-test:
	docker compose --profile test up --build hybrid-pki-tests
