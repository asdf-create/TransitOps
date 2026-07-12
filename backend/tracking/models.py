from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class VehicleLocation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    vehicle_id: int
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    speed: Optional[float] = Field(default=None, ge=0)
    heading: Optional[float] = Field(default=None, ge=0, le=360)

class LocationUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    vehicle_id: int
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    speed: Optional[float] = Field(default=None, ge=0)
    heading: Optional[float] = Field(default=None, ge=0, le=360)

class VehicleLocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    vehicle_id: int
    registration_number: str
    latitude: float
    longitude: float
    speed: Optional[float]
    heading: Optional[float]
    status: str
