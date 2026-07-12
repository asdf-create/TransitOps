from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import Engine

DATABASE_URL = "sqlite:///./transitops.db"

engine: Engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
