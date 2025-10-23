from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.token_schema import Token

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    repository = SQLAlchemyUserRepository(db)
    service = UserService(repository)

    try:
        user = await service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(response: Response, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    repository = SQLAlchemyUserRepository(db)
    service = UserService(repository)

    user = await service.authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = service.create_user_token(user_data.email)

    response.set_cookie(
        key="access_token",
        value=access_token,
        secure=True,
        path="/",
    )
    return {"access_token": access_token, "token_type": "bearer"}
