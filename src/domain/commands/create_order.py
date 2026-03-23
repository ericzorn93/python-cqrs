from cqrs.requests.request import Request


class CreateOrderCommand(Request):
    order_id: str
    amount: float
