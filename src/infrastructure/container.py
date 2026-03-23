from dependency_injector import containers, providers

from src.application.handlers.create_order import CreateOrderHandler
from src.application.handlers.order_created import OrderCreatedEventHandler
from src.infrastructure.adapters.console_order_notifier import ConsoleOrderCreatedNotifier


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    order_created_notifier = providers.Singleton(ConsoleOrderCreatedNotifier)

    order_handler = providers.Factory(CreateOrderHandler)
    order_created_event_handler = providers.Factory(
        OrderCreatedEventHandler,
        notifier=order_created_notifier,
    )
