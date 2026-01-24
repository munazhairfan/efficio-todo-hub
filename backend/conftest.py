"""
Test configuration file for pytest
Contains fixtures and setup/teardown functions for testing
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database.session import get_db, Base
from src.models.task import Task
from src.models.user import User
from sqlmodel import SQLModel

# Use a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables for both SQLAlchemy and SQLModel
Base.metadata.create_all(bind=engine)
SQLModel.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_client():
    """Create a test client for API testing"""
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
def db_session():
    """Create a database session for testing with rollback"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def create_test_user(db_session):
    """Helper to create a test user"""
    def _create_test_user(email="test@example.com", name="Test User"):
        from src.models.user import User
        user = User(email=email, name=name)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    return _create_test_user

@pytest.fixture
def create_test_task(db_session, create_test_user):
    """Helper to create a test task"""
    def _create_test_task(user_id, title="Test Task", description="Test Description"):
        from src.models.task import Task
        user = create_test_user()
        task = Task(user_id=user.id, title=title, description=description)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task
    return _create_test_task