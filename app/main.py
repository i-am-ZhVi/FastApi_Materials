from fastapi import FastAPI
from app.api import router as api_router
from app.database.session import engine
from app.models import Base
from contextlib import asynccontextmanager
from app.database.migration_utils import run_migrations
from app.config import settings
import asyncio

app = FastAPI(title="FastAPI Starter", version="1.0.0")

app.include_router(api_router)

async def init_db(retries=5, delay=5):
    for attempt in range(retries):
        try:
            print("Running database migrations...")
            await run_migrations(settings.DATABASE_URL)
            print("Migrations completed!")
            return
        except ConnectionRefusedError:
            if attempt == retries - 1:
                raise
            print(f"Database connection attempt {attempt + 1} failed, retrying in {delay} seconds...")
            await asyncio.sleep(delay)


@app.on_event("startup")
async def startup_event():
    await init_db()



@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Starter API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
