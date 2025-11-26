from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.cars.router import router as cars_router
from src.favourites.router import router as favourites_router



app = FastAPI()

app.include_router(auth_router)
app.include_router(cars_router)
app.include_router(favourites_router)


