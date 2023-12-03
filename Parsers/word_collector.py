from core.config import settings
from core.database.models import Word
from core.schemas import SWord, SSense
from core.database import db_helper

import api_v1.word.crud as word_crud

from Parsers.Image import get_links_by_query_list
from Parsers.Dictionary import get_dictionary_word_by_url

from urllib.parse import urlparse
import aiohttp
from aiohttp import TCPConnector
from aiohttp.client_exceptions import ClientError
import os
from utils import join_url
from typing import Iterable

import asyncio
from aiohttp.client import ClientSession, ClientTimeout

search_endpoint_url = "/search/english"
url = join_url(settings.DICTIONARY_BASE_URL, search_endpoint_url) + "/"


def get_aiohttp_session():
    aiohttp_session_config: dict = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        },
        "connector": TCPConnector(force_close=True),
        "timeout": ClientTimeout(6 * 60 * 60),
    }
    return aiohttp.ClientSession(**aiohttp_session_config)


async def fetch_image(session: ClientSession, url: str) -> tuple[str, bytes]:
    async with session.get(url) as response:
        file = await response.read()
        return url, file


def define_download_path_for_image(word: SWord, sense: SSense, url: str) -> str:
    extension = url.split(".")[-1]
    idx: int = 1
    clear_definition = sense.definition.replace(" ", "").replace("/", "_").replace("\\", "_")
    while True:
        static_path = join_url(settings.static_path, "/word_images/")
        file_name = f"{word.word}__{clear_definition}"[:50] + f"__{idx}.{extension}"
        new_file_path = join_url(static_path, file_name)
        if not os.path.exists(new_file_path):
            return new_file_path
        idx += 1


def _save_images(image: bytes, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "wb") as file:
        file.write(image)


async def try_to_get_image(session: ClientSession, urls: Iterable[str]) -> tuple[str, bytes]:
    attempt = 1
    while attempt < 4:
        try:
            images = await asyncio.gather(*[fetch_image(session, url) for url in urls])
            return images
        except ClientError:
            print(f"Attempt {attempt} unsuccessful")
    raise ClientError("To much attempts without result")


async def download_images_for_sense(
    session: ClientSession, word: SWord, sense: SSense, urls: Iterable[str]
):
    images: tuple[str, bytes] = await try_to_get_image(session, urls)
    for url, image in images:
        file_path = define_download_path_for_image(word, sense, url)
        _save_images(image, file_path)
        sense.images.append(file_path)


async def set_images_for_word(session: ClientSession, word: SWord):
    common_urls = get_links_by_query_list([word.word])[word.word]
    for sense in word.senses:
        sense_urls = get_links_by_query_list([sense.definition])[sense.definition]
        all_sense_urls = {*common_urls, *sense_urls}
        await download_images_for_sense(session, word, sense, all_sense_urls)


async def get_word_by_url_and_save(session: ClientSession, dictionary_word_link: str):
    word: SWord = await get_dictionary_word_by_url(session, dictionary_word_link)
    await set_images_for_word(session, word)

    async with db_helper.session_factory() as db_session:
        async with db_session.begin():
            db_word = await word_crud.add(db_session, word)
    print("saved to db:", word.word)

    return db_word


async def get_url_by_query(session: ClientSession, query: str) -> str | None:
    params = {"q": query}
    async with session.get(url, params=params) as response:
        row_html: str = await response.text()
        if "headword" in row_html:
            return urlparse(str(response.url)).path


async def search_by_query_and_save_to_db(query: str) -> Word | None:
    async with get_aiohttp_session() as session:
        word_dictionary_url = await get_url_by_query(session, query)
        if word_dictionary_url:
            return await get_word_by_url_and_save(session, word_dictionary_url)


#########################################################################


async def main(word: str | None):
    print(await search_by_query_and_save_to_db(word))


if __name__ == "__main__":
    asyncio.run(main("wadawdawdas2"))
