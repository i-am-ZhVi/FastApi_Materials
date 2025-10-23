from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import verify_password, create_access_token
from datetime import timedelta
from app.config import settings

class UserService:
    def __init__(self, repository: SQLAlchemyUserRepository):
        self.repository = repository

    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        user = await self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None

        return UserResponse.from_orm(user)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        # Check if user already exists
        existing_user = await self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        user = await self.repository.create(user_data)
        return UserResponse.from_orm(user)

    async def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = await self.repository.get_by_id(user_id)
        return UserResponse.from_orm(user) if user else None

    def create_user_token(self, email: str) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )
        return access_token
