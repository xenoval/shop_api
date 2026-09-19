# routers/__init__.py
from routers.user import router as users_router
from routers.product import router as products_router
from routers.order import router as orders_router

__all__ = ['users_router', 'products_router', 'orders_router']