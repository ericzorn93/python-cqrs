import asyncio
import logging
import random

from cqrs.mediator import RequestMediator

from src.domain.commands import CreateOrderCommand


async def run() -> None:
    from src.infrastructure.composition import build_mediator

    mediator = build_mediator()
    await process_orders(mediator)


async def process_orders(mediator: RequestMediator) -> None:
    for i in range(5):
        amount = round(random.uniform(10.0, 100.0), 2)
        await mediator.send(CreateOrderCommand(order_id=f"ord-{i}", amount=amount))


def main() -> None:
    from src.utils.logger import configure_logging

    configure_logging(level=logging.INFO)
    asyncio.run(run())
