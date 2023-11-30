from core.schemas import SSense
from .sense_parser import Sense

from bs4 import BeautifulSoup
from bs4.element import Tag


def parse_single(soup: BeautifulSoup, link: str | None = None) -> list[SSense]:
    sense_single = soup.find("ol", "sense_single")

    row_sense = sense_single.find("li", class_="sense")
    return [Sense(row_sense, link).parsed_sense] if row_sense else []
