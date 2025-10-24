from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router

# инициализация роутера для пути /api/v1/...
router = APIRouter(prefix="/v1")

# подключение роутера с ендпоинтами аутентификации
router.include_router(auth_router)
# подключение роутера с ендпоинтами для взаимодействия с пользовательскими данными
router.include_router(users_router)
