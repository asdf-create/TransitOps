from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlmodel import Session, select

from database.models import User, Role
from database.connection import get_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_user(session: Session, user_data: dict) -> User:
    # Check for duplicate email
    existing = session.exec(select(User).where(User.email == user_data["email"])).first()
    if existing:
        raise ValueError(f"User with email {user_data['email']} already exists")

    hashed_password = get_password_hash(user_data["password"])
    db_user = User(
        full_name=user_data["full_name"],
        email=user_data["email"],
        password_hash=hashed_password,
        role_id=user_data["role_id"],
        phone=user_data.get("phone")
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
