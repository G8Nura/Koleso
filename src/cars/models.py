from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.models import Base
from src.enums import CarStatus

class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    brand: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column (nullable=False)
    status: Mapped[str] = mapped_column(Enum(CarStatus), default=CarStatus.PENDING)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner = relationship("User", back_populates="cars")
    favourites = relationship("Favourite", back_populates="car")
    