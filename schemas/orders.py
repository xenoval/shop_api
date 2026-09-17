from pydantic import BaseModel, field_validator, Field


class CreateOrder(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

class CreateOrders(BaseModel):
    user_id: int
    items: list[CreateOrder]

class OrdersResponse(BaseModel):
    order_id: int
    total: float
