from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.database import get_db
from app.schemas.user import UserOut
from app.schemas.sale import SaleOut
from app.services import user as user_service
from app.services import sale as sale_service

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],   # every admin route requires is_admin
)


@router.get("/users", response_model=list[UserOut])
def list_all_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.get("/sales", response_model=list[SaleOut])
def list_all_sales(db: Session = Depends(get_db)):
    return sale_service.list_all_sales(db)


@router.delete("/sales/{sale_id}", status_code=204)
def delete_any_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = sale_service.get_sale(db, sale_id)
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    sale_service.delete_sale(db, sale)