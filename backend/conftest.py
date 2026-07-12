import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

# Use in-memory SQLite so tests never touch the production database
TEST_DATABASE_URL = "sqlite://"


@pytest.fixture(scope="function")
def session():
    """Create a fresh in-memory database session for each test."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)
