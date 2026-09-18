from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, func, CHAR, DECIMAL, ForeignKey
from models.base import Base


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(CHAR(1), nullable=False)
    total = Column(DECIMAL(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("Users", back_populates="orders")
    order_items = relationship("OrderItems", back_populates="orders", cascade="all, delete-orphan")