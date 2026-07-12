from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from database.models import TripStatus

class TripCreate(BaseModel):
    source: str
    destination: str
    vehicle_id: int
    driver_id: int
    cargo_description: str
    cargo_weight: float = Field(gt=0)
    planned_distance: float = Field(gt=0)
    planned_duration: int = Field(gt=0)
    planned_departure: datetime
    revenue: float = Field(gt=0)

class TripUpdate(BaseModel):
    source: Optional[str] = None
    destination: Optional[str] = None
    cargo_description: Optional[str] = None
    cargo_weight: Optional[float] = Field(default=None, gt=0)
    planned_distance: Optional[float] = Field(default=None, gt=0)
    actual_distance: Optional[float] = Field(default=None, ge=0)
    planned_duration: Optional[int] = Field(default=None, gt=0)
    actual_duration: Optional[int] = Field(default=None, ge=0)
    estimated_arrival: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    planned_departure: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    revenue: Optional[float] = Field(default=None, gt=0)
    status: Optional[TripStatus] = None

class TripResponse(BaseModel):
    id: int
    tracking_id: str
    source: str
    destination: str
    vehicle_id: int
    driver_id: int
    cargo_description: str
    cargo_weight: float
    planned_distance: float
    actual_distance: Optional[float]
    planned_duration: int
    actual_duration: Optional[int]
    estimated_arrival: Optional[datetime]
    actual_arrival: Optional[datetime]
    planned_departure: datetime
    actual_departure: Optional[datetime]
    revenue: float
    status: TripStatus
    route_geometry: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    vehicle_name: Optional[str]
    driver_name: Optional[str]
    vehicle_registration: Optional[str]
    driver_license_number: Optional[str]
    
    class Config:
        from_attributes = True
