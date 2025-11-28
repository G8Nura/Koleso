from pydantic import BaseModel


class FavouriteOut(BaseModel):
    id: int
    user_id: int
    car_id: int

    model_config = {"from_attributes": True}
        