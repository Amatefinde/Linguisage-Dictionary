import base64
from time import sleep
from typing import Iterable, Sequence
from seleniumbase import Driver

# Создаем глобальный экземпляр браузера
driver = Driver(uc=True, headless=True)

def fetch_one( url: str) -> bytes | None:
    max_retry = 5       # Максимальное количество попыток
    retry_wait = 3      # Ожидание между попытками (сек)
    for attempt in range(max_retry):
        try:
            driver.open(url)
            # Небольшая задержка для загрузки изображения
            sleep(1)
            # Выполняем JS для получения base64-кодированного содержимого изображения
            js = """
            var img = document.images[0];
            if (!img) { return null; }
            var canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            var ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            return canvas.toDataURL('image/png').substring(22);
            """
            b64_data = driver.execute_script(js)
            if b64_data is None:
                print(f"Ресурс удален или не найден: {url}")
                return None
            return base64.b64decode(b64_data)
        except Exception as e:
            print(f"Ошибка при загрузке {url} (попытка {attempt+1}): {e}")
            sleep(retry_wait)
            if attempt == max_retry - 1:
                raise

def fetch_many(urls: Iterable[str]) -> Sequence[bytes | None]:
    # Сохраняем интерфейс: функция принимает список URL-ов
    return [fetch_one(url) for url in urls]

def main():
    url = "https://o.quizlet.com/ig1PqUlooEepF2aq6lNgGg_m.jpg"
    results = fetch_many([url])
    print(f"Successfully fetched {len(results)} images.")

if __name__ == "__main__":
    try:
        main()
    finally:
        driver.quit()
