from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class SalesReport(BaseModel):
    date: date
    sales_count: int
    total_revenue: Decimal