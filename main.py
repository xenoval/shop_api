from fastapi import FastAPI
from routers import products, users, orders
from db.mysql import create_tables


app = FastAPI()
app.include_router(products.router)  #  Подключает отдельный модуль с маршрутами (роутерами)
app.include_router(users.router)
app.include_router(orders.router)

@app.on_event("startup")
async def create():
    await create_tables()