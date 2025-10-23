from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from app.config import settings
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.database.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Авторизуйтесь"
    )
    token = request.cookies.get("access_token")

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    repository = SQLAlchemyUserRepository(db)
    user = await repository.get_by_email(email)
    if user is None:
        raise credentials_exception

    return user
