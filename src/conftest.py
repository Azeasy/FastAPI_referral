import asyncio
import logging

import pytest
import pytest as pytest
import pytest_asyncio
import fakeredis
from httpx import ASGITransport, AsyncClient

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.db.redis import get_cache
from src.db.session import get_db
from src.main import app
from src.db.base import Base

from src.tests.fixtures import *

# Create a new engine for the default database
default_engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create a new engine for the test database
test_engine = create_async_engine(settings.TEST_DATABASE_URL, echo=True)


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def test_db():
    # Create the test database if it does not exist
    async with default_engine.connect() as conn:
        try:
            await conn.execute(text("COMMIT"))  # Ensure no transaction is active
            await conn.execute(text(f"CREATE DATABASE test_db"))
        except ProgrammingError:
            logging.warning("Database already exists, continuing...")

    # Create tables in the test database
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop tables in the test database
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Drop the test database
    async with default_engine.connect() as conn:
        await conn.execute(text("COMMIT"))  # Ensure no transaction is active
        await conn.execute(text("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'test_db'
              AND pid <> pg_backend_pid();
        """))
        await conn.execute(text(f"DROP DATABASE test_db"))


@pytest_asyncio.fixture(scope="module")
async def test_redis():
    # Create a fake Redis instance
    fake_redis = fakeredis.FakeRedis()
    yield fake_redis
    # Close the fake Redis instance
    fake_redis.flushall()
    fake_redis.close()


@pytest_asyncio.fixture(scope="module")
async def db_session(test_db):
    async_session = sessionmaker(bind=test_engine, class_=AsyncSession,
                                 expire_on_commit=False)

    async with async_session() as session:
        yield session
    await session.close()


@pytest_asyncio.fixture(scope="module")
async def client(test_redis, db_session):
    app.dependency_overrides[get_cache] = lambda: test_redis

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000/"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
