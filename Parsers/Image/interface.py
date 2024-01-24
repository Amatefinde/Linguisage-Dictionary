from abc import ABC, abstractmethod
import json
from json.decoder import JSONDecodeError
from loguru import logger
from core import settings


class GetImageLinksError(Exception):
    pass


class SeleniumCollectorAbstract(ABC):
    def __init__(self):
        self.driver = None

    @staticmethod
    def _parse_images_links(json_as_text: str) -> list[str]:
        try:
            row_image_objs = json.loads(json_as_text)["responses"][0]["models"]["image"]
            return [x["_legacyUrl"] for x in row_image_objs]
        except JSONDecodeError:
            logger.error(json_as_text)
            raise GetImageLinksError("Could not get image links")
        except KeyError:
            logger.error(json_as_text)
            raise GetImageLinksError("Could not get image links")

    @abstractmethod
    def get_images_url_by_query(self, query: str, amount: int = 10) -> list[str]:
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass
