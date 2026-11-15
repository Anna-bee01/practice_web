import pytest
from models import UserCreate
from repository import UserRepository
from service import UserService

# Unit-тесты для бизнес-логики


def test_create_user_too_young():
    """Ошибочный сценарий: возраст меньше 18"""
    # Создаем Pydantic-модель (она сама выдаст ошибку, если возраст < 18)
    with pytest.raises(ValueError):
        UserCreate(
            name='Петя',
            email='petya@example.com',
            age=15,
            password='password123',
        )


def test_create_user_success():
    """Обычный сценарий: успешное создание"""
    repo = UserRepository()
    service = UserService(repo)

    user_data = UserCreate(
        name='Иван', email='ivan@example.com', age=25, password='password123'
    )

    user = service.create_user(user_data)

    assert user['name'] == 'Иван'
    assert user['id'] is not None
    assert user['id'] > 0
    assert 'password' not in user
