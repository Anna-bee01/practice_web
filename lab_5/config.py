import os


class Settings:
    # Если переменной окружения нет, берется значение по умолчанию (после запятой)
    APP_NAME: str = os.getenv('APP_NAME', 'Lab 4 Users API')
    DEBUG: bool = os.getenv('DEBUG', 'True').lower() == 'true'
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///./test.db')


settings = Settings()
