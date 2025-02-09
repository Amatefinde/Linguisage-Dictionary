import asyncio
from pathlib import Path
from .fetcher import fetch_one, fetch_many
from aiohttp import ClientSession


async def download_one(url: str, filepath: Path | str, session: ClientSession = None):
    filepath = Path(filepath)
    file: bytes | None = fetch_one(url)
    if file is not None:
        filepath.write_bytes(file)


async def download_many(
    filenames_and_urls: dict[str, str], pathdir: str, session: ClientSession = None
) -> tuple[str, ...]:
    """filenames_and_urls: dict[filename, url]"""
    files = fetch_many(filenames_and_urls.values())
    for idx, filename in enumerate(filenames_and_urls):
        if files[idx]:
            Path(pathdir, filename).write_bytes(files[idx])
    return tuple(filenames_and_urls.keys())


async def main():
    await download_one(
        "https://www.oxfordlearnersdictionaries.com/us/media/english/uk_pron/c/cat/cat__/cat__gb_2.mp3",
        r"C:\Users\AMDisPOWER\PycharmProjects\Linguisage-Dictionary\Parsers\Downloader\cat.mp3",
    )


if __name__ == "__main__":
    asyncio.run(main())
