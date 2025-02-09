import asyncio
import aiohttp
from aiohttp import ClientSession
from pathlib import Path
from os.path import join
from typing import NamedTuple, TYPE_CHECKING

from Parsers.Dictionary import get_words
from Parsers.Downloader import download_one, download_many
from Parsers.Image.image_parser import find_images_by_word
from core import settings
from core import make_static_folder
from core.schemas import CoreSSense, CoreSWord

if TYPE_CHECKING:
    from Parsers.Dictionary.schemas import SWord as parser_SWord

make_static_folder()


class Sounds(NamedTuple):
    sound_uk: str | None
    sound_us: str | None


async def __get_sound_from_words(words) -> Sounds:
    sound_us = None
    if words[0].sound_us_url:
        sound_us = f"{words[0].word}_us.mp3"
        await download_one(
            words[0].sound_us_url, join(settings.STATIC_PATH, "word_audio", sound_us)
        )

    sound_uk = None
    if words[0].sound_uk_url:
        sound_uk = f"{words[0].word}_uk.mp3"
        await download_one(
            words[0].sound_uk_url, join(settings.STATIC_PATH, "word_audio", sound_uk)
        )

    return Sounds(sound_uk=sound_uk, sound_us=sound_us)


class WordNotExist(Exception):
    pass


async def collect_and_download_one(
    session: ClientSession,
    query: str,
    amount_images: int = 15,
) -> CoreSWord:
    images_urls = find_images_by_word(query, amount_images)

    words: list[parser_SWord] = await get_words(session, query)
    if not words:
        raise WordNotExist()
    s_senses: list[CoreSSense] = []
    sound_uk, sound_us = await __get_sound_from_words(words)
    for word in words:
        for sense in word.senses:
            s_senses.append(
                CoreSSense(
                    lvl=sense.lvl,
                    part_of_speech=word.part_of_speech,
                    definition=sense.definition,
                    short_cut=sense.short_cut,
                    examples=sense.examples,
                    html_examples=sense.row_examples,
                )
            )
    image_filenames_and_urls = {
        f"{words[0].word}_{idx}{Path(url).suffix}": url for idx, url in enumerate(images_urls, 1)
    }
    image_names = await download_many(
        image_filenames_and_urls, join(settings.STATIC_PATH, "word_images")
    )
    return CoreSWord(
        word=words[0].word,
        senses=s_senses,
        alias=query,
        sound_uk=sound_uk,
        sound_us=sound_us,
        images=image_names,
    )


async def main():
    async with aiohttp.ClientSession() as session:
        print(await collect_and_download_one(session, "hello"))


if __name__ == "__main__":
    asyncio.run(main())
