from cqrs.events.event_handler import EventHandler

from src.domain.events import OrderCreatedEvent
from src.ports.notifications import OrderCreatedNotifier


class OrderCreatedEventHandler(EventHandler[OrderCreatedEvent]):
    def __init__(self, notifier: OrderCreatedNotifier) -> None:
        self._notifier = notifier

    async def handle(self, event: OrderCreatedEvent) -> None:
        await self._notifier.order_created(event.order_id, event.amount)
