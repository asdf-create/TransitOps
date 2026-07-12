"""Database connection and session management with SQLite WAL mode and FK support."""
import logging
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import Engine
from sqlalchemy import event

from core.config import settings

logger = logging.getLogger(__name__)

engine: Engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def set_sqlite_pragmas(dbapi_connection, connection_record):
    """Enable WAL mode and foreign key enforcement on every new connection."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def init_db():
    """Create all tables from SQLModel metadata."""
    SQLModel.metadata.create_all(engine)
    logger.info("Database initialized successfully")


def get_session():
    """FastAPI dependency that yields a database session."""
    with Session(engine) as session:
        yield session
