from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleItemCreate(BaseModel):
    """One line the client wants to sell: which product, how many."""
    product_id: int
    quantity: int = Field(gt=0)


class SaleCreate(BaseModel):
    """A sale is a list of line items. Price/total come from the server, not the client."""
    items: list[SaleItemCreate] = Field(min_length=1)


class SaleItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class SaleOut(BaseModel):
    id: int
    created_at: datetime
    total: Decimal
    cashier_id: int
    items: list[SaleItemOut]

    model_config = ConfigDict(from_attributes=True)