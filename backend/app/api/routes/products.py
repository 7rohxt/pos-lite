from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services import product as product_service

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_current_user)],   # every product route now needs a token
)


@router.get("", response_model=list[ProductOut])
def list_products(search: str | None = None, db: Session = Depends(get_db)):
    return product_service.list_products(db, search=search)


@router.post("", response_model=ProductOut, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db),
                   _: object = Depends(require_admin)):
    return product_service.create_product(db, payload)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db),
                   _: object = Depends(require_admin)):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_service.update_product(db, product, payload)


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db),
                   _: object = Depends(require_admin)):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product_service.delete_product(db, product)