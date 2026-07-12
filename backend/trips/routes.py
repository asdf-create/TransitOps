from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional, List
from pydantic import BaseModel

from database.connection import get_session
from database.models import TripStatus
from trips.models import TripCreate, TripUpdate, TripResponse
from trips.service import TripService

class TripCompleteRequest(BaseModel):
    actual_distance: float
    actual_duration: int

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    trip_data: TripCreate, 
    session: Session = Depends(get_session)
):
    service = TripService(session)
    try:
        return service.create_trip(trip_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[TripResponse])
def get_trips(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[TripStatus] = None,
    vehicle_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    service = TripService(session)
    return service.get_trips(skip, limit, status, vehicle_id, driver_id)

@router.get("/tracking/{tracking_id}", response_model=TripResponse)
def get_trip_by_tracking_id(tracking_id: str, session: Session = Depends(get_session)):
    service = TripService(session)
    trip = service.get_trip_by_tracking_id(tracking_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    return trip

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, session: Session = Depends(get_session)):
    service = TripService(session)
    trip = service.get_trip(trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    return trip

@router.post("/{trip_id}/dispatch", response_model=TripResponse)
def dispatch_trip(trip_id: int, session: Session = Depends(get_session)):
    service = TripService(session)
    try:
        trip = service.dispatch_trip(trip_id)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )
        return trip
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{trip_id}/complete", response_model=TripResponse)
def complete_trip(
    trip_id: int,
    completion_data: TripCompleteRequest,
    session: Session = Depends(get_session)
):
    service = TripService(session)
    try:
        trip = service.complete_trip(trip_id, completion_data.actual_distance, completion_data.actual_duration)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )
        return trip
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{trip_id}/cancel", response_model=TripResponse)
def cancel_trip(trip_id: int, session: Session = Depends(get_session)):
    service = TripService(session)
    try:
        trip = service.cancel_trip(trip_id)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )
        return trip
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: int,
    trip_data: TripUpdate,
    session: Session = Depends(get_session)
):
    service = TripService(session)
    trip = service.get_trip(trip_id)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )
    
    trip_data_dict = trip_data.model_dump(exclude_unset=True)
    for key, value in trip_data_dict.items():
        setattr(trip, key, value)
    
    session.add(trip)
    session.commit()
    session.refresh(trip)
    return trip
