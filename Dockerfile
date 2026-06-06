# Phase 2: Minimal python:3.11-slim runtime base
FROM python:3.11-slim

# Prevent bytecode generation and enforce unbuffered log streaming
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install build dependencies for native database extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv manager for lightning-fast deterministic syncing
RUN pip install --no-cache-dir uv==0.5.11

# Copy dependency configuration files
COPY pyproject.toml requirements.txt ./

# Install dependencies deterministically using requirements.txt
RUN uv pip install --system -r requirements.txt

# Copy application source code
COPY . .

# Phase 3 (US1): Enforce unprivileged non-root user execution (UID 10001)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/bash -m appuser && \
    chown -R appuser:appgroup /app

USER appuser

# Launch live production server entrypoint dynamically binding to $PORT
CMD ["python", "server.py"]
