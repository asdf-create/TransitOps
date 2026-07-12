import pytest
from sqlmodel import SQLModel, Session
from database.connection import engine

@pytest.fixture(scope="function")
def session():
    """Create a fresh database session for each test"""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)
