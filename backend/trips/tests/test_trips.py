import pytest
from datetime import datetime, timedelta, timezone
from database.models import Vehicle, Driver, Trip, VehicleStatus, DriverStatus, TripStatus
from trips.service import TripService
from trips.models import TripCreate

@pytest.fixture
def trip_service(session):
    return TripService(session)

@pytest.fixture
def available_vehicle(session):
    vehicle = Vehicle(
        registration_number="TEST-VEH-001",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        status=VehicleStatus.AVAILABLE,
        region="North"
    )
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return vehicle

@pytest.fixture
def available_driver(session):
    driver = Driver(
        full_name="Test Driver",
        license_number="TEST-LIC-001",
        license_category="C",
        license_expiry=datetime.now() + timedelta(days=365),
        phone="+1234567890",
        safety_score=95.0,
        years_experience=5,
        assigned_region="North",
        status=DriverStatus.AVAILABLE
    )
    session.add(driver)
    session.commit()
    session.refresh(driver)
    return driver

def test_create_trip(trip_service, available_vehicle, available_driver):
    """Test basic trip creation"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    
    assert trip.id is not None
    assert trip.status == TripStatus.DRAFT
    assert trip.tracking_id.startswith("TRK-")
    assert trip.vehicle_id == available_vehicle.id
    assert trip.driver_id == available_driver.id

def test_create_trip_invalid_vehicle(trip_service, available_driver):
    """Test trip creation with non-existent vehicle"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=99999,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(ValueError, match="Vehicle not found"):
        trip_service.create_trip(trip_data)

def test_create_trip_invalid_driver(trip_service, available_vehicle):
    """Test trip creation with non-existent driver"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=99999,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(ValueError, match="Driver not found"):
        trip_service.create_trip(trip_data)

def test_create_trip_retired_vehicle(session, trip_service, available_driver):
    """Test trip creation with retired vehicle"""
    vehicle = Vehicle(
        registration_number="TEST-VEH-002",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        status=VehicleStatus.RETIRED,
        region="North"
    )
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(ValueError, match="RETIRED"):
        trip_service.create_trip(trip_data)

def test_create_trip_in_shop_vehicle(session, trip_service, available_driver):
    """Test trip creation with vehicle in shop"""
    vehicle = Vehicle(
        registration_number="TEST-VEH-003",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        status=VehicleStatus.IN_SHOP,
        region="North"
    )
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(ValueError, match="IN_SHOP"):
        trip_service.create_trip(trip_data)

def test_create_trip_vehicle_on_trip(session, trip_service, available_driver):
    """Test trip creation with vehicle already on trip"""
    vehicle = Vehicle(
        registration_number="TEST-VEH-004",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        status=VehicleStatus.ON_TRIP,
        region="North"
    )
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(ValueError, match="ON_TRIP"):
        trip_service.create_trip(trip_data)

def test_create_trip_suspended_driver(session, trip_service, available_vehicle):
    """Test trip creation with suspended driver"""
    driver = Driver(
        full_name="Test Driver",
        license_number="TEST-LIC-002",
        license_category="C",
        license_expiry=datetime.now() + timedelta(days=365),
        phone="+1234567890",
        safety_score=95.0,
        years_experience=5,
        assigned_region="North",
        status=DriverStatus.SUSPENDED
    )
    session.add(driver)
    session.commit()
    session.refresh(driver)
    
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(ValueError, match="SUSPENDED"):
        trip_service.create_trip(trip_data)

def test_create_trip_expired_license(session, trip_service, available_vehicle):
    """Test trip creation with expired driver license"""
    driver = Driver(
        full_name="Test Driver",
        license_number="TEST-LIC-003",
        license_category="C",
        license_expiry=datetime.now() - timedelta(days=1),
        phone="+1234567890",
        safety_score=95.0,
        years_experience=5,
        assigned_region="North",
        status=DriverStatus.AVAILABLE
    )
    session.add(driver)
    session.commit()
    session.refresh(driver)
    
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(ValueError, match="expired"):
        trip_service.create_trip(trip_data)

def test_create_trip_driver_on_trip(session, trip_service, available_vehicle):
    """Test trip creation with driver already on trip"""
    driver = Driver(
        full_name="Test Driver",
        license_number="TEST-LIC-004",
        license_category="C",
        license_expiry=datetime.now() + timedelta(days=365),
        phone="+1234567890",
        safety_score=95.0,
        years_experience=5,
        assigned_region="North",
        status=DriverStatus.ON_TRIP
    )
    session.add(driver)
    session.commit()
    session.refresh(driver)
    
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(ValueError, match="ON_TRIP"):
        trip_service.create_trip(trip_data)

def test_create_trip_exceeds_capacity(trip_service, available_vehicle, available_driver):
    """Test trip creation with cargo exceeding vehicle capacity"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=10000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(ValueError, match="exceeds vehicle capacity"):
        trip_service.create_trip(trip_data)

