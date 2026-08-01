from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Fields shared by input and output."""
    name: str = Field(min_length=1)
    price: Decimal = Field(gt=0, decimal_places=2)   # must be > 0
    stock: int = Field(ge=0)                          # can't be negative


class ProductCreate(ProductBase):
    """What the client sends to CREATE a product (all fields required, no id)."""
    pass


class ProductUpdate(BaseModel):
    """What the client sends to UPDATE — every field optional, change only what you pass."""
    name: str | None = Field(default=None, min_length=1)
    price: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)


class ProductOut(ProductBase):
    """What the API RETURNS (includes the DB-assigned id)."""
    id: int

    model_config = ConfigDict(from_attributes=True)