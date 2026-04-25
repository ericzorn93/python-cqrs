FROM python:3.14 AS builder

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN pip install uv
COPY pyproject.toml README.md ./
RUN uv sync
FROM python:3.14-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .
EXPOSE 8000
CMD [".venv/bin/python", "-m", "uvicorn", "src.entrypoints.fastapi:create_app", "--host", "0.0.0.0", "--port", "8000"]
