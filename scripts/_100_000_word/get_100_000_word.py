import asyncio
from scripts import find_many_and_save_to_db


def clear_words(words: list[str]) -> list[str]:
    words = map(lambda x: x.strip().lower(), words)
    words = filter(lambda x: x[0] != "#", words)
    return list(words)


async def main():
    with open("wiki-100k.txt", "r", encoding="utf-8") as file:
        aliases = file.readlines()
        aliases = clear_words(aliases)
        await find_many_and_save_to_db(aliases)


if __name__ == "__main__":
    asyncio.run(main())
