from typing import Protocol, runtime_checkable


@runtime_checkable
class OrderCreatedNotifier(Protocol):
    """Outbound port: react when an order is created (replace with email, bus, etc.)."""

    async def order_created(self, order_id: str, amount: float) -> None: ...
