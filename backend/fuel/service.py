from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime, timezone

from database.models import FuelLog, Vehicle
from fuel.models import FuelLogCreate, FuelLogUpdate

class FuelService:
    def __init__(self, session: Session):
        self.session = session

    def create_fuel_log(self, fuel_data: FuelLogCreate) -> FuelLog:
        # Validate vehicle exists
        vehicle = self.session.get(Vehicle, fuel_data.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")
        
        # Business Rule: Fuel logs cannot use future dates
        if fuel_data.timestamp and fuel_data.timestamp > datetime.now(timezone.utc):
            raise ValueError("Fuel log timestamp cannot be in the future")
        
        # Business Rule: Odometer values may only increase
        if fuel_data.odometer < vehicle.odometer:
            raise ValueError(f"Odometer reading ({fuel_data.odometer}) is less than current vehicle odometer ({vehicle.odometer})")
        
        # Business Rule: Duplicate fuel log detection
        existing = self.session.exec(
            select(FuelLog).where(
                FuelLog.vehicle_id == fuel_data.vehicle_id,
                FuelLog.odometer == fuel_data.odometer,
                FuelLog.timestamp == (fuel_data.timestamp or datetime.now(timezone.utc))
            )
        ).first()
        if existing:
            raise ValueError("Duplicate fuel log detected")
        
        db_fuel_log = FuelLog.model_validate(fuel_data)
        if not db_fuel_log.timestamp:
            db_fuel_log.timestamp = datetime.now(timezone.utc)
        
        # Update vehicle odometer
        vehicle.odometer = fuel_data.odometer
        
        self.session.add(db_fuel_log)
        self.session.add(vehicle)
        self.session.commit()
        self.session.refresh(db_fuel_log)
        return db_fuel_log

    def get_fuel_log(self, fuel_log_id: int) -> Optional[FuelLog]:
        return self.session.get(FuelLog, fuel_log_id)

    def get_fuel_logs(
        self, 
        skip: int = 0, 
        limit: int = 100,
        vehicle_id: Optional[int] = None,
        driver_id: Optional[int] = None
    ) -> List[FuelLog]:
        query = select(FuelLog)
        
        if vehicle_id:
            query = query.where(FuelLog.vehicle_id == vehicle_id)
        if driver_id:
            query = query.where(FuelLog.driver_id == driver_id)
            
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def update_fuel_log(self, fuel_log_id: int, fuel_data: FuelLogUpdate) -> Optional[FuelLog]:
        db_fuel_log = self.get_fuel_log(fuel_log_id)
        if not db_fuel_log:
            return None
        
        fuel_data_dict = fuel_data.model_dump(exclude_unset=True)
        for key, value in fuel_data_dict.items():
            setattr(db_fuel_log, key, value)
        
        self.session.add(db_fuel_log)
        self.session.commit()
        self.session.refresh(db_fuel_log)
        return db_fuel_log

    def delete_fuel_log(self, fuel_log_id: int) -> bool:
        db_fuel_log = self.get_fuel_log(fuel_log_id)
        if not db_fuel_log:
            return False
        
        self.session.delete(db_fuel_log)
        self.session.commit()
        return True

    def get_vehicle_fuel_efficiency(self, vehicle_id: int) -> dict:
        fuel_logs = self.session.exec(
            select(FuelLog).where(FuelLog.vehicle_id == vehicle_id)
        ).all()
        
        if not fuel_logs:
            return {"total_liters": 0, "total_cost": 0, "efficiency_kmpl": 0}
        
        total_liters = sum(log.liters for log in fuel_logs)
        total_cost = sum(log.cost for log in fuel_logs)
        
        # Calculate efficiency from first to last odometer reading
        if len(fuel_logs) >= 2:
            distance = fuel_logs[-1].odometer - fuel_logs[0].odometer
            efficiency = distance / total_liters if total_liters > 0 else 0
        else:
            efficiency = 0
        
        return {
            "total_liters": total_liters,
            "total_cost": total_cost,
            "efficiency_kmpl": efficiency
        }
