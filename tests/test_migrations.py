import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class TestMigrations:
    @pytest.mark.asyncio
    async def test_migrations_applied(self, db_session: AsyncSession):
        result = await db_session.execute(text("""
            SELECT *
            FROM users
        """))

        assert result != None

    @pytest.mark.asyncio
    async def test_data_insertion(self, db_session: AsyncSession):
        from app.models.user_model import User
        from app.services.auth_service import get_password_hash

        user = User(
            email="migration_test@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Migration Test User"
        )

        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        assert user.id is not None
        assert user.email == "migration_test@example.com"
