from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt 
from . import models, utils 
from src.config import settings 


def register_user(
        db: Session,
        username:str,
        email:str,
        password: str
):
    existing_user = db.query(models.User).filter(
        (models.User.email == email) | (models.User.username == username)
    ).first()
    if existing_user:
        raise ValueError("Username or email already registered.")
    
    new_user = models.User(
        username=username,
        email=email,
        password_hash=utils.hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authtenticate_user(
        db: Session,
        email: str,
        password: str
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not utils.verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(
        email:str
):
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(
        {"sub": email,
         "exp": expire
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return token 