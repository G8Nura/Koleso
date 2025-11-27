from src.models import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from pydantic import EmailStr


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[EmailStr] = mapped_column(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    cars = relationship("Car", back_populates="owner")
    favourites = relationship("Favourite", back_populates="user")
    