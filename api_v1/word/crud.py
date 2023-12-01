from core.database.models import Word, Image, Example, Sense, RowExample
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.schemas import SWord, SSense


async def get_word_by_id(
    session: AsyncSession,
    word_id: int,
) -> Word | None:
    return await session.get(Word, word_id)


async def get_word_by_name(
    session: AsyncSession,
    name: str,
) -> Word | None:
    stmt = select(Word).where(Word.word == name)
    return await session.scalar(stmt)


def get_db_images_from_s_sense(sense: SSense) -> list[Image]:
    images = []
    for image in sense.images:
        images.append(Image(img=image))
    return images


def get_examples_from_s_sense(sense: SSense) -> list[Example]:
    examples = []
    for example in sense.examples:
        examples.append(Example(example=example))
    return examples


def get_row_examples_from_s_sense(sense: SSense) -> list[RowExample]:
    row_examples = []
    for row_example in sense.row_examples:
        row_examples.append(RowExample(row_example=row_example))
    return row_examples


def get_db_senses_from_s_word(word: SWord) -> list[Sense]:
    senses = []
    for sense in word.senses:
        db_sense = Sense(
            lvl=sense.lvl,
            definition=sense.definition,
            short_cut=sense.short_cut,
            images=get_db_images_from_s_sense(sense),
            examples=get_examples_from_s_sense(sense),
            row_examples=get_row_examples_from_s_sense(sense),
        )
        senses.append(db_sense)
    return senses


async def add(
    session: AsyncSession,
    word: SWord,
):
    db_word = Word(word=word.word)
    db_word.senses = get_db_senses_from_s_word(word)
    session.add(db_word)
    await session.commit()
