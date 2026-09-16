from fastapi import APIRouter, Depends
from db.mongo import products_collection
from db.postgres import get_connection
from bson import ObjectId 
from sqlalchemy.orm import Session
from sqlalchemy import text
from models.order_items import OrderItems
from models.orders import Orders
from schemas.orders import CreateOrders, OrdersResponse
import asyncio


router = APIRouter()

@router.post("/orders", response_model=OrdersResponse)
async def create_order(orders: CreateOrders, db: Session = Depends(get_connection)):
    total = 0
    products_data = []

    for item in orders.items:
        product = await products_collection.find_one({"_id": ObjectId(item.product_id)})
        total += product["price"] * item.quantity
        products_data.append({
            "product": product,
            "quantity": item.quantity
        })

    def create_order_in_db(products_data, total, user_id):
        new_order = Orders(
            user_id=user_id,
            status='A',
            total=total
        )
        db.add(new_order)
        db.flush()

        for item_data in products_data:
            product = item_data["product"]
            quantity = item_data["quantity"]

            order_item = OrderItems(
                order_id=new_order.id,
                product_id=str(product["_id"]),
                product_name=product["name"],
                price=product["price"],
                quantity=quantity
            )
            db.add(order_item)
    
        db.commit()
        db.refresh(new_order)
        return new_order.id, total
        
    order_id, total = await asyncio.to_thread(
        create_order_in_db,
        products_data,
        total,
        orders.user_id
    )

    return OrdersResponse(
        order_id=order_id,
        total=total
    )

@router.get("/stats/top-products")
def top_products(db: Session = Depends(get_connection)):
    query = text('''
        SELECT product_id, product_name, SUM(quantity) AS total_quantity 
        FROM order_items 
        GROUP BY product_id, product_name 
        ORDER BY total_quantity DESC 
        LIMIT 5
    ''')
    
    result = db.execute(query).fetchall()
    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "total_quantity": row[2]
        }
        for row in result
    ]