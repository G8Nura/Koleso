from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship 
from src.database import Base 


class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))

    user = relationship("User", back_populates="favourites")
    car = relationship("Car", back_populates="favourites")

    __table_args__ = (UniqueConstraint("user_id", "car_id", name="unique_user_car"),)
