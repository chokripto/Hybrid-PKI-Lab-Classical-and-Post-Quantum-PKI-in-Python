SHELL := /bin/bash

PROJECT_NAME := hybrid-pki-lab
PACKAGE_NAME := hybrid_pki
PYTHON := python
PIP := pip

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo ""
	@echo "Hybrid-PKI-Lab Makefile"
	@echo "======================="
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make install          Install project dependencies"
	@echo "  make install-dev      Install project with development dependencies"
	@echo "  make install-all      Install all optional dependencies"
	@echo "  make run-api          Run FastAPI server"
	@echo "  make test             Run tests"
	@echo "  make coverage         Run tests with coverage"
	@echo "  make lint             Run Ruff linting"
	@echo "  make format           Format code with Black and Ruff"
	@echo "  make type-check       Run mypy"
	@echo "  make security         Run Bandit and pip-audit"
	@echo "  make benchmark        Run benchmarks"
	@echo "  make clean            Remove cache and build files"
	@echo "  make docker-build     Build Docker image"
	@echo "  make docker-up        Run API with Docker Compose"
	@echo "  make docker-down      Stop Docker Compose services"
	@echo "  make docker-test      Run tests inside Docker"
	@echo "  make init-dirs        Create certificate and log directories"
	@echo "  make classical-demo   Run classical PKI demo"
	@echo "  make hybrid-demo      Run hybrid PKI demo"
	@echo ""

.PHONY: install
install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

.PHONY: install-dev
install-dev:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev]"

.PHONY: install-all
install-all:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[all]"

.PHONY: install-pqc
install-pqc:
	$(PIP) install liboqs-python

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
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: init-dirs
init-dirs:
	mkdir -p certs/root
	mkdir -p certs/intermediate
	mkdir -p certs/issued
	mkdir -p certs/revoked
	mkdir -p certs/hybrid
	mkdir -p logs
	mkdir -p benchmarks/results

.PHONY: classical-demo
classical-demo:
	$(PYTHON) examples/classical_pki_demo.py

.PHONY: hybrid-demo
hybrid-demo:
	$(PYTHON) examples/hybrid_pki_demo.py

.PHONY: migration-demo
migration-demo:
	$(PYTHON) examples/migration_demo.py

.PHONY: revoke-demo
revoke-demo:
	$(PYTHON) examples/revoke_certificate_demo.py

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

.PHONY: docker-shell
docker-shell:
	docker compose --profile shell run --rm hybrid-pki-shell

.PHONY: docs
docs:
	mkdocs serve

.PHONY: check
check: lint type-check test security

.PHONY: all
all: clean install-dev init-dirs format lint type-check test
