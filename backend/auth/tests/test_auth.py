import pytest
from sqlmodel import Session
from database.models import User, Role
from auth.service import authenticate_user, create_user, get_password_hash, verify_password
from auth.models import UserCreate

@pytest.fixture
def test_role(session):
    role = Role(name="Test Role", description="Test role for unit tests")
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

def test_password_hashing():
    """Test password hashing and verification"""
    password = "pass123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpass", hashed) is False

def test_create_user(session, test_role):
    """Test user creation"""
    user_data = UserCreate(
        full_name="Test User",
        email="test@example.com",
        password="testpass",
        role_id=test_role.id,
        phone="+1234567890"
    )
    
    user = create_user(session, user_data.model_dump())
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.password_hash != "secure_password"
    assert user.role_id == test_role.id
    assert user.is_active is True

def test_create_duplicate_user(session, test_role):
    """Test duplicate email rejection"""
    user_data = UserCreate(
        full_name="Test User",
        email="test@example.com",
        password="testpass",
        role_id=test_role.id
    )
    
    create_user(session, user_data.model_dump())
    
    with pytest.raises(ValueError, match="already exists"):
        create_user(session, user_data.model_dump())

def test_authenticate_valid_user(session, test_role):
    """Test successful authentication"""
    user_data = UserCreate(
        full_name="Test User",
        email="auth@example.com",
        password="testpass",
        role_id=test_role.id
    )
    
    create_user(session, user_data.model_dump())
    
    authenticated_user = authenticate_user(session, "auth@example.com", "testpass")
    
    assert authenticated_user is not None
    assert authenticated_user.email == "auth@example.com"

def test_authenticate_invalid_password(session, test_role):
    """Test authentication with wrong password"""
    user_data = UserCreate(
        full_name="Test User",
        email="auth@example.com",
        password="correctpass",
        role_id=test_role.id
    )
    
    create_user(session, user_data.model_dump())
    
    authenticated_user = authenticate_user(session, "auth@example.com", "wrong_password")
    
    assert authenticated_user is None

def test_authenticate_nonexistent_user(session):
    """Test authentication with non-existent user"""
    authenticated_user = authenticate_user(session, "nonexistent@example.com", "password")
    
    assert authenticated_user is None

def test_authenticate_inactive_user(session, test_role):
    """Test authentication with inactive user"""
    user_data = UserCreate(
        full_name="Test User",
        email="inactive@example.com",
        password="testpass",
        role_id=test_role.id
    )
    
    user = create_user(session, user_data.model_dump())
    user.is_active = False
    session.add(user)
    session.commit()
    
    authenticated_user = authenticate_user(session, "inactive@example.com", "testpass")
    
    assert authenticated_user is not None
    assert authenticated_user.is_active is False

def test_user_validation_missing_email(session, test_role):
    """Test user creation with missing email"""
    user_data = {
        "full_name": "Test User",
        "password": "password",
        "role_id": test_role.id
    }
    
    with pytest.raises(Exception):
        create_user(session, user_data)

def test_user_validation_missing_password(session, test_role):
    """Test user creation with missing password"""
    user_data = {
        "full_name": "Test User",
        "email": "test@example.com",
        "role_id": test_role.id
    }
    
    with pytest.raises(Exception):
        create_user(session, user_data)

def test_user_validation_missing_role(session):
    """Test user creation with missing role"""
    user_data = {
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "password"
    }
    
    with pytest.raises(Exception):
        create_user(session, user_data)
