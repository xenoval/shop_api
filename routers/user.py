from uuid import UUID
from fastapi import APIRouter, Depends


from db.postgres import get_connection 
from repositories.user import UserRepository
from services.user import UserService
from schemas.user import UserCreate, UserResponse

router = APIRouter()

# Функция, которая собирает цепочку зависимостей
async def get_user_service(session = Depends(get_connection)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)

@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate, 
    user_service: UserService = Depends(get_user_service)
    ):
    return await user_service.register_user(user)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service) 
    ):
    
    return await user_service.get_user_by_id(user_id)