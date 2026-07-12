from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional, List

from database.connection import get_session
from database.models import VehicleStatus
from vehicles.models import VehicleCreate, VehicleUpdate, VehicleResponse
from vehicles.service import VehicleService

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle_data: VehicleCreate, 
    session: Session = Depends(get_session)
):
    service = VehicleService(session)
    try:
        return service.create_vehicle(vehicle_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[VehicleResponse])
def get_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[VehicleStatus] = None,
    vehicle_type: Optional[str] = None,
    region: Optional[str] = None,
    session: Session = Depends(get_session)
):
    service = VehicleService(session)
    return service.get_vehicles(skip, limit, status, vehicle_type, region)

@router.get("/available", response_model=List[VehicleResponse])
def get_available_vehicles(session: Session = Depends(get_session)):
    service = VehicleService(session)
    return service.get_available_vehicles()

@router.get("/statistics")
def get_vehicle_statistics(session: Session = Depends(get_session)):
    service = VehicleService(session)
    return service.get_vehicle_statistics()

@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, session: Session = Depends(get_session)):
    service = VehicleService(session)
    vehicle = service.get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    return vehicle

@router.patch("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    session: Session = Depends(get_session)
):
    service = VehicleService(session)
    vehicle = service.update_vehicle(vehicle_id, vehicle_data)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    return vehicle

@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, session: Session = Depends(get_session)):
    service = VehicleService(session)
    if not service.delete_vehicle(vehicle_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    return {"message": "Vehicle deleted successfully"}
