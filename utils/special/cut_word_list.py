from core.schemas import SWordDictionaryLink


def _cut_word_link_list(
    word_links: list[SWordDictionaryLink],
    start_word: str | None = None,
) -> list[SWordDictionaryLink]:
    if not start_word:
        return word_links
    words = [word_link.word for word_link in word_links]
    index_start_word = words.index(start_word)
    return word_links[index_start_word:]
