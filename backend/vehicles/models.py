from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from database.models import VehicleStatus

class VehicleCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    registration_number: str
    model: str
    manufacturer: str
    vehicle_type: str
    year: int
    vin: Optional[str] = None
    fuel_type: str
    max_load_capacity: float = Field(gt=0)
    acquisition_cost: float
    odometer: float = Field(default=0, ge=0)
    insurance_expiry: Optional[datetime] = None
    registration_expiry: Optional[datetime] = None
    status: VehicleStatus = VehicleStatus.AVAILABLE
    region: str
    notes: Optional[str] = None

class VehicleUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    vehicle_type: Optional[str] = None
    year: Optional[int] = None
    vin: Optional[str] = None
    fuel_type: Optional[str] = None
    max_load_capacity: Optional[float] = Field(default=None, gt=0)
    acquisition_cost: Optional[float] = None
    odometer: Optional[float] = Field(default=None, ge=0)
    insurance_expiry: Optional[datetime] = None
    registration_expiry: Optional[datetime] = None
    status: Optional[VehicleStatus] = None
    region: Optional[str] = None
    notes: Optional[str] = None

class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    registration_number: str
    model: str
    manufacturer: str
    vehicle_type: str
    year: int
    vin: Optional[str]
    fuel_type: str
    max_load_capacity: float
    acquisition_cost: float
    odometer: float
    insurance_expiry: Optional[datetime]
    registration_expiry: Optional[datetime]
    status: VehicleStatus
    mileage: float
    region: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
