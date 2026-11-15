from datetime import datetime

fake_db = {}
current_id = 1


class UserRepository:
    def create(self, user_data: dict) -> dict:
        global current_id
        new_user = {
            'id': current_id,
            **user_data,
            'created_at': datetime.now(),
        }
        fake_db[current_id] = new_user
        current_id += 1
        return new_user

    def get_by_id(self, user_id: int) -> dict | None:
        return fake_db.get(user_id)

    def get_all(self) -> list:
        return list(fake_db.values())

    def update(self, user_id: int, update_data: dict) -> dict | None:
        if user_id in fake_db:
            fake_db[user_id].update(update_data)
            return fake_db[user_id]
        return None

    def delete(self, user_id: int) -> bool:
        if user_id in fake_db:
            del fake_db[user_id]
            return True
        return False

    def find_by_email(self, email: str) -> dict | None:
        for user in fake_db.values():
            if user['email'] == email:
                return user
        return None
