from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class ExpenseCategory(str, Enum):
    FUEL = "Fuel"
    MAINTENANCE = "Maintenance"
    TOLL = "Toll"
    PARKING = "Parking"
    INSURANCE = "Insurance"
    REGISTRATION = "Registration"
    REPAIRS = "Repairs"
    MISCELLANEOUS = "Miscellaneous"

class ExpenseCreate(BaseModel):
    vehicle_id: Optional[int] = None
    trip_id: Optional[int] = None
    category: ExpenseCategory
    amount: float = Field(gt=0)
    description: str
    expense_date: Optional[datetime] = None

class ExpenseUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    trip_id: Optional[int] = None
    category: Optional[ExpenseCategory] = None
    amount: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = None
    expense_date: Optional[datetime] = None

class ExpenseResponse(BaseModel):
    id: int
    vehicle_id: Optional[int]
    trip_id: Optional[int]
    category: ExpenseCategory
    amount: float
    description: str
    expense_date: datetime
    
    class Config:
        from_attributes = True
