from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")

class TokenData(BaseModel):
    sub: Optional[str] = Field(default=None, description="Идентификатор пользователя (ID or Email)")