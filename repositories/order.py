from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.order import OrderModel
from models.order_item import OrderItemModel

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order_with_items(self, user_id: str, products_data: list) -> OrderModel:
        """Создает заказ."""
        new_order = OrderModel(user_id=user_id, status="A")
        self.session.add(new_order)
        await self.session.flush()

        for item_data in products_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            order_item = OrderItemModel(
                order_id=new_order.id,
                product_id=str(product.id),
                product_name=product.name,
                price=product.price,
                quantity=quantity,
            )
            self.session.add(order_item)

        await self.session.commit()
        await self.session.refresh(new_order)
        return new_order

    async def get_top_products(self, limit: int = 5) -> list:
        """Возвращает топ продаваемых товаров."""
        stmt = (
            select(
                OrderItemModel.product_id,
                OrderItemModel.product_name,
                func.sum(OrderItemModel.quantity).label("total_quantity"),
            )
            .group_by(OrderItemModel.product_id, OrderItemModel.product_name)
            .order_by(func.sum(OrderItemModel.quantity).desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.all())