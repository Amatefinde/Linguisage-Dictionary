from celery import Celery
from core import settings


celery = Celery(
    "dictionary_tasks",
    broker=f"redis://{settings.REDIS_HOST}:6379",
    include=["background_tasks.tasks"],
)

celery.conf.task_default_queue = "dictionary_queue"
