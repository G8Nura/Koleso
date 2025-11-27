from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import service, schemas
from src.dependencies import get_db, get_current_user
from src.pagination import paginate, PaginationParams, PaginatedResponse

router = APIRouter(
    prefix="/favourites",
    tags=["favourites"]
)


@router.post("/", response_model=schemas.FavouriteOut)
def add_favourite(
    car_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    fav = service.add_favourite(db, current_user.id, car_id)
    return fav 


@router.get("/", response_model=PaginatedResponse[schemas.FavouriteOut])
def get_favourites(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = service.get_user_favourites(db, current_user.id)
    return paginate(query, page=pagination.page, limit=pagination.limit)