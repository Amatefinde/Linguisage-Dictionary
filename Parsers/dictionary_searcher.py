import aiohttp
from aiohttp import TCPConnector, ClientTimeout
from bs4 import BeautifulSoup
import asyncio
from core.config import settings
from utils import join_url

search_endpoint_url = "/search/english"
url = join_url(settings.DICTIONARY_BASE_URL, search_endpoint_url) + "/"


async def get_url_by_query(session, query: str):
    aiohttp_session_config: dict = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        },
        "connector": TCPConnector(force_close=True),
        "timeout": ClientTimeout(6 * 60 * 60),
    }

    params = {"q": query}
    async with aiohttp.ClientSession(**aiohttp_session_config) as session:
        async with session.get(url, params=params) as response:
            print(response.url)


async def main():
    await get_url_by_query("tank")


asyncio.run(main())
