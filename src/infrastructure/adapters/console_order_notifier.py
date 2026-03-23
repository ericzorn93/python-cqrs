from src.ports.notifications import OrderCreatedNotifier
from src.utils.logger import logger


class ConsoleOrderCreatedNotifier:
    """Adapter: order-created notifications via the logging stack."""

    async def order_created(self, order_id: str, amount: float) -> None:
        logger.info("Order created: order_id=%s amount=%s", order_id, amount)
