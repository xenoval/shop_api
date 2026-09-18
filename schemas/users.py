from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, Field


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1)

    @field_validator("name")
    @classmethod
    def check_name(cls, value: str) -> str:
        if any(char.isdigit() for char in value):
            raise ValueError("Имя не должно содержать цифр")
        return value

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}