from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone 
from jose import jwt 
from sqlalchemy.orm import Session
from src.config import settings
from .import models 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    truncated = password[:72]
    return pwd_context.hash(truncated)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = plain_password[:72]
    return pwd_context.verify(truncated, hashed_password)


def create_access_token(
        data: dict,
        expires_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
):
   to_encode = data.copy()

   expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
   to_encode.update({"exp":expire.timestamp()})

   encoded_jwt = jwt.encode(
       to_encode,
       settings.SECRET_KEY,
       algorithm=settings.ALGORITHM
   )
   return encoded_jwt


def authenticate_user(
        db: Session,
        email: str,
        password: str
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None 
    return user 
