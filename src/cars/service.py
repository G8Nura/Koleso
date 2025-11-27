from sqlalchemy.orm import Session
from . import models
from src import enums 
from typing import Optional, Dict 


def create_car(
    db: Session, 
    car_data, 
    user_id: int 
):
    new_car = models.Car(**car_data.model_dump(), owner_id=user_id)
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


def get_car_by_id(
        db: Session,
        filters: Dict,
        sort: Optional[str] = None
):
    query = db.query(models.Car).filter(models.Car.status == enums.CarStatus.APPROVED).first()


    if 'brand' in filters and filters['brand']:
        query = query.filter(models.Car.brand.ilike(f"%{filters['brand']}%"))
    if 'model' in filters and filters['model']:
        query = query.filter(models.Car.model.ilike(f"%{filters['model']}%"))
    if 'price_min' in filters and filters['price_min'] is not None:
        query = query.filter(models.Car.price >= filters['price_min'])
    if 'price_max' in filters and filters['price_max'] is not None:
        query = query.filter(models.Car.price <= filters['price_max'])
    if 'year_min' in filters and filters['year_min'] is not None:
        query = query.filter(models.Car.year >= filters['year_min'])
    if 'year_max' in filters and filters['year_max'] is not None:
        query = query.filter(models.Car.year <= filters['year_max'])

    
    if sort:
        if sort == "price_asc":
            query = query.order_by(models.Car.price.asc())
        elif sort == "price_desc":
            query = query.order_by(models.Car.price.desc())
        elif sort == "year_asc":
            query = query.order_by(models.Car.year.asc())
        elif sort == "year_desc":
            query = query.order_by(models.Car.year.desc())
    return query


def get_car_by_id(
        db: Session,
        car_id: int
):
    return db.query(models.Car).filter(models.Car.id == car_id).first()


def update_car(
        db: Session,
        car_id: int,
        car_data,
        user_id: int
):
    car = db.query(models.Car).filter(models.Car.id == car_id, models.Car.owner_id == user_id).first()
    if not car:
        return None
    for key, value in car_data.model_dump().items():
        setattr(car, key, value)
    car.status = enums.CarStatus.PENDING
    db.commit()
    db.refresh(car)
    return car


def delete_car(
        db: Session,
        car_id: int,
        user_id: int
):
    car = db.query(models.Car).filter(models.Car.id == car_id, models.Car.owner_id == user_id).first()
    if not car:
        return None
    db.delete(car)
    db.commit()
    return car


def approve_car(
        db: Session,
        car_id: int
):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()
    if not car:
        return None
    car.status = enums.CarStatus.APPROVED
    db.commit()
    return car