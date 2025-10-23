from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.services.user_service import UserService
from app.schemas.user_schema import UserResponse
from app.services.jwt_handler import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
