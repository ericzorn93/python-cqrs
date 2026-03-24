from cqrs.events.event_handler import EventHandler

from src.domain.events import OrderCreatedEvent
from src.utils.logger import logger


class OrderCreatedEventHandler(EventHandler[OrderCreatedEvent]):
    async def handle(self, event: OrderCreatedEvent) -> None:
        logger.info("Order created: order_id=%s amount=%s", event.order_id, event.amount)
