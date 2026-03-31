from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt

from server.database import get_db
from server.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


class UserRegister(BaseModel):
    username: str
    password: str
    age: int | None = None
    weight: float | None = None
    height: float | None = None
    gender: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    daily_goal_kcal: float

    class Config:
        from_attributes = True


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8")
    )


@router.post("/register", response_model=UserResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        age=data.age,
        weight=data.weight,
        height=data.height,
        gender=data.gender,
    )

    if data.weight and data.height and data.age and data.gender:
        if data.gender == "male":
            bmr = 10 * data.weight + 6.25 * data.height - 5 * data.age + 5
        else:
            bmr = 10 * data.weight + 6.25 * data.height - 5 * data.age - 161
        user.daily_goal_kcal = round(bmr * 1.55, 1)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=UserResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return user