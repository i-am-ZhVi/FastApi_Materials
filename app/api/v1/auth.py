from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.token_schema import Token

# инициализация роутера для пути /api/v1/auth/...
router = APIRouter(prefix="/auth", tags=["authentication"])

# endpoint для отправки данных для регистрации имеет путь /api/v1/auth/register
@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate, # Данные для регистрации
    db: AsyncSession = Depends(get_db) # зависимость генерирующая сессию для работы с базой данных
):
    repository = SQLAlchemyUserRepository(db) # вспомогательный репозиторий с необходимым набором инструментов для взаимодействия с базой данных
    service = UserService(repository) # cервис бизнес логики с необходимым набором инструментов для обработки информации

    try:
        user = await service.create_user(user_data) # создание нового пользователя
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) # при ошибке в создании пользователя возвращаем ошибку 400 - не корректный запрос с сообщением 'e'


# endpoint для отправки данных для входа имеет путь /api/v1/auth/login
@router.post("/login", response_model=Token)
async def login(
    response: Response, # тело ответа
    user_data: UserCreate, # Данные для входа, тут они такие же как и для регистрации, в реальных приложениях они могут отличаться
    db: AsyncSession = Depends(get_db) # зависимость генерирующая сессию для работы с базой данных
):
    repository = SQLAlchemyUserRepository(db) # вспомогательный репозиторий с необходимым набором инструментов для взаимодействия с базой данных
    service = UserService(repository) # cервис бизнес логики с необходимым набором инструментов для обработки информации

    user = await service.authenticate_user(user_data.email, user_data.password) # попытка найти пользователя по введенным данным
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        ) # если пользователь не найден выдаем ошибку 401 - требуется авторизация

    access_token = service.create_user_token(user_data.email) # создаем токен для дальнейшей проверки доступа

    response.set_cookie( # вставляем куки хранящие токен в тело ответа
        key="access_token",
        value=access_token,
        secure=True,
        path="/",
    )
    return {"access_token": access_token, "token_type": "bearer"} # выводим токен для приложений без куки
