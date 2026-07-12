from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional, List

from database.connection import get_session
from database.models import DriverStatus
from drivers.models import DriverCreate, DriverUpdate, DriverResponse
from drivers.service import DriverService

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
def create_driver(
    driver_data: DriverCreate, 
    session: Session = Depends(get_session)
):
    service = DriverService(session)
    try:
        return service.create_driver(driver_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[DriverResponse])
def get_drivers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[DriverStatus] = None,
    region: Optional[str] = None,
    session: Session = Depends(get_session)
):
    service = DriverService(session)
    return service.get_drivers(skip, limit, status, region)

@router.get("/available", response_model=List[DriverResponse])
def get_available_drivers(session: Session = Depends(get_session)):
    service = DriverService(session)
    return service.get_available_drivers()

@router.get("/rankings", response_model=List[DriverResponse])
def get_driver_rankings(
    limit: int = Query(10, ge=1, le=50),
    session: Session = Depends(get_session)
):
    service = DriverService(session)
    return service.get_driver_rankings(limit)

@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, session: Session = Depends(get_session)):
    service = DriverService(session)
    driver = service.get_driver(driver_id)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    return driver

@router.get("/{driver_id}/license-expiry")
def check_license_expiry(driver_id: int, session: Session = Depends(get_session)):
    service = DriverService(session)
    is_expired = service.check_license_expiry(driver_id)
    return {"driver_id": driver_id, "is_expired": is_expired}

@router.patch("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: int,
    driver_data: DriverUpdate,
    session: Session = Depends(get_session)
):
    service = DriverService(session)
    driver = service.update_driver(driver_id, driver_data)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    return driver

@router.delete("/{driver_id}")
def delete_driver(driver_id: int, session: Session = Depends(get_session)):
    service = DriverService(session)
    if not service.delete_driver(driver_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )
    return {"message": "Driver deleted successfully"}
