try:
    from .schemas import SRowServerResponse
except ImportError:
    from schemas import SRowServerResponse

from requests.exceptions import JSONDecodeError
from typing import TypedDict
import cloudscraper
import concurrent.futures


class GetImageLinksError(Exception):
    pass


url: str = "https://quizlet.com/webapi/3.2/images/search"


QueryParams = TypedDict("QueryParams", {"perPage": int, "query": str})


def _make_request_to_server(params: QueryParams, max_attempts=16) -> list[str]:
    if max_attempts < 1:
        raise ValueError("max_attempts must be greater or equal them 1")
    current_attempt = 1
    while current_attempt <= max_attempts:
        scrapper = cloudscraper.create_scraper()
        response = scrapper.get(url, params=params)
        if response.status_code == 200:
            break
        current_attempt += 1
        print(response)
    try:
        server_response = SRowServerResponse.model_validate(response.json(), from_attributes=True)
    except JSONDecodeError:
        raise GetImageLinksError()
    return server_response.get_image_urls()


def _get_images_by_query(query: str, amount: int = 10) -> list[str]:
    params: QueryParams = {"perPage": amount, "query": query}
    return _make_request_to_server(params)


queryT = str
imagesT = list[str]


def get_links_by_query_list(query: queryT) -> dict[queryT, imagesT]:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(_get_images_by_query, query))
    return dict(zip(query, results))


if __name__ == "__main__":
    text = """Himawari is very mature and responsible for her age, often helping her mother with chores. At the same time, Himawari has a temper; she can become very violent when provoked. When her favourite plush was accidentally damaged by Boruto, she assaulted him. She usually has no memory of these outbursts. This display of aggression made her elder brother run away and hide from her and vow never to anger her again.[2] The same event also caused her father and Kurama to be terrified of her.[8] As mentioned by Iruka Umino, Himawari possesses the same stubbornness that her father and brother possess, while also being somewhat boisterous and hyperactive, mainly when she's determined in achieving a certain goal. Himawari also shows signs of her father's nindō of never giving up at the face of difficulty, urging Ehō Norimaki to continue their Academy trial session despite them being trapped in a well. However, contrary to Boruto she is also shown to display the same traits of patience and humbleness of her grandfather by continually being understanding of Naruto's circumstances for not being present for events such as her birthday. Himawari is very brave and loyal to her friends, able to remain calm under dangerous situations and push herself to help others. She is also very forgiving, able to acknowledge peoples' change when they make the effort to do the right thing.[9]"""
    print(get_links_by_query_list(text.split()))
