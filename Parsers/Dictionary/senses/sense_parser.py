from bs4 import BeautifulSoup
from bs4.element import Tag
from core.schemas import SSense
import unicodedata


class Sense:
    def __init__(self, sense: BeautifulSoup | Tag, link=None):
        self.__validate_sense(sense, link)
        self.sense = sense
        self.link = link

        self.__parsed_sense = SSense.model_validate(self.parse_sense())

    @staticmethod
    def __validate_sense(sense, link):
        if type(sense) not in (BeautifulSoup, Tag):
            raise TypeError('arg: sense - must be  "BeautifulSoup" or "Tag"')

    def parse_sense(self) -> SSense:
        parsed_sense = {
            "lvl": self._get_lvl(),
            "examples": self._get_examples(),
            "row_examples": self._get_row_examples(as_str=True),
            "definition": self._get_definition(),
        }

        return SSense.model_validate(parsed_sense)

    @property
    def parsed_sense(self):
        return self.__parsed_sense

    def _get_lvl(self) -> str | None:
        if lvl := self.sense.get("cefr") or self.sense.get("fkcefr"):
            return lvl.upper()

    def _get_row_examples(self, as_str=False) -> list[BeautifulSoup] | list[str]:
        try:
            row_examples = self.sense.find("ul", class_="examples").find_all("li")
            return [str(row_example) for row_example in row_examples] if as_str else row_examples
        except AttributeError:
            return []

    def _get_examples(self):
        row_examples = self._get_row_examples()
        examples = []

        for row_example in row_examples:  # type: BeautifulSoup
            if not (example := row_example.find("span", class_="x")):
                if not (example := row_example.find("span", class_="unx")):
                    example = row_example
            examples.append(self.normalize(example.text))

        return examples

    @staticmethod
    def normalize(string: str) -> str:
        normalized = unicodedata.normalize("NFKC", string)
        return normalized.replace("\u200b", "")

    def _get_definition(self):
        try:
            return self.normalize(self.sense.find("span", class_="def").text)
        except AttributeError:
            return self.normalize(self.sense.text)
