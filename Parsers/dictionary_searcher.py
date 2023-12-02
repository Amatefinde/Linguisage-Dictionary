import aiohttp
from aiohttp import TCPConnector, ClientTimeout, ClientSession
from bs4 import BeautifulSoup
import asyncio
from core.config import settings
from utils import join_url
from urllib.parse import urlparse

search_endpoint_url = "/search/english"
url = join_url(settings.DICTIONARY_BASE_URL, search_endpoint_url) + "/"


async def get_url_by_query(session: ClientSession, query: str) -> str:
    params = {"q": query}
    async with session.get(url, params=params) as response:
        return urlparse(str(response.url)).path


async def main():
    aiohttp_session_config: dict = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        },
        "connector": TCPConnector(force_close=True),
        "timeout": ClientTimeout(6 * 60 * 60),
    }

    async with aiohttp.ClientSession(**aiohttp_session_config) as session:
        print(await asyncio.gather(*[get_url_by_query(session, "tank") for _ in range(20)]))


if __name__ == "__main__":
    asyncio.run(main())
