from cqrs.events.event import DomainEvent


class OrderCreatedEvent(DomainEvent):
    order_id: str
    amount: float
