from pydantic import BaseModel


class OrderCreate(BaseModel):
    product_id: str
    quantity: int

class OrdersCreate(BaseModel):
    user_id: int
    items: list[OrderCreate]

class OrdersResponse(BaseModel):
    order_id: int
    total: float
