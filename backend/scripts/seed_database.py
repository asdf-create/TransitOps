import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from database.connection import engine, get_session
from database.models import Role, User, UserRole
from auth.service import get_password_hash

def seed_database():
    with Session(engine) as session:
        # Check if roles already exist
        existing_roles = session.exec(select(Role)).all()
        if not existing_roles:
            print("Seeding roles...")
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
            print("Roles seeded successfully")
        else:
            print("Roles already exist")

        # Check if admin user exists
        existing_admin = session.exec(select(User).where(User.email == "admin@transitops.com")).first()
        if not existing_admin:
            print("Creating admin user...")
            admin_role = session.exec(select(Role).where(Role.name == UserRole.ADMINISTRATOR)).first()
            admin_user = User(
                full_name="System Administrator",
                email="admin@transitops.com",
                password_hash=get_password_hash("admin123"),
                role_id=admin_role.id,
                phone="+1234567890",
                is_active=True
            )
            session.add(admin_user)
            session.commit()
            print("Admin user created successfully")
        else:
            print("Admin user already exists")

        print("Database seeding completed!")

if __name__ == "__main__":
    seed_database()
