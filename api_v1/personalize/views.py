from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from .schemas import RequestAddSense

router = APIRouter(tags=["Personalize"], prefix="/personalize")


@router.post("/")
def add_custom_sense(sense: RequestAddSense, images: list[UploadFile] = File(...)):
    for image in images:
        if image.content_type.startswith("image/") is False:
            raise HTTPException(status_code=400, detail=f"File '{image.filename}' is not image")


class Item(BaseModel):
    word: str
    sense: str


@router.post("/items/")
async def create_item(item: Item, images: list[UploadFile] = File(...)):
    for image in images:
        if image.content_type.startswith("image/") is False:
            raise HTTPException(status_code=400, detail=f"File '{image.filename}' is not an image.")
    return {"item": item, "images": [image.filename for image in images]}
