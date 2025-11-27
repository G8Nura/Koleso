from sqlalchemy.orm import Session
from . import models
from src.enums import CarStatus
from fastapi import HTTPException, status


def add_favourite(
        db: Session,
        user_id: int,
        car_id: int
):
    car = db.query(models.Car).filter(
        models.Car.id == car_id,
        models.Car.status == CarStatus.APPROVED 
    ).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot favourite your own car"
        )
    
    existing = db.query(models.Favourite).filter_by(user_id=user_id, car_id=car_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car already in favourites"
        )
    
    fav = models.Favourite(user_id=user_id, car_id=car_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav                              


def get_user_favourites(
        db: Session,
        user_id: int
):
    return db.query(models.Favourite).filter(models.Favourite.user_id == user_id)