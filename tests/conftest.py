import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from alembic import command
from alembic.config import Config
from app.db.session import database
from app.main import app
from httpx import AsyncClient

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac  

@pytest.fixture
async def test_db():
    async with database.async_session() as session:
        yield session  
        await session.rollback() 
