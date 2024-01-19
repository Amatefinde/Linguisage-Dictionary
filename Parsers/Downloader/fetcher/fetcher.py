import asyncio
from fake_useragent import UserAgent
import aiohttp
from typing import Iterable, Sequence


async def __fetch(url: str, session: aiohttp.ClientSession, user_agent: str) -> bytes:
    response = await session.get(url, headers={"User-Agent": user_agent})
    return await response.content.read()


async def fetch_one(url: str, session: aiohttp.ClientSession | None = None) -> bytes:
    random_user_agent: str = UserAgent().random
    if session is None:
        async with aiohttp.ClientSession() as session:
            return await __fetch(url, session, random_user_agent)
    return await __fetch(url, session, random_user_agent)


async def fetch_many(
    urls: Iterable[str], session: aiohttp.ClientSession | None = None
) -> Sequence[bytes]:
    if session is None:
        async with aiohttp.ClientSession() as session:
            return await asyncio.gather(*[fetch_one(url, session) for url in urls])
    return await asyncio.gather(*[fetch_one(url, session) for url in urls])


async def main():
    url = "https://o.quizlet.com/ig1PqUlooEepF2aq6lNgGg_m.jpg"
    await fetch_many([url])


if __name__ == "__main__":
    asyncio.run(main())
