from typing import TypedDict
import asyncio

from core.config import settings
from Dictionary import get_dictionary_word_by_url

import aiohttp
from bs4 import BeautifulSoup


class Word(TypedDict):
    name: str
    link: str


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}


async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.text()


def get_links_to_words(row_html: str) -> list[Word]:
    soup = BeautifulSoup(row_html, "lxml")
    parent_obj = soup.find("div", id="wordlistsContentPanel")
    row_words: list = parent_obj.find_all("li")
    words = []
    for row_word in row_words:
        row_word = row_word.find("a")
        word: Word = {"name": row_word.text, "link": row_word["href"]}
        words.append(word)
    return words


async def main(link_to_list: str):
    async with aiohttp.ClientSession(headers=headers) as session:
        row_html = await fetch_data(session, link_to_list)
        words: list[Word] = get_links_to_words(row_html)
        tasks = []
        for word in words:  # type: Word
            tasks.append(get_dictionary_word_by_url(session, word.get("link")))
        print(await asyncio.gather(*tasks))


asyncio.run(main(settings.URL_TO_WORD_LIST))
