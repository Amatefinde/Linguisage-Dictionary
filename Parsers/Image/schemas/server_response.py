from pydantic import BaseModel, ConfigDict, Field
from pprint import pprint


class SImage(BaseModel):
    url: str = Field(alias="_legacyUrl")
    model_config = ConfigDict(populate_by_name=True)


class SModel(BaseModel):
    image: list[SImage]


class SResponse(BaseModel):
    models: SModel


class SRowServerResponse(BaseModel):
    responses: list[SResponse]

    def get_image_urls(self) -> list[str]:
        _image_list: list[SImage] = self.responses[0].models.image
        urls: list[str] = [getattr(image, "url") for image in _image_list]
        return urls
