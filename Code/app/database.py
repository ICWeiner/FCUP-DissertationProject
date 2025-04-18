from sqlmodel import SQLModel, Session, create_engine
from app.config import settings

from pathlib import Path

BASE_DIR = Path(__file__).parent

sqlite_url = settings.DATABASE_URL

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        yield session
