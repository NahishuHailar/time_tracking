import asyncio
import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import PostgresSettings
from app.db.session import get_database
from app.main import app
from tests.const import test_db_sett


@pytest.fixture(scope="session", autouse=True)
def set_env_sett():
    for key, value in test_db_sett.items():
        os.environ[key.upper()] = str(value)


@pytest.fixture(scope="session", autouse=True)
def reset_test_db():
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")


    async def recreate_db():
        engine = create_async_engine(PostgresSettings.get_settings().url)

        async with engine.begin() as conn:
            result = await conn.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            )
            tables = [row[0] for row in result.fetchall()]

            for table in tables:
                await conn.execute(text(f"DROP TABLE {table} CASCADE"))


        await engine.dispose()

    asyncio.run(recreate_db())
    command.upgrade(alembic_cfg, "head")


@pytest_asyncio.fixture
async def test_db() -> AsyncSession:
    async for session in get_database().get_client():
        await session.begin()
        yield session
        await session.rollback()


@pytest_asyncio.fixture(autouse=True)
async def clean_db(test_db: AsyncSession):
    async with test_db as session:
        result = await session.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        )
        tables = [row[0] for row in result.fetchall()]

        for table in tables:
            await session.execute(
                text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
            )
        await session.commit()


@pytest_asyncio.fixture
async def client(test_db) -> AsyncClient:
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_database().get_client] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
