from decimal import Decimal
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class ProductModel(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(400))
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    order_items: Mapped["OrderItemModel"] = relationship(back_populates="products")