from .page_fetcher import get_html_pages_by_query
from .senses import parse_multiply, parse_single
from .schemas import SDictionarySense, SWord

import asyncio
import aiohttp
from loguru import logger
from typing import NamedTuple
from aiohttp.client import ClientSession
from bs4 import BeautifulSoup


def _parse_senses(soup: BeautifulSoup, link: str | None = None) -> list[SDictionarySense]:
    senses: list[SDictionarySense] = []
    if soup.find("ol", class_="senses_multiple"):
        senses = parse_multiply(soup, link)
    elif soup.find("ol", class_="sense_single"):
        senses = parse_single(soup, link)
    else:
        logger.debug("Undefined case: ", link)
    return senses


def _parse_headword(soup: BeautifulSoup, link: str | None = None):
    return soup.find("h1", class_="headword").text


def _parse_part_of_speech(soup: BeautifulSoup) -> str | None:
    if pos := soup.find("span", class_="pos"):
        return pos.text


class WordSound(NamedTuple):
    us: str | None
    uk: str | None


def _parse_sounds(soup: BeautifulSoup) -> WordSound:
    sound_us = soup.find("div", class_="pron-us")
    sound_uk = soup.find("div", class_="pron-uk")
    if sound_us:
        sound_us = sound_us["data-src-mp3"]
    if sound_uk:
        sound_uk = sound_uk["data-src-mp3"]
    return WordSound(sound_us, sound_uk)


async def _parse_page(row_html: str, query: str) -> SWord:
    soup = BeautifulSoup(row_html, "lxml")
    senses: list[SDictionarySense] = _parse_senses(soup, query)
    word: str = _parse_headword(soup)
    part_of_speech: str = _parse_part_of_speech(soup)
    sound: WordSound = _parse_sounds(soup)
    return SWord(
        alias=query.lower(),
        word=word,
        senses=senses,
        part_of_speech=part_of_speech,
        sound_us_url=sound.us,
        sound_uk_url=sound.uk,
    )


async def get_words(session: ClientSession, query: str) -> list[SWord]:
    html_pages: list[str] = await get_html_pages_by_query(session, query)
    words: list[SWord] = []
    for page in html_pages:
        words.append(await _parse_page(page, query))  # todo
    return words


###########################################################################


async def main():
    async with aiohttp.ClientSession() as session:
        print(await get_words(session, "word"))


if __name__ == "__main__":
    asyncio.run(main())
