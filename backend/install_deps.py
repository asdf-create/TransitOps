import subprocess
import sys

print("Installing backend dependencies...")
packages = [
    "fastapi>=0.115.0",
    "uvicorn>=0.32.0",
    "sqlmodel>=0.0.22",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.6.0",
    "passlib[bcrypt]>=1.7.4",
    "python-jose[cryptography]>=3.3.0",
    "python-multipart>=0.0.12",
    "alembic>=1.14.0",
    "email-validator>=2.1.0",
]

for package in packages:
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("All dependencies installed successfully!")
