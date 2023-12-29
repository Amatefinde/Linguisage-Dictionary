import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api_v1 import router as api_v1_router
from core.config import settings
from Parsers.Image import link_collector
import os

if not os.path.exists("./static"):
    os.mkdir("./static")

if not os.path.exists("./static/word_images"):
    os.mkdir("./static/word_images")

app = FastAPI(title=settings.MICROSERVICE_NAME)
app.include_router(api_v1_router)

app.mount(
    f"/static/word_images",
    StaticFiles(directory=f"./static/word_images"),
    name="static_images",
)


app.add_event_handler("shutdown", lambda: link_collector.shutdown())
