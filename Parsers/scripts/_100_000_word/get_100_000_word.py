import asyncio

import aiohttp
from aiohttp import TCPConnector, ClientTimeout, ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from Parsers import get_url_by_query
import api_v1
from core.database import db_helper
from utils import split_on_batches


def clear_words(words: list[str]) -> list[str]:
    words = map(lambda x: x.strip().lower(), words)
    words = filter(lambda x: x[0] != "#", words)
    return list(words)


def get_session() -> ClientSession:
    aiohttp_session_config: dict = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        },
        "connector": TCPConnector(force_close=True),
        "timeout": ClientTimeout(6 * 60 * 60),
    }

    return aiohttp.ClientSession(**aiohttp_session_config)


async def get_word_by_alias(session, alias: str) -> str:
    word_url = await get_url_by_query(session, alias)
    word = word_url.split("/")[-1]
    word = word.split("_")[0]
    return word


async def set_alias_to_word(
    session: ClientSession,
    alias: str,
):
    async with db_helper.session_factory() as db_session:
        async with db_session.begin():
            word = await get_word_by_alias(session, alias)
            db_alias = await api_v1.word.crud.add_alias_to_word(db_session, alias, word)
            print(word, db_alias)


async def main():
    with open("wiki-100k.txt", "r", encoding="utf-8") as file:
        aliases = file.readlines()
        aliases = clear_words(aliases)
    async with get_session() as session:
        for alias_batch in split_on_batches(aliases, 10):
            await asyncio.gather(*[set_alias_to_word(session, alias) for alias in alias_batch])

    print(aliases[:100], sep="\n")


if __name__ == "__main__":
    asyncio.run(main())
