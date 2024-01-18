import asyncio
from pathlib import Path
from fetcher import fetch
from aiohttp import ClientSession


async def download(url: str, filename: Path | str, session: ClientSession = None) -> None:
    filename = Path(filename)
    file: bytes = await fetch(url, session)
    filename.write_bytes(file)


async def main():
    await download(
        "https://www.oxfordlearnersdictionaries.com/us/media/english/uk_pron/c/cat/cat__/cat__gb_2.mp3",
        r"C:\Users\AMDisPOWER\PycharmProjects\Linguisage-Dictionary\Parsers\Downloader\cat.mp3",
    )


asyncio.run(main())
