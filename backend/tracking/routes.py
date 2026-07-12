from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database.connection import get_session
from tracking.service import TrackingService
from tracking.models import LocationUpdate, VehicleLocationResponse

router = APIRouter(prefix="/tracking", tags=["tracking"])

@router.get("/vehicles", response_model=list[VehicleLocationResponse])
def get_all_vehicle_locations(session: Session = Depends(get_session)):
    service = TrackingService(session)
    return service.get_all_vehicle_locations()

@router.get("/vehicles/{vehicle_id}", response_model=VehicleLocationResponse)
def get_vehicle_location(vehicle_id: int, session: Session = Depends(get_session)):
    service = TrackingService(session)
    location = service.get_vehicle_location(vehicle_id)
    if not location:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return location

@router.post("/vehicles/{vehicle_id}/location", response_model=VehicleLocationResponse)
def update_vehicle_location(
    vehicle_id: int,
    location_data: LocationUpdate,
    session: Session = Depends(get_session)
):
    service = TrackingService(session)
    location_data.vehicle_id = vehicle_id
    return service.update_vehicle_location(location_data)

@router.get("/trips/{trip_id}/location", response_model=VehicleLocationResponse)
def get_trip_location(trip_id: int, session: Session = Depends(get_session)):
    service = TrackingService(session)
    location = service.get_active_trip_location(trip_id)
    if not location:
        raise HTTPException(status_code=404, detail="Trip not found or not active")
    return location
