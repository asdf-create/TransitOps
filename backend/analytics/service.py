from sqlmodel import Session, select
from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta
import csv
from io import StringIO

from database.models import Trip, Vehicle, Driver, FuelLog, Expense, TripStatus

class AnalyticsService:
    def __init__(self, session: Session):
        self.session = session

    def get_revenue_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get revenue analytics for the specified time period"""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        completed_trips = self.session.exec(
            select(Trip)
            .where(Trip.status == TripStatus.COMPLETED)
            .where(Trip.completed_at >= start_date)
        ).all()
        
        total_revenue = sum(trip.revenue for trip in completed_trips)
        avg_revenue_per_trip = total_revenue / len(completed_trips) if completed_trips else 0
        
        # Group by day
        daily_revenue = {}
        for trip in completed_trips:
            if trip.completed_at:
                date_key = trip.completed_at.date().isoformat()
                daily_revenue[date_key] = daily_revenue.get(date_key, 0) + trip.revenue
        
        return {
            "total_revenue": round(total_revenue, 2),
            "average_revenue_per_trip": round(avg_revenue_per_trip, 2),
            "total_trips": len(completed_trips),
            "daily_revenue": daily_revenue,
            "period_days": days
        }

    def get_fuel_efficiency_analytics(self) -> Dict[str, Any]:
        """Get fuel efficiency analytics across the fleet"""
        fuel_logs = self.session.exec(select(FuelLog)).all()
        vehicles = self.session.exec(select(Vehicle)).all()
        
        vehicle_efficiency = {}
        total_efficiency = 0
        vehicle_count = 0
        
        for vehicle in vehicles:
            vehicle_fuel_logs = [log for log in fuel_logs if log.vehicle_id == vehicle.id]
            if len(vehicle_fuel_logs) >= 2:
                distance = vehicle_fuel_logs[-1].odometer - vehicle_fuel_logs[0].odometer
                total_liters = sum(log.liters for log in vehicle_fuel_logs)
                efficiency = distance / total_liters if total_liters > 0 else 0
                
                vehicle_efficiency[vehicle.registration_number] = {
                    "efficiency_kmpl": round(efficiency, 2),
                    "total_liters": round(total_liters, 2),
                    "total_distance": round(distance, 2)
                }
                
                total_efficiency += efficiency
                vehicle_count += 1
        
        avg_fleet_efficiency = total_efficiency / vehicle_count if vehicle_count > 0 else 0
        
        return {
            "average_fleet_efficiency": round(avg_fleet_efficiency, 2),
            "vehicle_count": vehicle_count,
            "vehicle_efficiency": vehicle_efficiency
        }

    def get_driver_rankings(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get driver rankings based on safety score and performance"""
        drivers = self.session.exec(select(Driver)).all()
        
        driver_rankings = []
        for driver in drivers:
            # Get completed trips for this driver
            completed_trips = self.session.exec(
                select(Trip)
                .where(Trip.driver_id == driver.id)
                .where(Trip.status == TripStatus.COMPLETED)
            ).all()
            
            total_revenue = sum(trip.revenue for trip in completed_trips)
            avg_trip_revenue = total_revenue / len(completed_trips) if completed_trips else 0
            
            driver_rankings.append({
                "driver_id": driver.id,
                "name": driver.full_name,
                "safety_score": driver.safety_score,
                "total_trips": driver.total_trips,
                "total_distance": round(driver.total_distance, 2),
                "total_revenue": round(total_revenue, 2),
                "avg_trip_revenue": round(avg_trip_revenue, 2)
            })
        
        # Sort by safety score first, then by total trips
        driver_rankings.sort(key=lambda x: (x["safety_score"], x["total_trips"]), reverse=True)
        
        return driver_rankings[:limit]

    def get_vehicle_roi(self) -> Dict[str, Any]:
        """Calculate ROI for each vehicle"""
        vehicles = self.session.exec(select(Vehicle)).all()
        
        vehicle_roi = {}
        for vehicle in vehicles:
            # Get completed trips for this vehicle
            completed_trips = self.session.exec(
                select(Trip)
                .where(Trip.vehicle_id == vehicle.id)
                .where(Trip.status == TripStatus.COMPLETED)
            ).all()
            
            total_revenue = sum(trip.revenue for trip in completed_trips)
            
            # Get expenses for this vehicle
            vehicle_expenses = self.session.exec(
                select(Expense).where(Expense.vehicle_id == vehicle.id)
            ).all()
            total_expenses = sum(exp.amount for exp in vehicle_expenses)
            
            # Get fuel costs
            vehicle_fuel_logs = self.session.exec(
                select(FuelLog).where(FuelLog.vehicle_id == vehicle.id)
            ).all()
            total_fuel_cost = sum(log.cost for log in vehicle_fuel_logs) if vehicle_fuel_logs else 0
            
            # Calculate ROI
            operational_cost = total_expenses + total_fuel_cost
            roi = (total_revenue - operational_cost) / vehicle.acquisition_cost * 100 if vehicle.acquisition_cost > 0 else 0
            
            vehicle_roi[vehicle.registration_number] = {
                "total_revenue": round(total_revenue, 2),
                "operational_cost": round(operational_cost, 2),
                "acquisition_cost": round(vehicle.acquisition_cost, 2),
                "roi_percentage": round(roi, 2),
                "total_trips": len(completed_trips)
            }
        
        return vehicle_roi

    def export_analytics_csv(self) -> str:
        """Export analytics data as CSV"""
        # Get vehicle ROI data
        vehicle_roi = self.get_vehicle_roi()
        
        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "Vehicle Registration", "Total Revenue", "Operational Cost", 
            "Acquisition Cost", "ROI %", "Total Trips"
        ])
        
        # Write data
        for registration, data in vehicle_roi.items():
            writer.writerow([
                registration,
                data["total_revenue"],
                data["operational_cost"],
                data["acquisition_cost"],
                data["roi_percentage"],
                data["total_trips"]
            ])
        
        return output.getvalue()

    def get_fleet_analytics_summary(self) -> Dict[str, Any]:
        """Get comprehensive fleet analytics summary"""
        vehicles = self.session.exec(select(Vehicle)).all()
        drivers = self.session.exec(select(Driver)).all()
        trips = self.session.exec(select(Trip)).all()
        completed_trips = [trip for trip in trips if trip.status == TripStatus.COMPLETED]
        
        total_revenue = sum(trip.revenue for trip in completed_trips)
        total_distance = sum(trip.actual_distance or 0 for trip in completed_trips)
        
        # Get fuel analytics
        fuel_analytics = self.get_fuel_efficiency_analytics()
        
        # Get expense analytics
        all_expenses = self.session.exec(select(Expense)).all()
        total_expenses = sum(exp.amount for exp in all_expenses)
        
        return {
            "fleet": {
                "total_vehicles": len(vehicles),
                "total_drivers": len(drivers),
                "total_trips": len(trips),
                "completed_trips": len(completed_trips)
            },
            "financial": {
                "total_revenue": round(total_revenue, 2),
                "total_expenses": round(total_expenses, 2),
                "net_profit": round(total_revenue - total_expenses, 2)
            },
            "performance": {
                "total_distance": round(total_distance, 2),
                "average_fuel_efficiency": fuel_analytics["average_fleet_efficiency"]
            }
        }
