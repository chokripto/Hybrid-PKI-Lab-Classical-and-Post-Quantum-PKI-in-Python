FROM python:3.11-slim

LABEL maintainer="Chokri"
LABEL project="Hybrid-PKI-Lab"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV APP_HOME=/app

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    git cmake ninja-build build-essential pkg-config libssl-dev ca-certificates curl python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/open-quantum-safe/liboqs.git /tmp/liboqs \
    && cmake -S /tmp/liboqs -B /tmp/liboqs/build -GNinja \
        -DCMAKE_INSTALL_PREFIX=/usr/local -DOQS_BUILD_ONLY_LIB=ON -DOQS_USE_OPENSSL=ON \
    && cmake --build /tmp/liboqs/build \
    && cmake --install /tmp/liboqs/build \
    && rm -rf /tmp/liboqs

ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

COPY requirements.txt pyproject.toml README.md ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && pip install liboqs-python || true

COPY src ./src
COPY examples ./examples
COPY tests ./tests
COPY benchmarks ./benchmarks
COPY docs ./docs
COPY scripts ./scripts

RUN pip install -e .
RUN mkdir -p certs/root certs/intermediate certs/issued certs/revoked certs/hybrid logs

EXPOSE 8000
CMD ["uvicorn", "hybrid_pki.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
