import cloudscraper
import concurrent.futures


scrapper = cloudscraper.create_scraper(
    # delay=10,
    browser={"browser": "firefox", "platform": "android", "desktop": False},
)


def collect_img_links_from_json(data: dict) -> list[str]:
    image_links = []
    for image in data.get("responses")[0].get("models").get("image"):
        image_link = image.get("_legacyUrl")
        image_links.append(image_link)
    return image_links


def fetch_url(
    query: str,
    amount: int = 10,
    url: str = "https://quizlet.com/webapi/3.2/images/search",
):
    params = {"query": query, "perPage": amount}
    response = scrapper.get(url, params=params)
    if response.status_code != 200:
        print(response)
    data = response.json()
    return collect_img_links_from_json(data)


def get_links_by_query_list(words: list[str]):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_url, words))
    return dict(zip(words, results))


if __name__ == "__main__":
    text = """Himawari is very mature and responsible for her age, often helping her mother with chores. At the same time, Himawari has a temper; she can become very violent when provoked. When her favourite plush was accidentally damaged by Boruto, she assaulted him. She usually has no memory of these outbursts. This display of aggression made her elder brother run away and hide from her and vow never to anger her again.[2] The same event also caused her father and Kurama to be terrified of her.[8] As mentioned by Iruka Umino, Himawari possesses the same stubbornness that her father and brother possess, while also being somewhat boisterous and hyperactive, mainly when she's determined in achieving a certain goal. Himawari also shows signs of her father's nindō of never giving up at the face of difficulty, urging Ehō Norimaki to continue their Academy trial session despite them being trapped in a well. However, contrary to Boruto she is also shown to display the same traits of patience and humbleness of her grandfather by continually being understanding of Naruto's circumstances for not being present for events such as her birthday. Himawari is very brave and loyal to her friends, able to remain calm under dangerous situations and push herself to help others. She is also very forgiving, able to acknowledge peoples' change when they make the effort to do the right thing.[9]"""
    print(get_links_by_query_list(text.split()[:10]))
