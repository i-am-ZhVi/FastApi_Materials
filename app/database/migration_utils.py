import asyncio
import os
from alembic.config import Config
from alembic import command
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

__config_path__ = "alembic.ini"
__migration_path__ = "migrations"


cfg = Config(__config_path__) # обьект конфигурации алембика для работы с миграциями
cfg.set_main_option("script_location", __migration_path__) # установка пути до директории алембика


# применение миграций
async def run_migrations(conn_url: str):
    async_engine = create_async_engine(conn_url, echo=True) # генерация двигателя для взаимодействия с базой данных
    async with async_engine.begin() as conn: # подключение к базе данных
        await conn.run_sync(__execute_upgrade) # синхронный запуск мигрирования

def __execute_upgrade(connection):
    cfg.attributes["connection"] = connection # вставляем подключение к базе данных в атрибуты
    command.upgrade(cfg, "head") # мигрирование до последней версии


# создание новой миграции
async def create_migration(conn_url, message: str):
    async_engine = create_async_engine(conn_url, echo=True) # генерация двигателя для взаимодействия с базой данных
    async with async_engine.begin() as conn: # подключение к базе данных
        await conn.run_sync(__execute_create, message) # синхронный запуск создания миграции

def __execute_create(connection, message):
    cfg.attributes["connection"] = connection # вставляем подключение к базе данных в атрибуты
    command.revision(cfg, message=message, autogenerate=True) # создание новой миграции


# проверка статуса
async def check_migration_status(conn_url):
    async_engine = create_async_engine(conn_url, echo=True) # генерация двигателя для взаимодействия с базой данных
    async with async_engine.begin() as conn: # подключение к базе данных
        await conn.run_sync(__execute_check) # синхронный запуск проверки

def __execute_check(connection):
    cfg.attributes["connection"] = connection # вставляем подключение к базе данных в атрибуты
    command.current(cfg) # проверяем статус
