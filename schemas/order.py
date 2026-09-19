from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class OrderCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(..., gt=0)

class OrdersCreate(BaseModel):
    user_id: UUID
    items: list[OrderCreate]

class OrdersResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: UUID
    total: float
