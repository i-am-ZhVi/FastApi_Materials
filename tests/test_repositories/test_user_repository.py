import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.schemas.user_schema import UserCreate
from app.models.user_model import User

class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        user_data = UserCreate(
            email="test7@example.com",
            password="password123",
            full_name="Test User"
        )

        user = await repository.create(user_data)

        assert user.id is not None
        assert user.email == "test7@example.com"
        assert user.full_name == "Test User"
        assert user.hashed_password is not None
        assert user.hashed_password != "password123"

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        user_data = UserCreate(
            email="test6@example.com",
            password="password123",
            full_name="Test User"
        )

        created_user = await repository.create(user_data)

        found_user = await repository.get_by_email("test6@example.com")

        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == created_user.email

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)

        found_user = await repository.get_by_email("nonexistent@example.com")

        assert found_user is None

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            full_name="Test User"
        )

        created_user = await repository.create(user_data)

        found_user = await repository.get_by_id(created_user.id)

        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == created_user.email

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)

        found_user = await repository.get_by_id(999)

        assert found_user is None
