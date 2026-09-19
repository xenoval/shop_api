from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import ProductModel
from schemas.product import ProductCreate

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product: ProductCreate) -> ProductModel:
        """Создает продукт в базе данных."""
        new_product = ProductModel(
                name=product.name,
                description=product.description,
                price=product.price
            )
        
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product

    async def get_by_id(self, product_id: UUID) -> ProductModel | None:
        """Ищет продукт в БД по его UUID."""
        query = select(ProductModel).where(ProductModel.id == product_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_paged_products(self, limit: int, offset: int) -> tuple[list[ProductModel], int]:
        """Возвращает список продуктов для текущей страницы и общее количество записей."""
        total_query = select(func.count()).select_from(ProductModel)
        total_result = await self.session.execute(total_query)
        total = total_result.scalar() or 0

        products_query = select(ProductModel).offset(offset * limit).limit(limit)
        products_result = await self.session.execute(products_query)
        products = list(products_result.scalars().all())

        return products, total