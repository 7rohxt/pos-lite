from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """What a client sends to register."""
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)   # 72 = bcrypt's limit


class UserOut(BaseModel):
    """What the API returns — NEVER includes the password hash."""
    id: int
    username: str
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)