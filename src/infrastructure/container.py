from dependency_injector import containers, providers

from src.application.handlers.create_order import CreateOrderHandler
from src.application.handlers.get_orders import GetOrdersHandler
from src.application.handlers.order_created import OrderCreatedEventHandler


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Command handlers
    order_handler = providers.Factory(CreateOrderHandler)

    # Query handlers
    get_orders_handler = providers.Factory(GetOrdersHandler)

    # Event handlers
    order_created_event_handler = providers.Factory(
        OrderCreatedEventHandler,
    )
