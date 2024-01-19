from pprint import pprint

from .page_fetcher import get_html_pages_by_query
from .main import get_words
import aiohttp
import pytest
from loguru import logger


@pytest.mark.asyncio
async def test_number_pages_for_word():
    async with aiohttp.ClientSession() as session:
        html_pages = await get_html_pages_by_query(session, "word")
        assert len(html_pages) == 3

        html_pages = await get_html_pages_by_query(session, "home")
        assert len(html_pages) == 4


@pytest.mark.asyncio
async def test_valid_page():
    async with aiohttp.ClientSession() as session:
        html_pages = await get_html_pages_by_query(session, "word")
        html_pages += await get_html_pages_by_query(session, "home")

        for page in html_pages:
            assert "headword" in page


@pytest.mark.asyncio
async def test_valid_word():
    async with aiohttp.ClientSession() as session:
        words = await get_words(session, "word")
        assert words[0].word == "word"
        logger.info(words[1].words)
