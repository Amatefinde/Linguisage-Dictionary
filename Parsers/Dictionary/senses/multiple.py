from bs4 import BeautifulSoup
from typing import TypedDict


class ParsedSense(TypedDict):
    lvl: str | None
    definition: str
    examples: list[str | None]


class FullParsedSense(ParsedSense):
    short_cut: str


def _check_multiply(soup: BeautifulSoup) -> None:
    if not soup.find("ol", class_="senses_multiple"):
        raise TypeError(
            "method parse multiply can be applied only for page with multiple senses "
        )


def _determine_lvl(sense: BeautifulSoup):
    try:
        return sense.find("div", class_="symbols").find("a")["href"][-2:].upper()
    except (TypeError, AttributeError) as Ex:
        pass


def _parse_senses(senses: list[BeautifulSoup], link):
    parsed_senses: list[ParsedSense] = []
    for sense in senses:  # type : B
        parsed_sense: ParsedSense = dict()
        parsed_sense["lvl"] = _determine_lvl(sense)

        try:
            parsed_sense["definition"] = sense.find("span", class_="def").text
        except AttributeError:
            continue
        row_examples = []
        try:
            row_examples = sense.find("ul", class_="examples").find_all("li")
        except AttributeError:
            pass

        examples = []
        for row_example in row_examples:  # type: BeautifulSoup
            example = row_example.find("span", class_="x")
            if not example:
                example = row_example.find("span", class_="unx")

            examples.append(example.text)
        parsed_sense["examples"] = examples

        parsed_senses.append(parsed_sense)
    return parsed_senses


def _parse_short_cuts(short_cuts: list[BeautifulSoup], link):
    full_parsed_senses: list[FullParsedSense] = []
    short_cut_name: None | str = None
    for short_cut in short_cuts:  # type: BeautifulSoup
        try:
            short_cut_name: str | None = short_cut.find("h2", class_="shcut").text
        except AttributeError:
            pass

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