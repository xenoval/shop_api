from pydantic import BaseModel


class CreateOrder(BaseModel):
    product_id: str
    quantity: int

class CreateOrders(BaseModel):
    user_id: int
    items: list[CreateOrder]

class OrdersResponse(BaseModel):
    order_id: int
    total: float
