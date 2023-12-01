from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api_v1 import router as api_v1_router

app = FastAPI()
app.include_router(api_v1_router)


# app.mount("/static", StaticFiles(directory="app/static"), name="static")
