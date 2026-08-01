from fastapi import APIRouter

from app.api.routes import products, auth

api_router = APIRouter()

api_router.include_router(products.router)
api_router.include_router(auth.router)
# api_router.include_router(sales.router)   # later
# api_router.include_router(admin.router)   # later