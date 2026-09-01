FROM python:3.12.8-slim-bookworm

LABEL maintainer="Dr. Chokri NOUAR"
LABEL project="Hybrid-PKI-Lab"
LABEL security.profile="local-educational-lab"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app \
    HYBRID_PKI_DISABLE_OQS=1

WORKDIR ${APP_HOME}

COPY requirements.txt pyproject.toml README.md ./
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && pip install .

COPY src ./src
COPY examples ./examples
COPY tests ./tests
COPY benchmarks ./benchmarks
COPY docs ./docs
COPY scripts ./scripts

RUN groupadd --system hybridpki \
    && useradd --system --gid hybridpki --home-dir /app hybridpki \
    && mkdir -p certs/root certs/intermediate certs/issued certs/revoked certs/hybrid logs benchmarks/results \
    && chown -R hybridpki:hybridpki /app

USER hybridpki

EXPOSE 8000
CMD ["uvicorn", "hybrid_pki.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
