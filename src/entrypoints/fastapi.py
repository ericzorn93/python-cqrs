import logging
from contextlib import asynccontextmanager
from typing import Annotated

from cqrs.mediator import RequestMediator
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel

from src.domain.commands import CreateOrderCommand
from src.infrastructure.composition import build_mediator
from src.utils.logger import configure_logging


class CreateOrderRequest(BaseModel):
    order_id: str
    amount: float


def get_mediator(request: Request) -> RequestMediator:
    """Dependency provider to inject the mediator from app state."""
    return request.app.state.mediator


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown."""
    # Startup logic
    configure_logging(level=logging.INFO)

    # Initialize mediator and store in app state
    mediator = build_mediator()
    app.state.mediator: RequestMediator = mediator

    yield

    # Shutdown logic
    # Add any cleanup here if needed


def create_app() -> FastAPI:
    app = FastAPI(title="MediaTr API", version="0.1.0", lifespan=lifespan)

    @app.post("/orders")
    async def create_order(
        request: CreateOrderRequest,
        mediator: Annotated[RequestMediator, Depends(get_mediator)],
    ) -> dict:
        """Create a new order via CQRS mediator using dependency injection."""
        command = CreateOrderCommand(order_id=request.order_id, amount=request.amount)
        await mediator.send(command)
        return {
            "status": "success",
            "order_id": request.order_id,
            "amount": request.amount,
        }

    @app.get("/health")
    async def health(mediator: Annotated[RequestMediator, Depends(get_mediator)]) -> dict:
        """Health check endpoint - also uses dependency injection."""
        return {"status": "healthy", "mediator": type(mediator).__name__}

    return app


def run() -> None:
    """Run the FastAPI server with uvicorn."""
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run()
