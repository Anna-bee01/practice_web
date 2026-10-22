from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# --- Модели данных (для POST запросов) ---
class UserCreate(BaseModel):
    name: str
    email: str
    age: int | None = None


# --- 1. GET запрос (просто читаем) ---
@app.get('/')
def read_root():
    return {'message': 'Привет! Это мой первый HTTP-сервер на FastAPI.'}


@app.get('/users/{user_id}')
def get_user(user_id: int):
    # Имитация поиска пользователя
    if user_id == 404:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return {
        'user_id': user_id,
        'name': 'John Doe',
        'email': 'john@example.com',
    }


# --- 2. POST запрос (создаем) ---
@app.post('/users', status_code=201)
def create_user(user: UserCreate):
    # Просто возвращаем то, что прислали + добавляем ID
    return {'id': 1, **user.model_dump(), 'status': 'created'}


# --- 3. Query-параметры (фильтрация) ---
@app.get('/search')
def search_users(name: str | None = None, age: int | None = None):
    return {'search_params': {'name': name, 'age': age}, 'results': []}
