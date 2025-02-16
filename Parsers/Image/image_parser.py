import json

from bs4 import BeautifulSoup
from seleniumbase import Driver

# Создаём один экземпляр браузера
driver = Driver(uc=True, headless=True)

def parse_json(html):
    """
    Парсит переданный HTML и извлекает JSON, который находится в теге <pre>.
    Возвращает Python-объект, полученный из JSON, либо None в случае ошибки.
    """
    soup = BeautifulSoup(html, 'html.parser')
    pre_tag = soup.find('pre')
    if pre_tag is None:
        print("Не удалось найти тег <pre> с JSON данными.")
        return None

    json_text = pre_tag.get_text()
    try:
        data = json.loads(json_text)
        return data
    except json.JSONDecodeError as e:
        print("Ошибка декодирования JSON:", e)
        return None


def find_images_by_word(word: str, amount_images: int = 10) -> list[str]:
    try:
        # Формируем URL с текущим словом
        url = f"https://quizlet.com/webapi/3.2/images/search?query={word}&perPage={amount_images}"

        # Делаем GET-запрос к указанному URL
        driver.open(url)
        html_str = driver.get_page_source()
        response = parse_json(html_str)
        if response:
            row_image_objs = response["responses"][0]["models"]["image"]
            return [x["_secureLegacyUrlSmall"] for x in row_image_objs]


    except Exception as e:
        # Логируем ошибку
        print(f"Ошибка при загрузке страницы для слова '{word}': {str(e)}")
        # Повторяем попытку или выбрасываем исключение после max_retry попыток
        raise

find_images_by_word("cat")