from core.schemas import SSense
from .sense_parser import Sense
from bs4 import BeautifulSoup


def _check_multiply(soup: BeautifulSoup) -> None:
    if not soup.find("ol", class_="senses_multiple"):
        raise TypeError(
            "method parse multiply can be applied only for page with multiple senses "
        )


def _parse_senses(senses: list[BeautifulSoup], link):
    parsed_senses: list[SSense] = []
    for sense in senses:
        parsed_sense: SSense = Sense(sense, link).parsed_sense
        parsed_senses.append(SSense.model_validate(parsed_sense))
    return parsed_senses


def _define_short_cut_name(short_cut_g: BeautifulSoup) -> str | None:
    try:
        return short_cut_g.find("h2", class_="shcut").text
    except AttributeError:
        pass


def _get_senses_from_sh_cut_g(short_cuts: list[BeautifulSoup], link):
    all_parsed_senses: list[SSense] = []
    for short_cut in short_cuts:  # type: BeautifulSoup
        short_cut_name: str = _define_short_cut_name(short_cut)
        senses: list[BeautifulSoup] | None = short_cut.find_all("li", class_="sense")
        parsed_senses: list[SSense] = _parse_senses(senses, link)
        for parsed_sense in parsed_senses:
            parsed_sense.short_cut = short_cut_name
        all_parsed_senses.extend(parsed_senses)
    return all_parsed_senses


def parse_multiply(row_html: str, link):
    soup = BeautifulSoup(row_html, "lxml")

    _check_multiply(soup)

    senses: BeautifulSoup = soup.find("ol", class_="senses_multiple")
    if sh_cut_g := senses.find_all("span", class_="shcut-g"):
        full_parsed_senses: list[SSense] = _get_senses_from_sh_cut_g(sh_cut_g, link)
        print(full_parsed_senses)
        return full_parsed_senses
