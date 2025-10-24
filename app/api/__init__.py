from fastapi import APIRouter
from app.api.v1 import router as v1_router

# инициализация роутера для пути /api/...
router = APIRouter(prefix="/api")

# подключение роутера с ендпоинтами 1 версии
router.include_router(v1_router)
