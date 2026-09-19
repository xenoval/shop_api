from uuid import UUID
from fastapi import HTTPException, status
from repositories.product import ProductRepository
from schemas.product import ProductCreate, PagedProducts
from models.product import ProductModel

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def register_product(self, product_data: ProductCreate) -> ProductModel:
        return await self.product_repo.create(product_data)

    async def get_product_by_id(self, product_id: UUID) -> ProductModel:
        """Получает продукт по ID или генерирует 404 ошибку."""
        product = await self.product_repo.get_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Продукт не найден"
            )
            
        return product

    async def get_products_list(self, limit: int, offset: int) -> PagedProducts:
        """Получает пагинированный список продуктов."""
        products, total = await self.product_repo.get_paged_products(limit=limit, offset=offset)
        
        return PagedProducts(
            items=products,
            limit=limit,
            offset=offset,
            total=total,
        )