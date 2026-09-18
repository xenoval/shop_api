from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_connection
from models.products import Products
from schemas.products import ProductResponse, PagedProducts, ProductCreate


router = APIRouter()


@router.post("/products", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_connection)):
    new_product = Products(
        name=product.name,
        description=product.description,
        price=product.price
    )

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@router.get("/products", response_model=PagedProducts)
async def get_products(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_connection)):
    total_result = await db.execute(select(func.count()).select_from(Products))
    total = total_result.scalar()
    products_result = await db.execute(select(Products).offset(offset * limit).limit(limit))
    products = products_result.scalars().all()

    return PagedProducts(
        items=products,
        limit=limit,
        offset=offset,
        total=total,
    )

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_connection)):
    result = await db.execute(select(Products).where(Products.id == product_id))
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    return product