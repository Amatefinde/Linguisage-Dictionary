import base64
import binascii
import io
from os.path import join
from uuid import uuid4

from PIL import Image
from fastapi import HTTPException, status


def img2str(image: Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode("utf-8")


def str2img(base64_str: str) -> Image:
    img_bytes = base64.b64decode(base64_str, validate=True)
    img = Image.open(io.BytesIO(img_bytes))
    return img


def compress_image(image: Image) -> Image:
    image = image.copy()
    if image.size > (500, 500):
        image.thumbnail((500, 500))
    return image


def read_image_from_disk_file(image_file) -> Image:
    try:
        image = Image.open(io.BytesIO(image_file.read()))
        return image
    except IOError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file.")


async def read_image_from_fastapi_file(image_file) -> Image:
    try:
        image = Image.open(io.BytesIO(await image_file.read()))
        return image
    except IOError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file.")


def base64_strings_to_images(base64_strings: list[str]) -> list[Image]:
    images: list[Image] = []
    for image_base64str in base64_strings:
        try:
            image: Image = str2img(image_base64str)
        except binascii.Error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file.",
            )
        images.append(image)
    return images


def save_images(path_to_dir: str, images: list[Image]) -> list[str]:
    image_filenames = []
    for image in images:
        image: Image = compress_image(image)
        filename = f"{uuid4()}.jpeg"
        image.save(join(path_to_dir, filename), "JPEG", quality=90)
        image_filenames.append(filename)
    return image_filenames
