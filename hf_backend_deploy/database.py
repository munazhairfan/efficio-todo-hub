from sqlmodel import create_engine, Session
from typing import Generator


# Create database engine
# For now, using SQLite for simplicity. In production, you'd use PostgreSQL connection
DATABASE_URL = "sqlite:///./todo_app.db"  # Change this to your actual database URL

engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session