from fastapi.testclient import TestClient
from main import app

# Создаем виртуального клиента (как будто мы открыли браузер)
client = TestClient(app)


def test_root_endpoint():
    """Проверка корневого эндпоинта (GET /)"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Server is running. Architecture is clean!'
    }


def test_create_user_api_success():
    """Обычный сценарий: POST /users успешно создает пользователя"""
    response = client.post(
        '/users',
        json={
            'name': 'Анна',
            'email': 'anna@example.com',
            'age': 20,
            'password': 'securepass123',
        },
    )
    assert response.status_code == 201
    assert response.json()['name'] == 'Анна'


def test_create_user_api_validation_error():
    """Ошибочный сценарий: невалидные данные (возраст < 18)"""
    response = client.post(
        '/users',
        json={
            'name': 'Петя',
            'email': 'petya@example.com',
            'age': 15,  # Ошибка!
            'password': 'securepass123',
        },
    )
    assert response.status_code == 422


def test_get_non_existent_user():
    """Граничный сценарий: запрос несуществующего пользователя"""
    response = client.get('/users/9999')
    assert response.status_code == 404
