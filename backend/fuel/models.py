from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FuelLogCreate(BaseModel):
    trip_id: Optional[int] = None
    vehicle_id: int
    driver_id: Optional[int] = None
    liters: float = Field(gt=0)
    cost: float = Field(gt=0)
    odometer: float = Field(ge=0)
    station: str
    timestamp: Optional[datetime] = None

class FuelLogUpdate(BaseModel):
    trip_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None
    liters: Optional[float] = Field(default=None, gt=0)
    cost: Optional[float] = Field(default=None, gt=0)
    odometer: Optional[float] = Field(default=None, ge=0)
    station: Optional[str] = None
    timestamp: Optional[datetime] = None

class FuelLogResponse(BaseModel):
    id: int
    trip_id: Optional[int]
    vehicle_id: int
    driver_id: Optional[int]
    liters: float
    cost: float
    odometer: float
    station: str
    timestamp: datetime
    
    class Config:
        from_attributes = True
