from decimal import Decimal

from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))   # money → Numeric, not Float
    stock: Mapped[int] = mapped_column(Integer, default=0)

    sale_items: Mapped[list["SaleItem"]] = relationship(back_populates="product")