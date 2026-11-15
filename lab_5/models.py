from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=18, le=120)
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr | None = None
    age: int | None = Field(None, ge=18, le=120)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    created_at: datetime
