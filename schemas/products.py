from pydantic import BaseModel, Field, field_validator
from bson import ObjectId


class Product(BaseModel):
    # полная схема продукта
    # None - так как непостоянная структура полей
    id: str = Field(..., alias='_id')
    name: str | None = None
    description: str | None = None
    price: float | None = None

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, value:ObjectId) -> str:
        return str(value)
    

class PagedProducts(BaseModel):
    # схема списка продуктов с пагинацией
    items: list[Product]
    limit: int 
    offset: int
    total: int


class CreateProduct(BaseModel):
    # схема создания продукта
    name: str
    description: str
    price: float