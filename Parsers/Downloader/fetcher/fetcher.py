import requests
from botasaurus.request import request, Request
from typing import Iterable, Sequence



@request(
    max_retry=5,  # Максимальное количество повторных попыток
    retry_wait=3,  # Время ожидания между попытками (в секундах)
    output=None
)

def fetch_one(request: Request, url: str) -> bytes | None:
    try:
        response = request.get(url)
        response.raise_for_status()  # Проверяем статус код ответа

        # Если все хорошо, возвращаем содержимое
        return response.content

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 410 or e.response.status_code == 404:
            print(f"Ресурс удален: {url}")
            return None  # Возвращаем None для удаленных ресурсов
        else:
            print(f"Ошибка при загрузке {url}: {e}")
            raise  # Повторяем попытку для других ошибок

    except Exception as e:
        print(f"Неожиданная ошибка при загрузке {url}: {e}")
        sleep(3)  # Ждем перед повторной попыткой
        raise

def fetch_many(urls: Iterable[str]) -> Sequence[bytes | None]:
    # Используем list comprehension для выполнения запросов к каждому URL
    return [fetch_one(url) for url in urls]

def main():
    url = "https://o.quizlet.com/ig1PqUlooEepF2aq6lNgGg_m.jpg"
    results = fetch_many([url])
    print(f"Successfully fetched {len(results)} images.")

if __name__ == "__main__":
    main()