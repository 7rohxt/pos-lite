from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.sale import Sale, SaleItem
from app.schemas.sale import SaleItemCreate


def create_sale(db: Session, cashier_id: int, items: list[SaleItemCreate]) -> Sale:
    sale = Sale(cashier_id=cashier_id, total=Decimal("0"))
    total = Decimal("0")

    for item in items:
        product = db.get(Product, item.product_id)
        if product is None:
            raise ValueError(f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise ValueError(
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