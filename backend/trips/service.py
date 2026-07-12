from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime, timedelta, timezone
import random
import string

from database.models import Trip, Vehicle, Driver, VehicleStatus, DriverStatus, TripStatus
from trips.models import TripCreate, TripUpdate

class TripService:
    def __init__(self, session: Session):
        self.session = session

    def generate_tracking_id(self) -> str:
        return f"TRK-{''.join(random.choices(string.digits, k=4))}"

    def create_trip(self, trip_data: TripCreate) -> Trip:
        # Validate vehicle
        vehicle = self.session.get(Vehicle, trip_data.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")
        
        # Business Rule: Retired or In Shop vehicles cannot be dispatched
        if vehicle.status in [VehicleStatus.RETIRED, VehicleStatus.IN_SHOP]:
            raise ValueError(f"Vehicle is {vehicle.status} and cannot be dispatched")
        
        # Business Rule: Vehicle already on trip cannot be assigned
        if vehicle.status == VehicleStatus.ON_TRIP:
            raise ValueError("Vehicle is already on a trip")
        
        # Business Rule: Cargo weight must not exceed vehicle capacity
        if trip_data.cargo_weight > vehicle.max_load_capacity:
            raise ValueError(f"Cargo weight ({trip_data.cargo_weight}) exceeds vehicle capacity ({vehicle.max_load_capacity})")
        
        # Validate driver
        driver = self.session.get(Driver, trip_data.driver_id)
        if not driver:
            raise ValueError("Driver not found")
        
        # Business Rule: Suspended drivers cannot be assigned
        if driver.status == DriverStatus.SUSPENDED:
            raise ValueError("Driver is suspended and cannot be assigned")
        
        # Business Rule: Expired license check
        if driver.license_expiry < datetime.now(timezone.utc):
            raise ValueError("Driver's license has expired")
        
        # Business Rule: Driver already on trip cannot be assigned
        if driver.status == DriverStatus.ON_TRIP:
            raise ValueError("Driver is already on a trip")
        
        # Create trip with historical snapshots
        tracking_id = self.generate_tracking_id()
        estimated_arrival = trip_data.planned_departure + timedelta(minutes=trip_data.planned_duration)
        
        db_trip = Trip(
            tracking_id=tracking_id,
            source=trip_data.source,
            destination=trip_data.destination,
            vehicle_id=trip_data.vehicle_id,
            driver_id=trip_data.driver_id,
            cargo_description=trip_data.cargo_description,
            cargo_weight=trip_data.cargo_weight,
            planned_distance=trip_data.planned_distance,
            planned_duration=trip_data.planned_duration,
            planned_departure=trip_data.planned_departure,
            estimated_arrival=estimated_arrival,
            revenue=trip_data.revenue,
            status=TripStatus.DRAFT,
            # Historical snapshots
            vehicle_name=f"{vehicle.manufacturer} {vehicle.model}",
            driver_name=driver.full_name,
            vehicle_registration=vehicle.registration_number,
            driver_license_number=driver.license_number
        )
        
        self.session.add(db_trip)
        self.session.commit()
        self.session.refresh(db_trip)
        return db_trip

    def dispatch_trip(self, trip_id: int) -> Optional[Trip]:
        trip = self.session.get(Trip, trip_id)
        if not trip:
            return None
        
        if trip.status != TripStatus.DRAFT:
            raise ValueError("Only draft trips can be dispatched")
        
        # Business Rule: Dispatching changes vehicle and driver status to On Trip
        vehicle = self.session.get(Vehicle, trip.vehicle_id)
        driver = self.session.get(Driver, trip.driver_id)
        
        vehicle.status = VehicleStatus.ON_TRIP
        driver.status = DriverStatus.ON_TRIP
        
        trip.status = TripStatus.DISPATCHED
        trip.actual_departure = datetime.now(timezone.utc)
        
        self.session.add(vehicle)
        self.session.add(driver)
        self.session.add(trip)
        self.session.commit()
        self.session.refresh(trip)
        return trip

    def complete_trip(self, trip_id: int, actual_distance: float, actual_duration: int) -> Optional[Trip]:
        trip = self.session.get(Trip, trip_id)
        if not trip:
            return None
        
        if trip.status != TripStatus.DISPATCHED:
            raise ValueError("Only dispatched trips can be completed")
        
        # Business Rule: Completing trip changes vehicle and driver status back to Available
        vehicle = self.session.get(Vehicle, trip.vehicle_id)
        driver = self.session.get(Driver, trip.driver_id)
        
        vehicle.status = VehicleStatus.AVAILABLE
        driver.status = DriverStatus.AVAILABLE
        
        # Update trip data
        trip.status = TripStatus.COMPLETED
        trip.actual_distance = actual_distance
        trip.actual_duration = actual_duration
        trip.actual_arrival = datetime.now(timezone.utc)
        trip.completed_at = datetime.now(timezone.utc)
        
        # Update vehicle odometer
        vehicle.odometer += actual_distance
        vehicle.mileage += actual_distance
        
        # Update driver stats
        driver.total_trips += 1
        driver.total_distance += actual_distance
        
        self.session.add(vehicle)
        self.session.add(driver)
        self.session.add(trip)
        self.session.commit()
        self.session.refresh(trip)
        return trip

    def cancel_trip(self, trip_id: int) -> Optional[Trip]:
        trip = self.session.get(Trip, trip_id)
        if not trip:
            return None
        
        if trip.status not in [TripStatus.DRAFT, TripStatus.DISPATCHED]:
            raise ValueError("Only draft or dispatched trips can be cancelled")
        
        # Business Rule: Cancelling restores vehicle and driver to Available
        if trip.status == TripStatus.DISPATCHED:
            vehicle = self.session.get(Vehicle, trip.vehicle_id)
            driver = self.session.get(Driver, trip.driver_id)
            
            vehicle.status = VehicleStatus.AVAILABLE
            driver.status = DriverStatus.AVAILABLE
            
            self.session.add(vehicle)
            self.session.add(driver)
        
        trip.status = TripStatus.CANCELLED
        
        self.session.add(trip)
        self.session.commit()
        self.session.refresh(trip)
        return trip

    def get_trip(self, trip_id: int) -> Optional[Trip]:
        return self.session.get(Trip, trip_id)

    def get_trips(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[TripStatus] = None,
        vehicle_id: Optional[int] = None,
        driver_id: Optional[int] = None
    ) -> List[Trip]:
        query = select(Trip)
        
        if status:
            query = query.where(Trip.status == status)
        if vehicle_id:
            query = query.where(Trip.vehicle_id == vehicle_id)
        if driver_id:
            query = query.where(Trip.driver_id == driver_id)
            
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def get_trip_by_tracking_id(self, tracking_id: str) -> Optional[Trip]:
        return self.session.exec(
            select(Trip).where(Trip.tracking_id == tracking_id)
        ).first()
