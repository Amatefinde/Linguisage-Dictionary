import asyncio
import aiohttp
from loguru import logger
from bs4 import BeautifulSoup
from aiohttp import TCPConnector
from aiohttp.client import ClientSession
from aiohttp.client import ClientTimeout

from core.config import settings
from core.database import db_helper
from core.schemas import CoreSWord
from api_v1.word import crud
from Parsers.main_collector import collect_and_download_one
from Parsers import SeleniumBaseImgCollector, GetImageLinksError

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
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        },
        "connector": TCPConnector(force_close=True),
        "timeout": ClientTimeout(6 * 60 * 60),
    }
    return aiohttp.ClientSession(**aiohttp_session_config)


async def find_and_save_to_db(
    query: str,
    collector: SeleniumBaseImgCollector,
    aiohttp_session: ClientSession,
) -> None:
    try:
        core_word: CoreSWord = await collect_and_download_one(
            aiohttp_session, query=query, collector=collector
        )
    except GetImageLinksError:
        await asyncio.sleep(2)
        logger.error(query)
        core_word: CoreSWord = await collect_and_download_one(
            aiohttp_session, query=query, collector=collector
        )
    logger.info(core_word)
    async with db_helper.session_factory() as db_session:
        async with db_session.begin():
            await crud.create_or_supplement_db_public_word(db_session, core_word)


async def main(link_to_list: str, start_word: str | None = None):
    async with await get_aiohttp_session() as aiohttp_session:
        image_collector = SeleniumBaseImgCollector()
        with image_collector:
            row_html = await fetch_as_html(aiohttp_session, link_to_list)
            words: set[str] = set(get_words_from_dictionary_list(row_html))
            logger.info(f"Found {len(words)} words")
            for idx, word in enumerate(words, 1):
                logger.info((idx, word))
                await find_and_save_to_db(word, image_collector, aiohttp_session)


asyncio.run(main(settings.URL_TO_WORD_LIST))
