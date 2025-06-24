FROM python:3.13.5-bookworm AS builder

RUN apt update && apt upgrade -y && \
    apt install -y --no-install-recommends \
    gcc libc6-dev curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR=/root/.cache/uv

WORKDIR /build

COPY uv.lock pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY ./migrations/ /build/migrations/
COPY ./alembic.ini /build/
COPY ./src/ /build/src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.13.5-slim-bookworm AS prod

RUN apt update && apt upgrade -y && \
    apt install -y --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --gid 1001 --system appuser && \
    adduser --gid 1001 --shell /bin/false --disabled-password --uid 1001 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

COPY --from=builder --chown=appuser:appuser /build /app

USER appuser
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

CMD runserver -u appuser -- /app/.venv/bin/gunicorn \
    --workers 4 --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 --forwarded-allow-ips='*' --timeout=120 src.app.main:app
