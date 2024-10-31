from pydantic import BaseModel
from config.mongoConfig import user_collection, pwd_context, SECRET_KEY, ALGORITHM
import jwt
from datetime import datetime, timedelta


class ProgramCreate(BaseModel):
    filename: str
    content: str


class Program(BaseModel):
    id: str
    filename: str
    content: str


class User(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool | None = False


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str


def get_user(username: str):
    user_data = user_collection.find_one({"username": username})
    if user_data:
        return UserInDB(**user_data)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user and verify_password(password, user.hashed_password):
        return user
    return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)