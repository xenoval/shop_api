from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_connection
from models.users import User
from schemas.users import CreateUser, UserResponse


router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user: CreateUser, db: AsyncSession = Depends(get_connection)):
    new_user = User(
        email=user.email,
        name=user.name
    )

    db.add(new_user)
    await db.commit()  
    await db.refresh(new_user)
    
    return new_user

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_connection),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user