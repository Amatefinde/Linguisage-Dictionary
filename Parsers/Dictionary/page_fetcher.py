from loguru import logger

from core.config import settings
from utils import join_url

from urllib.parse import urlparse
from aiohttp import ClientSession


SEARCH_ENDPOINT_URL = "/us/search/english"
SEARCH_DICTIONARY_URL = join_url(settings.DICTIONARY_BASE_URL, SEARCH_ENDPOINT_URL) + "/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
)
headers = {"User-Agent": USER_AGENT}


async def _fetch_page(session: ClientSession, url_path: str) -> str | None:
    """Return html of page by url"""
    url = join_url(settings.DICTIONARY_BASE_URL, url_path)
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            return None
        return await response.text()


async def _find_page_in_dictionary(session: ClientSession, query: str) -> str | None:
    """return path for dictionary page, for word, that has been found by this query"""
    params = {"q": query}
    async with session.get(SEARCH_DICTIONARY_URL, params=params, headers=headers) as response:
        row_html: str = await response.text()
        if "headword" in row_html:
            return urlparse(str(response.url)).path


async def _get_all_pages_for_word(session: ClientSession, word_base_url_path: str) -> list[str]:
    html_pages: list[str] = []
    if word_base_url_path.split("/")[-1].split("_")[-1].isdigit():
        while word_number := word_base_url_path.split("/")[-1].split("_")[-1]:
            if not (html_page := await _fetch_page(session, word_base_url_path)):
                break
            html_pages.append(html_page)
            word_base_url_path = word_base_url_path.replace(
                f"_{word_number}",
                f"_{int(word_number)+1}",
            )
        return html_pages
    return [await _fetch_page(session, word_base_url_path)]


async def get_html_pages_by_query(session: ClientSession, query: str) -> list[str]:
    word_base_url_path = await _find_page_in_dictionary(session, query)
    if not word_base_url_path:
        return []
    all_html_pages: list[str] = await _get_all_pages_for_word(session, word_base_url_path)
    return all_html_pages
