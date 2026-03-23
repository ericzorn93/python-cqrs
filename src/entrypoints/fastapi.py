import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from src.domain.commands import CreateOrderCommand
from src.infrastructure.composition import build_mediator
from src.utils.logger import configure_logging


class CreateOrderRequest(BaseModel):
    order_id: str
    amount: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    configure_logging(level=logging.INFO)
    yield
    # Shutdown logic


def create_app() -> FastAPI:
    app = FastAPI(title="MediaTr API", version="0.1.0", lifespan=lifespan)
    mediator = build_mediator()

    @app.post("/orders")
    async def create_order(request: CreateOrderRequest) -> dict:
        """Create a new order via CQRS mediator."""
        command = CreateOrderCommand(order_id=request.order_id, amount=request.amount)
        await mediator.send(command)
        return {
            "status": "success",
            "order_id": request.order_id,
            "amount": request.amount,
        }

    @app.get("/health")
    async def health() -> dict:
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


def run() -> None:
    """Run the FastAPI server with uvicorn."""
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
