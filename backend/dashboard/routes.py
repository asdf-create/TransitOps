from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from database.connection import get_session
from dashboard.service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/kpis")
def get_kpis(session: Session = Depends(get_session)):
    service = DashboardService(session)
    return service.get_kpis()

@router.get("/fleet-status")
def get_fleet_status(session: Session = Depends(get_session)):
    service = DashboardService(session)
    return service.get_fleet_status()

@router.get("/driver-status")
def get_driver_status(session: Session = Depends(get_session)):
    service = DashboardService(session)
    return service.get_driver_status()

@router.get("/recent-activity")
def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    session: Session = Depends(get_session)
):
    service = DashboardService(session)
    return service.get_recent_activity(limit)
