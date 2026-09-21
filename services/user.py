from uuid import UUID
from fastapi import HTTPException, status
from repositories.user import UserRepository
from schemas.user import UserCreate
from models.user import UserModel
from auth.security import get_password_hash

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> UserModel:
        existing = await self.user_repo.get_by_email(user_data.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email уже занят")

        hashed = get_password_hash(user_data.password)

        return await self.user_repo.create(user_data, hashed)

    async def get_user_by_id(self, user_id: UUID) -> UserModel:
        """Получает пользователя по ID или генерирует 404 ошибку."""
        user = await self.user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Пользователь не найден"
            )
            
        return user