import asyncio
import cloudscraper
from loguru import logger

from core.config import settings


class GetImageLinksError(Exception):
    pass


scraper = cloudscraper.create_scraper(
    server_hostname="www.quizlet.com",
    disableCloudflareV1=True,
)


async def get_image_urls(query: str, amount: int = 10):
    result = scraper.get(
        "https://quizlet.com/webapi/3.1/images",
        params={"query": query, "perPage": amount},
    )
    logger.debug(result.text)


async def main():
    await get_image_urls("start")


if __name__ == "__main__":
    asyncio.run(main())
else:
    raise NotImplemented("This module is not implemented")
