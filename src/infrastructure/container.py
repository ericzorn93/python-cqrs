from dependency_injector import containers, providers

from src.application.handlers.create_order import CreateOrderHandler
from src.application.handlers.order_created import OrderCreatedEventHandler


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Command handlers
    order_handler = providers.Factory(CreateOrderHandler)

    # Event handlers
    order_created_event_handler = providers.Factory(
        OrderCreatedEventHandler,
    )
