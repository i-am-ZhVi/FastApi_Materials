import pytest
from app.services.auth_service import verify_password, get_password_hash, create_access_token
from jose import jwt
from app.config import settings
from datetime import datetime, timedelta, timezone

class TestAuthService:
    def test_password_hashing_and_verification(self):
        password = "testpassword123"
        hashed_password = get_password_hash(password)

        assert verify_password(password, hashed_password) is True

        assert verify_password("wrongpassword", hashed_password) is False

    def test_create_access_token(self):
        email = "test@example.com"
        token = create_access_token(data={"sub": email})

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        assert payload["sub"] == email
        assert "exp" in payload

    def test_token_expiration(self):
        email = "test@example.com"
        expires_delta = timedelta(minutes=30)
        token = create_access_token(
            data={"sub": email},
            expires_delta=expires_delta
        )

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        exp_timestamp = payload["exp"]
        now_timestamp = int(datetime.now(timezone.utc).timestamp())

        assert exp_timestamp > now_timestamp
        assert exp_timestamp <= now_timestamp + 1800  # 30 minutes in seconds
