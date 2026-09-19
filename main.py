from fastapi import FastAPI
from routers import order, product, user
from db.postgres import create_tables
from contextlib import asynccontextmanager

@asynccontextmanager    # Менеджер контекста
async def lifespan(app: FastAPI):    # Специальный контекстный менеджер события жизненного цикла
    await create_tables()    # Код до yield - до запуска приложения
    yield    # Код после yield - после остановки приложения

app = FastAPI(lifespan=lifespan)
app.include_router(product.router)  
app.include_router(user.router)
app.include_router(order.router)
