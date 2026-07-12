from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from database.models import DriverStatus

class DriverCreate(BaseModel):
    full_name: str
    license_number: str
    license_category: str
    license_expiry: datetime
    phone: str
    emergency_contact: Optional[str] = None
    safety_score: float = Field(default=100, ge=0, le=100)
    years_experience: int = Field(default=0, ge=0)
    assigned_region: str
    status: DriverStatus = DriverStatus.AVAILABLE

class DriverUpdate(BaseModel):
    full_name: Optional[str] = None
    license_number: Optional[str] = None
    license_category: Optional[str] = None
    license_expiry: Optional[datetime] = None
    phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    safety_score: Optional[float] = Field(default=None, ge=0, le=100)
    years_experience: Optional[int] = Field(default=None, ge=0)
    assigned_region: Optional[str] = None
    status: Optional[DriverStatus] = None

class DriverResponse(BaseModel):
    id: int
    full_name: str
    license_number: str
    license_category: str
    license_expiry: datetime
    phone: str
    emergency_contact: Optional[str]
    safety_score: float
    years_experience: int
    assigned_region: str
    status: DriverStatus
    total_trips: int
    total_distance: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
