from decimal import Decimal

from datetime import datetime, timezone

from sqlalchemy import select, func   
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.sale import Sale, SaleItem
from app.schemas.sale import SaleItemCreate
from app.core.exceptions import NotFoundError, ConflictError


def create_sale(db: Session, cashier_id: int, items: list[SaleItemCreate]) -> Sale:
    sale = Sale(cashier_id=cashier_id, total=Decimal("0"))
    total = Decimal("0")

    for item in items:
        product = db.get(Product, item.product_id)
        if product is None:
            raise NotFoundError(f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise ConflictError(
                f"Not enough stock for '{product.name}': "
                f"have {product.stock}, requested {item.quantity}"
            )

        # snapshot the price NOW, so the receipt is correct even if price changes later
        sale.items.append(
            SaleItem(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
            )
        )
        total += product.price * item.quantity
        product.stock -= item.quantity      # decrement inventory

    sale.total = total
    db.add(sale)
    db.commit()          # sale + all its items + stock changes commit together
    db.refresh(sale)
    return sale


def list_sales_for_cashier(db: Session, cashier_id: int) -> list[Sale]:
    return list(db.scalars(select(Sale).where(Sale.cashier_id == cashier_id)))


def get_sale(db: Session, sale_id: int) -> Sale | None:
    return db.get(Sale, sale_id)


# Admin Fucntions

def list_all_sales(db: Session) -> list[Sale]:
    return list(db.scalars(select(Sale)))


def delete_sale(db: Session, sale: Sale) -> None:
    db.delete(sale)
    db.commit()

def sales_report_today(db: Session) -> dict:
    start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    count, total = db.execute(
        select(
            func.count(Sale.id),
            func.coalesce(func.sum(Sale.total), 0),   # 0 instead of NULL when no sales
        ).where(Sale.created_at >= start)
    ).one()
    return {"date": start.date(), "sales_count": count, "total_revenue": total}