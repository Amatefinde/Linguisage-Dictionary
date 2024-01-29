import asyncio
import traceback
import aiohttp

from typing import Iterable
from loguru import logger

from core.database import db_helper
from core.schemas import CoreSWord
from core.database import create_or_supplement_db_public_word
from Parsers.main_collector import collect_and_download_one, WordNotExist
from Parsers import SeleniumImgCollector, GetImageLinksError
from fake_useragent import UserAgent


async def get_aiohttp_session():
    aiohttp_session_config: dict = {"headers": {"User-Agent": UserAgent().random}}
    return aiohttp.ClientSession(**aiohttp_session_config)


async def find_and_save_to_db(
    query: str,
    collector: SeleniumImgCollector,
) -> None:
    async with await get_aiohttp_session() as aiohttp_session:
        try:
            core_word: CoreSWord = await collect_and_download_one(
                aiohttp_session, query=query, collector=collector
            )
        except GetImageLinksError:
            await asyncio.sleep(15)
            logger.error(query)
            core_word: CoreSWord = await collect_and_download_one(
                aiohttp_session, query=query, collector=collector
            )
        async with db_helper.session_factory() as db_session:
            async with db_session.begin():
                await create_or_supplement_db_public_word(db_session, core_word)


async def __find_many_and_save_to_db(words: Iterable[str], start: int = 0) -> int | None:
    image_collector = SeleniumImgCollector()
    with image_collector:
        for idx, word in enumerate(words[start:], start):
            logger.info((idx, word))
            try:
                await find_and_save_to_db(word, image_collector)
                start += 1
            except WordNotExist:
                logger.info(f"Word by query {word} not found in dictionary")
            except Exception as Ex:
                logger.error(Ex)
                logger.error(traceback.format_exc())

                await asyncio.sleep(50)
                return start


async def find_many_and_save_to_db(words: Iterable[str], start: int = 0, max_retry_count=3) -> None:
    loop_counter = 0
    while start is not None:
        prev_start = start
        start = await __find_many_and_save_to_db(words, start)
        if prev_start == start:
            loop_counter += 1
        else:
            loop_counter = 0
        if loop_counter > max_retry_count:
            raise Exception(f"Something went wrong...")
