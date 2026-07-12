from sqlmodel import Session, select
from typing import Optional, List
from database.models import Vehicle, VehicleStatus
from vehicles.models import VehicleCreate, VehicleUpdate

class VehicleService:
    def __init__(self, session: Session):
        self.session = session

    def create_vehicle(self, vehicle_data: VehicleCreate) -> Vehicle:
        # Validate registration number is not empty
        if not vehicle_data.registration_number or not vehicle_data.registration_number.strip():
            raise ValueError("Registration number cannot be empty")

        # Check if registration number already exists
        existing = self.session.exec(
            select(Vehicle).where(Vehicle.registration_number == vehicle_data.registration_number)
        ).first()
        if existing:
            raise ValueError(f"Vehicle with registration number {vehicle_data.registration_number} already exists")
        
        db_vehicle = Vehicle.model_validate(vehicle_data)
        self.session.add(db_vehicle)
        self.session.commit()
        self.session.refresh(db_vehicle)
        return db_vehicle

    def get_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.session.get(Vehicle, vehicle_id)

    def get_vehicles(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[VehicleStatus] = None,
        vehicle_type: Optional[str] = None,
        region: Optional[str] = None
    ) -> List[Vehicle]:
        query = select(Vehicle)
        
        if status:
            query = query.where(Vehicle.status == status)
        if vehicle_type:
            query = query.where(Vehicle.vehicle_type == vehicle_type)
        if region:
            query = query.where(Vehicle.region == region)
            
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def update_vehicle(self, vehicle_id: int, vehicle_data: VehicleUpdate) -> Optional[Vehicle]:
        db_vehicle = self.get_vehicle(vehicle_id)
        if not db_vehicle:
            return None
        
        vehicle_data_dict = vehicle_data.model_dump(exclude_unset=True)
        for key, value in vehicle_data_dict.items():
            setattr(db_vehicle, key, value)
        
        self.session.add(db_vehicle)
        self.session.commit()
        self.session.refresh(db_vehicle)
        return db_vehicle

    def delete_vehicle(self, vehicle_id: int) -> bool:
        db_vehicle = self.get_vehicle(vehicle_id)
        if not db_vehicle:
            return False
        
        # Soft delete by setting status to RETIRED
        db_vehicle.status = VehicleStatus.RETIRED
        self.session.add(db_vehicle)
        self.session.commit()
        return True

    def get_available_vehicles(self) -> List[Vehicle]:
        return self.session.exec(
            select(Vehicle).where(Vehicle.status == VehicleStatus.AVAILABLE)
        ).all()

    def get_vehicle_statistics(self) -> dict:
        total = self.session.exec(select(Vehicle)).all()
        available = self.session.exec(
            select(Vehicle).where(Vehicle.status == VehicleStatus.AVAILABLE)
        ).all()
        on_trip = self.session.exec(
            select(Vehicle).where(Vehicle.status == VehicleStatus.ON_TRIP)
        ).all()
        in_shop = self.session.exec(
            select(Vehicle).where(Vehicle.status == VehicleStatus.IN_SHOP)
        ).all()
        retired = self.session.exec(
            select(Vehicle).where(Vehicle.status == VehicleStatus.RETIRED)
        ).all()
        
        return {
            "total": len(total),
            "available": len(available),
            "on_trip": len(on_trip),
            "in_shop": len(in_shop),
            "retired": len(retired),
            "utilization": len(on_trip) / len(total) * 100 if total else 0
        }
