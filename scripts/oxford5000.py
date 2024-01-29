import asyncio
import aiohttp
from loguru import logger
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from aiohttp import TCPConnector
from aiohttp.client import ClientSession
from aiohttp.client import ClientTimeout

from . import find_many_and_save_to_db
from core.config import settings


logger.add("oxford5000_test.log")


async def fetch_as_html(session: ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


def get_words_from_dictionary_list(row_html: str) -> list[str]:
    soup = BeautifulSoup(row_html, "lxml")
    parent_obj = soup.find("div", id="wordlistsContentPanel")
    row_words: list = parent_obj.find_all("li")
    words = []
    for row_word in row_words:
        row_word = row_word.find("a")
        words.append(row_word.text)
    return words


async def get_aiohttp_session():
    aiohttp_session_config: dict = {
        "headers": {"User-Agent": UserAgent().random},
        "connector": TCPConnector(force_close=True),
        "timeout": ClientTimeout(6 * 60 * 60),
    }
    return aiohttp.ClientSession(**aiohttp_session_config)


START = 4585


async def main(link_to_list):
    async with await get_aiohttp_session() as aiohttp_session:
        row_html = await fetch_as_html(aiohttp_session, link_to_list)
        words = list(dict.fromkeys(get_words_from_dictionary_list(row_html)))
        logger.info(f"Found {len(words)} words")
        await find_many_and_save_to_db(words, START)


asyncio.run(main(settings.URL_TO_WORD_LIST))
