from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship 
from src.database import Base 

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year =Column(Integer, nullable=False)
    status = Column(String, default="pending")
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="cars")
    favourites = relationship("Favourite", back_populates="car")
    