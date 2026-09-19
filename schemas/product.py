from uuid import UUID
from decimal import Decimal
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str
    price: Decimal
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"from_attributes": True}

class PagedProducts(BaseModel):
    # схема списка продуктов с пагинацией
    items: list[ProductResponse]
    limit: int 
    offset: int
    total: int

class ProductCreate(BaseModel):
    # схема создания продукта
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)

    @field_validator("name")
    @classmethod
    def check_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Имя не может быть пустым")
        return value