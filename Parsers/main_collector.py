from typing import NamedTuple, TYPE_CHECKING
from Image.cloudparser_collector import

if TYPE_CHECKING:
    from Parsers.Dictionary.schemas import SWord


class CollectedWord(NamedTuple):
    dictionary: list[SWord]
    image_urls: list[str]

async def collect_one(query: str) -> CollectedWord:

