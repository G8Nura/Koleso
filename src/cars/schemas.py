from pydantic import BaseModel
from typing import Optional


class CarBase(BaseModel):
    title: str
    description: Optional[str]
    price: float
    brand: str
    model: str
    year: int


class CarCreate(CarBase):
    pass

class CarOut(CarBase):
    id: int
    status: str
    owner_id: int

    class Config:
        from_attributes = True
        