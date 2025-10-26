from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.base import Mapped
from datetime import datetime

from sqlalchemy.sql import text
from app.models import Base

# модель таблицы пользователей для базы данных
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), server_default=text("TIMEZONE('utc', now())"))

    # для красивого вывода текстом
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
