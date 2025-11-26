from pydantic import BaseModel


class FavouriteOut(BaseModel):
    id: int
    user_id: int
    car_id: int

    class Config:
        from_attributes = True
        