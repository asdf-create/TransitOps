from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

class UserLogin(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    full_name: str
    email: EmailStr
    password: str
    role_id: int
    phone: Optional[str] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: str
    role_id: int
    phone: Optional[str]
    is_active: bool

class TokenResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
