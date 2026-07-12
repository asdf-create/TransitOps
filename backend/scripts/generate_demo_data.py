import sys
import os
import random
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from database.connection import engine, init_db
from database.models import (
    Role, User, UserRole, Vehicle, VehicleStatus,
    Driver, DriverStatus, Trip, TripStatus,
    MaintenanceLog, MaintenanceStatus, FuelLog, Expense
)
from auth.service import get_password_hash
from expenses.models import ExpenseCategory

FIRST_NAMES = ["Amit", "Rahul", "Priya", "Sunita", "Rajesh", "Vikram", "Sneha", "Anil", "John", "Sarah", "David", "Emma"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Singh", "Kumar", "Das", "Joshi", "Smith", "Jones", "Taylor", "Brown"]
CITIES = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Surat"]
CARGOS = ["Electronics", "Automobile Parts", "Pharmaceuticals", "Textiles", "Fresh Produce", "Chemicals", "E-commerce Packages", "Consumer Goods"]

def generate_demo_data():
    print("Initializing Database...")
    init_db()
    
    with Session(engine) as session:
        # 1. Seed Roles
        print("Checking Roles...")
        existing_roles = session.exec(select(Role)).all()
        if not existing_roles:
            roles = [
                Role(name=UserRole.ADMINISTRATOR, description="Full system access"),
                Role(name=UserRole.FLEET_MANAGER, description="Fleet operations management"),
                Role(name=UserRole.DISPATCHER, description="Trip dispatch and management"),
                Role(name=UserRole.DRIVER, description="Driver operations"),
                Role(name=UserRole.SAFETY_OFFICER, description="Safety compliance"),
                Role(name=UserRole.FINANCIAL_ANALYST, description="Financial reporting"),
            ]
            for role in roles:
                session.add(role)
            session.commit()
            print("Roles seeded.")
        else:
            print("Roles already exist.")
            
        admin_role = session.exec(select(Role).where(Role.name == UserRole.ADMINISTRATOR)).first()
        
        # 2. Seed Users
        print("Checking Users...")
        admin_user = session.exec(select(User).where(User.email == "admin@transitops.com")).first()
        if not admin_user:
            admin_user = User(
                full_name="System Administrator",
                email="admin@transitops.com",
                password_hash=get_password_hash("admin123"),
                role_id=admin_role.id,
                phone="+919876543210",
                is_active=True
            )
            session.add(admin_user)
            session.commit()
            print("Admin user seeded.")
        else:
            print("Admin user already exists.")

        # 3. Seed Vehicles (500)
        print("Checking Vehicles...")
        existing_vehicles_count = len(session.exec(select(Vehicle)).all())
        if existing_vehicles_count < 500:
            to_add = 500 - existing_vehicles_count
            print(f"Seeding {to_add} Vehicles...")
            
            manufacturers = [
                ("Tata", ["LPT 1613", "Signa", "Prima", "Ultra", "Ace"]),
                ("Mahindra", ["Bolero Pik-Up", "Furio", "Blazo X", "Supro"]),
                ("Ashok Leyland", ["Dost", "Bada Dost", "Ecomet", "Partner", "U-Truck"]),
                ("Toyota", ["Hilux", "HiAce"]),
                ("Mercedes-Benz", ["Actros", "Atego", "Sprinter"]),
                ("Ford", ["Transit", "F-150"])
            ]
            
            v_types = ["Van", "Light Truck", "Heavy Truck", "Pickup", "Container"]
            fuel_types = ["Diesel", "Diesel", "Diesel", "Petrol", "CNG", "Electric"]
            regions = ["North", "South", "East", "West", "Central"]
            
            vehicles = []
            for i in range(to_add):
                make, models = random.choice(manufacturers)
                model = random.choice(models)
                v_type = random.choice(v_types)
                fuel = random.choice(fuel_types)
                region = random.choice(regions)
                reg_num = f"MH-12-VT-{1000 + i}"
                vin = f"VIN{random.randint(100000000, 999999999)}XYZ"
                
                vehicle = Vehicle(
                    registration_number=reg_num,
                    model=model,
                    manufacturer=make,
                    vehicle_type=v_type,
                    year=random.randint(2016, 2024),
                    vin=vin,
                    fuel_type=fuel,
                    max_load_capacity=float(random.randint(1000, 15000)),
                    acquisition_cost=float(random.randint(20000, 120000)),
                    odometer=float(random.randint(1000, 250000)),
                    status=random.choice([VehicleStatus.AVAILABLE, VehicleStatus.AVAILABLE, VehicleStatus.ON_TRIP, VehicleStatus.IN_SHOP]),
                    region=region,
                    notes=f"Seeded vehicle {reg_num}"
                )
                vehicles.append(vehicle)
                session.add(vehicle)
                if len(vehicles) % 100 == 0:
                    session.commit()
            session.commit()
            print("Vehicles seeded.")
        else:
            print("Vehicles already exist.")

        # 4. Seed Drivers (100)
        print("Checking Drivers...")
        existing_drivers_count = len(session.exec(select(Driver)).all())
        if existing_drivers_count < 100:
            to_add = 100 - existing_drivers_count
            print(f"Seeding {to_add} Drivers...")
            
            categories = ["C", "CE", "D", "DE", "Light"]
            regions = ["North", "South", "East", "West", "Central"]
            
            drivers = []
            for i in range(to_add):
                fname = random.choice(FIRST_NAMES)
                lname = random.choice(LAST_NAMES)
                lic_num = f"DL-{random.randint(100000, 999999)}"
                region = random.choice(regions)
                
                driver = Driver(
                    full_name=f"{fname} {lname}",
                    license_number=lic_num,
                    license_category=random.choice(categories),
                    license_expiry=datetime.now() + timedelta(days=random.randint(30, 1500)),
                    phone=f"+919{random.randint(10000000, 99999999)}",
                    safety_score=float(random.randint(70, 100)),
                    years_experience=random.randint(1, 20),
                    assigned_region=region,
                    status=random.choice([DriverStatus.AVAILABLE, DriverStatus.AVAILABLE, DriverStatus.ON_TRIP, DriverStatus.OFF_DUTY]),
                    total_trips=random.randint(5, 200),
                    total_distance=float(random.randint(500, 80000))
                )
                drivers.append(driver)
                session.add(driver)
            session.commit()
            print("Drivers seeded.")
        else:
            print("Drivers already exist.")

        all_vehicles = session.exec(select(Vehicle)).all()
        all_drivers = session.exec(select(Driver)).all()
        
        vehicle_ids = [v.id for v in all_vehicles]
        driver_ids = [d.id for d in all_drivers]

        # 5. Seed Trips (2,000)
        print("Checking Trips...")
        existing_trips = session.exec(select(Trip)).all()
        existing_trips_count = len(existing_trips)
        used_tracking_ids = {t.tracking_id for t in existing_trips}
        
        if existing_trips_count < 2000:
            to_add = 2000 - existing_trips_count
            print(f"Seeding {to_add} Trips...")
            
            trips = []
            for i in range(to_add):
                src = random.choice(CITIES)
                dest = random.choice([c for c in CITIES if c != src])
                vehicle_id = random.choice(vehicle_ids)
                driver_id = random.choice(driver_ids)
                
                v_obj = session.get(Vehicle, vehicle_id)
                d_obj = session.get(Driver, driver_id)
                
                dist = float(random.randint(100, 1200))
                duration = int(dist / random.randint(50, 70) * 60) # minutes
                
                status_choice = random.choices(
                    [TripStatus.COMPLETED, TripStatus.DISPATCHED, TripStatus.DRAFT, TripStatus.CANCELLED],
                    weights=[75, 15, 7, 3],
                    k=1
                )[0]
                
                planned_dep = datetime.now() - timedelta(days=random.randint(1, 180))
                actual_dep = planned_dep + timedelta(minutes=random.randint(-15, 30)) if status_choice in [TripStatus.DISPATCHED, TripStatus.COMPLETED] else None
                actual_arr = actual_dep + timedelta(minutes=duration + random.randint(-60, 120)) if status_choice == TripStatus.COMPLETED else None
                
                while True:
                    trk_id = f"TRK-{random.randint(100000, 999999)}"
                    if trk_id not in used_tracking_ids:
                        used_tracking_ids.add(trk_id)
                        break
                
                trip = Trip(
                    tracking_id=trk_id,
                    source=src,
                    destination=dest,
                    vehicle_id=vehicle_id,
                    driver_id=driver_id,
                    cargo_description=random.choice(CARGOS),
                    cargo_weight=float(random.randint(500, int(v_obj.max_load_capacity))),
                    planned_distance=dist,
                    actual_distance=dist if status_choice == TripStatus.COMPLETED else None,
                    planned_duration=duration,
                    actual_duration=duration if status_choice == TripStatus.COMPLETED else None,
                    planned_departure=planned_dep,
                    actual_departure=actual_dep,
                    estimated_arrival=planned_dep + timedelta(minutes=duration),
                    actual_arrival=actual_arr,
                    revenue=float(random.randint(1000, 15000)),
                    status=status_choice,
                    completed_at=actual_arr if status_choice == TripStatus.COMPLETED else None,
                    vehicle_name=f"{v_obj.manufacturer} {v_obj.model}",
                    driver_name=d_obj.full_name,
                    vehicle_registration=v_obj.registration_number,
                    driver_license_number=d_obj.license_number
                )
                trips.append(trip)
                session.add(trip)
                if len(trips) % 200 == 0:
                    session.commit()
            session.commit()
            print("Trips seeded.")
        else:
            print("Trips already exist.")

        # 6. Seed Maintenance Logs (300)
        print("Checking Maintenance...")
        existing_maint_count = len(session.exec(select(MaintenanceLog)).all())
        if existing_maint_count < 300:
            to_add = 300 - existing_maint_count
            print(f"Seeding {to_add} Maintenance Logs...")
            
            maint_types = ["Preventative Maintenance", "Engine Diagnostic", "Brake Pad Change", "Tire Replacement", "Transmission Check", "AC Repair"]
            maint_statuses = [MaintenanceStatus.COMPLETED, MaintenanceStatus.COMPLETED, MaintenanceStatus.SCHEDULED, MaintenanceStatus.IN_PROGRESS]
            
            logs = []
            for i in range(to_add):
                v_id = random.choice(vehicle_ids)
                m_type = random.choice(maint_types)
                sched_date = datetime.now() - timedelta(days=random.randint(1, 180))
                status_choice = random.choice(maint_statuses)
                
                started_date = sched_date + timedelta(hours=random.randint(1, 4)) if status_choice in [MaintenanceStatus.IN_PROGRESS, MaintenanceStatus.COMPLETED] else None
                completed_date = started_date + timedelta(days=random.randint(1, 5)) if status_choice == MaintenanceStatus.COMPLETED else None
                
                est_cost = float(random.randint(500, 8000))
                act_cost = est_cost * random.uniform(0.9, 1.2) if status_choice == MaintenanceStatus.COMPLETED else None
                
                log = MaintenanceLog(
                    vehicle_id=v_id,
                    maintenance_type=m_type,
                    description=f"Scheduled {m_type} for vehicle {v_id}.",
                    scheduled_date=sched_date,
                    started_date=started_date,
                    completed_date=completed_date,
                    estimated_cost=est_cost,
                    actual_cost=act_cost,
                    status=status_choice,
                    mechanic_notes=f"Notes for {m_type}."
                )
                logs.append(log)
                session.add(log)
            session.commit()
            print("Maintenance Logs seeded.")
        else:
            print("Maintenance Logs already exist.")

        # 7. Seed Fuel Logs (5,000)
        print("Checking Fuel Logs...")
        existing_fuel_count = len(session.exec(select(FuelLog)).all())
        if existing_fuel_count < 5000:
            to_add = 5000 - existing_fuel_count
            print(f"Seeding {to_add} Fuel Logs...")
            
            logs = []
            for i in range(to_add):
                v_id = random.choice(vehicle_ids)
                d_id = random.choice(driver_ids)
                v_obj = session.get(Vehicle, v_id)
                
                liters = float(random.randint(30, 200))
                cost = liters * random.uniform(85, 105)
                
                log = FuelLog(
                    vehicle_id=v_id,
                    driver_id=d_id,
                    liters=liters,
                    cost=cost,
                    odometer=v_obj.odometer - random.randint(100, 1000) * (i // 1000 + 1),
                    station=f"{random.choice(['IndianOil', 'HP Pay', 'Bharat Petroleum', 'Shell'])} Station",
                    timestamp=datetime.now() - timedelta(days=random.randint(1, 180))
                )
                logs.append(log)
                session.add(log)
                if len(logs) % 500 == 0:
                    session.commit()
            session.commit()
            print("Fuel Logs seeded.")
        else:
            print("Fuel Logs already exist.")

        # 8. Seed Expenses (2,500)
        print("Checking Expenses...")
        existing_expenses_count = len(session.exec(select(Expense)).all())
        if existing_expenses_count < 2500:
            to_add = 2500 - existing_expenses_count
            print(f"Seeding {to_add} Expenses...")
            
            categories = list(ExpenseCategory)
            
            expenses = []
            for i in range(to_add):
                v_id = random.choice(vehicle_ids)
                cat = random.choice(categories)
                amount = float(random.randint(100, 8000))
                
                expense = Expense(
                    vehicle_id=v_id,
                    category=cat,
                    amount=amount,
                    description=f"Expense for {cat.value}.",
                    expense_date=datetime.now() - timedelta(days=random.randint(1, 180))
                )
                expenses.append(expense)
                session.add(expense)
                if len(expenses) % 500 == 0:
                    session.commit()
            session.commit()
            print("Expenses seeded.")
        else:
            print("Expenses already exist.")
            
        print("Demo Database Generation Completed Successfully!")

if __name__ == "__main__":
    generate_demo_data()
