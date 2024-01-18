import asyncio
from fake_useragent import UserAgent
import aiohttp


async def __fetch(url: str, session: aiohttp.ClientSession, user_agent: str) -> bytes:
    response = await session.get(url, headers={"User-Agent": user_agent})
    return await response.content.read()


async def fetch(url: str, session: aiohttp.ClientSession = None) -> bytes:
    random_user_agent = UserAgent().random
    if session is None:
        async with aiohttp.ClientSession() as session:
            return await __fetch(url, session, random_user_agent)
    return await __fetch(url, session, random_user_agent)


async def main():
    url = "https://o.quizlet.com/ig1PqUlooEepF2aq6lNgGg_m.jpg"
    await fetch(url=url)


if __name__ == "__main__":
    asyncio.run(main())
