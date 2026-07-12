from sqlmodel import Field, SQLModel, Relationship, Text
from datetime import datetime, timezone
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMINISTRATOR = "Administrator"
    FLEET_MANAGER = "Fleet Manager"
    DISPATCHER = "Dispatcher"
    DRIVER = "Driver"
    SAFETY_OFFICER = "Safety Officer"
    FINANCIAL_ANALYST = "Financial Analyst"

class VehicleStatus(str, Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    IN_SHOP = "In Shop"
    RETIRED = "Retired"

class DriverStatus(str, Enum):
    AVAILABLE = "Available"
    ON_TRIP = "On Trip"
    OFF_DUTY = "Off Duty"
    SUSPENDED = "Suspended"

class TripStatus(str, Enum):
    DRAFT = "Draft"
    DISPATCHED = "Dispatched"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class MaintenanceStatus(str, Enum):
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    role_id: int = Field(foreign_key="role.id")
    phone: Optional[str] = None
    avatar: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None
    is_active: bool = True

class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None

class Vehicle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    registration_number: str = Field(unique=True, index=True)
    model: str
    manufacturer: str
    vehicle_type: str = Field(index=True)
    year: int
    vin: Optional[str] = None
    fuel_type: str
    max_load_capacity: float = Field(gt=0)
    acquisition_cost: float
    odometer: float = Field(default=0, ge=0)
    insurance_expiry: Optional[datetime] = None
    registration_expiry: Optional[datetime] = None
    status: VehicleStatus = Field(default=VehicleStatus.AVAILABLE, index=True)
    mileage: float = Field(default=0)
    region: str = Field(index=True)
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Driver(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(index=True)
    license_number: str = Field(unique=True, index=True)
    license_category: str
    license_expiry: datetime
    phone: str
    emergency_contact: Optional[str] = None
    safety_score: float = Field(default=100, ge=0, le=100)
    years_experience: int = Field(default=0, ge=0)
    assigned_region: str = Field(index=True)
    status: DriverStatus = Field(default=DriverStatus.AVAILABLE, index=True)
    total_trips: int = Field(default=0)
    total_distance: float = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tracking_id: str = Field(unique=True, index=True)
    source: str
    destination: str
    vehicle_id: int = Field(foreign_key="vehicle.id", index=True)
    driver_id: int = Field(foreign_key="driver.id", index=True)
    cargo_description: str
    cargo_weight: float = Field(gt=0)
    planned_distance: float
    actual_distance: Optional[float] = None
    planned_duration: int
    actual_duration: Optional[int] = None
    estimated_arrival: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    planned_departure: datetime
    actual_departure: Optional[datetime] = None
    revenue: float
    status: TripStatus = Field(default=TripStatus.DRAFT, index=True)
    route_geometry: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    
    vehicle_name: Optional[str] = None
    driver_name: Optional[str] = None
    vehicle_registration: Optional[str] = None
    driver_license_number: Optional[str] = None

class MaintenanceLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle_id: int = Field(foreign_key="vehicle.id", index=True)
    maintenance_type: str
    description: str = Field(sa_type=Text)
    scheduled_date: datetime
    started_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    estimated_cost: float
    actual_cost: Optional[float] = None
    predicted_completion: Optional[datetime] = None
    status: MaintenanceStatus = Field(default=MaintenanceStatus.SCHEDULED, index=True)
    mechanic_notes: Optional[str] = Field(sa_type=Text)

class FuelLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: Optional[int] = Field(foreign_key="trip.id")
    vehicle_id: int = Field(foreign_key="vehicle.id", index=True)
    driver_id: Optional[int] = Field(foreign_key="driver.id")
    liters: float = Field(gt=0)
    cost: float
    odometer: float = Field(ge=0)
    station: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle_id: Optional[int] = Field(foreign_key="vehicle.id", index=True)
    trip_id: Optional[int] = Field(foreign_key="trip.id")
    category: str
    amount: float = Field(gt=0)
    description: str
    expense_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str
    message: str = Field(sa_type=Text)
    priority: Priority = Field(default=Priority.MEDIUM)
    category: str
    read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EmailLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(foreign_key="trip.id", index=True)
    recipient_email: str
    subject: str
    body_html: str = Field(sa_type=Text)
    sent_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
