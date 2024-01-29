import asyncio
from scripts import find_many_and_save_to_db
from os import path


def clear_words(words: list[str]) -> list[str]:
    words = map(lambda x: x.strip().lower(), words)
    words = filter(lambda x: x[0] != "#", words)
    return list(words)


async def main():
    current_dir = path.dirname(__file__)
    with open(path.join(current_dir, "wiki-100k.txt"), "r", encoding="utf-8") as file:
        aliases = file.readlines()
        aliases = clear_words(aliases)
        await find_many_and_save_to_db(aliases, 1)


asyncio.run(main())
