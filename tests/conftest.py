import pytest
import pytest_asyncio
import asyncio

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
async def test_db() -> AsyncSession:
    async for session in database.get_db():
        await session.begin() 
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(test_db) -> AsyncClient:
    async def override_get_db():
        yield test_db

    app.dependency_overrides[database.get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost:8000") as ac:
        yield ac
    app.dependency_overrides.clear()    


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()