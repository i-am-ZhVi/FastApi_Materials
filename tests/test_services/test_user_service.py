import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate

class TestUserService:
    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        service = UserService(repository)

        user_data = UserCreate(
            email="test1@example.com",
            password="password123",
            full_name="Test User"
        )
        await service.create_user(user_data)

        authenticated_user = await service.authenticate_user(
            "test1@example.com", "password123"
        )

        assert authenticated_user is not None
        assert authenticated_user.email == "test1@example.com"
        assert authenticated_user.full_name == "Test User"

    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        service = UserService(repository)

        user_data = UserCreate(
            email="test2@example.com",
            password="password123",
            full_name="Test User"
        )
        await service.create_user(user_data)

        authenticated_user = await service.authenticate_user(
            "test2@example.com", "wrongpassword"
        )

        assert authenticated_user is None

    @pytest.mark.asyncio
    async def test_authenticate_user_nonexistent(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        service = UserService(repository)

        authenticated_user = await service.authenticate_user(
            "nonexistent@example.com", "password123"
        )

        assert authenticated_user is None

    @pytest.mark.asyncio
    async def test_create_user_success(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        service = UserService(repository)

        user_data = UserCreate(
            email="test3@example.com",
            password="password123",
            full_name="Test User"
        )

        user = await service.create_user(user_data)

        assert user.id is not None
        assert user.email == "test3@example.com"
        assert user.full_name == "Test User"

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        service = UserService(repository)

        user_data = UserCreate(
            email="test8@example.com",
            password="password123",
            full_name="Test User"
        )

        await service.create_user(user_data)

        with pytest.raises(ValueError, match="User with this email already exists"):
            await service.create_user(user_data)

    @pytest.mark.asyncio
    async def test_get_user_success(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        service = UserService(repository)

        user_data = UserCreate(
            email="test4@example.com",
            password="password123",
            full_name="Test User"
        )
        created_user = await service.create_user(user_data)

        found_user = await service.get_user(created_user.id)

        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == created_user.email

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, db_session: AsyncSession):
        repository = SQLAlchemyUserRepository(db_session)
        service = UserService(repository)

        found_user = await service.get_user(999)

        assert found_user is None

    def test_create_user_token(self):
        service = UserService(None)

        token = service.create_user_token("test@example.com")

        assert token is not None
        assert isinstance(token, str)
