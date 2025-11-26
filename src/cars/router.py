from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas 
from src.dependencies import get_db, get_current_user, get_current_admin


router = APIRouter(
    prefix="/cars",
    tags=["cars"]
)


@router.post("/", response_model=schemas.CarOut)
def create_car(
    car: schemas.CarCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_car = models.Car(
        **car.model_dump(),
        owner_id=current_user.id
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


@router.get("/", response_model=List[schemas.CarOut])
def get_cars(
    brand: Optional[str] = None,
    model: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Car).filter(models.Car.status == "approved")
    if brand:
        query = query.filter(models.Car.brand.ilike(f"%{brand}%"))
    if model:
        query = query.filter(models.Car.model.ilike(f"%{model}%"))
    if price_min is not None:
        query = query.filter(models.Car.price >= price_min)
    if price_max is not None:
        query = query.filter(models.Car.price <= price_max)
    if year_min is not None:
        query = query.filter(models.Car.year >= year_min)
    if year_max is not None:
        query = query.filter(models.Car.year <= year_max)
    
    if sort:
        if sort == "price_asc":
            query = query.order_by(models.Car.price.asc())
        elif sort == "price_desc":
            query = query.order_by(models.Car.price.desc())
        elif sort == "year_asc":
            query = query.order_by(models.Car.year.asc())
        elif sort == "year_desc":
            query = query.order_by(models.Car.year.desc())
    
    return query.all()


@router.get("/me", response_model = List[schemas.CarOut])
def get_my_cars(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(models.Car).filter(models.Car.owner_id == current_user.id).all()


@router.get("/{car_id}", response_model=schemas.CarOut)
def get_car(
    car_id:int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    if car.status !="approved" and not current_user.is_admin and car.owner_id != current_user.id:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this car"
        )
    return car  


@router.put("/{car_id}", response_model=schemas.CarOut)
def update_car(
    car_id: int, 
    car_data: schemas.CarCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    car = db.query(models.Car).filter(models.Car.id == car_id, models.Car.owner_id == current_user.id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found or not yours."
        )
    for key, value in car_data.model_dump().items():
        setattr(car, key, value)
    car.status = "pending"
    db.commit()
    db.refresh(car)
    return car


@router.delete("/{car_id}")
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    car = db.query(models.Car).filter(models.Car.id == car_id, models.Car.owner_id == current_user.id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found or not yours."
        )
    db.delete(car)
    db.commit()
    return {"detail": "Car deleted successfully."}


@router.put("/{car_id}/approve")
def approve_car(
    car_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found."
        )
    car.status = "approved"
    db.commit()
    return {"detail": "Car approved successfully."}
