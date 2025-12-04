from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from .config import settings
from .models import Base
from src.auth.models import User
from src.cars.models import Car
from src.favourites.models import Favourite

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} 
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)