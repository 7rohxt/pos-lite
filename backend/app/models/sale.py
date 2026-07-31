from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)

    cashier_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    cashier: Mapped["User"] = relationship(back_populates="sales")

    items: Mapped[list["SaleItem"]] = relationship(
        back_populates="sale", cascade="all, delete-orphan"
    )


class SaleItem(Base):
    __tablename__ = "sale_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # price AT TIME OF SALE

    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"))
    sale: Mapped["Sale"] = relationship(back_populates="items")

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(back_populates="sale_items")