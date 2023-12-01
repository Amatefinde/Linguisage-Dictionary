import aiohttp
from aiohttp import TCPConnector

from Parsers.Dictionary import get_dictionary_word_by_url
from Parsers.Image import get_links_by_query_list
from core.config import settings
from core.schemas import SWord, SSense
import api_v1.word.crud as word_crud
import os
from utils import join_url
from typing import Iterable
from core.database import db_helper

import asyncio
from aiohttp.client import ClientSession, ClientTimeout


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
        file_name = f"{word.word}__{clear_definition}__{idx}.{extension}"
        new_file_path = join_url(static_path, file_name)
        if not os.path.exists(new_file_path):
            return new_file_path
        idx += 1


def _save_images(image: bytes, filepath: str):
    with open(filepath, "wb") as file:
        file.write(image)


async def download_images_for_sense(
    session: ClientSession, word: SWord, sense: SSense, urls: Iterable[str]
):
    images: tuple[str, bytes] = await asyncio.gather(*[fetch_image(session, url) for url in urls])
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


async def get_word(session: ClientSession, dictionary_word_link: str):
    word: SWord = await get_dictionary_word_by_url(session, dictionary_word_link)
    await set_images_for_word(session, word)
    print(word)
    async with db_helper.session_factory() as db_session:
        async with db_session.begin():
            await word_crud.add(db_session, word)

    return dictionary_word_link


async def main():
    aiohttp_session_config: dict = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        },
        "connector": TCPConnector(force_close=True),
        "timeout": ClientTimeout(6 * 60 * 60),
    }

    async with aiohttp.ClientSession(**aiohttp_session_config) as session:
        await get_word(session, r"/definition/english/accident")


if __name__ == "__main__":
    asyncio.run(main())
