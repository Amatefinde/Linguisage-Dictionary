from bs4 import BeautifulSoup
from typing import TypedDict


class ParsedSense(TypedDict):
    lvl: str | None
    definition: str
    examples: list[str | None]
    row_examples: list[str | None]


class FullParsedSense(ParsedSense):
    short_cut: str


def _check_multiply(soup: BeautifulSoup) -> None:
    if not soup.find("ol", class_="senses_multiple"):
        raise TypeError(
            "method parse multiply can be applied only for page with multiple senses "
        )


class Sense:
    def __init__(self, sense: BeautifulSoup, link=None):
        self.sense = sense
        self.link = link

        self.__parsed_sense = self.parse_sense()

    def parse_sense(self):
        parsed_sense: ParsedSense = {
            "lvl": self._get_lvl(),
            "examples": self._get_examples(),
            "row_examples": self._get_row_examples(),
            "definition": self._get_definition(),
        }

        return parsed_sense

    @property
    def parsed_sense(self):
        return self.__parsed_sense

    def _get_lvl(self) -> str | None:
        if lvl := self.sense.get("cefr"):
            return lvl.upper()

    def _get_row_examples(self):
        try:
            return self.sense.find("ul", class_="examples").find_all("li")
        except AttributeError:
            return []

    def _get_examples(self):
        row_examples = self._get_row_examples()
        examples = []

        for row_example in row_examples:  # type: BeautifulSoup
            if not (example := row_example.find("span", class_="x")):
                if not (example := row_example.find("span", class_="unx")):
                    example = row_example
            examples.append(example.text)

        return examples

    def _get_definition(self):
        try:
            return self.sense.find("span", class_="def").text
        except AttributeError:
            return self.sense.text


def _parse_senses(senses: list[BeautifulSoup], link):
    parsed_senses: list[ParsedSense] = []
    for sense in senses:
        parsed_sense: ParsedSense = Sense(sense, link).parsed_sense
        parsed_senses.append(parsed_sense)
    return parsed_senses


def _define_short_cut_name(short_cut_g: BeautifulSoup) -> str | None:
    try:
        return short_cut_g.find("h2", class_="shcut").text
    except AttributeError:
        pass


def _parse_short_cuts(short_cuts: list[BeautifulSoup], link):
    full_parsed_senses: list[FullParsedSense] = []
    for short_cut in short_cuts:  # type: BeautifulSoup
        short_cut_name: str = _define_short_cut_name(short_cut)
        senses: list[BeautifulSoup] | None = short_cut.find_all("li", class_="sense")
        parsed_senses: list[ParsedSense] = _parse_senses(senses, link)
        full_parsed_senses.extend(
            [x | {"short_cut": short_cut_name} for x in parsed_senses]
        )
    return full_parsed_senses


def parse_multiply(row_html: str, link):
    soup = BeautifulSoup(row_html, "lxml")

    _check_multiply(soup)

    senses: BeautifulSoup = soup.find("ol", class_="senses_multiple")
    if short_cuts := senses.find_all("span", class_="shcut-g"):
        full_parsed_senses = _parse_short_cuts(short_cuts, link)
        print(link, full_parsed_senses)
        return full_parsed_senses
