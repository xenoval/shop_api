from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"))
    product_name: Mapped[Optional[str]] = mapped_column(String(255))
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    quantity: Mapped[int] = mapped_column(default=1)

    # Связи (relationships) в 2.0 также аннотируются через Mapped
    orders: Mapped["OrderModel"] = relationship(back_populates="order_items")
    products: Mapped["ProductModel"] = relationship(back_populates="order_items")


# product_id: Mapped[str] = mapped_column(String(50))

# order_items: Mapped[List["OrderItems"]] = relationship(
        # back_populates="orders", 
        # cascade="all, delete-orphan"
        # )

# created_at: Mapped[datetime] = mapped_column(server_default=func.now())