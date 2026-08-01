from fastapi import APIRouter

from app.api.routes import products

api_router = APIRouter()

api_router.include_router(products.router)
# Register new resources here — main.py never changes:
# api_router.include_router(sales.router)
# api_router.include_router(auth.router)
# api_router.include_router(admin.router)