from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api_v1 import router as api_v1_router
from core.config import settings


app = FastAPI()
app.include_router(api_v1_router)


app.mount(
    f"/static/word_images",
    StaticFiles(directory=f"./static/word_images"),
    name="static_images",
)
