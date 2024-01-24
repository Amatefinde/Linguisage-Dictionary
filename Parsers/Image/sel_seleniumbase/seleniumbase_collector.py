from loguru import logger
from seleniumbase import Driver
from Parsers.Image.interface import SeleniumCollectorAbstract
from core import settings


class SeleniumBaseImgCollector(SeleniumCollectorAbstract):
    def get_images_url_by_query(self, query: str, amount: int = 10) -> list[str]:
        self.driver.get(f"{settings.IMAGE_PROVIDER1_URL}?query={query}&perPage={amount}")
        json_as_text: str = self.driver.get_text("body")
        return self._parse_images_links(json_as_text)

    def __enter__(self):
        self.driver = Driver(uc=True, headless2=True, disable_js=True)
        self.get = self.driver.get
        logger.info("Selenium base image collector started")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.quit()
        logger.info("Selenium base image collector closed")


if __name__ == "__main__":
    collector = SeleniumBaseImgCollector()
    with collector:
        logger.info(collector.get_images_url_by_query("ethic"))
