import os
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Initialize MongoDB client
client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DATABASE_NAME")]
user_collection = db["users"]

# OAuth2 setup for FastAPI to manage token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password hashing configuration
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

mongoApp = FastAPI()
