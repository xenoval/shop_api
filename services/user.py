from uuid import UUID
from fastapi import HTTPException, status
from repositories.user import UserRepository
from schemas.user import UserCreate
from models.user import UserModel

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> UserModel:
        """Бизнес-логика регистрации нового пользователя."""
        # Пример бизнес-логики: проверка уникальности email
        # (представим, что у репозитория есть метод get_by_email)
        # existing_user = await self.user_repo.get_by_email(user_data.email)
        # if existing_user:
        #     raise HTTPException(status_code=400, detail="Email уже занят")

        # Если всё ок — отдаем задачу репозиторию
        return await self.user_repo.create(user_data)

    async def get_user_by_id(self, user_id: UUID) -> UserModel:
        """Получает пользователя по ID или генерирует 404 ошибку."""
        user = await self.user_repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Пользователь не найден"
            )
            
        return user