import pytest
import pytest_asyncio

import os
from sqlalchemy.ext.asyncio import AsyncSession
from alembic import command
from alembic.config import Config
from app.db.session import database
from app.main import app
from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv

load_dotenv(".env.test") 
os.environ["TESTING"] = "true"

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as ac:
        yield ac

@pytest_asyncio.fixture
async def test_db() -> AsyncSession:
    async for session in database.get_db():
        yield session
        await session.rollback()


