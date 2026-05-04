# ============================================================================
# Dockerfile – Deep-Agents Procaps Template
# ============================================================================
# Multi-stage build: install deps in a builder layer, then copy to a slim
# runtime image.  The resulting container runs a FastAPI application via
# uvicorn, matching the Azure Container Apps deployment in Pipelines/main.yml.
# ============================================================================

# ── Builder stage ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build-time OS dependencies (gcc may be needed for some wheels)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Runtime stage ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL maintainer="Procaps Digital <devops@procaps.com>" \
      description="Non-conversational DeepAgents template API" \
      version="0.1.0"

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY . .

# Non-root user for security
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

# Azure Container Apps injects PORT; default to 8000 for local dev
ENV PORT=8000

EXPOSE ${PORT}

# Health-check so Docker / Container Apps can probe readiness
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health')" || exit 1

# Start uvicorn pointing at the FastAPI app
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
