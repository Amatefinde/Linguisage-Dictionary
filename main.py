from api_v1 import router as api_v1_router
from core import make_static_folder
from core.config import settings

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

make_static_folder()

app = FastAPI(title=settings.MICROSERVICE_NAME)
app.include_router(api_v1_router)

app.mount(
    "/static",  # url_path
    StaticFiles(directory=settings.STATIC_PATH),  # path_to_directory
    name="/static_files",
)

# app.add_event_handler("shutdown", lambda: link_collector.shutdown())
