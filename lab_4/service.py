from models import UserCreate, UserUpdate
from repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    def create_user(self, user_data: UserCreate) -> dict:
        # email должен быть уникальным
        if self.repo.find_by_email(user_data.email):
            raise ValueError('Email already exists')

        # Превращаем Pydantic-модель в словарь и сохраняем
        data_to_save = user_data.model_dump(
            exclude={'password'}
        )  # пароль не сохраняем в ответ
        return self.repo.create(data_to_save)

    def get_user(self, user_id: int) -> dict:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        return user

    def get_all_users(self) -> list:
        return self.repo.get_all()

    def update_user(self, user_id: int, update_data: UserUpdate) -> dict:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')

        # Если меняем email, проверяем, что он не занят
        if update_data.email and update_data.email != user['email']:
            if self.repo.find_by_email(update_data.email):
                raise ValueError('Email already exists')

        # Сохраняем только те поля, которые пришли (исключаем None)
        data_to_update = update_data.model_dump(exclude_unset=True)
        return self.repo.update(user_id, data_to_update)

    def delete_user(self, user_id: int) -> bool:
        if not self.repo.delete(user_id):
            raise ValueError('User not found')
        return True
