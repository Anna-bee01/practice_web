from fastapi import APIRouter, HTTPException, status
from models import UserCreate, UserResponse, UserUpdate
from repository import UserRepository
from service import UserService

repo = UserRepository()
service = UserService(repo)

router = APIRouter()


@router.post(
    '/users', response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get('/users', response_model=list[UserResponse])
def get_users():
    return service.get_all_users()


@router.get('/users/{user_id}', response_model=UserResponse)
def get_user(user_id: int):
    try:
        return service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put('/users/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    try:
        return service.update_user(user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    try:
        service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
