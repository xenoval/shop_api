from fastapi import APIRouter, Depends, HTTPException
from db.mysql import get_connection
from schemas.schemas_users import UserCreate, UserResponse
from models.users import User
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_connection)):
    users = User(
        email=user.email,
        name=user.name
    )

    db.add(users)
    db.commit()  
    db.refresh(users)
    
    return UserResponse(
        id=users.id,
        email=users.email,
        name=users.name,
        created_at=users.created_at
    )

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_connection)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at
    )
    


