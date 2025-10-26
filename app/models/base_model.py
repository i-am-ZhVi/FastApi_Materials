from sqlalchemy.orm import DeclarativeBase

# Ядро всех моделей
class Base(DeclarativeBase):
    __abstract__ = True
