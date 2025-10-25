from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True) # генерация двигателя для взаимодействия с базой данных
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # генерация фабрики для генерации сессий взаимодействия с базой данных

# Получение сессии
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session: # генерация сессии
        try:
            yield session # возврацаем сессию
        finally:
            await session.close() # закрываем сессию
