from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import get_db
from . import schemas, service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=schemas.UserOut)
def register(
    user:schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    try:
        return service.register_user(db, user.username, user.email, user.password)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/logiin")
def login(
    user:schemas.UserCreate,
    db: Session = Depends(get_db)
):
    db_user = service.authtenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password."
        )
    token = service.create_access_token(db_user.email)
    return {"access_token": token, "token_type": "bearer"}

