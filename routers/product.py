from uuid import UUID
from fastapi import APIRouter, Depends

from db.postgres import get_connection
from repositories.product import ProductRepository
from services.product import ProductService
from schemas.product import ProductResponse, PagedProducts, ProductCreate


router = APIRouter()


# Функция, которая собирает цепочку зависимостей
async def get_product_service(session = Depends(get_connection)) -> ProductService:
    repo = ProductRepository(session)
    return ProductService(repo)

@router.post("/products", response_model=ProductResponse)
async def create_product(
    product: ProductCreate, 
    product_service: ProductService = Depends(get_product_service)
    ):
    return await product_service.register_product(product)

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    product_service: ProductService = Depends(get_product_service) 
    ):
    
    return await product_service.get_product_by_id(product_id)

@router.get("/products", response_model=PagedProducts)
async def get_products(
    limit: int = 50, 
    offset: int = 0, 
    product_service: ProductService = Depends(get_product_service)
):
    return await product_service.get_products_list(limit=limit, offset=offset)

