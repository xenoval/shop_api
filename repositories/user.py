from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import UserModel
from schemas.user import UserCreate  

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_data: UserCreate) -> UserModel:
        """Создает пользователя в базе данных."""
        new_user = UserModel(
            email=user_data.email,
            name=user_data.name
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def get_by_id(self, user_id: UUID) -> UserModel | None:
        """Ищет пользователя в БД по его UUID."""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()