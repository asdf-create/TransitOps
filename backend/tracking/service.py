from sqlmodel import Session, select
from typing import Optional, List

from database.models import Vehicle, Trip, VehicleStatus, TripStatus
from tracking.models import VehicleLocation, LocationUpdate, VehicleLocationResponse

class TrackingService:
    def __init__(self, session: Session):
        self.session = session

    def update_vehicle_location(self, location_data: LocationUpdate) -> VehicleLocationResponse:
        vehicle = self.session.get(Vehicle, location_data.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")
        
        return VehicleLocationResponse(
            vehicle_id=vehicle.id,
            registration_number=vehicle.registration_number,
            latitude=location_data.latitude,
            longitude=location_data.longitude,
            speed=location_data.speed,
            heading=location_data.heading,
            status=vehicle.status
        )

    def get_all_vehicle_locations(self) -> List[VehicleLocationResponse]:
        vehicles = self.session.exec(select(Vehicle).where(Vehicle.status == VehicleStatus.ON_TRIP)).all()
        
        locations = []
        for vehicle in vehicles:
            locations.append(VehicleLocationResponse(
                vehicle_id=vehicle.id,
                registration_number=vehicle.registration_number,
                latitude=0.0,
                longitude=0.0,
                speed=0.0,
                heading=0.0,
                status=vehicle.status
            ))
        
        return locations

    def get_vehicle_location(self, vehicle_id: int) -> Optional[VehicleLocationResponse]:
        vehicle = self.session.get(Vehicle, vehicle_id)
        if not vehicle:
            return None
        
        return VehicleLocationResponse(
            vehicle_id=vehicle.id,
            registration_number=vehicle.registration_number,
            latitude=0.0,
            longitude=0.0,
            speed=0.0,
            heading=0.0,
            status=vehicle.status
        )

    def get_active_trip_location(self, trip_id: int) -> Optional[VehicleLocationResponse]:
        trip = self.session.get(Trip, trip_id)
        if not trip or trip.status != TripStatus.DISPATCHED:
            return None
        
        vehicle = self.session.get(Vehicle, trip.vehicle_id)
        if not vehicle:
            return None
        
        return VehicleLocationResponse(
            vehicle_id=vehicle.id,
            registration_number=vehicle.registration_number,
            latitude=0.0,
            longitude=0.0,
            speed=0.0,
            heading=0.0,
            status=vehicle.status
        )
