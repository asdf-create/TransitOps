from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional, List
from pydantic import BaseModel

from database.connection import get_session
from database.models import MaintenanceStatus
from maintenance.models import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse
from maintenance.service import MaintenanceService

class MaintenanceCompleteRequest(BaseModel):
    actual_cost: Optional[float] = None

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

@router.post("/", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(
    maintenance_data: MaintenanceCreate, 
    session: Session = Depends(get_session)
):
    service = MaintenanceService(session)
    try:
        return service.create_maintenance(maintenance_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[MaintenanceResponse])
def get_maintenance_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    vehicle_id: Optional[int] = None,
    status: Optional[MaintenanceStatus] = None,
    session: Session = Depends(get_session)
):
    service = MaintenanceService(session)
    return service.get_maintenance_records(skip, limit, vehicle_id, status)

@router.get("/vehicle/{vehicle_id}", response_model=List[MaintenanceResponse])
def get_vehicle_maintenance_history(vehicle_id: int, session: Session = Depends(get_session)):
    service = MaintenanceService(session)
    return service.get_vehicle_maintenance_history(vehicle_id)

@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance(maintenance_id: int, session: Session = Depends(get_session)):
    service = MaintenanceService(session)
    maintenance = service.get_maintenance(maintenance_id)
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance record not found"
        )
    return maintenance

@router.post("/{maintenance_id}/start", response_model=MaintenanceResponse)
def start_maintenance(maintenance_id: int, session: Session = Depends(get_session)):
    service = MaintenanceService(session)
    try:
        maintenance = service.start_maintenance(maintenance_id)
        if not maintenance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance record not found"
            )
        return maintenance
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{maintenance_id}/complete", response_model=MaintenanceResponse)
def complete_maintenance(
    maintenance_id: int,
    completion_data: MaintenanceCompleteRequest,
    session: Session = Depends(get_session)
):
    service = MaintenanceService(session)
    try:
        maintenance = service.complete_maintenance(maintenance_id, completion_data.actual_cost)
        if not maintenance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance record not found"
            )
        return maintenance
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{maintenance_id}/cancel", response_model=MaintenanceResponse)
def cancel_maintenance(maintenance_id: int, session: Session = Depends(get_session)):
    service = MaintenanceService(session)
    try:
        maintenance = service.cancel_maintenance(maintenance_id)
        if not maintenance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance record not found"
            )
        return maintenance
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance(
    maintenance_id: int,
    maintenance_data: MaintenanceUpdate,
    session: Session = Depends(get_session)
):
    service = MaintenanceService(session)
    maintenance = service.update_maintenance(maintenance_id, maintenance_data)
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance record not found"
        )
    return maintenance
