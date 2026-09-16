from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CreateUser(BaseModel):
    email: EmailStr
    name: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}