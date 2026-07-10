from fastapi import APIRouter
from db.mongo import products_collection
from db.mysql import get_connection
from bson import ObjectId 


router = APIRouter()

@router.post("/orders")
async def create_order(orders: dict):
    total = 0
    for item in orders["items"]:
        product = await products_collection.find_one({"_id": ObjectId(item["product_id"])})
        total += product["price"] * item["quantity"]

    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute(
            "INSERT INTO orders (user_id, total) VALUES (%s, %s)",
            (orders["user_id"], total)
        )
        await conn.commit()
        order_id = cur.lastrowid

    for item in orders["items"]:
        product = await products_collection.find_one({"_id": ObjectId(item["product_id"])})    
        async with conn.cursor() as cur:
            sql_now_item = '''
            INSERT INTO order_items (order_id, product_id, product_name, price, quantity) VALUES (%s, %s, %s, %s, %s);'''
            await cur.execute(sql_now_item, (order_id, item["product_id"], product["name"], product["price"], item["quantity"]))
            await conn.commit()
        
    conn.ensure_closed()
    return {"order_id": order_id, "total": total}

@router.get("/stats/top-products")
async def top_products():
    conn = await get_connection()
    async with conn.cursor() as cur:
        await cur.execute('''SELECT product_id, product_name, SUM(quantity) AS top_products FROM order_items GROUP BY product_id, product_name ORDER BY top_products DESC LIMIT 5;''')
        result = await cur.fetchall()
        conn.ensure_closed()
        return result
    
    