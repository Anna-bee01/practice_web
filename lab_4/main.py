from config import settings
from fastapi import FastAPI
from routers import router

app = FastAPI(title=settings.APP_NAME)

app.include_router(router)


@app.get('/')
def read_root():
    return {'message': 'Server is running. Architecture is clean!'}
