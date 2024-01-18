import json
from json.decoder import JSONDecodeError
from loguru import logger
from seleniumbase import Driver

from core.config import settings


class GetImageLinksError(Exception):
    pass


class SeleniumBaseImgCollector:
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

    def get_images_url_by_query(self, query: str, amount: int = 10) -> list[str]:
        self.driver.get(f"{settings.IMAGE_PROVIDER1_URL}?query={query}&perPage={amount}")
        json_as_text: str = self.driver.get_text("body")
        return self._parse_images_links(json_as_text)

    def __enter__(self):
        self.driver = Driver(uc=True, headless2=True, disable_js=True)
        logger.info("Selenium base image collector started")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.quit()
        logger.info("Selenium base image collector closed")


if __name__ == "__main__":
    collector = SeleniumBaseImgCollector()
    with collector:
        logger.info(collector.get_images_url_by_query("ethic"))
