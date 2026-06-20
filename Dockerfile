FROM python:3.11-slim

LABEL maintainer="Chokri"
LABEL project="Hybrid-PKI-Lab"
LABEL description="Classical and Post-Quantum Hybrid PKI in Python"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV APP_HOME=/app

WORKDIR ${APP_HOME}

# System dependencies required for cryptography, OpenSSL, liboqs and Python builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    cmake \
    ninja-build \
    build-essential \
    pkg-config \
    libssl-dev \
    ca-certificates \
    curl \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------------------
# Build and install liboqs
# ----------------------------------------------------------------------
RUN git clone --depth 1 https://github.com/open-quantum-safe/liboqs.git /tmp/liboqs \
    && cmake -S /tmp/liboqs -B /tmp/liboqs/build \
        -GNinja \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DOQS_BUILD_ONLY_LIB=ON \
        -DOQS_USE_OPENSSL=ON \
    && cmake --build /tmp/liboqs/build \
    && cmake --install /tmp/liboqs/build \
    && rm -rf /tmp/liboqs

ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

# Copy project files
COPY requirements.txt .
COPY pyproject.toml .
COPY README.md .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && pip install liboqs-python || true

# Copy source code
COPY src ./src
COPY examples ./examples
COPY tests ./tests
COPY benchmarks ./benchmarks
COPY docs ./docs
COPY scripts ./scripts

# Install package in editable mode
RUN pip install -e .

# Create certificate storage directories
RUN mkdir -p \
    certs/root \
    certs/intermediate \
    certs/issued \
    certs/revoked \
    certs/hybrid \
    logs

EXPOSE 8000

CMD ["uvicorn", "hybrid_pki.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
