from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional, List

from database.connection import get_session
from fuel.models import FuelLogCreate, FuelLogUpdate, FuelLogResponse
from fuel.service import FuelService

router = APIRouter(prefix="/fuel", tags=["Fuel"])

@router.post("/", response_model=FuelLogResponse, status_code=status.HTTP_201_CREATED)
def create_fuel_log(
    fuel_data: FuelLogCreate, 
    session: Session = Depends(get_session)
):
    service = FuelService(session)
    try:
        return service.create_fuel_log(fuel_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[FuelLogResponse])
def get_fuel_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    vehicle_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    service = FuelService(session)
    return service.get_fuel_logs(skip, limit, vehicle_id, driver_id)

@router.get("/vehicle/{vehicle_id}/efficiency")
def get_vehicle_fuel_efficiency(vehicle_id: int, session: Session = Depends(get_session)):
    service = FuelService(session)
    return service.get_vehicle_fuel_efficiency(vehicle_id)

@router.get("/{fuel_log_id}", response_model=FuelLogResponse)
def get_fuel_log(fuel_log_id: int, session: Session = Depends(get_session)):
    service = FuelService(session)
    fuel_log = service.get_fuel_log(fuel_log_id)
    if not fuel_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fuel log not found"
        )
    return fuel_log

@router.patch("/{fuel_log_id}", response_model=FuelLogResponse)
def update_fuel_log(
    fuel_log_id: int,
    fuel_data: FuelLogUpdate,
    session: Session = Depends(get_session)
):
    service = FuelService(session)
    fuel_log = service.update_fuel_log(fuel_log_id, fuel_data)
    if not fuel_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fuel log not found"
        )
    return fuel_log

@router.delete("/{fuel_log_id}")
def delete_fuel_log(fuel_log_id: int, session: Session = Depends(get_session)):
    service = FuelService(session)
    if not service.delete_fuel_log(fuel_log_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fuel log not found"
        )
    return {"message": "Fuel log deleted successfully"}
