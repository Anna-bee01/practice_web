from database import Base
from sqlalchemy import Column, Integer, Numeric, String


class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class AccountDB(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    owner_email = Column(
        String, index=True
    )  # Индекс для быстрого поиска по email
    balance = Column(
        Numeric(10, 2), default=1000.00
    )  # Баланс по умолчанию 1000
