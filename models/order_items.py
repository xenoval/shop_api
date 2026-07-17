from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from models.base import Base


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(String(50), nullable=False)
    product_name = Column(String(255))
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    orders = relationship("Orders", back_populates="order_items")
