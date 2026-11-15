import logging
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, field_validator

# 1. Настройка логирования
# Создаем логгер, который будет писать и в консоль, и в файл app.log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Пишем в файл
        logging.StreamHandler(),  # Пишем в консоль
    ],
)
logger = logging.getLogger(__name__)

app = FastAPI(title='Users API (Lab 3)', version='1.0.0')


# 2. Коды ошибок
class ErrorCode(str, Enum):
    VALIDATION_ERROR = 'VALIDATION_ERROR'
    EMAIL_EXISTS = 'EMAIL_EXISTS'
    NOT_FOUND = 'NOT_FOUND'


# 3. Модели с валидацией
class UserCreate(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=50, description='Имя пользователя'
    )
    email: EmailStr = Field(..., description='Валидный email')
    age: int = Field(..., ge=18, le=120, description='Возраст от 18 до 120')
    password: str = Field(
        ..., min_length=8, description='Пароль от 8 символов'
    )

    # Кастомная проверка: имя только из букв
    @field_validator('name')
    @classmethod
    def name_must_contain_letters(cls, v: str) -> str:
        if not v.replace(' ', '').isalpha():
            raise ValueError('Имя должно содержать только буквы и пробелы')
        return v

    # Кастомная проверка: пароль должен содержать буквы и цифры
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isalpha() for c in v):
            raise ValueError('Пароль должен содержать буквы')
        if not any(c.isdigit() for c in v):
            raise ValueError('Пароль должен содержать цифры')
        return v


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr | None = None
    age: int | None = Field(None, ge=18, le=120)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    created_at: datetime


fake_db = {}
current_id = 1
existing_emails = [
    'existing@example.com',
    'test@test.com',
]  # Для бизнес-правила


# 4. Обработчик ошибок валидации
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, ValueError):
        logger.warning(f'Business rule error: {exc}')
        raise HTTPException(
            status_code=409, detail={'error': str(exc), 'code': 'EMAIL_EXISTS'}
        )

    logger.error(f'Internal Server Error: {exc}', exc_info=True)
    return JSONResponse(
        status_code=500,
        content={'error': 'Internal server error', 'code': 'INTERNAL_ERROR'},
    )


# 5. Эндпоинты


@app.post(
    '/users', response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):
    global current_id
    logger.info(f'Попытка создания пользователя: {user.email}')

    # email должен быть уникальным
    if user.email in existing_emails or any(
        u['email'] == user.email for u in fake_db.values()
    ):
        logger.warning(f'Конфликт: email {user.email} уже существует')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                'error': 'Email already exists',
                'code': ErrorCode.EMAIL_EXISTS,
            },
        )

    new_user = {
        'id': current_id,
        'name': user.name,
        'email': user.email,
        'age': user.age,
        'created_at': datetime.now(),
    }
    fake_db[current_id] = new_user
    current_id += 1

    logger.info(f'Пользователь создан успешно. ID: {new_user["id"]}')
    return new_user


@app.get('/users/{id}', response_model=UserResponse)
def get_user(id: int):
    if id not in fake_db:
        logger.warning(f'Пользователь с ID {id} не найден')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'error': 'User not found', 'code': ErrorCode.NOT_FOUND},
        )
    return fake_db[id]


@app.get('/users')
def get_users(page: int = 1, limit: int = 10):
    users_list = list(fake_db.values())
    return {
        'users': users_list,
        'total': len(users_list),
        'page': page,
        'pages': 1,
    }


@app.put('/users/{id}', response_model=UserResponse)
def update_user(id: int, user: UserUpdate):
    if id not in fake_db:
        raise HTTPException(
            status_code=404, detail={'error': 'User not found'}
        )

    updated_user = fake_db[id]
    if user.name is not None:
        updated_user['name'] = user.name
    if user.email is not None:
        # Проверка на уникальность при обновлении
        if (
            user.email != updated_user['email']
            and user.email in existing_emails
        ):
            raise HTTPException(
                status_code=409, detail={'error': 'Email already exists'}
            )
        updated_user['email'] = user.email
    if user.age is not None:
        updated_user['age'] = user.age

    logger.info(f'Пользователь ID {id} обновлен')
    return updated_user


@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    if id not in fake_db:
        raise HTTPException(
            status_code=404, detail={'error': 'User not found'}
        )
    del fake_db[id]
    logger.info(f'Пользователь ID {id} удален')
