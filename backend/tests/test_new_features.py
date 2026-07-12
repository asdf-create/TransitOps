import pytest
from database.models import User, Role, UserRole, Priority, Vehicle, Driver, Trip, VehicleStatus, DriverStatus, TripStatus
from notifications.models import NotificationCreate
from notifications.service import NotificationService
from email_service.models import EmailSendRequest
from email_service.service import EmailService
from search.service import SearchService

@pytest.fixture
def seeded_user(session):
    role = Role(name=UserRole.ADMINISTRATOR, description="Admin")
    session.add(role)
    session.commit()
    session.refresh(role)
    
    user = User(
        full_name="Seeded User",
        email="test_user@example.com",
        password_hash="hash",
        role_id=role.id,
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def test_notification_lifecycle(session, seeded_user):
    service = NotificationService(session)
    
    # 1. Create notification
    notif_data = NotificationCreate(
        user_id=seeded_user.id,
        title="Test Notification",
        message="This is a test notification",
        priority=Priority.HIGH,
        category="system"
    )
    notif = service.create_notification(notif_data)
    assert notif.id is not None
    assert notif.read is False
    
    # 2. Get notifications
    notifs = service.get_notifications(seeded_user.id, unread_only=True)
    assert len(notifs) == 1
    assert notifs[0].title == "Test Notification"
    
    # 3. Get unread count
    count = service.get_unread_count(seeded_user.id)
    assert count == 1
    
    # 4. Mark read
    marked = service.mark_read(notif.id)
    assert marked.read is True
    assert service.get_unread_count(seeded_user.id) == 0
    
    # 5. Delete notification
    success = service.delete_notification(notif.id)
    assert success is True
    assert len(service.get_notifications(seeded_user.id)) == 0

def test_email_simulation(session):
    # Setup trip
    v = Vehicle(registration_number="MH-12-VT-9999", model="Bolero", manufacturer="Mahindra", vehicle_type="Pickup", year=2022, fuel_type="Diesel", max_load_capacity=2000, acquisition_cost=30000, odometer=1000, region="West")
    d = Driver(full_name="Rajesh Kumar", license_number="DL-999999", license_category="C", license_expiry=datetime_now_naive(), phone="+919876543210", assigned_region="West")
    session.add(v)
    session.add(d)
    session.commit()
    session.refresh(v)
    session.refresh(d)
    
    import datetime
    trip = Trip(
        tracking_id="TRK-999999",
        source="Mumbai",
        destination="Pune",
        vehicle_id=v.id,
        driver_id=d.id,
        cargo_description="Medicines",
        cargo_weight=500,
        planned_distance=150,
        planned_duration=180,
        planned_departure=datetime_now_naive(),
        revenue=3000,
        status=TripStatus.DISPATCHED,
        vehicle_name="Mahindra Bolero",
        driver_name="Rajesh Kumar",
        vehicle_registration="MH-12-VT-9999",
        driver_license_number="DL-999999"
    )
    session.add(trip)
    session.commit()
    session.refresh(trip)
    
    service = EmailService(session)
    
    # 1. Preview
    preview = service.generate_preview(trip.id, "customer@example.com")
    assert "dispatched" in preview.subject
    assert "Rajesh Kumar" in preview.body_html
    
    # 2. Send simulation
    log = service.send_email(trip.id, "customer@example.com")
    assert log.id is not None
    assert log.recipient_email == "customer@example.com"
    
    # 3. History
    history = service.get_history()
    assert len(history) == 1
    assert history[0].trip_id == trip.id

def test_global_search(session):
    # Setup records
    v = Vehicle(registration_number="MH-12-VT-8888", model="Furio", manufacturer="Mahindra", vehicle_type="Pickup", year=2022, fuel_type="Diesel", max_load_capacity=2000, acquisition_cost=30000, odometer=1000, region="West")
    d = Driver(full_name="Vijay Sharma", license_number="DL-888888", license_category="C", license_expiry=datetime_now_naive(), phone="+919876543210", assigned_region="West")
    session.add(v)
    session.add(d)
    session.commit()
    
    service = SearchService(session)
    
    # Search vehicle
    results = service.global_search("Furio")
    assert len(results) >= 1
    assert results[0]["type"] == "vehicle"
    assert "Furio" in results[0]["title"]
    
    # Search driver
    results = service.global_search("Vijay")
    assert len(results) >= 1
    assert results[0]["type"] == "driver"
    assert "Vijay" in results[0]["title"]

def datetime_now_naive():
    import datetime
    return datetime.datetime.now()
