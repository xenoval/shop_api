from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_connection
from models.products import Products
from models.order_items import OrderItems
from models.orders import Orders
from schemas.orders import OrdersCreate, OrdersResponse


router = APIRouter()

@router.post("/orders", response_model=OrdersResponse)
async def create_order(orders: OrdersCreate, db: AsyncSession = Depends(get_connection)):
    total = 0
    products_data = []

    for item in orders.items:
        result = await db.execute(select(Products).where(Products.id == item.product_id))
        product = result.scalar_one_or_none()

        if product is None:
            raise HTTPException(404, f"Товар {item.product_id} не найден")
        total += product.price * item.quantity
        products_data.append({"product": product, "quantity": item.quantity})

    new_order = Orders(user_id=orders.user_id, status="A", total=total)
    db.add(new_order)
    await db.flush()

    for item_data in products_data:
        product = item_data["product"]
        quantity = item_data["quantity"]

        order_item = OrderItems(
            order_id=new_order.id,
            product_id=str(product.id),
            product_name=product.name,
            price=product.price,
            quantity=quantity,
        )
        db.add(order_item)

    await db.commit()
    await db.refresh(new_order)

    return OrdersResponse(order_id=new_order.id, total=new_order.total)

@router.get("/stats/top-products")
async def top_products(db: AsyncSession = Depends(get_connection)):
    stmt = (
        select(
            OrderItems.product_id,
            OrderItems.product_name,
            func.sum(OrderItems.quantity).label("total_quantity"),
        )
        .group_by(OrderItems.product_id, OrderItems.product_name)
        .order_by(func.sum(OrderItems.quantity).desc()). limit(5)
    )

    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            "product_id": row.product_id,
            "product_name": row.product_name,
            "total_quantity": row.total_quantity,
        }
        for row in rows
    ]