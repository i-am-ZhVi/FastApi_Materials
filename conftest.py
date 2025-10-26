import sys
import os
import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from testcontainers.postgres import PostgresContainer
from app.main import app
from app.database.session import get_db
from app.database.migration_utils import run_migrations

username = "postgres"
password = "postgres"
dbname = "fastapi_test"

@pytest_asyncio.fixture(scope="session")
async def postgres_container():

    with PostgresContainer(
        image="postgres:15",
        username=username,
        password=password,
        dbname=dbname
    ) as postgres:

        postgres.start()
        import time
        time.sleep(3)

        yield postgres



@pytest_asyncio.fixture(scope="session")
async def test_engine(postgres_container):
    host = postgres_container.get_container_host_ip()
    port = postgres_container.get_exposed_port(5432)
    database_url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{dbname}"

    engine = create_async_engine(
        database_url,
        poolclass=NullPool,
        echo=True
    )

    await run_migrations(database_url)

    yield engine

    await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def TestAsyncSessionLocal(test_engine):
    TestAsyncSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with TestAsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db

    return TestAsyncSessionLocal

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def db_session(TestAsyncSessionLocal):
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
