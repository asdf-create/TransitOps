from fastapi import APIRouter, Depends, Query, Response
from sqlmodel import Session
from typing import Optional

from database.connection import get_session
from analytics.service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/revenue")
def get_revenue_analytics(
    days: int = Query(30, ge=1, le=365),
    session: Session = Depends(get_session)
):
    service = AnalyticsService(session)
    return service.get_revenue_analytics(days)

@router.get("/fuel-efficiency")
def get_fuel_efficiency_analytics(session: Session = Depends(get_session)):
    service = AnalyticsService(session)
    return service.get_fuel_efficiency_analytics()

@router.get("/driver-rankings")
def get_driver_rankings(
    limit: int = Query(10, ge=1, le=50),
    session: Session = Depends(get_session)
):
    service = AnalyticsService(session)
    return service.get_driver_rankings(limit)

@router.get("/vehicle-roi")
def get_vehicle_roi(session: Session = Depends(get_session)):
    service = AnalyticsService(session)
    return service.get_vehicle_roi()

@router.get("/export/csv")
def export_analytics_csv(session: Session = Depends(get_session)):
    service = AnalyticsService(session)
    csv_data = service.export_analytics_csv()
    
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transitops_analytics.csv"}
    )

@router.get("/summary")
def get_fleet_analytics_summary(session: Session = Depends(get_session)):
    service = AnalyticsService(session)
    return service.get_fleet_analytics_summary()
