from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, Numeric
from models.base import Base

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(400), nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())