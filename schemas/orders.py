from pydantic import BaseModel, Field, ConfigDict


class OrderCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

class OrdersCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    items: list[OrderCreate]

class OrdersResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    total: float
