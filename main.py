from fastapi import FastAPI
from routers import products, users, orders
from db.mysql import create_tables
from contextlib import asynccontextmanager

@asynccontextmanager    # Менеджер контекста
async def lifespan(app: FastAPI):    # Специальный контекстный менеджер события жизненного цикла
    create_tables()    # Код до yield - до запуска приложения
    yield    # Код после yield - после остановки приложения

app = FastAPI(lifespan=lifespan)
app.include_router(products.router)  
app.include_router(users.router)
app.include_router(orders.router)
