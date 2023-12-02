import asyncio

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from core.config import settings

import aiohttp
from aiohttp.client import ClientTimeout
from bs4 import BeautifulSoup
from utils.special import _cut_word_link_list
from Parsers.word_collector import get_word
from core.schemas import SWordDictionaryLink


async def fetch_data(session: ClientSession, url: str):
    async with session.get(url) as response:
        return await response.text()


def get_links_to_words(row_html: str) -> list[SWordDictionaryLink]:
    soup = BeautifulSoup(row_html, "lxml")
    parent_obj = soup.find("div", id="wordlistsContentPanel")
    row_words: list = parent_obj.find_all("li")
    word_links = []
    for row_word in row_words:
        row_word = row_word.find("a")
        word_link = SWordDictionaryLink(word=row_word.text, link=row_word["href"])
        word_links.append(word_link)
    return word_links


async def get_aiohttp_session():
    aiohttp_session_config: dict = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        },
        "connector": TCPConnector(force_close=True),
        "timeout": ClientTimeout(6 * 60 * 60),
    }
    return aiohttp.ClientSession(**aiohttp_session_config)


async def main(link_to_list: str, start_word: str | None = None):
    async with await get_aiohttp_session() as session:
        row_html = await fetch_data(session, link_to_list)
        word_links: list[SWordDictionaryLink] = get_links_to_words(row_html)
        word_links_from_start_word: list[SWordDictionaryLink] = _cut_word_link_list(
            word_links, start_word
        )

        for word_link in word_links_from_start_word:  # type: SWordDictionaryLink
            await get_word(session, word_link.link)

    print("end")


asyncio.run(main(settings.URL_TO_WORD_LIST))
