import logging
from contextlib import asynccontextmanager
from decimal import Decimal
from typing import Annotated


from cqrs.mediator import RequestMediator
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel, ConfigDict, Field, field_validator, condecimal
from pydantic.alias_generators import to_camel

from src.domain.commands import CreateOrderCommand
from src.infrastructure.composition import build_mediator
from src.utils.logger import configure_logging


class CreateOrderRequest(BaseModel):
    order_id: str
    amount: Decimal


class CreateOrderResponse(BaseModel):
    """Response model for order creation with camelCase aliases."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    status: str
    order_id: str
    amount: condecimal(decimal_places=2) = Field(example="19.99")

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
    app = FastAPI(title="Mediatr API", version="0.1.0", lifespan=lifespan)

    @app.post("/orders")
    async def create_order(
        request: CreateOrderRequest,
        mediator: Annotated[RequestMediator, Depends(get_mediator)],
    ) -> CreateOrderResponse:
        """Create a new order via CQRS mediator using dependency injection."""
        command = CreateOrderCommand(order_id=request.order_id, amount=float(request.amount))
        await mediator.send(command)
        return CreateOrderResponse(
            status="success",
            order_id=request.order_id,
            amount=request.amount.quantize(Decimal("0.00")),
        )

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
