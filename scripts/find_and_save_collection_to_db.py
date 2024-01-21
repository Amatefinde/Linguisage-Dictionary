import asyncio
import traceback
import aiohttp

from typing import Iterable
from loguru import logger

from core.database import db_helper
from core.schemas import CoreSWord
from api_v1.public_word import crud
from Parsers.main_collector import collect_and_download_one, WordNotExist
from Parsers import SeleniumBaseImgCollector, GetImageLinksError
from fake_useragent import UserAgent


async def get_aiohttp_session():
    aiohttp_session_config: dict = {"headers": {"User-Agent": UserAgent().random}}
    return aiohttp.ClientSession(**aiohttp_session_config)


async def find_and_save_to_db(
    query: str,
    collector: SeleniumBaseImgCollector,
) -> None:
    async with await get_aiohttp_session() as aiohttp_session:
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
        async with db_helper.session_factory() as db_session:
            async with db_session.begin():
                await crud.create_or_supplement_db_public_word(db_session, core_word)


@logger.catch
async def find_many_and_save_to_db(words: Iterable[str], start: int = None) -> None:
    image_collector = SeleniumBaseImgCollector()
    with image_collector:
        for idx, word in enumerate(words[start:], start):
            logger.info((idx, word))
            try:
                await find_and_save_to_db(word, image_collector)
            except WordNotExist:
                logger.info(f"Word by query {word} not found in dictionary")
            except Exception as Ex:
                logger.error(Ex)
                logger.error(traceback.format_exc())
                await asyncio.sleep(5)
                await find_and_save_to_db(word, image_collector)
