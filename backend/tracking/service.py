from sqlmodel import Session, select
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
import hashlib

from database.models import Vehicle, Trip, VehicleStatus, TripStatus, Driver
from tracking.models import VehicleLocation, LocationUpdate, VehicleLocationResponse, TrackingDetailResponse, TrackingTimelineEvent, TrackingTimelineResponse, RouteGeometryResponse

class TrackingService:
    def __init__(self, session: Session):
        self.session = session

    def _get_city_coords(self, city_name: str) -> tuple[float, float]:
        """Get deterministic lat/lon for a city name (Indian and Australian hubs)."""
        cities = {
            "warehouse a": (-33.8688, 151.2093),  # Sydney
            "warehouse b": (-37.8136, 144.9631),  # Melbourne
            "warehouse c": (-27.4705, 153.0260),  # Brisbane
            "warehouse d": (-31.9505, 115.8605),  # Perth
            "distribution center a": (-34.9285, 138.6007),  # Adelaide
            "delhi": (28.6139, 77.2090),
            "mumbai": (19.0760, 72.8777),
            "bengaluru": (12.9716, 77.5946),
            "chennai": (13.0827, 80.2707),
            "kolkata": (22.5726, 88.3639),
            "hyderabad": (17.3850, 78.4867),
            "pune": (18.5204, 73.8567),
        }
        
        name_lower = city_name.lower().strip()
        if name_lower in cities:
            return cities[name_lower]
        
        # Generate deterministically from hash
        h = int(hashlib.md5(name_lower.encode('utf-8')).hexdigest(), 16)
        lat = 12.0 + (h % 15000) / 1000.0  # Between 12.0 and 27.0
        lon = 72.0 + ((h >> 16) % 15000) / 1000.0  # Between 72.0 and 87.0
        return lat, lon

    def _get_trip_tracking_info(self, trip: Trip) -> Dict[str, Any]:
        """Calculate live progress and interpolated position for a trip."""
        source_lat, source_lon = self._get_city_coords(trip.source)
        dest_lat, dest_lon = self._get_city_coords(trip.destination)
        
        if trip.status == TripStatus.DRAFT:
            return {
                "lat": source_lat,
                "lon": source_lon,
                "progress": 0.0,
                "speed": 0.0,
                "remaining_distance": trip.planned_distance,
                "status": "Draft - Preparing Cargo"
            }
        elif trip.status == TripStatus.COMPLETED:
            return {
                "lat": dest_lat,
                "lon": dest_lon,
                "progress": 100.0,
                "speed": 0.0,
                "remaining_distance": 0.0,
                "status": "Delivered"
            }
        elif trip.status == TripStatus.CANCELLED:
            return {
                "lat": source_lat,
                "lon": source_lon,
                "progress": 0.0,
                "speed": 0.0,
                "remaining_distance": trip.planned_distance,
                "status": "Cancelled"
            }
        elif trip.status == TripStatus.DISPATCHED:
            # Calculate progress based on actual departure and duration
            dep_time = trip.actual_departure or trip.planned_departure or datetime.now()
            # If naive, make aware for delta check
            if dep_time.tzinfo is None:
                dep_time = dep_time.replace(tzinfo=timezone.utc)
            now_aware = datetime.now(timezone.utc)
            
            elapsed = (now_aware - dep_time).total_seconds()
            duration_seconds = max(trip.planned_duration * 60, 60)
            
            progress = min((elapsed / duration_seconds) * 100.0, 99.5)
            progress = max(progress, 0.0)
            
            lat = source_lat + (dest_lat - source_lat) * (progress / 100.0)
            lon = source_lon + (dest_lon - source_lon) * (progress / 100.0)
            speed = 55.0 + (int(elapsed) % 15)  # simulated speed around 55-70 km/h
            remaining = trip.planned_distance * (1.0 - progress / 100.0)
            
            return {
                "lat": lat,
                "lon": lon,
                "progress": progress,
                "speed": speed,
                "remaining_distance": remaining,
                "status": "In Transit"
            }
        
        return {
            "lat": source_lat,
            "lon": source_lon,
            "progress": 0.0,
            "speed": 0.0,
            "remaining_distance": trip.planned_distance,
            "status": "Unknown"
        }

    def update_vehicle_location(self, location_data: LocationUpdate) -> VehicleLocationResponse:
        vehicle = self.session.get(Vehicle, location_data.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")
        
        return VehicleLocationResponse(
            vehicle_id=vehicle.id,
            registration_number=vehicle.registration_number,
            latitude=location_data.latitude,
            longitude=location_data.longitude,
            speed=location_data.speed,
            heading=location_data.heading,
            status=vehicle.status.value
        )

    def get_all_vehicle_locations(self) -> List[VehicleLocationResponse]:
        vehicles = self.session.exec(select(Vehicle).where(Vehicle.status == VehicleStatus.ON_TRIP)).all()
        
        locations = []
        for vehicle in vehicles:
            # Find the active trip for this vehicle
            trip = self.session.exec(
                select(Trip)
                .where(Trip.vehicle_id == vehicle.id)
                .where(Trip.status == TripStatus.DISPATCHED)
            ).first()
            
            lat, lon = 0.0, 0.0
            speed = 0.0
            if trip:
                info = self._get_trip_tracking_info(trip)
                lat, lon = info["lat"], info["lon"]
                speed = info["speed"]
                
            locations.append(VehicleLocationResponse(
                vehicle_id=vehicle.id,
                registration_number=vehicle.registration_number,
                latitude=lat,
                longitude=lon,
                speed=speed,
                heading=90.0,
                status=vehicle.status.value
            ))
        
        return locations

    def get_vehicle_location(self, vehicle_id: int) -> Optional[VehicleLocationResponse]:
        vehicle = self.session.get(Vehicle, vehicle_id)
        if not vehicle:
            return None
            
        trip = self.session.exec(
            select(Trip)
            .where(Trip.vehicle_id == vehicle.id)
            .where(Trip.status == TripStatus.DISPATCHED)
        ).first()
        
        lat, lon = 0.0, 0.0
        speed = 0.0
        if trip:
            info = self._get_trip_tracking_info(trip)
            lat, lon = info["lat"], info["lon"]
            speed = info["speed"]
            
        return VehicleLocationResponse(
            vehicle_id=vehicle.id,
            registration_number=vehicle.registration_number,
            latitude=lat,
            longitude=lon,
            speed=speed,
            heading=90.0,
            status=vehicle.status.value
        )

    def get_active_trip_location(self, trip_id: int) -> Optional[VehicleLocationResponse]:
        trip = self.session.get(Trip, trip_id)
        if not trip or trip.status != TripStatus.DISPATCHED:
            return None
        
        vehicle = self.session.get(Vehicle, trip.vehicle_id)
        if not vehicle:
            return None
            
        info = self._get_trip_tracking_info(trip)
        return VehicleLocationResponse(
            vehicle_id=vehicle.id,
            registration_number=vehicle.registration_number,
            latitude=info["lat"],
            longitude=info["lon"],
            speed=info["speed"],
            heading=90.0,
            status=vehicle.status.value
        )

    def get_tracking_details(self, tracking_id: str) -> Optional[TrackingDetailResponse]:
        trip = self.session.exec(
            select(Trip).where(Trip.tracking_id == tracking_id)
        ).first()
        if not trip:
            return None
            
        info = self._get_trip_tracking_info(trip)
        return TrackingDetailResponse(
            tracking_id=trip.tracking_id,
            latitude=info["lat"],
            longitude=info["lon"],
            progress_percentage=info["progress"],
            current_speed=info["speed"],
            remaining_distance=info["remaining_distance"],
            estimated_arrival=trip.estimated_arrival,
            current_status=info["status"],
            driver_name=trip.driver_name or "Unknown Driver",
            vehicle_registration=trip.vehicle_registration or "Unknown Reg",
            vehicle_name=trip.vehicle_name or "Unknown Vehicle",
            source=trip.source,
            destination=trip.destination,
            revenue=trip.revenue
        )

    def get_tracking_history(self, tracking_id: str) -> Optional[TrackingTimelineResponse]:
        trip = self.session.exec(
            select(Trip).where(Trip.tracking_id == tracking_id)
        ).first()
        if not trip:
            return None
            
        events = []
        created_at = trip.created_at
        
        # 1. Registered
        events.append(TrackingTimelineEvent(
            status="Order Created",
            description=f"Shipment registered from {trip.source} to {trip.destination}.",
            timestamp=created_at
        ))
        
        # 2. Dispatched
        if trip.status in [TripStatus.DISPATCHED, TripStatus.COMPLETED]:
            disp_time = trip.actual_departure or (created_at + timedelta(minutes=15))
            events.append(TrackingTimelineEvent(
                status="Dispatched",
                description=f"Vehicle {trip.vehicle_registration} driven by {trip.driver_name} departed from {trip.source}.",
                timestamp=disp_time
            ))
            
        # 3. Completed
        if trip.status == TripStatus.COMPLETED:
            comp_time = trip.completed_at or (created_at + timedelta(minutes=trip.planned_duration + 15))
            events.append(TrackingTimelineEvent(
                status="Delivered",
                description=f"Successfully arrived at {trip.destination}. Cargo weight {trip.cargo_weight} kg verified.",
                timestamp=comp_time
            ))
            
        # 4. Cancelled
        if trip.status == TripStatus.CANCELLED:
            cancel_time = trip.completed_at or (created_at + timedelta(minutes=5))
            events.append(TrackingTimelineEvent(
                status="Cancelled",
                description="Delivery cancelled and resources released.",
                timestamp=cancel_time
            ))
            
        return TrackingTimelineResponse(tracking_id=tracking_id, events=events)

    def get_tracking_route(self, tracking_id: str) -> Optional[RouteGeometryResponse]:
        trip = self.session.exec(
            select(Trip).where(Trip.tracking_id == tracking_id)
        ).first()
        if not trip:
            return None
            
        source_lat, source_lon = self._get_city_coords(trip.source)
        dest_lat, dest_lon = self._get_city_coords(trip.destination)
        
        # Create route geometry as simulated street geometry (GeoJSON coordinate list of [lon, lat])
        # We can generate a few intermediate waypoints to make the route look non-linear
        coordinates = []
        steps = 10
        for i in range(steps + 1):
            t = i / steps
            # Add a small curved offset for realistic visual appearance
            offset_factor = 0.15 * (1.0 - (2.0 * t - 1.0) ** 2)  # parabolic offset
            lat = source_lat + (dest_lat - source_lat) * t + offset_factor * (dest_lon - source_lon)
            lon = source_lon + (dest_lon - source_lon) * t - offset_factor * (dest_lat - source_lat)
            coordinates.append([lon, lat])
            
        return RouteGeometryResponse(
            tracking_id=tracking_id,
            route_geometry=trip.route_geometry,
            coordinates=coordinates
        )
