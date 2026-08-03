from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleOut
from app.services import sale as sale_service

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("", response_model=SaleOut, status_code=201)
def create_sale(payload: SaleCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return sale_service.create_sale(db, cashier_id=current_user.id, items=payload.items)


@router.get("", response_model=list[SaleOut])
def list_my_sales(db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    return sale_service.list_sales_for_cashier(db, current_user.id)


@router.get("/{sale_id}", response_model=SaleOut)
def get_sale(sale_id: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    sale = sale_service.get_sale(db, sale_id)
    if sale is None or sale.cashier_id != current_user.id:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale