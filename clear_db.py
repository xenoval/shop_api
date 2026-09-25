from models.base import Base
from db.postgres import engine
import asyncio

async def clear_database():
    print("Удаление всех таблиц...")
    # Открываем асинхронное соединение и запускаем синхронную команду внутри run_sync
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("Готово!")

if __name__ == "__main__":
    asyncio.run(clear_database())