def test_dispatch_trip(trip_service, available_vehicle, available_driver):
    """Test trip dispatch"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    dispatched_trip = trip_service.dispatch_trip(trip.id)
    
    assert dispatched_trip.status == TripStatus.DISPATCHED
    assert dispatched_trip.actual_departure is not None

def test_dispatch_trip_status_changes(trip_service, available_vehicle, available_driver):
    """Test that dispatch changes vehicle and driver status"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    trip_service.dispatch_trip(trip.id)
    
    # Refresh to get updated vehicle and driver status
    session = trip_service.session
    vehicle = session.get(Vehicle, available_vehicle.id)
    driver = session.get(Driver, available_driver.id)
    
    assert vehicle.status == VehicleStatus.ON_TRIP
    assert driver.status == DriverStatus.ON_TRIP

def test_dispatch_non_draft_trip(trip_service, available_vehicle, available_driver):
    """Test dispatching a non-draft trip"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    trip.status = TripStatus.COMPLETED
    trip_service.session.add(trip)
    trip_service.session.commit()
    
    with pytest.raises(ValueError, match="Only draft trips"):
        trip_service.dispatch_trip(trip.id)

def test_complete_trip(trip_service, available_vehicle, available_driver):
    """Test trip completion"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    trip_service.dispatch_trip(trip.id)
    
    completed_trip = trip_service.complete_trip(trip.id, 105.0, 115)
    
    assert completed_trip.status == TripStatus.COMPLETED
    assert completed_trip.actual_distance == 105.0
    assert completed_trip.actual_duration == 115
    assert completed_trip.completed_at is not None

def test_complete_trip_status_restoration(trip_service, available_vehicle, available_driver):
    """Test that completion restores vehicle and driver status"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    trip_service.dispatch_trip(trip.id)
    trip_service.complete_trip(trip.id, 105.0, 115)
    
    session = trip_service.session
    vehicle = session.get(Vehicle, available_vehicle.id)
    driver = session.get(Driver, available_driver.id)
    
    assert vehicle.status == VehicleStatus.AVAILABLE
    assert driver.status == DriverStatus.AVAILABLE

def test_complete_trip_updates_odometer(trip_service, available_vehicle, available_driver):
    """Test that completion updates vehicle odometer"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    trip_service.dispatch_trip(trip.id)
    
    initial_odometer = available_vehicle.odometer
    trip_service.complete_trip(trip.id, 105.0, 115)
    
    session = trip_service.session
    vehicle = session.get(Vehicle, available_vehicle.id)
    
    assert vehicle.odometer == initial_odometer + 105.0

def test_complete_trip_updates_driver_stats(trip_service, available_vehicle, available_driver):
    """Test that completion updates driver statistics"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    trip_service.dispatch_trip(trip.id)
    
    initial_trips = available_driver.total_trips
    initial_distance = available_driver.total_distance
    trip_service.complete_trip(trip.id, 105.0, 115)
    
    session = trip_service.session
    driver = session.get(Driver, available_driver.id)
    
    assert driver.total_trips == initial_trips + 1
    assert driver.total_distance == initial_distance + 105.0

def test_cancel_trip(trip_service, available_vehicle, available_driver):
    """Test trip cancellation"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    cancelled_trip = trip_service.cancel_trip(trip.id)
    
    assert cancelled_trip.status == TripStatus.CANCELLED

