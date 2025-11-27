from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from . import service, schemas 
from src.dependencies import get_db, get_current_user, get_current_admin
from src.enums import CarStatus
from src.pagination import paginate, PaginationParams, PaginatedResponse


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
    return service.create_car(db, car, current_user.id)


@router.get("/", response_model=PaginatedResponse[schemas.CarOut])
def get_cars(
    brand: Optional[str] = None,
    model: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    sort: Optional[str] = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    filters = {
        "brand": brand, "model": model,
        "price_min": price_min, "price_max": price_max,
        "year_min": year_min, "year_max": year_max
    }
    query = service.get_cars(db, filters, sort)
    return paginate(query, page=pagination.page, limit=pagination.limit)


@router.get("/me", response_model=PaginatedResponse[schemas.CarOut])
def get_my_cars(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = service.get_user_cars(db, current_user.id)
    return paginate(query, page=pagination.page, limit=pagination.limit)


@router.get("/{car_id}", response_model=PaginatedResponse[schemas.CarOut])
def get_car(
    car_id: int,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    car = service.get_car_by_id(db, pagination, car_id)
    if not car:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )
    if car.status != CarStatus.APPROVED and not current_user.is_admin and car.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    return car


@router.put("/{car_id}", response_model=schemas.CarOut)
def update_car(
    car_id: int, 
    car_data: schemas.CarCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    car = service.update_car(db, car_id, car_data, current_user.id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found or not yours."
        )
    return car


@router.delete("/{car_id}")
def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    car = service.delete_car(db, car_id, current_user.id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found or not yours."
        )
    return {"detail": "Car deleted successfully."}


@router.put("/{car_id}/approve")
def approve_car(
    car_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    car = service.approve_car(db, car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found."
        )
    return {"detail": "Car approved successfully."}
