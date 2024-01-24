from botasaurus import *
from timeit import default_timer
from Parsers.Image.interface import SeleniumCollectorAbstract
from loguru import logger

from core import settings


class SeleniumBotsaurusImgCollector(SeleniumCollectorAbstract):
    def get_images_url_by_query(self, query: str, amount: int = 10) -> list[str]:
        json_as_text: str = self.scrape(
            f"{settings.IMAGE_PROVIDER1_URL}?query={query}&perPage={amount}"
        )
        return self._parse_images_links(json_as_text)

    def __enter__(self):
        def add_arguments(data, options):
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")

        @browser(
            keep_drivers_alive=True,
            reuse_driver=True,
            headless=True,
            add_arguments=add_arguments,
            close_on_crash=True,
        )
        def scrape(driver: AntiDetectDriver, link):
            driver.get(link)
            page = driver.bs4()
            return page.find("body").text

        self.scrape = scrape

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.scrape.close()


if __name__ == "__main__":
    collector = SeleniumBotsaurusImgCollector()
    with collector:
        logger.info(collector.get_images_url_by_query("ethic"))
