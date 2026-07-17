# routers/__init__.py
from routers.users import router as users_router
from routers.products import router as products_router
from routers.orders import router as orders_router

__all__ = ['users_router', 'products_router', 'orders_router']