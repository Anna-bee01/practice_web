import models
from database import engine
from fastapi import FastAPI
from routers import router

# Создаем таблицы в БД при запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Lab 6: Auth & DB')
app.include_router(router)
