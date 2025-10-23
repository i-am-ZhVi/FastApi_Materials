import asyncio
import os
from alembic.config import Config
from alembic import command
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

__config_path__ = "alembic.ini"
__migration_path__ = "migrations"

cfg = Config(__config_path__)
cfg.set_main_option("script_location", __migration_path__)


def __execute_upgrade(connection):
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")

async def run_migrations(conn_url: str):
    async_engine = create_async_engine(conn_url, echo=True)
    async with async_engine.begin() as conn:
        await conn.run_sync(__execute_upgrade)

async def create_migration(message: str):
    command.revision(cfg, message=message, autogenerate=True)

async def check_migration_status():
    command.current(cfg)
