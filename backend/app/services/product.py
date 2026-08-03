from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def list_products(db: Session, search: str | None = None) -> list[Product]:
    query = select(Product)
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    return list(db.scalars(query))


def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def create_product(db: Session, payload: ProductCreate) -> Product:
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, payload: ProductUpdate) -> Product:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()


def low_stock_products(db: Session, threshold: int) -> list[Product]:
    return list(db.scalars(select(Product).where(Product.stock <= threshold)))