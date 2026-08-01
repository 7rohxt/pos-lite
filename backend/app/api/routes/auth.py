from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.database import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserOut
from app.services import user as user_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if user_service.get_user_by_username(db, payload.username) is not None:
        raise HTTPException(status_code=400, detail="Username already taken")
    return user_service.create_user(db, payload)


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.username, "id": user.id})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user