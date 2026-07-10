from fastapi import APIRouter
from db.mongo import products_collection
from bson import ObjectId


def serialize_product(product):
    product["_id"] = str(product["_id"])
    return product

router = APIRouter()

@router.post("/products")
async def create_product(product: dict):
    res = await products_collection.insert_one(product)
    return {"id": str(res.inserted_id)}

@router.get("/products")
async def get_products():
    products = await products_collection.find().to_list(length=100)
    return [serialize_product(p) for p in products]

@router.get("/products/{product_id}")
async def get_product(product_id: str):
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    return serialize_product(product)