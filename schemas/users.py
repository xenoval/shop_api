from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class CreateUser(BaseModel):
    email: EmailStr
    name: str

    @field_validator("name")
    @classmethod
    def check_name(cls, value: str) -> str:
        if any(char.isdigit() for char in value):
            raise ValueError("Имя не должно содержать цифр")
        return value

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}