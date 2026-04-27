from cqrs.requests.request import Request
from cqrs.response import PydanticResponse
from pydantic import Field


class CreateOrderCommand(Request):
    order_id: str
    amount: float


class CreateOrderCommandResponse(PydanticResponse):
    is_success: bool = Field(
        False, description="Indicates if the order creation was successful"
    )
