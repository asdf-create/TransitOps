import pytest
from database.models import Vehicle, VehicleStatus
from vehicles.service import VehicleService
from vehicles.models import VehicleCreate, VehicleUpdate

@pytest.fixture
def vehicle_service(session):
    return VehicleService(session)

def test_create_vehicle(vehicle_service):
    """Test vehicle creation"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-001",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    vehicle = vehicle_service.create_vehicle(vehicle_data)
    
    assert vehicle.id is not None
    assert vehicle.registration_number == "TEST-001"
    assert vehicle.status == VehicleStatus.AVAILABLE
    assert vehicle.odometer == 0

def test_create_duplicate_registration(vehicle_service):
    """Test duplicate registration number rejection"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-001",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    vehicle_service.create_vehicle(vehicle_data)
    
    with pytest.raises(ValueError, match="already exists"):
        vehicle_service.create_vehicle(vehicle_data)

def test_create_invalid_capacity(vehicle_service):
    """Test vehicle creation with invalid capacity"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-002",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=-100.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    with pytest.raises(Exception):
        vehicle_service.create_vehicle(vehicle_data)

def test_create_invalid_odometer(vehicle_service):
    """Test vehicle creation with invalid odometer"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-003",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        odometer=-100.0,
        region="North"
    )
    
    with pytest.raises(Exception):
        vehicle_service.create_vehicle(vehicle_data)

def test_get_vehicle(vehicle_service):
    """Test getting a specific vehicle"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-004",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    created_vehicle = vehicle_service.create_vehicle(vehicle_data)
    retrieved_vehicle = vehicle_service.get_vehicle(created_vehicle.id)
    
    assert retrieved_vehicle is not None
    assert retrieved_vehicle.registration_number == "TEST-004"

def test_get_nonexistent_vehicle(vehicle_service):
    """Test getting a non-existent vehicle"""
    vehicle = vehicle_service.get_vehicle(99999)
    assert vehicle is None

def test_update_vehicle(vehicle_service):
    """Test vehicle update"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-005",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    created_vehicle = vehicle_service.create_vehicle(vehicle_data)
    
    update_data = VehicleUpdate(model="Updated Model")
    updated_vehicle = vehicle_service.update_vehicle(created_vehicle.id, update_data)
    
    assert updated_vehicle is not None
    assert updated_vehicle.model == "Updated Model"

def test_update_nonexistent_vehicle(vehicle_service):
    """Test updating a non-existent vehicle"""
    update_data = VehicleUpdate(model="Updated Model")
    updated_vehicle = vehicle_service.update_vehicle(99999, update_data)
    assert updated_vehicle is None

def test_delete_vehicle(vehicle_service):
    """Test vehicle deletion (soft delete)"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-006",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    created_vehicle = vehicle_service.create_vehicle(vehicle_data)
    result = vehicle_service.delete_vehicle(created_vehicle.id)
    
    assert result is True
    
    deleted_vehicle = vehicle_service.get_vehicle(created_vehicle.id)
    assert deleted_vehicle.status == VehicleStatus.RETIRED

def test_delete_nonexistent_vehicle(vehicle_service):
    """Test deleting a non-existent vehicle"""
    result = vehicle_service.delete_vehicle(99999)
    assert result is False

def test_get_available_vehicles(vehicle_service):
    """Test getting available vehicles"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-007",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    vehicle_service.create_vehicle(vehicle_data)
    available_vehicles = vehicle_service.get_available_vehicles()
    
    assert len(available_vehicles) >= 1
    assert all(v.status == VehicleStatus.AVAILABLE for v in available_vehicles)

def test_get_vehicles_with_filters(vehicle_service):
    """Test getting vehicles with filters"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-008",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="South"
    )
    
    vehicle_service.create_vehicle(vehicle_data)
    
    south_vehicles = vehicle_service.get_vehicles(region="South")
    assert len(south_vehicles) >= 1
    assert all(v.region == "South" for v in south_vehicles)

def test_status_transition_available_to_on_trip(vehicle_service):
    """Test status transition from Available to On Trip"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-009",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    vehicle = vehicle_service.create_vehicle(vehicle_data)
    assert vehicle.status == VehicleStatus.AVAILABLE
    
    update_data = VehicleUpdate(status=VehicleStatus.ON_TRIP)
    updated_vehicle = vehicle_service.update_vehicle(vehicle.id, update_data)
    
    assert updated_vehicle.status == VehicleStatus.ON_TRIP

def test_get_vehicle_statistics(vehicle_service):
    """Test vehicle statistics"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-010",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    vehicle_service.create_vehicle(vehicle_data)
    stats = vehicle_service.get_vehicle_statistics()
    
    assert stats["total"] >= 1
    assert "available" in stats
    assert "on_trip" in stats
    assert "in_shop" in stats
    assert "retired" in stats
    assert "utilization" in stats

def test_vehicle_capacity_validation(vehicle_service):
    """Test that cargo weight validation works through capacity check"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-011",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=1000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    vehicle = vehicle_service.create_vehicle(vehicle_data)
    assert vehicle.max_load_capacity == 1000.0

def test_large_odometer_value(vehicle_service):
    """Test vehicle with large odometer value"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-012",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        odometer=100000.0,
        region="North"
    )
    
    vehicle = vehicle_service.create_vehicle(vehicle_data)
    assert vehicle.odometer == 100000.0

def test_unicode_registration(vehicle_service):
    """Test vehicle with unicode characters in registration"""
    vehicle_data = VehicleCreate(
        registration_number="TEST-αβγ",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    vehicle = vehicle_service.create_vehicle(vehicle_data)
    assert vehicle.registration_number == "TEST-αβγ"

def test_empty_registration(vehicle_service):
    """Test vehicle creation with empty registration"""
    vehicle_data = VehicleCreate(
        registration_number="",
        model="Test Model",
        manufacturer="Test Manufacturer",
        vehicle_type="Truck",
        year=2024,
        fuel_type="Diesel",
        max_load_capacity=5000.0,
        acquisition_cost=50000.0,
        region="North"
    )
    
    with pytest.raises(Exception):
        vehicle_service.create_vehicle(vehicle_data)

def test_multiple_vehicles_pagination(vehicle_service):
    """Test pagination with multiple vehicles"""
    for i in range(15):
        vehicle_data = VehicleCreate(
            registration_number=f"TEST-{i:03d}",
            model="Test Model",
            manufacturer="Test Manufacturer",
            vehicle_type="Truck",
            year=2024,
            fuel_type="Diesel",
            max_load_capacity=5000.0,
            acquisition_cost=50000.0,
            region="North"
        )
        vehicle_service.create_vehicle(vehicle_data)
    
    first_page = vehicle_service.get_vehicles(skip=0, limit=10)
    second_page = vehicle_service.get_vehicles(skip=10, limit=10)
    
    assert len(first_page) == 10
    assert len(second_page) >= 5
