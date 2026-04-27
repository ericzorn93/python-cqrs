from cqrs.events.event import IEvent
from cqrs.requests.request_handler import RequestHandler

from src.domain.commands import CreateOrderCommand, CreateOrderCommandResponse
from src.domain.events import OrderCreatedEvent
from src.utils.logger import logger


class CreateOrderHandler(
    RequestHandler[CreateOrderCommand, CreateOrderCommandResponse]
):
    def __init__(self) -> None:
        self._events: list[IEvent] = []

    @property
    def events(self) -> list[IEvent]:
        return self._events

    async def handle(self, request: CreateOrderCommand) -> CreateOrderCommandResponse:
        logger.info(
            "Handling CreateOrder: order_id=%s amount=%s",
            request.order_id,
            request.amount,
        )
        self._events.append(
            OrderCreatedEvent(order_id=request.order_id, amount=request.amount)
        )
        logger.debug(
            "Collected OrderCreatedEvent for order_id=%s (pending emit)",
            request.order_id,
        )

        return CreateOrderCommandResponse(is_success=True)
