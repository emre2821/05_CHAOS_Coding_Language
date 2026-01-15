# CHAOS Language Runtime
# =======================
# Multi-stage build for minimal production image

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Copy only files needed for installation
COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY tools/cli_shims/ ./tools/cli_shims/

# Install build dependencies and build wheel
RUN pip install --no-cache-dir build && \
    python -m build --wheel

# Production stage
FROM python:3.11-slim

LABEL maintainer="Paradigm Eden"
LABEL description="CHAOS - Contextual Harmonics and Operational Stories"
LABEL version="0.1.0"

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash chaos

WORKDIR /app

# Copy wheel from builder and install
COPY --from=builder /app/dist/*.whl ./
RUN pip install --no-cache-dir *.whl && \
    rm -f *.whl

# Copy example corpus for reference
COPY artifacts/corpus_sn/ ./artifacts/corpus_sn/

# Set up environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV CHAOS_OUTPUT_DIR=/app/output

# Create output directory
RUN mkdir -p /app/output && chown chaos:chaos /app/output

# Switch to non-root user
USER chaos

# Default command - interactive agent
ENTRYPOINT ["chaos-agent"]
CMD ["--name", "Eden"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "from chaos_language import run_chaos; print('healthy')" || exit 1

# Alternative entry points:
# docker run chaos-language chaos-cli artifacts/corpus_sn/memory_garden.sn --json
# docker run chaos-language chaos-exec artifacts/corpus_sn/stability_call.sn --report
