from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime, timezone

from database.models import MaintenanceLog, Vehicle, VehicleStatus, MaintenanceStatus
from maintenance.models import MaintenanceCreate, MaintenanceUpdate

class MaintenanceService:
    def __init__(self, session: Session):
        self.session = session

    def create_maintenance(self, maintenance_data: MaintenanceCreate) -> MaintenanceLog:
        # Validate vehicle exists
        vehicle = self.session.get(Vehicle, maintenance_data.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")
        
        # Business Rule: Creating an active maintenance record automatically changes vehicle status to In Shop
        vehicle.status = VehicleStatus.IN_SHOP
        
        db_maintenance = MaintenanceLog.model_validate(maintenance_data)
        db_maintenance.status = MaintenanceStatus.SCHEDULED
        
        self.session.add(db_maintenance)
        self.session.add(vehicle)
        self.session.commit()
        self.session.refresh(db_maintenance)
        return db_maintenance

    def get_maintenance(self, maintenance_id: int) -> Optional[MaintenanceLog]:
        return self.session.get(MaintenanceLog, maintenance_id)

    def get_maintenance_records(
        self, 
        skip: int = 0, 
        limit: int = 100,
        vehicle_id: Optional[int] = None,
        status: Optional[MaintenanceStatus] = None
    ) -> List[MaintenanceLog]:
        query = select(MaintenanceLog)
        
        if vehicle_id:
            query = query.where(MaintenanceLog.vehicle_id == vehicle_id)
        if status:
            query = query.where(MaintenanceLog.status == status)
            
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def update_maintenance(self, maintenance_id: int, maintenance_data: MaintenanceUpdate) -> Optional[MaintenanceLog]:
        db_maintenance = self.get_maintenance(maintenance_id)
        if not db_maintenance:
            return None
        
        maintenance_data_dict = maintenance_data.model_dump(exclude_unset=True)
        for key, value in maintenance_data_dict.items():
            setattr(db_maintenance, key, value)
        
        self.session.add(db_maintenance)
        self.session.commit()
        self.session.refresh(db_maintenance)
        return db_maintenance

    def start_maintenance(self, maintenance_id: int) -> Optional[MaintenanceLog]:
        db_maintenance = self.get_maintenance(maintenance_id)
        if not db_maintenance:
            return None
        
        if db_maintenance.status != MaintenanceStatus.SCHEDULED:
            raise ValueError("Only scheduled maintenance can be started")
        
        db_maintenance.status = MaintenanceStatus.IN_PROGRESS
        db_maintenance.started_date = datetime.now(timezone.utc)
        
        self.session.add(db_maintenance)
        self.session.commit()
        self.session.refresh(db_maintenance)
        return db_maintenance

    def complete_maintenance(self, maintenance_id: int, actual_cost: Optional[float] = None) -> Optional[MaintenanceLog]:
        db_maintenance = self.get_maintenance(maintenance_id)
        if not db_maintenance:
            return None
        
        if db_maintenance.status != MaintenanceStatus.IN_PROGRESS:
            raise ValueError("Only in-progress maintenance can be completed")
        
        # Business Rule: Closing maintenance restores the vehicle to Available (unless retired)
        vehicle = self.session.get(Vehicle, db_maintenance.vehicle_id)
        if vehicle.status != VehicleStatus.RETIRED:
            vehicle.status = VehicleStatus.AVAILABLE
        
        db_maintenance.status = MaintenanceStatus.COMPLETED
        db_maintenance.completed_date = datetime.now(timezone.utc)
        if actual_cost is not None:
            db_maintenance.actual_cost = actual_cost
        
        self.session.add(db_maintenance)
        self.session.add(vehicle)
        self.session.commit()
        self.session.refresh(db_maintenance)
        return db_maintenance

    def cancel_maintenance(self, maintenance_id: int) -> Optional[MaintenanceLog]:
        db_maintenance = self.get_maintenance(maintenance_id)
        if not db_maintenance:
            return None
        
        if db_maintenance.status not in [MaintenanceStatus.SCHEDULED, MaintenanceStatus.IN_PROGRESS]:
            raise ValueError("Only scheduled or in-progress maintenance can be cancelled")
        
        # Restore vehicle status
        vehicle = self.session.get(Vehicle, db_maintenance.vehicle_id)
        if vehicle.status != VehicleStatus.RETIRED:
            vehicle.status = VehicleStatus.AVAILABLE
        
        db_maintenance.status = MaintenanceStatus.CANCELLED
        
        self.session.add(db_maintenance)
        self.session.add(vehicle)
        self.session.commit()
        self.session.refresh(db_maintenance)
        return db_maintenance

    def get_vehicle_maintenance_history(self, vehicle_id: int) -> List[MaintenanceLog]:
        return self.session.exec(
            select(MaintenanceLog)
            .where(MaintenanceLog.vehicle_id == vehicle_id)
            .order_by(MaintenanceLog.scheduled_date.desc())
        ).all()
