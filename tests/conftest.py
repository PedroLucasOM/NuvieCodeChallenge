import pytest
import pytest_asyncio
import asyncio
import sqlite3
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from app.main import app
from app.database.connection import get_db, Base

from app.models.user import User as UserModel
from app.models.patient import Patient as PatientModel

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test_database.db"
test_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False
)
TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

def create_test_tables():
    """Create tables using synchronous SQLAlchemy for reliability."""
    sync_engine = create_engine("sqlite:///./test_database.db")
    Base.metadata.create_all(bind=sync_engine)
    sync_engine.dispose()

create_test_tables()

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
def clean_database():
    """Clean database before each test."""
    sync_engine = create_engine("sqlite:///./test_database.db")
    with sync_engine.begin() as conn:
        try:
            conn.execute(text("DELETE FROM patients"))
        except:
            pass
        try:
            conn.execute(text("DELETE FROM users"))
        except:
            pass
    sync_engine.dispose()
    
    yield
    
    sync_engine = create_engine("sqlite:///./test_database.db")
    with sync_engine.begin() as conn:
        try:
            conn.execute(text("DELETE FROM patients"))
        except:
            pass
        try:
            conn.execute(text("DELETE FROM users"))
        except:
            pass
    sync_engine.dispose()

@pytest_asyncio.fixture
async def db_session():
    """Provide a database session for tests that need it directly."""
    async with TestingSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def override_get_db():
    """Override the get_db dependency for testing."""
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Provide a test client."""
    return TestClient(app)
