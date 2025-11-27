from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped 
from src.models import Base 


class Favourite(Base):
    __tablename__ = "favourites"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"))

    user = relationship("User", back_populates="favourites")
    car = relationship("Car", back_populates="favourites")

    __table_args__ = (UniqueConstraint("user_id", "car_id", name="unique_user_car"),)
