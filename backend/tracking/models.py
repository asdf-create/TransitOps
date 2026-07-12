from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

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

class TrackingDetailResponse(BaseModel):
    tracking_id: str
    latitude: float
    longitude: float
    progress_percentage: float
    current_speed: float
    remaining_distance: float
    estimated_arrival: Optional[datetime]
    current_status: str
    driver_name: str
    vehicle_registration: str
    vehicle_name: str
    source: str
    destination: str
    revenue: float

class TrackingTimelineEvent(BaseModel):
    status: str
    description: str
    timestamp: datetime

class TrackingTimelineResponse(BaseModel):
    tracking_id: str
    events: List[TrackingTimelineEvent]

class RouteGeometryResponse(BaseModel):
    tracking_id: str
    route_geometry: Optional[str]
    coordinates: List[List[float]]  # GeoJSON style List of [lng, lat]
