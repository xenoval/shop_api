from fastapi import APIRouter, Depends
from db.postgres import get_connection

from repositories.order import OrderRepository
from repositories.product import ProductRepository
from services.order import OrderService
from schemas.order import OrdersCreate, OrdersResponse

router = APIRouter()

async def get_order_service(session = Depends(get_connection)) -> OrderService:
    order_repo = OrderRepository(session)
    product_repo = ProductRepository(session)
    return OrderService(order_repo=order_repo, product_repo=product_repo)

@router.post("/orders", response_model=OrdersResponse)
async def create_order(
    orders: OrdersCreate, 
    order_service: OrderService = Depends(get_order_service)
):
    return await order_service.place_order(orders)

@router.get("/stats/top-products")
async def top_products(
    order_service: OrderService = Depends(get_order_service)
):
    return await order_service.get_top_selling_products()