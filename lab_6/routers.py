import models
import security
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


# 1. Регистрация
@router.post('/register', response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = (
        db.query(models.UserDB)
        .filter(models.UserDB.email == user.email)
        .first()
    )
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    hashed_pw = security.get_password_hash(user.password)
    new_user = models.UserDB(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 2. Логин (получение токена)
@router.post('/login')
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2PasswordRequestForm ожидает поля 'username' и 'password'.
    # Передаём email в поле username.
    user = (
        db.query(models.UserDB)
        .filter(models.UserDB.email == form_data.username)
        .first()
    )

    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401, detail='Incorrect email or password'
        )

    access_token = security.create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


# 3. Защищенный профиль (только с токеном)
@router.get('/profile')
def profile(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    from jose import JWTError, jwt

    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get('sub')
        if email is None:
            raise HTTPException(status_code=401, detail='Invalid token')
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')

    user = db.query(models.UserDB).filter(models.UserDB.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')

    return {
        'message': 'Вы авторизованы!',
        'user': {'id': user.id, 'email': user.email},
    }
