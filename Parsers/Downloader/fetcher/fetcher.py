import base64
from time import sleep
from typing import Iterable, Sequence
from seleniumbase import Driver

# Глобальный экземпляр браузера (постоянная сессия)
driver = Driver(uc=True, headless=True)

def fetch_one( url: str) -> bytes | None:
    max_retry = 5       # Максимальное количество попыток
    retry_wait = 3      # Время ожидания между попытками (сек)
    for attempt in range(max_retry):
        try:
            # Открываем URL в браузере
            driver.open(url)
            sleep(1)  # небольшая задержка на загрузку ресурса

            # Если URL указывает на аудиофайл
            if url.lower().endswith(('.mp3', '.wav', '.ogg')):
                js_audio = """
                var url = arguments[0];
                var callback = arguments[arguments.length - 1];
                fetch(url)
                  .then(response => { 
                      if (!response.ok) { 
                          callback("HTTP_ERROR_" + response.status);
                          return;
                      }
                      return response.blob();
                  })
                  .then(blob => {
                      if(blob === undefined){ return; }
                      var reader = new FileReader();
                      reader.onloadend = function() { 
                          callback(reader.result.split(',')[1]); 
                      };
                      reader.onerror = function(e) { callback(null); };
                      reader.readAsDataURL(blob);
                  })
                  .catch(error => { callback(null); });
                """
                b64_data = driver.execute_async_script(js_audio, url)
                if b64_data is None:
                    print(f"Не удалось загрузить ресурс: {url}")
                    return None
                if isinstance(b64_data, str) and b64_data.startswith("HTTP_ERROR_"):
                    status = int(b64_data.replace("HTTP_ERROR_", ""))
                    if status in (404, 410):
                        print(f"Ресурс удален: {url}")
                        return None
                    else:
                        raise Exception(f"HTTP ошибка {status} при загрузке {url}")
                return base64.b64decode(b64_data)

            else:
                # Предполагаем, что ресурс является изображением
                js_image = """
                var callback = arguments[arguments.length - 1];
                var img = document.images[0];
                if (!img) { 
                    callback(null);
                    return;
                }
                var canvas = document.createElement('canvas');
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                var ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                callback(canvas.toDataURL('image/png').substring(22));
                """
                b64_data = driver.execute_async_script(js_image)
                if b64_data is None:
                    print(f"Не удалось загрузить ресурс: {url}")
                    return None
                return base64.b64decode(b64_data)

        except Exception as e:
            print(f"Ошибка при загрузке {url} (попытка {attempt+1}): {e}")
            sleep(retry_wait)
            if attempt == max_retry - 1:
                raise

def fetch_many(urls: Iterable[str]) -> Sequence[bytes | None]:
    return [fetch_one(url) for url in urls]

def main():
    # Пример: загрузка изображения
    img_url = "https://o.quizlet.com/ig1PqUlooEepF2aq6lNgGg_m.jpg"
    # Пример: загрузка mp3-файла
    mp3_url = "https://www.oxfordlearnersdictionaries.com/us/media/english/us_pron/a/a__/a__us/a__us_2_rr.mp3"
    results = fetch_many([img_url, mp3_url])
    print(f"Successfully fetched {len(results)} resources.")

if __name__ == "__main__":
    try:
        main()
    finally:
        driver.quit()
