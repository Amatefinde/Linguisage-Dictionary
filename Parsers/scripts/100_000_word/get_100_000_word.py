import asyncio


def clear_words(words: list[str]) -> list[str]:
    words = map(lambda x: x.strip(), words)
    words = filter(lambda x: x[0] != "#", words)
    return list(words)


async def main():
    with open("wiki-100k.txt", "r", encoding="utf-8") as file:
        words = file.readlines()
        words = clear_words(words)

    print(words[:100], sep="\n")


if __name__ == "__main__":
    asyncio.run(main())
