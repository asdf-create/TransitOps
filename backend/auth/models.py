from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role_id: int
    phone: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role_id: int
    phone: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
