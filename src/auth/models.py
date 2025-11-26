from sqlalchemy import Column, Integer, String, Boolean 
from src.database import Base
from sqlalchemy.orm import relationship 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    cars = relationship("Car", back_populates="owner")
    favourites = relationship("Favourite", back_populates="user")
    