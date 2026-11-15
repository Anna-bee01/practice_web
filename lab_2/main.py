from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title='Users API', description='API for managing users', version='1.0.0'
)

# Модели данных


class UserCreate(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=50, description='Имя пользователя'
    )
    email: str = Field(
        ..., pattern=r'^\S+@\S+\.\S+$', description='Email пользователя'
    )
    age: int | None = Field(
        None, ge=18, le=120, description='Возраст (от 18 до 120)'
    )


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=50)
    email: str | None = Field(None, pattern=r'^\S+@\S+\.\S+$')
    age: int | None = Field(None, ge=18, le=120)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None
    created_at: datetime


class UsersListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    pages: int


# База данных
fake_db = {}
current_id = 1


# GET /users (получить всех)
@app.get('/users', response_model=UsersListResponse)
def get_users(page: int = 1, limit: int = 10):
    users_list = list(fake_db.values())
    return {
        'users': users_list,
        'total': len(users_list),
        'page': page,
        'pages': 1,
    }


# POST /users (создать)
@app.post(
    '/users', response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):
    global current_id
    new_user = {
        'id': current_id,
        'name': user.name,
        'email': user.email,
        'age': user.age,
        'created_at': datetime.now(),
    }
    fake_db[current_id] = new_user
    current_id += 1
    return new_user


# GET /users/{id} (получить одного)
@app.get('/users/{id}', response_model=UserResponse)
def get_user(id: int):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail='User not found')
    return fake_db[id]


# PUT /users/{id} (обновить)
@app.put('/users/{id}', response_model=UserResponse)
def update_user(id: int, user: UserUpdate):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail='User not found')

    updated_user = fake_db[id]
    if user.name is not None:
        updated_user['name'] = user.name
    if user.email is not None:
        updated_user['email'] = user.email
    if user.age is not None:
        updated_user['age'] = user.age

    fake_db[id] = updated_user
    return updated_user


# DELETE /users/{id} (удалить)
@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    if id not in fake_db:
        raise HTTPException(status_code=404, detail='User not found')
    del fake_db[id]
