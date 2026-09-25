from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(1))
    # total: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    users: Mapped["UserModel"] = relationship(back_populates="orders")
    order_items: Mapped[List["OrderItemModel"]] = relationship(
        back_populates="orders", 
        cascade="all, delete-orphan"
        )