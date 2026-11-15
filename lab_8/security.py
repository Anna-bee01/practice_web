import os
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password):
    """Хэшируем пароль (превращаем в нечитаемый набор символов)"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Проверяем, подходит ли пароль к хэшу"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """Создаем JWT токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
