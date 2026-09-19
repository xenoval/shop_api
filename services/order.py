from fastapi import HTTPException, status
from repositories.order import OrderRepository
from repositories.product import ProductRepository
from schemas.order import OrdersCreate, OrdersResponse

class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def place_order(self, orders_data: OrdersCreate) -> OrdersResponse:
        """Бизнес-логика создания заказа."""
        total = 0
        products_data = []

        # Проверяем существование товаров и их цены
        for item in orders_data.items:
            product = await self.product_repo.get_by_id(item.product_id)

            if product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Товар {item.product_id} не найден"
                )
            
            # Считаем total для ответа
            total += product.price * item.quantity
            products_data.append({"product": product, "quantity": item.quantity})

        new_order = await self.order_repo.create_order_with_items(
            user_id=orders_data.user_id,
            products_data=products_data
        )

        return OrdersResponse(order_id=new_order.id, total=total)

    async def get_top_selling_products(self) -> list[dict]:
        """Возвращает топ товаров."""
        rows = await self.order_repo.get_top_products(limit=5)
        return [
            {
                "product_id": row.product_id,
                "product_name": row.product_name,
                "total_quantity": row.total_quantity,
            }
            for row in rows
        ]