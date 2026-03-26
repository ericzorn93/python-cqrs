# mediatr

A small Python service that wires **CQRS-style commands and domain events** through [`python-cqrs`](https://pypi.org/project/python-cqrs/), with **dependency-injector** for handler construction and **FastAPI** as the HTTP entrypoint.

## Requirements

- **Python 3.14+** (see `.python-version`)
- [**uv**](https://docs.astral.sh/uv/) for dependencies and runs (lockfile: `uv.lock`)

## Setup

```bash
uv sync
```

## Run

### HTTP API

Starts Uvicorn on `0.0.0.0:8000` with structured JSON logging to stdout.

```bash
uv run python -m src.entrypoints.fastapi
```

- `POST /orders` — body: `{ "order_id": "<id>", "amount": "<decimal>" }` — dispatches `CreateOrderCommand` through the mediator.
- `GET /health` — liveness check; confirms the mediator is available.

### CLI demo

Sends five sample `CreateOrderCommand` messages through the same mediator (no HTTP server).

```bash
uv run python main.py
```

## How it works

1. **`build_mediator()`** (`src/infrastructure/composition.py`) bootstraps a `RequestMediator` with a `DependencyInjectorCQRSContainer` and your `Container`.
2. **Command mapping** (`src/infrastructure/mappers.py`) binds `CreateOrderCommand` → `CreateOrderHandler`.
3. **Event mapping** binds `OrderCreatedEvent` → `OrderCreatedEventHandler` after the command pipeline publishes domain events.
4. **FastAPI** stores the mediator on `app.state` and injects it into route handlers via `Depends`.

## Project layout

| Path | Role |
|------|------|
| `src/domain/` | Commands (`CreateOrderCommand`) and domain events (`OrderCreatedEvent`) |
| `src/application/handlers/` | Command and event handlers |
| `src/infrastructure/` | DI `Container`, mediator composition, CQRS mappers |
| `src/entrypoints/` | FastAPI app and CLI |
| `src/ports/` | Protocols for outbound adapters (e.g. notifications) |
| `src/utils/` | Shared logging (`python-json-logger`) |

## License

Add a license if you publish this repository.
