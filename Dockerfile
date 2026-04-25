FROM python:3.14 AS builder

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN pip install uv
COPY pyproject.toml README.md ./
RUN uv sync
FROM python:3.14-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .
CMD [".venv/bin/fastapi", "run"]
