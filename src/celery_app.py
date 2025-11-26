from celery import Celery 
import src.config as settings


celery = Celery(
    "kolesa_app",
    broker=settings.settings.REDIS_URL,
    backend=settings.settings.REDIS_URL
)


celery.conf.timezone = "Asia/Almaty"
