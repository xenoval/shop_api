from fastapi import APIRouter
from bson import ObjectId
from fastapi import HTTPException
from schemas.schemas_products import Product, ProductCreate, PagedProducts


from db.mongo import products_collection

router = APIRouter()

@router.post("/products", response_model=Product)
async def create_product(product: ProductCreate):
    res = await products_collection.insert_one(product.model_dump())
    return Product(
        _id=str(res.inserted_id),
        **product.model_dump(),
    )


@router.get("/products", response_model=PagedProducts)
async def get_products(limit: int = 50, offcet: int = 0):
    total = await products_collection.count_documents({})
    products = await products_collection.find().skip(offcet * limit).limit(limit).to_list()
    return PagedProducts(
        items=[Product.model_validate(product) for product  in products],
        limit=limit,
        offcet=offcet,
        total=total,
    )

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Неверный формат входных данных!")
    
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    
    return Product.model_validate(product)