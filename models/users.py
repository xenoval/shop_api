from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func
from models.base import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    orders = relationship("Orders", back_populates="user")