import json
from botasaurus.request import request, Request

@request(
    max_retry=5,  # Максимальное количество повторных попыток
    retry_wait=10,  # Время ожидания между попытками (в секундах)
    output=None,
)
def find_images_by_word(request: Request, word: str, amount_images: int = 10) -> list[str]:
    try:
        # Формируем URL с текущим словом
        url = f"https://quizlet.com/webapi/3.2/images/search?query={word}&perPage={amount_images}"

        # Делаем GET-запрос к указанному URL
        response = request.get(url)

        # Проверяем статус код ответа
        response.raise_for_status()
        row_image_objs = response.json()["responses"][0]["models"]["image"]
        return [x["_secureLegacyUrlSmall"] for x in row_image_objs]


    except Exception as e:
        # Логируем ошибку
        print(f"Ошибка при загрузке страницы для слова '{word}': {str(e)}")
        # Повторяем попытку или выбрасываем исключение после max_retry попыток
        raise