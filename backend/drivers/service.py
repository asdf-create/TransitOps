from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime, timezone
from database.models import Driver, DriverStatus
from drivers.models import DriverCreate, DriverUpdate

class DriverService:
    def __init__(self, session: Session):
        self.session = session

    def create_driver(self, driver_data: DriverCreate) -> Driver:
        # Check if license number already exists
        existing = self.session.exec(
            select(Driver).where(Driver.license_number == driver_data.license_number)
        ).first()
        if existing:
            raise ValueError(f"Driver with license number {driver_data.license_number} already exists")
        
        # Check if license is expired
        if driver_data.license_expiry < datetime.now(timezone.utc):
            raise ValueError("License has expired")
        
        db_driver = Driver.model_validate(driver_data)
        self.session.add(db_driver)
        self.session.commit()
        self.session.refresh(db_driver)
        return db_driver

    def get_driver(self, driver_id: int) -> Optional[Driver]:
        return self.session.get(Driver, driver_id)

    def get_drivers(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[DriverStatus] = None,
        region: Optional[str] = None
    ) -> List[Driver]:
        query = select(Driver)
        
        if status:
            query = query.where(Driver.status == status)
        if region:
            query = query.where(Driver.assigned_region == region)
            
        query = query.offset(skip).limit(limit)
        return self.session.exec(query).all()

    def update_driver(self, driver_id: int, driver_data: DriverUpdate) -> Optional[Driver]:
        db_driver = self.get_driver(driver_id)
        if not db_driver:
            return None
        
        driver_data_dict = driver_data.model_dump(exclude_unset=True)
        for key, value in driver_data_dict.items():
            setattr(db_driver, key, value)
        
        self.session.add(db_driver)
        self.session.commit()
        self.session.refresh(db_driver)
        return db_driver

    def delete_driver(self, driver_id: int) -> bool:
        db_driver = self.get_driver(driver_id)
        if not db_driver:
            return False
        
        # Soft delete by setting status to SUSPENDED
        db_driver.status = DriverStatus.SUSPENDED
        self.session.add(db_driver)
        self.session.commit()
        return True

    def get_available_drivers(self) -> List[Driver]:
        return self.session.exec(
            select(Driver).where(Driver.status == DriverStatus.AVAILABLE)
        ).all()

    def get_driver_rankings(self, limit: int = 10) -> List[Driver]:
        return self.session.exec(
            select(Driver)
            .order_by(Driver.safety_score.desc())
            .limit(limit)
        ).all()

    def check_license_expiry(self, driver_id: int) -> bool:
        driver = self.get_driver(driver_id)
        if not driver:
            return False
        return driver.license_expiry < datetime.now(timezone.utc)
