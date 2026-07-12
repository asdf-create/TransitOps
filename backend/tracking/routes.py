from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from database.connection import get_session
from tracking.service import TrackingService
from tracking.models import LocationUpdate, VehicleLocationResponse, TrackingDetailResponse, TrackingTimelineResponse, RouteGeometryResponse

router = APIRouter(prefix="/tracking", tags=["Tracking"])

@router.get("/vehicles", response_model=List[VehicleLocationResponse])
def get_all_vehicle_locations(session: Session = Depends(get_session)):
    service = TrackingService(session)
    return service.get_all_vehicle_locations()

@router.get("/vehicles/{vehicle_id}", response_model=VehicleLocationResponse)
def get_vehicle_location(vehicle_id: int, session: Session = Depends(get_session)):
    service = TrackingService(session)
    location = service.get_vehicle_location(vehicle_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    return location

@router.post("/vehicles/{vehicle_id}/location", response_model=VehicleLocationResponse)
def update_vehicle_location(
    vehicle_id: int,
    location_data: LocationUpdate,
    session: Session = Depends(get_session)
):
    service = TrackingService(session)
    location_data.vehicle_id = vehicle_id
    try:
        return service.update_vehicle_location(location_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/trips/{trip_id}/location", response_model=VehicleLocationResponse)
def get_trip_location(trip_id: int, session: Session = Depends(get_session)):
    service = TrackingService(session)
    location = service.get_active_trip_location(trip_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found or not active")
    return location

@router.get("/{tracking_id}", response_model=TrackingDetailResponse)
def get_tracking_details(tracking_id: str, session: Session = Depends(get_session)):
    service = TrackingService(session)
    details = service.get_tracking_details(tracking_id)
    if not details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tracking ID {tracking_id} not found")
    return details

@router.get("/{tracking_id}/history", response_model=TrackingTimelineResponse)
def get_tracking_history(tracking_id: str, session: Session = Depends(get_session)):
    service = TrackingService(session)
    history = service.get_tracking_history(tracking_id)
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tracking ID {tracking_id} not found")
    return history

@router.get("/{tracking_id}/route", response_model=RouteGeometryResponse)
def get_tracking_route(tracking_id: str, session: Session = Depends(get_session)):
    service = TrackingService(session)
    route = service.get_tracking_route(tracking_id)
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tracking ID {tracking_id} not found")
    return route
