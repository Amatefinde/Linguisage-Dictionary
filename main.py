from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from api_v1 import router as api_v1_router
from core.config import settings
from core import make_static_folder
from core.database import db_helper
from admin import (
    WordAdmin,
    SenseAdmin,
    AliasAdmin,
    ExampleAdmin,
    authentication_admin_backend,
)

make_static_folder()

app = FastAPI(title=settings.MICROSERVICE_NAME)
app.include_router(api_v1_router)

app.mount(
    "/static",  # url_path
    StaticFiles(directory=settings.STATIC_PATH),  # path_to_directory
    name="/static_files",
)

admin = Admin(app, engine=db_helper.engine, authentication_backend=authentication_admin_backend)
admin.add_view(WordAdmin)
admin.add_view(AliasAdmin)
admin.add_view(SenseAdmin)
admin.add_view(ExampleAdmin)

# app.add_event_handler("shutdown", lambda: link_collector.shutdown())
