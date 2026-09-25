from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import order, product, user, auth
from contextlib import asynccontextmanager

@asynccontextmanager   
async def lifespan(app: FastAPI):  
    yield  

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(product.router)  
app.include_router(user.router)
app.include_router(order.router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")