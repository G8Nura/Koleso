from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func 
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    created_at: Mapped = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)
