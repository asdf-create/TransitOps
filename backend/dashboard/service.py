from sqlmodel import Session, select
from typing import Dict, Any
from datetime import datetime, timezone, timedelta

from database.models import Vehicle, Driver, Trip, VehicleStatus, DriverStatus, TripStatus

class DashboardService:
    def __init__(self, session: Session):
        self.session = session

    def get_kpis(self) -> Dict[str, Any]:
        # Get vehicle statistics
        all_vehicles = self.session.exec(select(Vehicle)).all()
        available_vehicles = self.session.exec(
            select(Vehicle).where(Vehicle.status == VehicleStatus.AVAILABLE)
        ).all()
        on_trip_vehicles = self.session.exec(
            select(Vehicle).where(Vehicle.status == VehicleStatus.ON_TRIP)
        ).all()
        in_shop_vehicles = self.session.exec(
            select(Vehicle).where(Vehicle.status == VehicleStatus.IN_SHOP)
        ).all()
        
        # Get driver statistics
        all_drivers = self.session.exec(select(Driver)).all()
        available_drivers = self.session.exec(
            select(Driver).where(Driver.status == DriverStatus.AVAILABLE)
        ).all()
        on_trip_drivers = self.session.exec(
            select(Driver).where(Driver.status == DriverStatus.ON_TRIP)
        ).all()
        
        # Get trip statistics
        all_trips = self.session.exec(select(Trip)).all()
        active_trips = self.session.exec(
            select(Trip).where(Trip.status == TripStatus.DISPATCHED)
        ).all()
        completed_trips = self.session.exec(
            select(Trip).where(Trip.status == TripStatus.COMPLETED)
        ).all()
        
        # Calculate fleet utilization
        fleet_utilization = 0
        if all_vehicles:
            fleet_utilization = (len(on_trip_vehicles) / len(all_vehicles)) * 100
        
        # Calculate total revenue
        total_revenue = sum(trip.revenue for trip in completed_trips)
        
        # Calculate average safety score
        avg_safety_score = 0
        if all_drivers:
            avg_safety_score = sum(driver.safety_score for driver in all_drivers) / len(all_drivers)
        
        return {
            "vehicles": {
                "total": len(all_vehicles),
                "available": len(available_vehicles),
                "on_trip": len(on_trip_vehicles),
                "in_shop": len(in_shop_vehicles),
                "retired": len(all_vehicles) - len(available_vehicles) - len(on_trip_vehicles) - len(in_shop_vehicles)
            },
            "drivers": {
                "total": len(all_drivers),
                "available": len(available_drivers),
                "on_trip": len(on_trip_drivers),
                "off_duty": len(all_drivers) - len(available_drivers) - len(on_trip_drivers)
            },
            "trips": {
                "total": len(all_trips),
                "active": len(active_trips),
                "completed": len(completed_trips),
                "cancelled": len(all_trips) - len(active_trips) - len(completed_trips)
            },
            "metrics": {
                "fleet_utilization": round(fleet_utilization, 2),
                "total_revenue": round(total_revenue, 2),
                "average_safety_score": round(avg_safety_score, 2)
            },
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

    def get_fleet_status(self) -> Dict[str, Any]:
        vehicles = self.session.exec(select(Vehicle)).all()
        
        status_counts = {
            "available": 0,
            "on_trip": 0,
            "in_shop": 0,
            "retired": 0
        }
        
        for vehicle in vehicles:
            key = vehicle.status.value.lower().replace(" ", "_")
            if key in status_counts:
                status_counts[key] += 1
            else:
                logger.warning(f"Unknown vehicle status key: {key}")
        
        return status_counts

    def get_driver_status(self) -> Dict[str, Any]:
        drivers = self.session.exec(select(Driver)).all()
        
        status_counts = {
            "available": 0,
            "on_trip": 0,
            "off_duty": 0,
            "suspended": 0
        }
        
        for driver in drivers:
            status_counts[driver.status.value.lower().replace(" ", "_")] += 1
        
        return status_counts

    def get_recent_activity(self, limit: int = 10) -> list:
        # Get recent completed trips
        recent_trips = self.session.exec(
            select(Trip)
            .where(Trip.status == TripStatus.COMPLETED)
            .order_by(Trip.completed_at.desc())
            .limit(limit)
        ).all()
        
        activity = []
        for trip in recent_trips:
            activity.append({
                "type": "trip_completed",
                "tracking_id": trip.tracking_id,
                "vehicle": trip.vehicle_name,
                "driver": trip.driver_name,
                "timestamp": trip.completed_at.isoformat() if trip.completed_at else None
            })
        
        return activity
