from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from src.dependencies import get_db, get_current_user


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
    car = db.query(models.Car).filter(models.Car.id == car_id, models.Car.status == "approved").first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found or not approved."
        )
    if car.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot favourite your own car."
        )
    
    existing = db.query(models.Favourite).filter_by(user_id=current_user.id, car_id=car_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car already in favourites."
        )
    

    fav = models.Favourite(
        user_id=current_user.id,
        car_id=car_id
    )
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav 


@router.get("/", response_model=List[schemas.FavouriteOut])
def get_favourites(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.Favourite).filter(models.Favourite.user_id == current_user.id).all()
