from .senses import parse_multiply, parse_single
from core.config import settings
from core.schemas import SSense, SWord

from utils import join_url
from aiohttp.client import ClientSession
from bs4 import BeautifulSoup


async def fetch_page(session: ClientSession, link: str) -> str:
    link = join_url(settings.DICTIONARY_BASE_URL, link)
    async with session.get(link) as response:
        if response.status != 200:
            print("Ошибка! ParsePage - 7 строка. Статус код != 200")
        return await response.text()


def _parse_senses(soup: BeautifulSoup, link: str | None = None):
    senses: list[SSense] = []
    if soup.find("ol", class_="senses_multiple"):
        senses = parse_multiply(soup, link)
    elif soup.find("ol", class_="sense_single"):
        senses = parse_single(soup, link)
    else:
        print("Undefined case: ", link)
    return senses


def _parse_headword(soup: BeautifulSoup, link: str | None = None):
    return soup.find("h1", class_="headword").text


async def _parse_page(row_html: str, link) -> SWord:
    soup = BeautifulSoup(row_html, "lxml")
    senses: list[SSense] = _parse_senses(soup, link)
    word: str = _parse_headword(soup)
    return SWord(word=word, senses=senses)


async def main(session: ClientSession, dictionary_word_link: str) -> SWord:
    row_html = await fetch_page(session, dictionary_word_link)
    return await _parse_page(row_html, dictionary_word_link)
