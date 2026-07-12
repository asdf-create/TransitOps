from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from database.models import MaintenanceStatus

class MaintenanceCreate(BaseModel):
    vehicle_id: int
    maintenance_type: str
    description: str
    scheduled_date: datetime
    estimated_cost: float = Field(gt=0)
    mechanic_notes: Optional[str] = None

class MaintenanceUpdate(BaseModel):
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    started_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    estimated_cost: Optional[float] = Field(default=None, gt=0)
    actual_cost: Optional[float] = Field(default=None, ge=0)
    predicted_completion: Optional[datetime] = None
    status: Optional[MaintenanceStatus] = None
    mechanic_notes: Optional[str] = None

class MaintenanceResponse(BaseModel):
    id: int
    vehicle_id: int
    maintenance_type: str
    description: str
    scheduled_date: datetime
    started_date: Optional[datetime]
    completed_date: Optional[datetime]
    estimated_cost: float
    actual_cost: Optional[float]
    predicted_completion: Optional[datetime]
    status: MaintenanceStatus
    mechanic_notes: Optional[str]
    
    class Config:
        from_attributes = True