def test_cancel_dispatched_trip_restores_status(trip_service, available_vehicle, available_driver):
    """Test that cancelling dispatched trip restores status"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    trip_service.dispatch_trip(trip.id)
    trip_service.cancel_trip(trip.id)
    
    session = trip_service.session
    vehicle = session.get(Vehicle, available_vehicle.id)
    driver = session.get(Driver, available_driver.id)
    
    assert vehicle.status == VehicleStatus.AVAILABLE
    assert driver.status == DriverStatus.AVAILABLE

def test_double_completion(trip_service, available_vehicle, available_driver):
    """Test that completing a trip twice raises error"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    trip_service.dispatch_trip(trip.id)
    trip_service.complete_trip(trip.id, 105.0, 115)
    
    with pytest.raises(ValueError, match="Only dispatched trips"):
        trip_service.complete_trip(trip.id, 105.0, 115)

def test_invalid_distance(trip_service, available_vehicle, available_driver):
    """Test trip creation with invalid distance"""
    with pytest.raises(Exception):
        trip_data = TripCreate(
            source="Warehouse A",
            destination="Warehouse B",
            vehicle_id=available_vehicle.id,
            driver_id=available_driver.id,
            cargo_description="Test cargo",
            cargo_weight=3000.0,
            planned_distance=-100.0,
            planned_duration=120,
            planned_departure=datetime.now(),
            revenue=500.0
        )
        trip_service.create_trip(trip_data)

def test_missing_destination(trip_service, available_vehicle, available_driver):
    """Test trip creation with missing destination"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    with pytest.raises(Exception):
        trip_service.create_trip(trip_data)

def test_historical_snapshots(trip_service, available_vehicle, available_driver):
    """Test that historical snapshots are preserved"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    
    assert trip.vehicle_name == f"{available_vehicle.manufacturer} {available_vehicle.model}"
    assert trip.driver_name == available_driver.full_name
    assert trip.vehicle_registration == available_vehicle.registration_number
    assert trip.driver_license_number == available_driver.license_number

def test_tracking_id_generation(trip_service, available_vehicle, available_driver):
    """Test that tracking IDs are unique"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip1 = trip_service.create_trip(trip_data)
    trip2 = trip_service.create_trip(trip_data)
    
    assert trip1.tracking_id != trip2.tracking_id
    assert trip1.tracking_id.startswith("TRK-")
    assert trip2.tracking_id.startswith("TRK-")

def test_eta_calculation(trip_service, available_vehicle, available_driver):
    """Test ETA calculation"""
    # Use naive datetime to match SQLite storage (no timezone info)
    departure_time = datetime.now()
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=departure_time,
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    
    expected_eta = departure_time + timedelta(minutes=120)
    assert trip.estimated_arrival == expected_eta

def test_get_trip_by_tracking_id(trip_service, available_vehicle, available_driver):
    """Test getting trip by tracking ID"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    retrieved_trip = trip_service.get_trip_by_tracking_id(trip.tracking_id)
    
    assert retrieved_trip is not None
    assert retrieved_trip.id == trip.id
    assert retrieved_trip.tracking_id == trip.tracking_id

def test_get_trip_with_filters(trip_service, available_vehicle, available_driver):
    """Test getting trips with filters"""
    trip_data = TripCreate(
        source="Warehouse A",
        destination="Warehouse B",
        vehicle_id=available_vehicle.id,
        driver_id=available_driver.id,
        cargo_description="Test cargo",
        cargo_weight=3000.0,
        planned_distance=100.0,
        planned_duration=120,
        planned_departure=datetime.now(),
        revenue=500.0
    )
    
    trip = trip_service.create_trip(trip_data)
    
    draft_trips = trip_service.get_trips(status=TripStatus.DRAFT)
    assert len(draft_trips) >= 1
    assert all(t.status == TripStatus.DRAFT for t in draft_trips)
    
    vehicle_trips = trip_service.get_trips(vehicle_id=available_vehicle.id)
    assert len(vehicle_trips) >= 1
    assert all(t.vehicle_id == available_vehicle.id for t in vehicle_trips)
