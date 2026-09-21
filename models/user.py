from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    orders: Mapped["OrderModel"] = relationship(back_populates="users")