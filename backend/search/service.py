from sqlmodel import Session, select, or_
from typing import List, Dict, Any

from database.models import Vehicle, Driver, Trip, MaintenanceLog

class SearchService:
    def __init__(self, session: Session):
        self.session = session

    def global_search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        if not query or not query.strip():
            return []
        
        search_term = f"%{query}%"
        results = []

        # 1. Search Vehicles
        vehicles = self.session.exec(
            select(Vehicle)
            .where(
                or_(
                    Vehicle.registration_number.like(search_term),
                    Vehicle.manufacturer.like(search_term),
                    Vehicle.model.like(search_term)
                )
            )
            .limit(limit)
        ).all()
        for v in vehicles:
            results.append({
                "type": "vehicle",
                "id": v.id,
                "title": f"{v.manufacturer} {v.model}",
                "subtitle": f"Reg: {v.registration_number} | {v.status.value}",
                "url": "/vehicles"
            })

        # 2. Search Drivers
        drivers = self.session.exec(
            select(Driver)
            .where(
                or_(
                    Driver.full_name.like(search_term),
                    Driver.license_number.like(search_term)
                )
            )
            .limit(limit)
        ).all()
        for d in drivers:
            results.append({
                "type": "driver",
                "id": d.id,
                "title": d.full_name,
                "subtitle": f"Lic: {d.license_number} | {d.status.value}",
                "url": "/drivers"
            })

        # 3. Search Trips
        trips = self.session.exec(
            select(Trip)
            .where(
                or_(
                    Trip.tracking_id.like(search_term),
                    Trip.source.like(search_term),
                    Trip.destination.like(search_term)
                )
            )
            .limit(limit)
        ).all()
        for t in trips:
            results.append({
                "type": "trip",
                "id": t.id,
                "title": f"Trip {t.tracking_id}",
                "subtitle": f"{t.source} to {t.destination} | {t.status.value}",
                "url": "/trips"
            })

        # 4. Search Maintenance Logs
        maintenance = self.session.exec(
            select(MaintenanceLog)
            .where(
                or_(
                    MaintenanceLog.maintenance_type.like(search_term),
                    MaintenanceLog.description.like(search_term)
                )
            )
            .limit(limit)
        ).all()
        for m in maintenance:
            results.append({
                "type": "maintenance",
                "id": m.id,
                "title": f"Maintenance: {m.maintenance_type}",
                "subtitle": f"Desc: {m.description[:60]}... | {m.status.value}",
                "url": "/maintenance"
            })

        # Return combined sorted or limited results
        return results[:limit]
