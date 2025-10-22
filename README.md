# Материал по FastAPI

## Содержание:
- [Материал по FastAPI](#материал-по-fastapi)
  - [Модуль 1: Асинхронное программирование](#модуль-1-асинхронное-программирование)
  - [Модуль 2: Основы веб-разработки](#модуль-2-основы-веб-разработки)
  - [Модуль 3: Основы FastAPI](#модуль-3-основы-fastapi)
  - [Модуль 4: Безопасность и аутентификация](#модуль-4-безопасность-и-аутентификация)
  - [Модуль 5: Безопасность в продакшене](#модуль-5-безопасность-в-продакшене)
  - [Модуль 6: Основы Pydantic](#модуль-6-основы-pydantic)
  - [Модуль 7: Основы SqlAlchemy](#модуль-7-основы-sqlalchemy)
  - [Модуль 8: Конвертация SqlAlchemy в Pydantic](#модуль-8-конвертация-sqlalchemy-в-pydantic)
  - [Модуль 9: Зависимости (Dependencies) и внедрение](#модуль-9-зависимости-dependencies-и-внедрение)
  - [Модуль 10: Тестирование](#модуль-10-тестирование)
  - [Модуль 11: Деплой и DevOps](#модуль-11-деплой-и-devops)

## Модуль 1: Асинхронное программирование
 - [содержание](#содержание)

## Что такое асинхронность?

Асинхронное программирование позволяет выполнять несколько задач одновременно без создания отдельных потоков. Вместо блокирующих операций код "ждет" результаты, освобождая ресурсы для других задач.

## Ключевые элементы

### 1. async/await
```python
import asyncio

async def main():
    print("Начало")
    await asyncio.sleep(1)
    print("После паузы")

asyncio.run(main())
```

### 2. Задачи (Tasks)
```python
async def task1():
    await asyncio.sleep(1)
    return "Результат 1"

async def task2():
    await asyncio.sleep(2)
    return "Результат 2"

async def main():
    # Запуск одновременно
    result1, result2 = await asyncio.gather(task1(), task2())
    print(f"{result1}, {result2}")
```

## Преимущества

- **Эффективность**: одна задача ждет - другие работают
- **Простота**: код выглядит как последовательный
- **Производительность**: идеально для I/O операций

## Когда использовать?

✅ Веб-серверы и API  
✅ Работа с сетью  
✅ Базы данных  
✅ Веб-скрейпинг  

## Пример: параллельные HTTP-запросы

```python
import aiohttp
import asyncio

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = ["http://example.com", "http://example.org"]
    results = await asyncio.gather(*[fetch(url) for url in urls])
    # Все запросы выполняются параллельно
```

Асинхронность в Python — мощный инструмент для создания высокопроизводительных приложений с простым и читаемым кодом.

## Модуль 2: Основы веб-разработки

- [содержание](#содержание)

## Из чего состоит веб-сайт?

### 1. Фронтенд (Frontend) - то, что видит пользователь
- **HTML** - структура страницы (текст, заголовки, ссылки)
- **CSS** - внешний вид (цвета, шрифты, расположение)
- **JavaScript** - интерактивность (анимации, формы, реакции)

### 2. Бэкенд (Backend) - "мозги" сайта
- **Сервер** - компьютер, где хранится сайт
- **База данных** - хранилище информации
- **Логика** - обработка данных, пользователей, заказов

### 3. Как это работает?
```
Пользователь → Браузер → Интернет → Сервер → База данных
                     ↑                         ↓
Страница сайта ← Ответ ← Обработка ← Данные
```

## Ключевые понятия

### HTTP-запросы
- **GET** - получить данные (открыть страницу)
- **POST** - отправить данные (форма, регистрация)
- **PUT/PATCH** - изменить данные
- **DELETE** - удалить данные

### Базы данных
- **Таблицы** - как Excel, но для данных
- **Записи** - строки в таблице (например, пользователь)
- **Поля** - колонки (имя, email, пароль)

## Типы веб-приложений

### 1. Статические сайты
- Не меняются (визитка, портфолио)
- Быстрые, простые

### 2. Динамические сайты  
- Персонализированный контент
- Социальные сети, интернет-магазины

### 3. Веб-приложения
- Полноценные программы в браузере
- Gmail, Google Docs, Figma

## Процесс разработки

1. **Планирование** - идея, цели, аудитория
2. **Дизайн** - макеты, интерфейс
3. **Фронтенд** - верстка по дизайну
4. **Бэкенд** - функциональность
5. **Тестирование** - поиск ошибок
6. **Запуск** - размещение в интернете

## Современные тренды

- **Адаптивный дизайн** - сайт на всех устройствах
- **SPA** - одностраничные приложения
- **API** - связь между разными сервисами
- **Облачные технологии** - гибкость и масштабируемость

Веб-разработка - это создание цифровых продуктов, которые решают реальные задачи пользователей через интернет-браузер.

## Модуль 3: Основы FastAPI

- [содержание](#содержание)

## Что такое FastAPI?
FastAPI - современный фреймворк для создания API на Python. Вот его основные концепции:

## Основные принципы

### 1. Аннотации типов
```python
def get_user(user_id: int) -> dict:
    return {"id": user_id, "name": "John"}
```
- Указываем типы параметров и возвращаемых значений
- Помогает в документации и проверках

### 2. Декораторы маршрутов
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}
```

### 3. Pydantic модели (схемы)
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
```

## Базовая структура приложения

### Минимальное API
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### HTTP методы
- **GET** - получение данных
- **POST** - создание
- **PUT** - полное обновление
- **DELETE** - удаление
- **PATCH** - частичное обновление

## Ключевые возможности

### Параметры пути
```python
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    # user_id автоматически конвертируется в int
    return {"user_id": user_id}
```

### Query-параметры
```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### Тело запроса
```python
@app.post("/users/")
async def create_user(user: User):
    return user
```

## Что делает FastAPI особенным?

1. **Автоматическая документация**
   - Swagger UI: `/docs`
   - ReDoc: `/redoc`

2. **Валидация данных**
   - На основе аннотаций типов
   - Автоматические ошибки 422

3. **Асинхронность**
   - Поддержка async/await
   - Высокая производительность

4. **Стандарты**
   - OpenAPI
   - JSON Schema

## Преимущества

- **Быстрота разработки** - минимум кода для функционального API
- **Самодокументируемость** - автоматическая генерация документации
- **Надежность** - встроенная валидация и обработка ошибок
- **Производительность** - сравним с Node.js и Go

FastAPI позволяет создавать современные API с минимальными усилиями, используя возможности Python 3.6+.

## Модуль 4: Безопасность и аутентификация

- [содержание](#содержание)

## Базовая аутентификация

### 1. Простая проверка токена
```python
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

# Простой секретный ключ
SECRET_TOKEN = "your-secret-token-here"

def verify_token(token: str):
    if token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return True

@app.get("/protected")
async def protected_route(token: str):
    verify_token(token)
    return {"message": "Access granted"}
```

## Сессии и куки

### Базовая сессия
```python
from fastapi import Request, Response

# Простое хранилище сессий в памяти
sessions = {}

@app.post("/login")
async def login(username: str, password: str, response: Response):
    # Проверка логина/пароля
    if username == "admin" and password == "password":
        session_id = "session_" + str(len(sessions))
        sessions[session_id] = {"username": username}
        response.set_cookie(key="session_id", value=session_id)
        return {"message": "Logged in"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/profile")
async def profile(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return sessions[session_id]
```

## Кастомная JWT аутентификация

### Создание и проверка токенов
```python
import hashlib
import json
import base64
from datetime import datetime, timedelta

def create_simple_jwt(user_id: str, secret: str) -> str:
    # Заголовок (header)
    header = {"alg": "HS256", "typ": "JWT"}
    header_encoded = base64.b64encode(json.dumps(header).encode()).decode()
    
    # Полезная нагрузка (payload)
    payload = {
        "user_id": user_id,
        "exp": (datetime.utcnow() + timedelta(hours=24)).timestamp()
    }
    payload_encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    
    # Подпись (signature)
    signature = hashlib.sha256(
        f"{header_encoded}.{payload_encoded}.{secret}".encode()
    ).hexdigest()
    
    return f"{header_encoded}.{payload_encoded}.{signature}"

def verify_simple_jwt(token: str, secret: str) -> dict:
    try:
        header_encoded, payload_encoded, signature = token.split(".")
        
        # Проверяем подпись
        expected_signature = hashlib.sha256(
            f"{header_encoded}.{payload_encoded}.{secret}".encode()
        ).hexdigest()
        
        if signature != expected_signature:
            raise ValueError("Invalid signature")
        
        # Декодируем payload
        payload = json.loads(base64.b64decode(payload_encoded))
        
        # Проверяем срок действия
        if datetime.utcnow().timestamp() > payload["exp"]:
            raise ValueError("Token expired")
            
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Зависимости для аутентификации

### Простая зависимость с токеном
```python
from fastapi import Header, Depends

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    user_data = verify_simple_jwt(token, "your-secret-key")
    return user_data

@app.get("/user/data")
async def get_user_data(current_user: dict = Depends(get_current_user)):
    return {"user_id": current_user["user_id"], "data": "sensitive information"}
```

## Хеширование паролей

### Простое хеширование
```python
import hashlib
import secrets

def hash_password(password: str) -> tuple:
    """Возвращает хеш и соль"""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def verify_password(password: str, hashed: str, salt: str) -> bool:
    return hashlib.sha256((password + salt).encode()).hexdigest() == hashed

# Использование
@app.post("/register")
async def register(username: str, password: str):
    hashed_password, salt = hash_password(password)
    # Сохраняем в базу: username, hashed_password, salt
    return {"message": "User registered"}

@app.post("/login-simple")
async def login_simple(username: str, password: str):
    # Получаем из базы: hashed_password, salt по username
    # if verify_password(password, stored_hash, stored_salt):
    #     token = create_simple_jwt(username, "secret")
    #     return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")
```



## Модуль 5: Безопасность в продакшене

- [содержание](#содержание)

## Middleware для безопасности

### Базовые заголовки безопасности
```python
from fastapi import Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Добавляем middleware
app.add_middleware(HTTPSRedirectMiddleware)  # Перенаправление на HTTPS
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com"])  # Только доверенные хосты

# Кастомный middleware для безопасности
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

## Практики безопасности

### 1. Валидация входных данных
```python
from pydantic import BaseModel, constr

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)

@app.post("/create-user")
async def create_user(user: UserCreate):
    # FastAPI автоматически валидирует данные
    return {"message": "User created"}
```

### 2. Лимиты запросов
```python
from fastapi import Request
import time

# Простой rate limiting
request_times = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()
    
    # Очистка старых записей
    request_times[client_ip] = [
        t for t in request_times.get(client_ip, []) 
        if current_time - t < 60  # 60 секунд
    ]
    
    # Проверка лимита (макс 100 запросов в минуту)
    if len(request_times[client_ip]) >= 100:
        raise HTTPException(status_code=429, detail="Too many requests")
    
    request_times[client_ip].append(current_time)
    return await call_next(request)
```

## Основные принципы безопасности

1. **Никогда не храните пароли в открытом виде**
2. **Используйте HTTPS в продакшене**
3. **Валидируйте все входные данные**
4. **Ограничивайте частоту запросов**
5. **Используйте безопасные заголовки**
6. **Регулярно обновляйте секретные ключи**


## Модуль 6: Основы Pydantic

- [содержание](#содержание)

## Что такое Pydantic?

Pydantic - это библиотека для **валидации данных** и **парсинга** в Python. Она использует аннотации типов для автоматической проверки и преобразования данных.

## Базовые концепции

### 1. Модели Pydantic
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int = 18  # значение по умолчанию
```

### 2. Создание и валидация
```python
# Автоматическая валидация
user = User(id=1, name="John", email="john@example.com")
print(user.id)  # 1

# Из словаря
user_data = {"id": 2, "name": "Alice", "email": "alice@test.com"}
user2 = User(**user_data)
```

## Основные возможности

### Автоматическая конвертация типов
```python
class Product(BaseModel):
    price: float
    in_stock: bool

# Строка автоматически конвертируется в float
# Число в bool
product = Product(price="29.99", in_stock=1)
print(product.price)  # 29.99 (float)
print(product.in_stock)  # True (bool)
```

### Валидация данных
```python
from pydantic import ValidationError

try:
    user = User(id="not_a_number", name="John")
except ValidationError as e:
    print("Ошибка валидации:", e)
```

## Полезные типы данных

### Специальные типы
```python
from pydantic import EmailStr, HttpUrl
from typing import List, Optional

class Contact(BaseModel):
    email: EmailStr  # автоматическая проверка email
    website: Optional[HttpUrl]  # необязательное поле + проверка URL
    tags: List[str] = []  # список строк
```

### Ограничения значений
```python
from pydantic import Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(gt=0)  # больше 0
    quantity: int = Field(ge=0)  # больше или равно 0
```

## Методы моделей

### Сериализация
```python
user = User(id=1, name="John", email="john@example.com")

# В словарь
user_dict = user.dict()
print(user_dict)  # {'id': 1, 'name': 'John', 'email': 'john@example.com', 'age': 18}

# В JSON
user_json = user.json()
print(user_json)  # '{"id": 1, "name": "John", ...}'
```

### Обновление данных
```python
# Создание копии с обновленными данными
updated_user = user.copy(update={"name": "John Doe"})
```

## Валидаторы

### Кастомная валидация
```python
from pydantic import validator

class Person(BaseModel):
    name: str
    age: int
    
    @validator('age')
    def age_must_be_reasonable(cls, v):
        if v < 0 or v > 150:
            raise ValueError('age must be between 0 and 150')
        return v
    
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()  # Можно преобразовывать значение
```

## Использование с FastAPI

### Модели запросов/ответов
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/users/")
async def create_user(user: User):  # Автоматическая валидация
    return {"message": f"User {user.name} created", "user_id": user.id}

@app.get("/users/{user_id}", response_model=User)  # Автоматическая сериализация
async def get_user(user_id: int):
    return User(id=user_id, name="John", email="john@example.com")
```

## Преимущества Pydantic

### 1. **Безопасность типов**
- Автоматическая проверка типов
- Защита от невалидных данных

### 2. **Удобство**
- Читаемый код
- Автодополнение в IDE
- Автоматическая документация

### 3. **Гибкость**
- Кастомные валидаторы
- Наследование моделей
- Поддержка сложных структур

### 4. **Производительность**
- Написано на Cython
- Быстрая валидация

## Пример полной модели
```python
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    birth_year: int
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v
    
    @validator('birth_year')
    def valid_birth_year(cls, v):
        current_year = datetime.now().year
        if v < 1900 or v > current_year:
            raise ValueError('Invalid birth year')
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
```

Pydantic делает работу с данными безопасной, предсказуемой и удобной, экономя время на написании boilerplate-кода для валидации.

## Модуль 7: Основы SqlAlchemy

- [содержание](#содержание)

## Что такое SQLAlchemy?

SQLAlchemy - это **ORM** (Object-Relational Mapping) для Python, который позволяет работать с базами данных используя Python-объекты вместо SQL-запросов.

## Два подхода в SQLAlchemy

### 1. Core - низкоуровневый
```python
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

metadata = MetaData()
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String)
)
```

### 2. ORM - высокоуровневый (рекомендуемый)
```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

## Основные компоненты

### Движок (Engine)
```python
from sqlalchemy import create_engine

# Подключение к базе данных
engine = create_engine('sqlite:///database.db')
# или для PostgreSQL: 'postgresql://user:password@localhost/dbname'
```

### Сессия (Session)
```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```

## Базовые операции CRUD

### Create - создание
```python
# Создание объекта
new_user = User(name="John", email="john@example.com")

# Добавление в сессию
session.add(new_user)

# Сохранение в БД
session.commit()
```

### Read - чтение
```python
# Получить все записи
users = session.query(User).all()

# Получить по ID
user = session.query(User).get(1)

# Фильтрация
john = session.query(User).filter(User.name == "John").first()
adults = session.query(User).filter(User.age >= 18).all()
```

### Update - обновление
```python
user = session.query(User).get(1)
user.email = "new_email@example.com"
session.commit()
```

### Delete - удаление
```python
user = session.query(User).get(1)
session.delete(user)
session.commit()
```

## Типы колонок

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
import datetime

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))  # строка с ограничением длины
    price = Column(Float)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
```

## Связи между таблицами

### Один-ко-многим
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")
```

### Использование связей
```python
user = session.query(User).get(1)
posts = user.posts  # Все посты пользователя

post = session.query(Post).get(1)
author = post.user  # Автор поста
```

## Запросы и фильтрация

### Базовые запросы
```python
# Все пользователи
users = session.query(User).all()

# Только имена
names = session.query(User.name).all()

# Сортировка
users_ordered = session.query(User).order_by(User.name).all()

# Лимит
first_5 = session.query(User).limit(5).all()
```

### Фильтры
```python
from sqlalchemy import and_, or_

# Простые фильтры
active_users = session.query(User).filter(User.is_active == True).all()

# Несколько условий
specific_users = session.query(User).filter(
    and_(
        User.age >= 18,
        User.country == "USA"
    )
).all()

# Поиск по шаблону
johns = session.query(User).filter(User.name.like("%John%")).all()
```

## Миграции (Alembic)

### Создание миграций
```bash
# Инициализация
alembic init alembic

# Создание миграции
alembic revision --autogenerate -m "Create users table"

# Применение миграции
alembic upgrade head
```

## Интеграция с FastAPI

```python
from sqlalchemy.orm import Session

# Dependency для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## Преимущества SQLAlchemy

### 1. **Абстракция от БД**
- Один код для разных СУБД
- Легкая смена базы данных

### 2. **Безопасность**
- Защита от SQL-инъекций
- Автоматическое экранирование

### 3. **Производительность**
- Ленивая загрузка
- Оптимизированные запросы

### 4. **Гибкость**
- Можно писать сырые SQL-запросы
- Мощная система миграций

## Пример полной модели
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
```

SQLAlchemy делает работу с базами данных интуитивно понятной, безопасной и эффективной, позволяя сосредоточиться на бизнес-логике вместо написания SQL-запросов.

## Модуль 8: Конвертация SqlAlchemy в Pydantic

- [содержание](#содержание)

## Основная идея

**SQLAlchemy** модели описывают структуру базы данных  
**Pydantic** модели описывают структуру данных для API

## Базовый подход

### Модель SQLAlchemy
```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String(255))
```

### Модель Pydantic
```python
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    
    class Config:
        orm_mode = True  # Ключевая настройка!
```

## Конфигурация orm_mode

```python
class Config:
    orm_mode = True
```

Эта настройка позволяет Pydantic читать данные из **ORM-объектов**, а не только из словарей.

## Использование в FastAPI

### Response Model
```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # Получаем объект SQLAlchemy из БД
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    
    # Просто возвращаем объект - FastAPI автоматически конвертирует
    return db_user
```

## Разделение моделей

### Для разных операций
```python
# Pydantic модели для разных целей

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    
    class Config:
        orm_mode = True
```

## Ручная конвертация

### Из SQLAlchemy в Pydantic
```python
# Автоматически через orm_mode
db_user = session.query(UserDB).first()
user_response = UserResponse.from_orm(db_user)

# Или через распаковку
user_dict = {
    "id": db_user.id,
    "username": db_user.username,
    "email": db_user.email,
    "is_active": db_user.is_active
}
user_response = UserResponse(**user_dict)
```

### Из Pydantic в SQLAlchemy
```python
user_data = UserCreate(
    username="john", 
    email="john@example.com", 
    password="secret"
)

# Создаем объект SQLAlchemy
db_user = UserDB(
    username=user_data.username,
    email=user_data.email,
    hashed_password=hash_password(user_data.password)
)

session.add(db_user)
session.commit()
```

## Работа с отношениями

### SQLAlchemy с отношениями
```python
class PostDB(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Отношение
    author = relationship("UserDB", back_populates="posts")

class UserDB(Base):
    __tablename__ = "users"
    # ... поля ...
    
    posts = relationship("PostDB", back_populates="author")
```

### Pydantic с вложенными моделями
```python
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    
    class Config:
        orm_mode = True

class UserWithPostsResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    posts: List[PostResponse] = []
    
    class Config:
        orm_mode = True
```

## Автоматизация с помощью функций

### Утилита для конвертации
```python
def sqlalchemy_to_pydantic(model_class):
    """Создает Pydantic модель из SQLAlchemy модели"""
    fields = {}
    for column in model_class.__table__.columns:
        field_type = ...
        # Автоматическое определение типов
        fields[column.name] = (field_type, ...)
    
    return type(f"{model_class.__name__}Response", (BaseModel,), fields)

# Использование
UserResponse = sqlalchemy_to_pydantic(UserDB)
```

## Лучшие практики

### 1. Не смешивайте ответственность
```python
# НЕПРАВИЛЬНО - пароль в модели ответа
class BadUser(BaseModel):
    id: int
    username: str
    hashed_password: str  # ⚠️ конфиденциальные данные!

# ПРАВИЛЬНО - отдельные модели
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    # Без пароля!
```

### 2. Используйте наследование
```python
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True
```

### 3. Обработка опциональных полей
```python
from typing import Optional

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
```

## Полный пример

```python
# SQLAlchemy модель
class ProductDB(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    description = Column(Text, nullable=True)
    in_stock = Column(Boolean, default=True)

# Pydantic модели
class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    in_stock: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    in_stock: bool
    
    class Config:
        orm_mode = True

# Использование в FastAPI
@app.post("/products/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db)
):
    db_product = ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product  # Автоматическая конвертация благодаря orm_mode
```

Конвертация между SQLAlchemy и Pydantic - это мост между слоем данных и слоем API, который обеспечивает безопасность, валидацию и удобство работы с данными.

## Модуль 9: Зависимости (Dependencies) и внедрение

- [содержание](#содержание)

## Что такое зависимости?

**Зависимости** - это функции или классы, которые выполняются перед обработкой запроса и предоставляют данные или функциональность для эндпоинтов.

## Базовый синтаксис

```python
from fastapi import Depends

def common_dependency():
    return {"message": "I'm a dependency"}

@app.get("/")
async def root(dep_result: dict = Depends(common_dependency)):
    return dep_result
```

## Типы зависимостей

### 1. Функции как зависимости
```python
def get_database():
    # Подключение к БД
    db = "database_connection"
    return db

@app.get("/items/")
async def read_items(db: str = Depends(get_database)):
    return {"db": db}
```

### 2. Классы как зависимости
```python
class Pagination:
    def __init__(self, page: int = 1, limit: int = 10):
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit

@app.get("/products/")
async def get_products(pagination: Pagination = Depends(Pagination)):
    return {
        "page": pagination.page,
        "limit": pagination.limit,
        "offset": pagination.offset
    }
```

## Практические примеры

### Аутентификация
```python
from fastapi import HTTPException, status

def get_current_user(token: str = Header(...)):
    if token != "secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {"user_id": 1, "username": "john"}

@app.get("/profile/")
async def user_profile(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}
```

### База данных
```python
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user
```

## Цепочки зависимостей

### Зависимости могут зависеть от других зависимостей
```python
def get_query_params(q: str = None, limit: int = 10):
    return {"q": q, "limit": limit}

def get_current_user(token: str = Header(...)):
    # Проверка токена
    return {"user_id": 1}

def get_user_data(
    params: dict = Depends(get_query_params),
    user: dict = Depends(get_current_user)
):
    return {
        "user": user,
        "search_query": params["q"],
        "limit": params["limit"]
    }

@app.get("/data/")
async def get_data(data: dict = Depends(get_user_data)):
    return data
```

## Зависимости для групп эндпоинтов

### Использование в роутерах
```python
from fastapi import APIRouter

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/items/")
async def read_items():
    return ["item1", "item2"]

# Все эндпоинты в этом роутере требуют аутентификации
```

## Специальные возможности

### Зависимости без возвращаемого значения
```python
def verify_api_key(api_key: str = Header(...)):
    if api_key != "valid-key":
        raise HTTPException(status_code=400, detail="Invalid API key")
    # Не возвращаем значение, просто проверяем

@app.get("/secure/")
async def secure_endpoint(_ = Depends(verify_api_key)):
    return {"message": "Access granted"}
```

### Необязательные зависимости
```python
from typing import Optional

def optional_auth(token: Optional[str] = Header(None)):
    if token:
        return {"user": "authenticated"}
    return {"user": "anonymous"}

@app.get("/optional/")
async def optional_endpoint(user: dict = Depends(optional_auth)):
    return user
```

## Паттерны использования

### 1. Валидация и парсинг
```python
def parse_date_range(
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    # Преобразуем строки в даты
    return {
        "start": parse_date(start_date),
        "end": parse_date(end_date)
    }
```

### 2. Логирование и метрики
```python
def log_request(request: Request):
    logger.info(f"{request.method} {request.url}")
    return request

@app.get("/")
async def home(request: Request = Depends(log_request)):
    return {"message": "Hello"}
```

### 3. Кеширование
```python
def get_cached_data(key: str = Query(...)):
    cached = cache.get(key)
    if cached:
        return cached
    raise HTTPException(404, "Not found")

@app.get("/cache/")
async def cached_route(data: dict = Depends(get_cached_data)):
    return data
```

## Преимущества зависимостей

### 1. **Повторное использование кода**
```python
# Одна зависимость - много эндпоинтов
@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    ...

@app.post("/users/")
async def create_users(db: Session = Depends(get_db)):
    ...
```

### 2. **Тестируемость**
```python
# Легко мокать зависимости в тестах
def override_get_db():
    return mock_db

app.dependency_overrides[get_db] = override_get_db
```

### 3. **Чистая архитектура**
- Разделение ответственности
- Легкая поддержка
- Предсказуемое поведение

### 4. **Безопасность**
- Централизованная проверка прав
- Единая точка для аутентификации

## Полный пример
```python
from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional

app = FastAPI()

# Зависимость для БД
def get_db():
    db = "database"
    try:
        yield db
    finally:
        print("Closing DB")

# Зависимость для аутентификации
def get_current_user(
    authorization: Optional[str] = Header(None),
    db: str = Depends(get_db)
):
    if not authorization:
        raise HTTPException(401, "No token")
    
    # Проверяем пользователя в БД
    user = {"id": 1, "name": "John"}
    return user

# Зависимость для прав доступа
def require_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(403, "Admin required")
    return user

@app.get("/public/")
async def public_route():
    return {"message": "Public data"}

@app.get("/protected/")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"user": user, "data": "Protected data"}

@app.get("/admin/")
async def admin_route(admin: dict = Depends(require_admin)):
    return {"admin": admin, "data": "Admin data"}
```

Зависимости в FastAPI - это мощный механизм для создания чистого, модульного и безопасного кода, который следует принципам DRY (Don't Repeat Yourself) и обеспечивает легкую тестируемость приложения.

## Модуль 10: Тестирование

- [содержание](#содержание)

## Зачем нужно тестирование?

**Тестирование** - это проверка, что ваш код работает правильно. Как чертежник проверяет чертеж перед строительством.

## Типы тестирования

### 1. Модульные тесты (Unit Tests)
- Проверяют отдельные "кусочки" кода (функции, методы)
- Быстрые и изолированные

### 2. Интеграционные тесты
- Проверяют взаимодействие между компонентами
- Медленнее, но ближе к реальности

## Библиотеки для тестирования

### 1. unittest (встроенная)
```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

if __name__ == "__main__":
    unittest.main()
```

### 2. pytest (популярная)
```python
# test_math.py
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```

## Основные концепции

### Фикстуры (Fixtures)
```python
import pytest

@pytest.fixture
def database_connection():
    # Настройка перед тестом
    db = connect_to_db()
    yield db  # Возвращаем объект для теста
    # Очистка после теста
    db.close()

def test_user_query(database_connection):
    user = database_connection.get_user(1)
    assert user.name == "John"
```

### Mock-объекты
```python
from unittest.mock import Mock, patch

def test_send_email():
    # Создаем mock вместо реальной отправки email
    mock_sender = Mock()
    mock_sender.send.return_value = True
    
    result = send_notification(mock_sender, "test@example.com")
    
    assert result is True
    mock_sender.send.assert_called_once_with("test@example.com")
```

## Практические примеры

### Тестирование функции
```python
# calculator.py
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# test_calculator.py
import pytest

def test_divide_normal():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

### Тестирование класса
```python
# user.py
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def is_adult(self):
        return self.age >= 18

# test_user.py
def test_user_creation():
    user = User("John", 25)
    assert user.name == "John"
    assert user.age == 25

def test_is_adult():
    adult = User("John", 20)
    child = User("Alice", 16)
    
    assert adult.is_adult() is True
    assert child.is_adult() is False
```

## Тестирование FastAPI приложений

### Тестирование эндпоинтов
```python
from fastapi.testclient import TestClient
from main import app  # ваше FastAPI приложение

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    user_data = {"username": "john", "email": "john@example.com"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "john"
```

### Тестирование с зависимостями
```python
def override_get_db():
    # Заменяем реальную БД на тестовую
    return test_db

app.dependency_overrides[get_db] = override_get_db

def test_with_mock_database():
    response = client.get("/users/1")
    assert response.status_code == 200
```

## Асинхронное тестирование

### Тестирование async функций
```python
import pytest

async def async_function():
    await asyncio.sleep(0.1)
    return "result"

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == "result"
```

## Параметризованные тесты

### Множество тестовых случаев
```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5)
])
def test_add_multiple_cases(a, b, expected):
    assert add(a, b) == expected
```

## Лучшие практики

### 1. Именование тестов
```python
# ХОРОШО
def test_user_creation_with_valid_data()
def test_login_with_invalid_credentials()

# ПЛОХО
def test1()
def test_user()
```

### 2. Структура AAA
```python
def test_something():
    # Arrange - подготовка данных
    user = User(name="John", age=25)
    
    # Act - выполнение действия
    result = user.is_adult()
    
    # Assert - проверка результата
    assert result is True
```

### 3. Изоляция тестов
```python
# Каждый тест должен быть независимым
def test_one():
    # Не зависеть от test_two()
    pass

def test_two():
    # Не зависеть от test_one()
    pass
```

## Покрытие кода (Coverage)

### Установка и использование
```bash
pip install pytest-cov
pytest --cov=myapp tests/
```

## Запуск тестов

### Команды pytest
```bash
# Все тесты
pytest

# Конкретный файл
pytest test_calculator.py

# Конкретная функция
pytest test_calculator.py::test_add

# С покрытием кода
pytest --cov=myapp

# С подробным выводом
pytest -v
```

## Пример полного тестового файла

```python
# test_calculator.py
import pytest
from calculator import add, subtract, multiply, divide

class TestCalculator:
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
    
    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
    
    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(0, 100) == 0
    
    def test_divide(self):
        assert divide(10, 2) == 5
        assert divide(5, 2) == 2.5
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            divide(10, 0)

# Фикстура для повторно используемых данных
@pytest.fixture
def sample_numbers():
    return [1, 2, 3, 4, 5]

def test_with_fixture(sample_numbers):
    assert len(sample_numbers) == 5
    assert sum(sample_numbers) == 15
```

Тестирование - это не роскошь, а необходимость для создания надежного кода. Начните с простых unit-тестов и постепенно добавляйте более сложные сценарии.

## Модуль 11: Деплой и DevOps

- [содержание](#содержание)

### 🚀 Основные шаги деплоя FastAPI приложения

1. **Контейнеризация приложения (Docker)**  
   Создай `Dockerfile` для упаковки приложения в контейнер:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
   Собери и протестируй образ: `docker build -t fastapi-app .` и `docker run -p 8000:8000 fastapi-app`.

2. **Оркестрация (Docker Compose или Kubernetes)**  
   Для простых сценариев используй `docker-compose.yml` для связки приложения с Nginx. Для масштабирования выбирай Kubernetes:
   - Установи Minikube или используй Kubernetes в Docker Desktop
   - Опиши деплоймент и сервис в YAML-файлах
   - Примени конфигурацию: `kubectl apply -f deployment.yaml`

3. **Настройка CI/CD пайплайна**  
   Используй GitHub Actions для автоматизации. Пример workflow для тестов и сборки:
   ```yaml
   name: CI/CD Pipeline
   on: [push, pull_request]
   jobs:
     build-and-test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-python@v5
         - run: pip install -r requirements.txt
         - run: pytest
         - run: docker build -t fastapi-app .
   ```
   Для авторазвертывания добавь шаг деплоя по SSH на сервер.

4. **Развертывание на сервере**  
   - **Подготовка сервера**: создай VM (например, AWS EC2), открой порты (80, 22, 443), установи Docker и Docker Compose.
   - **Деплой**: настроенный CD-пайплайн может автоматически развертывать приложение на сервере через SSH.
   - **Обратный прокси**: настрой Nginx для проксирования запросов к приложению.

### 💡 Ключевые практики DevOps

- **Инфраструктура как код**: храни конфигурации Docker и Kubernetes в репозитории  
- **Настройка мониторинга здоровья**: добавь эндпоинт `/health` для проверок в Kubernetes  
- **Управление конфигурацией**: используй Kubernetes ConfigMap для настроек и Secrets для чувствительных данных  
- **Автоматическое масштабирование**: настрой Horizontal Pod Autoscaler в Kubernetes

### 🛠 Пример workflow для GitHub Actions

```yaml
name: CD Pipeline
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USERNAME }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app
            docker-compose down
            docker-compose up -d --build
```

### 🔧 Полезные команды

```bash
# Локальный запуск
fastapi run main.py

# Тестирование
pytest

# Kubernetes
kubectl get pods
kubectl apply -f deployment.yaml
```

Начни с простого пайплайна (сборка → тесты → деплой), затем добавляй сложность. Для продакшена обязательно настрой HTTPS, мониторинг и логирование.
