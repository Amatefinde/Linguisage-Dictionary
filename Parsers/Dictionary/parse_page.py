from .senses.multiple import parse_multiply

from typing import TypedDict
from core.config import settings
from aiohttp.client import ClientSession
from bs4 import BeautifulSoup
from utils import join_url


async def fetch_page(session: ClientSession, link: str) -> str:
    link = join_url(settings.DICTIONARY_BASE_URL, link)
    async with session.get(link) as response:
        if response.status != 200:
            print("Ошибка! ParsePage - 7 строка. Статус код != 200")
        return await response.text()


async def _parse_page(row_html: str, link):
    if not row_html:
        print("Error: parse page:20", link)

    soup = BeautifulSoup(row_html, "lxml")
    if soup.find("ol", class_="senses_multiple"):
        parse_multiply(row_html, link)
    elif soup.find("ol", class_="sense_single"):
        pass  # todo
    elif soup.find("ol", class_="sense"):
        pass  # todo
    else:
        print("Undefined case: ", link)


async def main(session: ClientSession, link: str, name: str):
    row_html = await fetch_page(session, link)
    await _parse_page(row_html, link)
