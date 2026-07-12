from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class DelayPredictionRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    vehicle_id: int
    driver_id: int
    source: str
    destination: str
    planned_distance: float
    planned_duration: int
    departure_time: Optional[datetime] = None

class DelayPredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    predicted_delay_minutes: int
    delay_probability: float
    delay_factors: List[str]
    confidence: float
    on_time_probability: float

class ETAEstimationRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    vehicle_id: int
    driver_id: int
    source: str
    destination: str
    current_location_lat: float
    current_location_lon: float
    destination_lat: float
    destination_lon: float

class ETAEstimationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    estimated_arrival: datetime
    estimated_duration_minutes: int
    confidence: float
    traffic_factor: float
    weather_factor: float

class DriverRecommendationRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    trip_distance: float
    trip_duration: int
    cargo_weight: float
    source: str
    destination: str
    required_skills: Optional[List[str]] = None

class DriverRecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    recommended_drivers: List[dict]
    reasoning: str

class VehicleRecommendationRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    cargo_weight: float
    cargo_type: str
    trip_distance: float
    source: str
    destination: str
    special_requirements: Optional[List[str]] = None

class VehicleRecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    recommended_vehicles: List[dict]
    reasoning: str