from cqrs.events.map import EventMap
from cqrs.requests.map import RequestMap

from src.application.handlers.create_order import CreateOrderHandler
from src.application.handlers.order_created import OrderCreatedEventHandler
from src.domain.commands import CreateOrderCommand
from src.domain.events import OrderCreatedEvent


def map_commands(mapper: RequestMap) -> None:
    mapper.bind(CreateOrderCommand, CreateOrderHandler)


def map_domain_events(mapper: EventMap) -> None:
    mapper.bind(OrderCreatedEvent, OrderCreatedEventHandler)
