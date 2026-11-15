import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Берем URL из переменных окружения
SQLALCHEMY_DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql://user:secret@localhost:5432/mydb'
)
# Если URL пришел из Docker, нужно заменить postgresql:// на postgresql+psycopg2://
if SQLALCHEMY_DATABASE_URL.startswith('postgresql://'):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        'postgresql://', 'postgresql+psycopg2://'
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Зависимость для получения сессии БД в роутерах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
